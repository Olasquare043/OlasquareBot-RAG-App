# 🤖 Olasquare Bot - Personal RAG Assistant

A professional AI-powered chatbot that provides detailed information about Olasquare's professional background, skills, projects, and experience using Retrieval-Augmented Generation (RAG) technology.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

- **💬 Interactive Chat Interface** - Clean, modern chat interface with user and bot message bubbles
- **🧠 RAG-Powered Responses** - Retrieval-Augmented Generation for accurate, context-aware answers
- **⚡ Quick Questions** - One-click access to common questions about Olasquare
- **📱 Responsive Design** - Works seamlessly on desktop and mobile devices
- **🎨 Professional UI** - Custom CSS styling with smooth animations
- **⏱️ Real-time Typing Effect** - Bot responses appear with realistic typing animation
- **🔌 API Health Monitoring** - Real-time connection status indicator

## 🚀 Live Demo

Access the live application: [https://olasquarebot.streamlit.app/](https://olasquarebot.streamlit.app/)

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Streamlit account (for deployment)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/olasquare-bot.git
cd olasquare-bot
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

For Streamlit Cloud, create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your_openai_api_key_here"
```

### 5. Set Up Vector Database
Ensure your ChromaDB vector store is in the `chroma_db/` directory with the pre-processed documents.

## 📁 Project Structure

```
olasquare-bot/
├── streamlit_app.py          # Main Streamlit application
├── helper.py                 # Core RAG functionality
├── requirements.txt          # Python dependencies
├── chroma_db/               # Vector database directory
│   ├── chroma.sqlite3
│   └── ... (ChromaDB files)
├── .streamlit/
│   └── secrets.toml         # Streamlit secrets
├── .env                     # Local environment variables
└── README.md               # This file
```

## 🔧 Usage

### Local Development
```bash
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501`

### Ask Questions
1. Type your question in the input box at the bottom
2. Use the Enter key or click "Send" to submit
3. Browse quick questions in the sidebar for common queries
4. View chat history with timestamps

### Available Information
The bot can answer questions about:
- Professional background and education
- Technical skills and expertise
- Projects and work experience
- Teaching and mentorship
- Community involvement
- Career achievements

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository, branch, and main file (`streamlit_app.py`)
   - Add your OpenAI API key in the Secrets section
   - Click "Deploy"

### Alternative: Deploy with FastAPI Backend

If using the FastAPI backend:

1. **Deploy FastAPI** on Railway/Render:
```bash
# Install FastAPI dependencies
pip install fastapi uvicorn

# Run locally
uvicorn olasquareBot:app --reload --host 0.0.0.0 --port 8000
```

2. **Update Streamlit app** with the deployed API URL

## 🧩 Core Components

### `helper.py`
- **DocumentProcessing**: Handles PDF loading and text chunking
- **VectorManager**: Manages embeddings and vector storage with ChromaDB
- **RagBuilder**: Builds the RAG chain with LangChain and GPT-3.5

### `streamlit_app.py`
- **OlasquareBotClient**: Manages RAG system interaction
- **Chat Interface**: Streamlit-based UI with custom CSS
- **Session Management**: Persistent chat history and state

## ⚙️ Configuration

### Customizing the Interface
Edit CSS in `streamlit_app.py` to modify:
- Color scheme
- Layout and spacing
- Animation effects
- Responsive behavior

### Modifying RAG Behavior
Update `helper.py` to adjust:
- Chunk size and overlap
- Retrieval parameters (top_k, MMR settings)
- Prompt templates
- Model settings (temperature, model version)

## 🐛 Troubleshooting

### Common Issues

1. **"API Connection Unavailable"**
   - Check if OpenAI API key is valid
   - Verify internet connection
   - Ensure `OPENAI_API_KEY` is set in secrets

2. **Vector Store Errors**
   - Ensure `chroma_db/` directory exists
   - Verify ChromaDB files are present
   - Check file permissions

3. **Slow Responses**
   - Reduce chunk size in `helper.py`
   - Adjust `top_k` parameter in `RagBuilder`
   - Check OpenAI API rate limits

4. **Deployment Issues**
   - Verify all dependencies in `requirements.txt`
   - Check Streamlit Cloud logs
   - Ensure proper secret management

## 🔄 Updating Content

To update the knowledge base:

1. Add new PDF documents to your source folder
2. Update the document processing in `helper.py`
3. Rebuild the vector store:
```python
from helper import DocumentProcessing, VectorManager

processor = DocumentProcessing()
vector_manager = VectorManager()

# Process new documents
pages = processor.extractdocument("new_document.pdf")
chunks = processor.chunk_document(pages)
vector_manager.create_vectorstore(chunks)
```

## 📊 Tech Stack

- **Frontend**: Streamlit, Custom CSS
- **Backend**: Python, LangChain, OpenAI GPT-3.5
- **Vector Database**: ChromaDB
- **Deployment**: Streamlit Cloud
- **Version Control**: Git, GitHub

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Olasquare**
- Portfolio: [https://saheed-olayemi.vercel.app/](https://saheed-olayemi.vercel.app/)
- GitHub: [@Olasquare043](https://github.com/Olasquare043)

## 🙏 Acknowledgments

- OpenAI for GPT-3.5 API
- Streamlit for the amazing framework
- LangChain for RAG implementation tools
- ChromaDB for vector storage

## 📞 Support

For support, email olasquareconsults@gmail.com or create an issue in the GitHub repository.

---

Made with ❤️ by Olasquare