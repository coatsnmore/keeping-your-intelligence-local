#!/usr/bin/env node

import fetch from 'node-fetch';
import chalk from 'chalk';

export function checkModelArgument() {
    const model = process.argv[2];
    if (!model) {
        console.error(chalk.red('No model provided. Usage: npm run <script> <model>'));
        process.exit(1);
    }
    return model;
}

export async function makeOllamaRequest(payload, endpoint = '/api/generate') {
    const OLLAMA_ENDPOINT = 'http://localhost:11434';
    const start = Date.now();

    try {
        const response = await fetch(`${OLLAMA_ENDPOINT}${endpoint}`, {
            method: 'POST',
            body: JSON.stringify(payload),
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        const elapsedTime = ((Date.now() - start) / 1000).toFixed(2);
        return { data, elapsedTime };
    } catch (error) {
        console.error(chalk.red('Request failed:'), error);
        process.exit(1);
    }
}

export function printResults(data, elapsedTime) {
    const eval_count = data.eval_count || 0;
    const prompt_eval_count = data.prompt_eval_count || 0;
    
    // Calculate tokens per second
    const eval_duration = data.eval_duration || 1;  // Prevent division by zero
    const calculationResult = eval_count / eval_duration * 1000000000;
    
    // Calculate time to coffee ($3.125 per 1M tokens)
    const timesToCoffee = 1000000 / (eval_count + prompt_eval_count);

    console.log(chalk.blue.bold("\n-------------------------------------------"));
    console.log(chalk.cyan(`Time to process request: ${chalk.green(elapsedTime)} seconds`));
    console.log(chalk.yellow(`Tokens: ${chalk.green(eval_count || 0)}`));
    console.log(chalk.magenta(`Tokens/s: ${chalk.green(calculationResult.toFixed(2))}`));
    console.log(chalk.blue(`TTC (Time to Coffee): ${chalk.green(timesToCoffee.toFixed(2))}`));
    console.log(chalk.blue.bold("-------------------------------------------\n"));
} 