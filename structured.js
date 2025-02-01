#!/usr/bin/env node

import { checkModelArgument, makeOllamaRequest, printResults } from './utils.js';
import fs from 'fs/promises';

const model = checkModelArgument();

async function runStructuredTest() {
    try {
        // Read the structured request JSON data
        const structuredData = await fs.readFile('structured-request.json', 'utf-8');
        const payload = JSON.parse(structuredData);
        
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

runStructuredTest(); 