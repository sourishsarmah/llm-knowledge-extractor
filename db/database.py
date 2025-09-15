from models import AnalysisResult
from supabase import Client


class Database:
    def __init__(self, supabase_client: Client):
        self.supabase: Client = supabase_client

    def store_analysis(self, analysis_data: AnalysisResult):
        try:
            result = self.supabase.table("analyses").insert(analysis_data).execute()
            return result
        except Exception as e:
            raise Exception(f"Failed to store analysis: {str(e)}")

    def search_analyses(self, topic: str):
        try:
            result = (
                self.supabase.table("analyses")
                .select("*")
                .or_(f"topics.cs.{{{topic}}},keywords.cs.{{{topic}}}")
                .execute()
            )
            return result.data
        except Exception as e:
            raise Exception(f"Failed to search analyses: {str(e)}")
