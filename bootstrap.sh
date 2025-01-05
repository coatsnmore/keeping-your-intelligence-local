#!/bin/bash

OLLAMA_ENDPOINT=http://localhost:11434

curl $OLLAMA_ENDPOINT/api/pull -d '{
  "model": "tinyllama"
}'

curl $OLLAMA_ENDPOINT/api/tags

template=$(curl $OLLAMA_ENDPOINT/api/show -d '{
  "model": "tinyllama"
}' |  jq '.template')

echo -e "Template:\n\n$template"
