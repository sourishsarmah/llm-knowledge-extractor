from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from config import OPENAI_API_KEY
from models import LLMAnalysisResult, AnalysisResult
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords


class LLMAnalyzer:

    def __init__(self):
        self.llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini")
        # Download required NLTK data
        nltk.download("punkt")
        nltk.download("punkt_tab")
        nltk.download("averaged_perceptron_tagger")
        nltk.download("averaged_perceptron_tagger_eng")
        nltk.download("stopwords")

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

    def extract_keywords(self, text: str, top_k: int = 3) -> list:
        """
        Extract the 3 most frequent nouns from the text using NLTK.
        """
        # Tokenize the text
        tokens = word_tokenize(text.lower())
        pos_tags = pos_tag(tokens)
        nouns = [word for word, pos in pos_tags if pos.startswith("NN")]
        stop_words = set(stopwords.words("english"))
        filtered_nouns = [
            noun for noun in nouns if noun not in stop_words and len(noun) > 2
        ]
        noun_counts = Counter(filtered_nouns)
        top_nouns = [noun for noun, count in noun_counts.most_common(top_k)]

        return top_nouns
