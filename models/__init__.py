from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class TextInput(BaseModel):
    text: str


class LLMAnalysisResult(BaseModel):
    title: Optional[str]
    topics: List[str]
    summary: str
    sentiment: Sentiment


class AnalysisResult(LLMAnalysisResult):
    keywords: List[str]
    text: str
