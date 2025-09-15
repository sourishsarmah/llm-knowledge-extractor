from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from config import OPENAI_API_KEY
from models import AnalysisResult


class LLMAnalyzer:

    def __init__(self):
        self.llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")

    def analyze_text(self, text: str):
        # Generate summary
        prompt = f"""
        You are a helpful assistant that analyses text.
        Analyse the following text: {text}

        TEXT: 
        ```
        {text}
        ```

        Return the analysis in the following format:
        {{
            "summary": "summary of the text",
            "title": "title of the text",
            "topics": "topics of the text",
            "sentiment": "sentiment of the text",
        }}
        """
        structured_llm = self.llm.with_structured_output(AnalysisResult)
        response = structured_llm.invoke([HumanMessage(content=prompt)])
        response.keywords = self.extract_keywords(text)

        return response

    def extract_keywords(self, text: str) -> list:
        return []
