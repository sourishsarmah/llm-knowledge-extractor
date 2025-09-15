from fastapi import Depends
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
from db.database import Database


def get_supabase_client() -> Client:
    """Create a Supabase client instance."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_database(supabase_client: Client = Depends(get_supabase_client)) -> Database:
    """Get a database instance with Supabase client dependency."""
    return Database(supabase_client)


# For dependency injection in FastAPI endpoints
DatabaseDep = Depends(get_database)
