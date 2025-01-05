curl http://localhost:11434/api/generate -d '{
  "model": "tinyllama",
  "stream": false,
  "prompt": "Why is the sky blue?"
}'