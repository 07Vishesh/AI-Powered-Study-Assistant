from rag.prompt import RAGPrompt
class QueryEngine:
    """Handles document retrieval and answer generation."""
    def __init__(
        self,
        index,
        llm,
        similarity_top_k: int = 3,):
        self.index = index
        self.llm = llm
        self.retriever = self.index.as_retriever(
            similarity_top_k=similarity_top_k
        )
        self.prompt_template = RAGPrompt()
    def ask(self, question: str):
        """Ask a question about the uploaded documents.
        Returns
        -------
        dict
            {
                "answer": str,
                "retrieved_nodes": list
            }
        """
        # Retrieve relevant chunks
        retrieved_nodes = self.retriever.retrieve(question)
        # Combine retrieved text
        context = "\n\n".join(
            node.text for node in retrieved_nodes
        )
        # Build prompt
        prompt = self.prompt_template.get_prompt().format(
            context_str=context,
            query_str=question,
        )
        # Generate answer
        answer = self.llm.generate_response(prompt)
        return {
            "answer": answer,
            "retrieved_nodes": retrieved_nodes,
        }