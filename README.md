# LLM Knowledge Extractor

A FastAPI application that uses LangChain and OpenAI to analyze unstructured text and extract structured information. The application stores analysis results in a Supabase database and provides search functionality.

## Features

- **Text Analysis**: Generates a summary, extracts topics, sentiment, and keywords from input text
- **Database Storage**: Stores analysis results in a Supabase database
- **Search Functionality**: Search through past analyses by topic
- **Robust Error Handling**: Handles empty input and API failures gracefully

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- OpenAI API key
- Supabase project

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd llm-knowledge-extractor
   ```

2. **Install dependencies using Poetry**

   ```bash
   poetry install
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_KEY=your_supabase_anon_key_here
   ```

4. **Set up the database**

   - Create a new Supabase project
   - Run the migration script in `db/migrations/001_InitialMigration.sql` to create the `analyses` table

5. **Run the application**

   ```bash
   poetry run python main.py
   ```

   The API will be available at `http://localhost:8000`

## API Schema

### Base URL

```
http://localhost:8000
```

### Endpoints

#### 1. Analyze Text

**POST** `/analyze`

Analyzes unstructured text and returns structured metadata.

**Request Body:**

```json
{
  "text": "string"
}
```

**Response:**

```json
{
  "title": "string | null",
  "topics": ["string", "string", "string"],
  "summary": "string",
  "sentiment": "positive" | "neutral" | "negative",
  "keywords": ["string", "string", "string"],
  "text": "string"
}
```

**Example Request:**

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "The new AI technology is revolutionizing healthcare with its ability to diagnose diseases more accurately than traditional methods."}'
```

**Example Response:**

```json
{
  "title": "AI Revolution in Healthcare",
  "topics": ["artificial intelligence", "healthcare", "medical diagnosis"],
  "summary": "New AI technology is transforming healthcare by providing more accurate disease diagnosis compared to traditional methods.",
  "sentiment": "positive",
  "keywords": ["technology", "healthcare", "diagnosis"],
  "text": "The new AI technology is revolutionizing healthcare with its ability to diagnose diseases more accurately than traditional methods."
}
```

#### 2. Search Analyses

**GET** `/search`

Search through stored analyses by topic.

**Query Parameters:**

- `topic` (string, required): The topic to search for

**Response:**

```json
[
  {
    "id": 1,
    "title": "string | null",
    "topics": ["string", "string", "string"],
    "summary": "string",
    "sentiment": "positive" | "neutral" | "negative",
    "keywords": ["string", "string", "string"],
    "text": "string",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

**Example Request:**

```bash
curl "http://localhost:8000/search?topic=healthcare"
```

### Error Responses

**400 Bad Request:**

```json
{
  "detail": "Input text cannot be empty."
}
```

**500 Internal Server Error:**

```json
{
  "detail": "An error occurred during analysis: <error_message>"
}
```

## Design Choices:

1. Used Python with FastAPI for faster setup.
2. Used Supabase for Database for minimal infra setup, without need for local database setup.
3. Used LangChain framework for better structured code and flexibility to change minimal code for better model switching.

## Trade Offs:

1. Lack of Logs.
2. Missing of validations in few spots. Mainly at LLM model calls - will probably like to add a rate limit or token count using tiktoken.
