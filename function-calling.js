#!/usr/bin/env node

import { checkModelArgument, makeOllamaRequest, printResults } from './utils.js';
import fs from 'fs/promises';

const model = checkModelArgument();

async function runFunctionTest() {
    try {
        // Read the function calling JSON data
        const functionData = await fs.readFile('function-calling.json', 'utf-8');
        const payload = JSON.parse(functionData);
        
        // Ensure the model from command line is used
        payload.model = model;
        
        const { data, elapsedTime } = await makeOllamaRequest(payload);
        console.log("response:", data);
        printResults(data, elapsedTime);
    } catch (error) {
        console.error('Error:', error);
        process.exit(1);
    }
}

runFunctionTest(); 