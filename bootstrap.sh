OLLAMA_ENDPOINT=http://localhost:11434

curl $OLLAMA_ENDPOINT/api/pull -d '{
  "model": "tinyllama"
}'

curl $OLLAMA_ENDPOINT/api/tags