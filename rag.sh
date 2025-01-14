export PGPASSWORD=password
# psql -h vector -d rag-example -U user <<EOF
# CREATE EXTENSION IF NOT EXISTS vector;
# -- Add any additional SQL commands here
# EOF

#!/bin/bash

# Define the API URL
# API_URL="http://localhost:11434/api/embed"
API_URL="ollama:11434/api/embed"

model="all-minilm"
# prompt="How do I fulfill orders in the Acme application?"
# cats=$(base64 cats.jpeg) # beware that base64 may work differently per OS/shell
technical_doc=$(cat technical-documentation.md)

payload=$(jq -n --arg model "$model" \
                --arg input "$technical_doc" \
                '{
                    model: $model,
                    input: $input
                }')
# echo $payload

embed_response=$(curl -s -X POST "$API_URL" -d "$payload")
embedding=$(echo $embed_response | jq -r '.embeddings | join(",")')
echo $embedding
# echo $response

# psql -h vector -d rag-example -U user <<EOF
# CREATE EXTENSION IF NOT EXISTS vector;
# -- Add any additional SQL commands here
# EOF



