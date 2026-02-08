import streamlit as st
from scripts.document_parser import DocumentParser
from scripts.text_processor import TextProcessor
from scripts.vector_store import VectorStore
from scripts.rag_engine import RAGEngine

st.set_page_config(page_title="ContextIQ Document Q&A",layout="wide")

st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    color: #1f77b4;
}
.stButton>button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)


if "chunks" not in st.session_state:
    st.session_state.chunks = None
if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = None
if "history" not in st.session_state:
    st.session_state.history = []
if "document_processed" not in st.session_state:
    st.session_state.document_processed = False


def main():

    st.markdown('<div class="main-header">ContextIQ Secure Document Q&A</div>', unsafe_allow_html=True)

    # ---------------- Sidebar ----------------
    with st.sidebar:
        st.header("Upload Document")

        uploaded_file = st.file_uploader(
            "Choose a document",
            type=["pdf", "docx", "pptx", "xlsx", "txt"]
        )

        st.markdown("---")
        st.subheader("Retrieval Settings")

        k_value = st.slider(
            "Number of document chunks",
            min_value=1,
            max_value=10,
            value=3,
            help="Number of relevant chunks to retrieve for answering questions"
        )

        if st.button("Clear Chat History"):
            st.session_state.history = []
            st.rerun()

        if st.button("Reset Document"):
            st.session_state.chunks = None
            st.session_state.rag_engine = None
            st.session_state.history = []
            st.session_state.document_processed = False
            st.rerun()

        st.markdown("---")

    # ---------------- Main Area ----------------
    if uploaded_file:

        # Process document only once
        if not st.session_state.document_processed:
            with st.spinner("Processing document..."):
                file_type = uploaded_file.name.split(".")[-1].lower()
                # Parse document
                parser = DocumentParser()
                text = parser.parse_document(uploaded_file, file_type)

                # Chunk + embed
                processor = TextProcessor()
                chunks, embeddings = processor.process_text(text)

                # Vector index
                vector_store = VectorStore()
                vector_store.create_index(embeddings)

                # RAG engine (LOCAL OpenVINO)
                rag_engine = RAGEngine()
                rag_engine.vector_store = vector_store
                rag_engine.chunks = chunks  # Set chunks in RAG engine

                # Store in session state
                st.session_state.chunks = chunks
                st.session_state.rag_engine = rag_engine
                st.session_state.document_processed = True

                st.success(f"Document indexed successfully! ({len(chunks)} chunks)")

        st.markdown("---")
        st.subheader("Ask a Question")

        # Question input
        question = st.text_input(
            "Enter your question",
            placeholder="What is this document about?",
            key="question_input"
        )

        # Ask button
        if st.button("🔍 Ask", type="primary") and question:
            if not question.strip():
                st.warning("Please enter a valid question.")
            else:
                with st.spinner(" Generating answer..."):
                    # Query the RAG engine - only pass question and k
                    result = st.session_state.rag_engine.query(
                        question=question,
                        k=k_value
                    )

                    # Add to history
                    st.session_state.history.append({
                        "question": question,
                        "answer": result["answer"],
                        "sources": result["sources"]
                    })

                    st.success("Answer generated!")

        # ---------------- History ----------------
        if st.session_state.history:
            st.markdown("---")
            st.subheader("Conversation History")

            for i, item in enumerate(reversed(st.session_state.history)):
                with st.expander(f"Q{len(st.session_state.history)-i}: {item['question']}", expanded=(i==0)):
                    st.markdown(f"** Answer:**")
                    st.write(item['answer'])

                    st.markdown("---")
                    st.markdown("** Retrieved Context:**")
                    for idx, src in enumerate(item["sources"], 1):
                        with st.expander(f"Chunk {idx}"):
                            st.text(src[:500] + "..." if len(src) > 500 else src)


if __name__ == "__main__":
    main()