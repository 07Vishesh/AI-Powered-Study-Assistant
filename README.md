# AI-Powered Study Assistant

A Retrieval-Augmented Generation (RAG) app built with **Streamlit** and **LlamaIndex** that lets you upload study materials (PDF, DOCX, TXT) and ask questions about them in natural language. The app retrieves the most relevant chunks from your documents and uses an LLM (via **OpenRouter**) to generate accurate, context-grounded answers — reducing manual searching and speeding up learning.

---

## Features

- Upload multiple **PDF**, **DOCX**, and **TXT** files at once
- Automatic text extraction and chunking (sentence-aware splitting)
- Local embeddings via HuggingFace `sentence-transformers` (no embedding API cost)
- Fast semantic search using a **FAISS** vector index
- Chat-style Q&A interface with conversation history
- Answers are grounded strictly in the uploaded documents — the model is instructed to say when information isn't found, and to merge information across chunks for comparison-style questions (with markdown tables where relevant)
- One-click buttons to clear the chat or clear all processed documents

---

## How It Works

```
Upload Files → Extract Text → Chunk Text → Embed Chunks → Store in FAISS
                                                                  │
                                                                  ▼
                        Question ──► Retrieve Top-K Chunks ──► Build Prompt ──► LLM (OpenRouter) ──► Answer
```

1. **Loader** (`rag/loader.py`) — extracts text from PDF (`pymupdf`), DOCX (`docx2txt`), and TXT files, preserving metadata like file name and page number.
2. **Chunker** (`rag/chunker.py`) — splits documents into overlapping chunks using LlamaIndex's `SentenceSplitter`.
3. **Embedding** (`rag/embedding.py`) — encodes chunks using the `sentence-transformers/all-MiniLM-L6-v2` model.
4. **Vector Store** (`rag/vector_stores.py`) — stores embeddings in a FAISS index and wraps it as a LlamaIndex `VectorStoreIndex`.
5. **Query Engine** (`rag/query_engine.py`) — retrieves the top-k relevant chunks for a question and builds the final prompt.
6. **Prompt** (`rag/prompt.py`) — a strict, context-only prompt template that instructs the model not to use outside knowledge.
7. **LLM** (`rag/llm.py`) — sends the prompt to an LLM through the [OpenRouter](https://openrouter.ai/) API (OpenAI-compatible client) and returns the generated answer.

---

## Project Structure

```
AI-Powered Study Assistant/
├── app.py                  # Streamlit app (UI + orchestration)
├── requirements.txt        # Python dependencies
├── data/                   # (optional) local folder for sample documents
├── storage/                # (optional) persisted index storage
├── .streamlit/
│   └── secrets.toml        # API keys and Streamlit config (not committed)
└── rag/
    ├── loader.py            # Multi-format document loader (PDF/DOCX/TXT)
    ├── chunker.py            # Splits documents into chunks/nodes
    ├── embedding.py          # HuggingFace embedding model wrapper
    ├── vector_stores.py      # FAISS vector store + LlamaIndex index builder
    ├── prompt.py              # RAG prompt template
    ├── llm.py                  # OpenRouter LLM wrapper
    └── query_engine.py         # Retrieval + answer generation logic
```

---

## Requirements

- Python 3.10+
- An [OpenRouter](https://openrouter.ai/) API key (used for the LLM; supports free models like `nvidia/nemotron-3-super-120b-a12b:free`)

All Python dependencies are listed in `requirements.txt`, including:

- `streamlit` — web UI
- `llama-index`, `llama-index-core`, `llama-index-embeddings-huggingface`, `llama-index-vector-stores-faiss` — RAG framework
- `sentence-transformers`, `torch`, `transformers` — embedding model
- `faiss-cpu` — vector similarity search
- `pymupdf`, `python-docx`, `docx2txt` — document parsing
- `openai` — OpenRouter API client (OpenAI-compatible)
- `python-dotenv`, `numpy`, `pandas` — utilities

---

## Setup & Installation

1. **Clone / unzip the project** and move into the folder:
   ```bash
   cd AI-Powered Study Assistant
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your OpenRouter API key.**
   Open `.streamlit/secrets.toml` and replace the placeholder with your real key:
   ```toml
   OPENROUTER_API_KEY = "your_openrouter_api_key_here"

   [server]
   fileWatcherType = "none"
   ```
   > Get a free API key at [openrouter.ai/keys](https://openrouter.ai/keys). Keep this file private — it should **not** be committed to version control.

5. **Run the app:**
   ```bash
   streamlit run app.py
   ```

6. Open the URL shown in the terminal (typically `http://localhost:8501`) in your browser.

---

## Usage

1. In the sidebar, upload one or more **PDF / DOCX / TXT** files.
2. Click **Process Documents** — this extracts, chunks, embeds, and indexes your files.
3. Once processing finishes, type a question in the **Ask Questions** box and click **Ask**.
4. The answer appears immediately, and the full conversation is kept below in a chat-style history.
5. Use **Clear Chat** to reset the conversation, or **Clear Documents** to remove the current index and start over with new files.

---

## Configuration

You can tweak these directly in the source files:

| Setting | File | Default |
|---|---|---|
| Chunk size / overlap | `rag/chunker.py` | `chunk_size=512`, `chunk_overlap=50` |
| Embedding model | `rag/embedding.py` | `sentence-transformers/all-MiniLM-L6-v2` |
| Number of retrieved chunks (`top_k`) | `rag/query_engine.py` | `similarity_top_k=3` |
| LLM model | `rag/llm.py` | `nvidia/nemotron-3-super-120b-a12b:free` (via OpenRouter) |
| LLM temperature / max tokens | `rag/llm.py` | `temperature=0.2`, `max_tokens=1024` |
| Prompt instructions | `rag/prompt.py` | Context-only answering, markdown tables for comparisons |

To use a different OpenRouter model, change `model_name` in `rag/llm.py` or pass it when constructing `LLMModel(api_key=..., model_name="...")`. See [openrouter.ai/models](https://openrouter.ai/models) for available options.

---

## Troubleshooting

- **"Error: ... api_key ..."** — make sure `OPENROUTER_API_KEY` is set correctly in `.streamlit/secrets.toml`.
- **No answer appears after clicking Ask** — check the terminal for a stack trace; this usually means the OpenRouter request failed (invalid key, rate limit, or an unavailable free model). Try a different model in `rag/llm.py`.
- **"No valid documents found"** — the uploaded file may be empty, scanned-image-only (no extractable text in the PDF), or an unsupported format.
- **Slow first run** — the embedding model (`all-MiniLM-L6-v2`) and its dependencies (`torch`, `transformers`) are downloaded and loaded on first use; subsequent runs are faster thanks to `st.cache_resource`.

---

## Possible Extensions

- Persist the FAISS index in `storage/` so documents don't need to be re-processed every session
- Add source citations (file name + page number) next to each answer
- Support additional file types (PPTX, Markdown, HTML)
- Add document summarization and quiz-generation features
- Swap FAISS for a hosted vector database (Pinecone, Weaviate, Qdrant) for larger, multi-user deployments

---

## License

This project is provided as-is for educational purposes. Add a license of your choice if you plan to distribute it.
