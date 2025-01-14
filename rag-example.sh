#!/bin/bash

# Initialize database and table for pgvector
initialize_database() {
    PGPASSWORD=password
  psql -h vector -d rag-example -U user  -c "
  CREATE TABLE IF NOT EXISTS documents (
      id SERIAL PRIMARY KEY,
      content TEXT NOT NULL,
      embedding VECTOR(1536) -- Match the dimension of Ollama embeddings
  );"
  echo "Database initialized."
}

# Insert a document with its embedding into the database
insert_document() {
  local content="$1"
  local embedding=$(curl -s ollama:11434/embedding -X POST -d "$content" | jq -r '.embedding | join(",")')

    PGPASSWORD=password

  psql -h vector -d rag-example -U user -c "
  INSERT INTO documents (content, embedding)
  VALUES ('$content', '[$embedding]');"
  echo "Document inserted: $content"
}

# Search for the most relevant document
search_document() {
  local query="$1"
  local query_embedding=$(curl -s ollama:11434/embedding -X POST -d "$query" | jq -r '.embedding | join(",")')

PGPASSWORD=password
  psql -h vector -d rag-example -U user -c "
  SELECT content
  FROM documents
  ORDER BY embedding <=> '[$query_embedding]'::vector
  LIMIT 1;"
}

# Generate a response using Ollama and the retrieved document
generate_response() {
  local query="$1"
  local context=$(search_document "$query")

  local response=$(curl -s ollama:11434/generate -X POST -d "{\"context\":\"$context\", \"query\":\"$query\"}")
  echo "Response: $response"
}

# Main menu for the script
echo "Choose an option:"
echo "1. Initialize Database"
echo "2. Insert Document"
echo "3. Query and Generate Response"
read -p "Enter your choice: " choice

case $choice in
  1)
    initialize_database
    ;;
  2)
    read -p "Enter document content: " doc
    insert_document "$doc"
    ;;
  3)
    read -p "Enter your query: " query
    generate_response "$query"
    ;;
  *)
    echo "Invalid choice."
    ;;
esac
