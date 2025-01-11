#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
    echo "No model provided. Usage: ./code.sh <model>"
    exit 1
fi

model="$1"

# Define the API URL
API_URL="http://localhost:11434/api/generate"

# Define the request payload
# payload='{
#   "model": "tinyllama",
#   "stream": false,
#   "prompt": "What are mirror neurons and how do they relate to empathy in primates?"
# }'
template="<|im_start|>system\nRespond only with the requested code. Do not include any explanation, comments, or additional text. Do not include any other text than the valid Python file. Do not include wrapping markdown code fences. \n<|im_end|>{{ if .Prompt }}<|im_start|>user\n{{ .Prompt }}\n<|im_end|>{{ end }}<|im_start|>assistant\n{{ .Response }}<|im_end|>"
prompt="Write me a Python script that only uses built-in libraries that says hello world and prints the local date. Only response with a valid Python file. Do not include any other text than the valid Python file. Do not include wrapping markdown code fences. For example \"python\nfrom datetime import datetime\nprint(\"Hello World\")\nprint(datetime.now())\n\""
payload=$(jq -n --arg model "$model" \
                --arg prompt "$prompt" \
                --arg template "$template" \
                '{
                    model: $model,
                    stream: false,
                    prompt: $prompt,
                    template: $template
                }')

# Use curl to send the request and store the JSON response
start_time=$(date +%s)  # Record start time in seconds (not nanoseconds)

response=$(curl -s -X POST "$API_URL" -d "$payload")

end_time=$(date +%s)  # Record end time in seconds
elapsed_time=$((end_time - start_time))  # Time in seconds

# Extract values from the response using jq
eval_count=$(echo "$response" | jq -r '.eval_count')
prompt_eval_count=$(echo "$response" | jq -r '.prompt_eval_count')
eval_duration=$(echo "$response" | jq -r '.eval_duration')
prompt_response=$(echo "$response" | jq -r '.response')

# Perform the calculation (eval_count / eval_duration * 10^9)
calculation_result=$(echo "scale=9; $eval_count / $eval_duration * 1000000000" | bc)

echo $prompt_response


