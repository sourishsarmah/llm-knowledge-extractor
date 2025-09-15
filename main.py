from typing import List
from fastapi import FastAPI, HTTPException
import uvicorn
from services.analyzer import LLMAnalyzer
from db.database import Database
from models import TextInput, AnalysisResult
from dependencies import DatabaseDep
import nltk

app = FastAPI(title="LLM Knowledge Extractor", version="1.0.0")


@app.post("/analyze", response_model=AnalysisResult)
async def analyze_text_endpoint(input_data: TextInput, db: Database = DatabaseDep):
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        result = LLMAnalyzer().analyze_text(input_data.text)
        db.store_analysis(result.dict())
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred during analysis: {str(e)}"
        )


@app.get("/search")
async def search_analyses_endpoint(
    topic: str, db: Database = DatabaseDep, response_model=List[AnalysisResult]
):
    try:
        results = db.search_analyses(topic)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred during search: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
