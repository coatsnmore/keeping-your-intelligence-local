#!/bin/bash

# # Check if an argument is provided
# if [ -z "$1" ]; then
#     echo "No model provided. Usage: ./code.sh <model>"
#     exit 1
# fi

# model="$1"
model=qwen2.5-coder:0.5b

# Define the API URL
API_URL="http://localhost:11434/api/generate"

template="<|im_start|>system\nYou are a python generator. You do not explain code or provide comments. You only output text and it is always valid python.\n<|im_end|>{{ if .Prompt }}<|im_start|>user\n{{ .Prompt }}\n<|im_end|>{{ end }}<|im_start|>assistant\n{{ .Response }}<|im_end|>"
prompt="Example prompt: \"Generate me a valid python script using only built in libraries that says hello world\"
Exammple Response:
print(\"Hello World\")

Prompt: Generate me a valid python script using only built in libraries that says hello world and prints out the local time. Only output valid Python. Do not include any other words or explanation.
Response:
"
payload=$(jq -n --arg model "$model" \
                --arg prompt "$prompt" \
                --arg template "$template" \
                '{
                    model: $model,
                    stream: false,
                    prompt: $prompt,
                    template: $template
                }')

response=$(curl -s -X POST "$API_URL" -d "$payload" | jq .response)
my_string=$response
trimmed_string="${my_string#\"}"  # Removes the first quote
trimmed_string="${trimmed_string%\"}"  # Removes the last quote
echo -ne "$trimmed_string" | sed 's/\\"/"/g' > app.py

pylint app.py
python app.py
