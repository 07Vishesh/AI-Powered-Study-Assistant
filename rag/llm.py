from openai import OpenAI
class LLMModel:
    """Loads and manages the OpenRouter Large Language Model."""
    def __init__(
        self,
        api_key: str,
        model_name: str = "nvidia/nemotron-3-super-120b-a12b:free",):
        self.api_key = api_key
        self.model_name = model_name
        self.client = None
    def load_model(self):
        """Initialize the OpenRouter client."""
        if self.client is None:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1",
            )
        return self.client
    def generate_response(self, prompt: str):
        """Generate a response from OpenRouter."""
        if self.client is None:
            self.load_model()
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
            max_tokens=1024,
        )
        return response.choices[0].message.content