import psycopg2
import numpy as np
from psycopg2.extras import Json
import requests

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "user",
    "password": "password",
}

# Function to connect to the PostgreSQL database
def connect_db():
    return psycopg2.connect(**DB_CONFIG)

# Function to initialize the database and create the necessary table
def initialize_database():
    query = """
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        content TEXT NOT NULL,
        embedding VECTOR(1536)
    );
    """
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
    print("Database initialized.")

# Function to insert a document and its embedding
def insert_document(content):
    # Generate embedding using an external service (e.g., OpenAI, Ollama)
    embedding = generate_embedding(content)
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
                (content, embedding),
            )
        conn.commit()
    print(f"Document inserted: {content}")

# Function to generate an embedding using Ollama
# Replace this with your preferred embedding generation API
def generate_embedding(text):
    url = "http://localhost:11434/embedding"
    response = requests.post(url, json={"text": text})
    response.raise_for_status()
    return response.json()["embedding"]

# Function to retrieve the most relevant document
def search_document(query):
    query_embedding = generate_embedding(query)
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT content
                FROM documents
                ORDER BY embedding <=> %s::vector
                LIMIT 1;
                """,
                (query_embedding,)
            )
            result = cur.fetchone()
    return result[0] if result else None

# Function to generate a response using retrieved context
def generate_response(query):
    context = search_document(query)
    if not context:
        return "No relevant documents found."

    url = "http://localhost:11434/generate"
    payload = {"context": context, "query": query}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["response"]

# Main script execution
if __name__ == "__main__":
    initialize_database()

    # Insert sample documents
    insert_document("My name is Nicholas Coats.")
    insert_document("Nicholas Coats is a real person.")
    insert_document("Nicholas Coats has been to the moon.")

    # Query the system
    query = "Is Nicholas Coats a real person and what are their accomplishments?"
    print(f"Query: {query}")
    response = generate_response(query)
    print(f"Response: {response}")
