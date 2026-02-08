import numpy as np
from typing import List, Dict
from rdflib import Graph, Namespace, RDF
from scripts.text_processor import TextProcessor
from scripts.vector_store import VectorStore
from openvino_genai import LLMPipeline


class RAGEngine:

    def __init__(self,model_path: str ="./model/phi-3-openvino",device: str = "CPU",max_tokens: int = 512 ):

        self.llm = LLMPipeline(model_path, device=device)
        self.max_tokens = max_tokens
        self.text_processor = TextProcessor()
        self.vector_store = VectorStore()
        self.graph = Graph()
        self.EX = Namespace("http://example.org/")
        self.graph.bind("ex", self.EX)

    def build_knowledge_graph(self, chunks: List[str]):
       
        self.graph.remove((None, None, None))
        
        for idx, chunk in enumerate(chunks):
            chunk_node = self.EX[f"Chunk_{idx}"]
            self.graph.add((chunk_node, RDF.type, self.EX.DocumentChunk))
            self.graph.add((chunk_node, self.EX.hasID, self.EX[f"id_{idx}"]))
            preview = chunk[:100].replace("\n", " ")
            self.graph.add((chunk_node, self.EX.preview, self.EX[preview]))

    def retrieve_relevant_docs(self, question: str, k: int = 3) -> List[str]: 
        if not hasattr(self, 'chunks') or not self.chunks:
            return []
        
        query_embedding = self.text_processor.get_embeddings([question])
        distances, indices = self.vector_store.search(query_embedding, k)
        relevant_docs = [self.chunks[idx] for idx in indices[0].tolist()]
        return relevant_docs

    def generate_answer(self, question: str, context: List[str]) -> str:
        
        context_text = "\n\n".join([f"[Context {i+1}]:\n{ctx}" for i, ctx in enumerate(context)])
        
        prompt = f"""You are a helpful document question-answering assistant.
        
    Instructions:
    1. Answer the question based ONLY on the provided context
    2. Provide clear, well-structured answers
    3. If listing items (contacts, requirements, dates), include ALL relevant items from the context
    4. Do not include partial lists - if you start a list, complete it
    5. Use proper formatting: bullet points for lists, clear sections for different topics
    6. If the answer cannot be found in the context, say: "I cannot find the answer in the provided documents."
    7. Do not add disclaimers about "limited information" if you can answer from the context
    8. Be concise but complete - include all relevant details
Context:
{context_text}

Question: {question}

Answer:"""
        
        result = self.llm.generate(prompt, max_new_tokens=self.max_tokens)
            
        # Handle different output formats
        if isinstance(result, str):
            return result
        elif hasattr(result, 'texts'):
            return result.texts[0]
        elif isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict) and 'generated_text' in result[0]:
                return result[0]['generated_text']
            return str(result[0])
        else:
            return str(result)

    def query(self, question: str, k: int = 3) -> Dict:
        relevant_docs = self.retrieve_relevant_docs(question, k)
        answer = self.generate_answer(question, relevant_docs)
        
        return {
            "answer": answer,
            "sources": relevant_docs,
            "num_sources": len(relevant_docs)
        }

    def save_index(self, filepath: str = "./data/faiss_index.bin"):
        self.vector_store.save_index(filepath)

    def load_index(self, filepath: str = "./data/faiss_index.bin", chunks: List[str] = None):
        self.vector_store.load_index(filepath)
        self.chunks = chunks
        self.build_knowledge_graph(chunks)