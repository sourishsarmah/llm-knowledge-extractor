from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from config import OPENAI_API_KEY
from models import LLMAnalysisResult, AnalysisResult


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
            "topics": ["topic1", "topic2", "topic3"],
            "sentiment": "positive/neutral/negative",
        }}
        """
        structured_llm = self.llm.with_structured_output(LLMAnalysisResult)

        try:
            response = structured_llm.invoke([HumanMessage(content=prompt)])

            analysis_result = AnalysisResult(
                summary=response.summary,
                title=response.title,
                topics=response.topics,
                sentiment=response.sentiment,
                keywords=self.extract_keywords(text),
                text=text,
            )

            return analysis_result
        except Exception as e:
            raise Exception(f"Failed to analyze text: {str(e)}")

    def extract_keywords(self, text: str) -> list:
        return []
