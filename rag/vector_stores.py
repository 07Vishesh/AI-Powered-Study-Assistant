import faiss
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.faiss import FaissVectorStore
class VectorStore:
    """Manages the FAISS vector store and LlamaIndex VectorStoreIndex."""
    def __init__(
        self,
        embed_model,
        embedding_dimension: int = 384,):
        self.embed_model = embed_model
        self.embedding_dimension = embedding_dimension
        self.faiss_index = None
        self.vector_store = None
        self.storage_context = None
        self.index = None
    def build_index(self, nodes):
        """Build a new vector index from document chunks."""
        self.faiss_index = faiss.IndexFlatL2(
            self.embedding_dimension
        )
        self.vector_store = FaissVectorStore(
            faiss_index=self.faiss_index
        )
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )
        self.index = VectorStoreIndex(
            nodes=nodes,
            storage_context=self.storage_context,
            embed_model=self.embed_model,
        )
        return self.index
    def get_index(self):
        """Return the current vector index."""
        if self.index is None:
            raise ValueError(
                "Vector index has not been created."
            )
        return self.index
    def clear(self):
        """Clear the vector database."""
        self.faiss_index = None
        self.vector_store = None
        self.storage_context = None
        self.index = None