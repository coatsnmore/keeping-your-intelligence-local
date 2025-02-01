#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
    echo "No model provided. Usage: ./inspect.sh <model>"
    exit 1
fi

model="$1"

# OLLAMA_ENDPOINT=http://localhost:11434
OLLAMA_ENDPOINT=ollama:11434

# define the payload with jq
payload=$(jq -n --arg model "$model" \
                  '{
                      model: $model
                  }')

# load the model
# template=$(curl -s -X POST "${OLLAMA_ENDPOINT}/api/show" -d "$payload" | jq '.template')
# curl -s -X POST "${OLLAMA_ENDPOINT}/api/show" -d "$payload"
response=$(curl -s -X POST "${OLLAMA_ENDPOINT}/api/show" -d "$payload")
context_window=$(echo -e "${response}" | jq .model_info.context_length)
family=
template=

echo $response

# template=$(curl $OLLAMA_ENDPOINT/api/show -d '{
#   "model": "tinyllama"
# }' |  jq '.template')

# echo -e "Template:\n\n$template"
echo -e "Details: ${model_info}"
