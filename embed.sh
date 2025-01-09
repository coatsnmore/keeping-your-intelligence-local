#!/bin/bash

# Define the API URL
API_URL="http://localhost:11434/api/embed"

start_time=$(date +%s)  # Record start time in seconds (not nanoseconds)

model="all-minilm"
# prompt="How do I fulfill orders in the Acme application?"
# cats=$(base64 cats.jpeg) # beware that base64 may work differently per OS/shell
technical_doc=$(cat technical-documentation.md)

payload=$(jq -n --arg model "$model" \
                --arg input "$technical_doc" \
                '{
                    model: $model,
                    input: $input
                }')
echo $payload

response=$(curl -s -X POST "$API_URL" -d "$payload")

echo $response

# exit 0

end_time=$(date +%s)  # Record end time in seconds
elapsed_time=$((end_time - start_time))  # Time in seconds

# Extract values from the response using jq
eval_count=$(echo "$response" | jq -r '.prompt_eval_count')
eval_duration=$(echo "$response" | jq -r '.total_duration')
# prompt_response=$(echo "$response" | jq -r '.response')

# Perform the calculation (eval_count / eval_duration * 10^9)
calculation_result=$(echo "scale=9; $eval_count / $eval_duration * 1000000000" | bc)

# Print the results
echo "Response: -------------------------------------------"
echo -e "$response\n"
echo "-------------------------------------------"
echo "Time to process request: $elapsed_time seconds"
echo "Tokens: $eval_count"
echo "Tokens/s: $calculation_result"

# $1.25 / 1m input tokens (OpenAI 1/5/25)
# $5 / 1m output tokens
# given eval_count is a combo of input/output tokens,
# let's assume an average of $3.125 / 1M tokens and $3.125 is about a cup of coffee 
times_to_coffee=$(echo "scale=9; 1000000 / $eval_count" | bc)
echo "TTC (Time to Coffee): $times_to_coffee"


