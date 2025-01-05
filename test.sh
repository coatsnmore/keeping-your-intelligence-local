#!/bin/bash

# Define the API URL
API_URL="http://localhost:11434/api/generate"

# Define the request payload
payload='{
  "model": "tinyllama",
  "stream": false,
  "prompt": "If a brain in a vat can experience a fully convincing and indistinguishable simulation of reality, how can we be sure that we are not currently in such a simulation?"
}'

# Use curl to send the request and store the JSON response
start_time=$(date +%s)  # Record start time in seconds (not nanoseconds)

response=$(curl -s -X POST "$API_URL" -d "$payload")

end_time=$(date +%s)  # Record end time in seconds
elapsed_time=$((end_time - start_time))  # Time in seconds

# Extract values from the response using jq
eval_count=$(echo "$response" | jq -r '.eval_count')
eval_duration=$(echo "$response" | jq -r '.eval_duration')
prompt_response=$(echo "$response" | jq -r '.response')

# Perform the calculation (eval_count / eval_duration * 10^9)
calculation_result=$(echo "scale=9; $eval_count / $eval_duration * 1000000000" | bc)

# Print the results
echo "Response: $prompt_response"
echo "Time to process request: $elapsed_time seconds"
echo "Tokens: $eval_count"
echo "Tokens/s: $calculation_result"

