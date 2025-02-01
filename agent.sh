#!/bin/bash

# Define the model and API URL
model="qwen2.5-coder:0.5b"
API_URL="http://localhost:11434/api/generate"

# Define the template and initial prompt
template="<|im_start|>system\nYou are a python generator. You do not explain code or provide comments. You only output text and it is always valid python.\n<|im_end|>{{ if .Prompt }}<|im_start|>user\n{{ .Prompt }}\n<|im_end|>{{ end }}<|im_start|>assistant\n{{ .Response }}<|im_end|>"
prompt="Generate me a valid python script using only built-in libraries that says hello world and prints out the local time. Only output valid Python. Do not include any other words or explanation."

# Loop until the script runs successfully
while true; do
    echo "Generating Python script with model $model..."

    # Generate the payload for the API request
    payload=$(jq -n --arg model "$model" \
                    --arg prompt "$prompt" \
                    --arg template "$template" \
                    '{
                        model: $model,
                        stream: false,
                        prompt: $prompt,
                        template: $template
                    }')

    # Call the API and extract the response
    response=$(curl -s -X POST "$API_URL" -d "$payload" | jq .response)
    if [ $? -ne 0 ]; then
        echo "Failed to get a response from the API. Retrying..."
        continue
    fi

    # Clean up the response and save to a file
    my_string=$response
    trimmed_string="${my_string#\"}"  # Removes the first quote
    trimmed_string="${trimmed_string%\"}"  # Removes the last quote
    echo -ne "$trimmed_string" | sed 's/\\"/"/g' > app.py

    # Run pylint to check for errors
    echo "Running pylint on app.py..."
    pylint_output=$(pylint app.py 2>&1)
    pylint_exit_code=$?

    if [ $pylint_exit_code -ne 0 ]; then
        echo "pylint found issues:"
        echo "$pylint_output"
        echo "Retrying..."
        continue
    fi

    # Run the Python script
    echo "Running app.py..."
    python app.py
    python_exit_code=$?

    if [ $python_exit_code -eq 0 ]; then
        echo "Script ran successfully!"
        break
    else
        echo "Python script encountered an error. Retrying..."
    fi
done
