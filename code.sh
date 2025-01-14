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
# API_URL="ollama:11434/api/generate"

# Define the request payload
# payload='{
#   "model": "tinyllama",
#   "stream": false,
#   "prompt": "What are mirror neurons and how do they relate to empathy in primates?"
# }'
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

# Use curl to send the request and store the JSON response
start_time=$(date +%s)  # Record start time in seconds (not nanoseconds)

response=$(curl -s -X POST "$API_URL" -d "$payload" | jq .response)


# echo -e "$response"  | tr -d '"' > app.py
# echo -e "$response"  | tr -d '"' > app.py

# echo -e $response  > app.py
my_string=$response
trimmed_string="${my_string#\"}"  # Removes the first quote
trimmed_string="${trimmed_string%\"}"  # Removes the last quote
echo -ne "$trimmed_string" | sed 's/\\"/"/g' > app.py
#  app.py > app.py
pylint app.py
python app.py


# sed -e '1s/^./&/' -e ':a' -e '$!{N;ba}' -e 's/^.\(.*\).$/\1/' app.py > edit-app.py
# sed ':a; N; $!ba; s/^.\(.*\).$/\1/' app.py > edit-app.py


# sed 's/^.\(.*\).$/\1/' app.py > edit-app.py

# sed '1s/^.\(.*\).$/\1/' app.py

# sed -e '1s/^["'\''"]//' -e '$s/["'\''"]$//' app.py > app.py


# end_time=$(date +%s)  # Record end time in seconds
# elapsed_time=$((end_time - start_time))  # Time in seconds

# # Extract values from the response using jq
# eval_count=$(echo "$response" | jq -r '.eval_count')
# prompt_eval_count=$(echo "$response" | jq -r '.prompt_eval_count')
# eval_duration=$(echo "$response" | jq -r '.eval_duration')
# prompt_response=$(echo "$response" | jq -r '.response')

# # Perform the calculation (eval_count / eval_duration * 10^9)
# calculation_result=$(echo "scale=9; $eval_count / $eval_duration * 1000000000" | bc)

# echo -n $prompt_response | tr =-d '"'


