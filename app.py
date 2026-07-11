import streamlit as st
from rag.loader import MultiDocumentLoader
from rag.chunker import DocumentChunker
from rag.embedding import EmbeddingModel
from rag.vector_stores import VectorStore
from rag.llm import LLMModel
from rag.query_engine import QueryEngine
st.set_page_config(
    page_title="AI-Powered Study Assistant",
    layout="wide",
)
st.title("AI-Powered Study Assistant")
st.markdown(
    "Upload your study materials (PDF, DOCX, TXT) and ask questions using AI."
)
st.divider()
if "documents" not in st.session_state:
    st.session_state.documents = None

if "nodes" not in st.session_state:
    st.session_state.nodes = None

if "index" not in st.session_state:
    st.session_state.index = None

if "engine" not in st.session_state:
    st.session_state.engine = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

@st.cache_resource
def load_embedding_model():
    embedding = EmbeddingModel()
    return embedding.load_model()

@st.cache_resource
def load_llm():
    api_key = st.secrets["OPENROUTER_API_KEY"]
    llm = LLMModel(api_key=api_key)
    llm.load_model()
    return llm

embed_model = load_embedding_model()
llm = load_llm()

# Sidebar
with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload one or more files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
    )
    st.divider()
    st.info(
        """
Supported Files

• PDF

• DOCX

• TXT
"""
    )
# Process Documents

if uploaded_files:
    st.sidebar.success(f"{len(uploaded_files)} file(s) selected.")
    if st.sidebar.button(
        "Process Documents",
        use_container_width=True,):
        with st.spinner("Processing documents..."):
            try:
                # Step 1: Load Documents
                loader = MultiDocumentLoader()
                documents = loader.load_documents(uploaded_files)
                if not documents:
                    st.error("No valid documents found.")
                    st.stop()
                # Step 2: Chunk Documents
                chunker = DocumentChunker()
                nodes = chunker.chunk_documents(documents)
                # Step 3: Create Vector Store
                vector_store = VectorStore(embed_model)
                index = vector_store.build_index(nodes)
                # Step 4: Create Query Engine
                engine = QueryEngine(
                    index=index,
                    llm=llm,
                )
                # Save into Session State
                st.session_state.documents = documents
                st.session_state.nodes = nodes
                st.session_state.index = index
                st.session_state.engine = engine
                st.success("Documents processed successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
# Ask Questions
if st.session_state.engine is not None:
    st.divider()
    st.subheader("Ask Questions")
    question = st.text_input(
        "Enter your question:",
        placeholder="Example: What is Machine Learning?",
    )
    if st.button(
        "Ask",
        use_container_width=True,
    ):
        if not question.strip():
            st.warning("Please enter a question.")
            st.stop()
        with st.spinner("Generating answer..."):
            try:
                result = st.session_state.engine.ask(question)
                answer=result["answer"]
                retrieved_nodes=result["retrieved_nodes"]
                st.session_state.chat_history.append(
                    {
                        "question":question,
                        "answer":answer,
                        "sources":retrieved_nodes,
                    }
                )
                st.write(answer)
            except Exception as e:
                st.error(f"Error: {e}")
# Chat History
if st.session_state.chat_history:
    st.divider()
    st.subheader("Conversation")
    for chat in reversed(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(chat["question"])
        with st.chat_message("assistant"):
            st.write(chat["answer"])
# Sidebar Actions
with st.sidebar:
    st.divider()
    if st.button(
        "Clear Chat",
        use_container_width=True,
    ):
        st.session_state.chat_history = []
        st.rerun()
    if st.button(
        "Clear Documents",
        use_container_width=True,
    ):
        st.session_state.documents = None
        st.session_state.nodes = None
        st.session_state.index = None
        st.session_state.engine = None
        st.session_state.chat_history = []
        st.success("Documents cleared successfully!")
        st.rerun()


st.markdown("""
<div style='text-align: center; color: gray; font-size: 14px; padding: 15px;'>
    <p><b>Future Enhancements</b></p>
    <p>
        This application can be extended with features such as
        <b>document summarization</b>,
        <b>voice interaction</b>, and
        <b>personalized recommendations</b>.
    </p>
</div>
""", unsafe_allow_html=True)

