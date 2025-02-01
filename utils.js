#!/usr/bin/env node

import fetch from 'node-fetch';

export function checkModelArgument() {
    if (process.argv.length < 3) {
        console.log("No model provided. Usage: node script.js <model>");
        process.exit(1);
    }
    return process.argv[2];
}

export async function makeOllamaRequest(payload) {
    const HOST = 'localhost'; // or 'ollama'
    const API_URL = `http://${HOST}:11434/api/generate`;

    const startTime = Math.floor(Date.now() / 1000);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        const endTime = Math.floor(Date.now() / 1000);
        
        return {
            data,
            elapsedTime: endTime - startTime
        };
    } catch (error) {
        console.error('Error:', error);
        process.exit(1);
    }
}

export function printResults(data, elapsedTime) {
    const { eval_count, prompt_eval_count, eval_duration, response: promptResponse } = data;

    // Calculate tokens per second (eval_count / eval_duration * 10^9)
    const calculationResult = (eval_count / eval_duration) * 1000000000;

    // Print the results
    console.log("Prompt Response: -------------------------------------------");
    console.log(promptResponse + "\n");
    console.log("-------------------------------------------");
    console.log(`Time to process request: ${elapsedTime} seconds`);
    console.log(`Tokens: ${eval_count}`);
    console.log(`Tokens/s: ${calculationResult}`);

    // Calculate Time to Coffee (TTC)
    // $1.25 / 1m input tokens (OpenAI 1/5/25)
    // $5 / 1m output tokens
    // Average of $3.125 / 1M tokens and $3.125 is about a cup of coffee
    const timesToCoffee = 1000000 / (eval_count + prompt_eval_count);
    console.log(`TTC (Time to Coffee): ${timesToCoffee}`);
} 