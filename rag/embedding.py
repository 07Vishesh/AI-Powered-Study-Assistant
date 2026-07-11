from llama_index.embeddings.huggingface import HuggingFaceEmbedding
class EmbeddingModel:
    """This helps to loads and manages the embedding model."""
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.embedding_model = None
    def load_model(self):
        """THis function helps to load the embedding model."""
        if self.embedding_model is None:
            self.embedding_model = HuggingFaceEmbedding(
                model_name=self.model_name)
        return self.embedding_model
    def get_model(self):
        """This function return the loaded embedding model."""
        if self.embedding_model is None:
            return self.load_model()
        return self.embedding_model