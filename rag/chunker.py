from llama_index.core.node_parser import SentenceSplitter
class DocumentChunker:
    """This helps to load and chunks the document."""
    def __init__(self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = SentenceSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,)
    def chunk_documents(self, documents):
        """This function helps to divide the text into chunks."""
        if not documents:
            return []
        nodes = self.splitter.get_nodes_from_documents(documents)
        return nodes
    def get_chunk_count(self, documents):
        """THis function returns the total number of chunks."""
        nodes = self.chunk_documents(documents)
        return len(nodes)