# 📄ContextIQ - A Secure Document Q&A System

A production-ready Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask questions about their content using AI-powered natural language processing.

## 🌟 Features

- **Multi-format Document Support**: PDF, Word (.docx), Excel (.xlsx), PowerPoint (.pptx), and Text (.txt)
- **Semantic Search**: Uses sentence transformers and FAISS for efficient vector similarity search
- **AI-Powered Answers**: Leverages Llama 3 70B through Groq API for accurate question answering
- **Interactive UI**: Clean Streamlit interface with conversation history
- **Source Attribution**: Shows which document sections were used to generate answers
- **Secure**: Environment-based API key management, no data persistence

## 🏗️ Architecture

```
User Upload → Document Parser → Text Chunker → Embedding Generator
                                                        ↓
User Question → Query Embedder → FAISS Search → Context Retrieval → LLM → Answer
```

## 📋 Prerequisites

- Python 3.8+
- Hugging Face API Token ([Get here](https://huggingface.co/settings/tokens))
- Groq API Key ([Get here](https://console.groq.com/keys))

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/document-qa-system.git
cd document-qa-system
```

### 2. Create virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```
HF_TOKEN=your_huggingface_token_here
GROQ_API_KEY=your_groq_api_key_here
```

## 🎯 Usage

### Run the application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the system

1. **Upload a document** using the sidebar file uploader
2. **Wait for processing** (you'll see a success message with chunk count)
3. **Ask questions** in the text input field
4. **View answers** with source attribution
5. **Check conversation history** to see previous Q&A pairs

## 📁 Project Structure

```
document-qa-system/
│
├── app.py                  # Main Streamlit application
├── document_parser.py      # Document parsing module
├── text_processor.py       # Text chunking and embedding
├── vector_store.py         # FAISS index management
├── rag_engine.py          # RAG query processing
│
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your API keys (not in git)
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## 🔧 Configuration

### Adjustable Parameters

In the sidebar, you can adjust:
- **Number of chunks to retrieve** (1-10): More chunks = more context but slower
- **Model selection**: Choose between different Llama 3 and Mixtral models

In the code, you can modify:
- `chunk_size` and `chunk_overlap` in `TextProcessor`
- `temperature` and `max_tokens` in `RAGEngine`
- Embedding model in `TextProcessor.api_url`

## 🧪 Example Use Cases

1. **Research Papers**: Upload PDFs and ask about methodologies, findings, conclusions
2. **Legal Documents**: Query contracts, agreements for specific clauses
3. **Business Reports**: Extract insights from quarterly reports, presentations
4. **Technical Documentation**: Search for specific procedures, configurations
5. **Academic Notes**: Ask questions about study materials, lecture slides

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Document Processing**: PyMuPDF, python-docx, python-pptx, pandas
- **Text Processing**: LangChain
- **Embeddings**: Hugging Face sentence-transformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS
- **LLM**: Groq API (Llama 3 70B)

## 📊 Performance Metrics

- **Processing Speed**: ~5-10 seconds for 100-page PDF
- **Answer Latency**: ~2-5 seconds per query
- **Embedding Model**: 384 dimensions, ~22M parameters
- **Chunk Size**: 500 characters with 100 character overlap

## 🔒 Security Considerations

- API keys stored in `.env` file (not committed to git)
- No document storage on server (session-based only)
- No conversation logging to external services
- Secure HTTPS communication with API endpoints

## 🐛 Troubleshooting

### Common Issues

**"HF_TOKEN environment variable not set"**
- Make sure you created `.env` file and added your Hugging Face token

**"Error generating embeddings: 503"**
- Hugging Face model is loading, wait 30 seconds and try again

**"Out of memory error"**
- Try reducing chunk size or processing smaller documents
- Use smaller embedding model if needed

**PDF parsing errors**
- Some PDFs are image-based and need OCR (not currently supported)
- Try converting to text-based PDF first

## 🚀 Future Enhancements

- [ ] Support for image-based PDFs (OCR)
- [ ] Multi-document comparison queries
- [ ] Export conversation history
- [ ] Custom embedding model selection
- [ ] Response quality scoring
- [ ] Batch document processing
- [ ] Docker containerization
- [ ] Cloud deployment guide

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Author

Your Name - [Your Email/GitHub]

## 🙏 Acknowledgments

- Hugging Face for embedding models
- Groq for LLM API access
- LangChain for RAG framework
- Streamlit for the UI framework

## 📧 Contact

For questions or support, please open an issue on GitHub or contact [your-email@example.com]

---

**⭐ If you find this project useful, please consider giving it a star!**
