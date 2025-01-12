#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
    echo "No model provided. Usage: ./load-model.sh <model>"
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
curl -s -X POST "${OLLAMA_ENDPOINT}/api/pull" -d "$payload"

# list loaded models
curl $OLLAMA_ENDPOINT/api/tags
