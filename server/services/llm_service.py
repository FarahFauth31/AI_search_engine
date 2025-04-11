import os
import sys
from google import genai
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from config import Settings

settings = Settings()

class LLMService:
    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API,
        )
        self.model = "gemini-2.0-flash"
    
    def return_full_prompt(self, query: str, search_results: list[dict]):
        context_text = "\n\n".join([
            f"Source {i+1} {result['url']}:\n{result['content']}"
            for i, result in enumerate(search_results)
        ])
        full_prompt = f""""
        Context from web search:
        {context_text}

        Query: {query}

        Please provide a comprehensive, detailed, well-cited accurate response using the above conext. Think and reason deeply. Ensure it answers the query the user is asking. Do not use your own knowledge until it is absolutely necessary.
        """
        return full_prompt

    def generate_llm_response(self, query: str, search_results: list[dict]):
        full_prompt = self.return_full_prompt(query, search_results)

        response = self.client.models.generate_content(
            model=self.model, contents=full_prompt,
        )
        return response.text

    def generate_streamed_llm_response(self, query: str, search_results: list[dict]):
        full_prompt = self.return_full_prompt(query, search_results)

        response = self.client.models.generate_content_stream(
            model=self.model, contents=full_prompt,
        )

        for chunk in response:
            yield chunk.text
        
        #return response.text