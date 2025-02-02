#!/usr/bin/env node

import fetch from 'node-fetch';
import chalk from 'chalk';
import fs from 'fs/promises';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const OLLAMA_ENDPOINT = process.env.OLLAMA_ENDPOINT || 'http://localhost:11434';

export function checkModelArgument() {
    const model = process.argv[2];
    if (!model) {
        console.error(chalk.red('No model provided. Usage: npm run <script> <model>'));
        process.exit(1);
    }
    return model;
}

export async function makeOllamaRequest(payload, endpoint = '/api/generate') {
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
    const eval_count = data.eval_count || data.prompt_eval_count || 0;
    const prompt_eval_count = data.prompt_eval_count || 0;
    
    // Calculate tokens per second (using wall clock time for more accurate real-world measurement)
    const tokensPerSecond = eval_count / parseFloat(elapsedTime);
    
    // Calculate time to coffee ($3.125 per 1M tokens)
    // How many more requests like this one would we need to reach 1M tokens
    const totalTokens = eval_count + prompt_eval_count;
    const timesToCoffee = totalTokens > 0 ? (1000000 / totalTokens) : 0;

    console.log(chalk.blue.bold("\n-------------------------------------------"));
    console.log(chalk.cyan(`Time to process request: ${chalk.green(elapsedTime)} seconds`));
    console.log(chalk.yellow(`Tokens: ${chalk.green(eval_count || 0)}`));
    console.log(chalk.magenta(`Tokens/s: ${chalk.green(tokensPerSecond.toFixed(2))}`));
    console.log(chalk.blue(`TTC (Time to Coffee): ${chalk.green(timesToCoffee.toFixed(2))} requests`));
    console.log(chalk.blue.bold("-------------------------------------------\n"));
}

export async function readJsonRequest(filepath) {
    try {
        const data = await fs.readFile(filepath, 'utf-8');
        return JSON.parse(data);
    } catch (error) {
        console.error(chalk.red(`Failed to read request file: ${filepath}`), error);
        process.exit(1);
    }
}

export async function readResourceFile(filepath) {
    try {
        return await fs.readFile(filepath, 'utf-8');
    } catch (error) {
        console.error(chalk.red(`Failed to read resource file: ${filepath}`), error);
        process.exit(1);
    }
}

export function createRequestHandler(processRequest) {
    return async function() {
        try {
            await processRequest();
        } catch (error) {
            console.error(chalk.red('Error:'), error);
            process.exit(1);
        }
    };
}

export function logResponse(description, data) {
    console.log(chalk.blue.bold(`\n${description}:`));
    console.log(data);
} 