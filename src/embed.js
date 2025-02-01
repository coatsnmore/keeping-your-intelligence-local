#!/usr/bin/env node

import { checkModelArgument, makeOllamaRequest, printResults } from './utils.js';
import fs from 'fs/promises';

// const model = checkModelArgument();
// const model = 'qwen2.5-coder:0.5b';
const model = 'all-minilm';

const runEmbedTest = async function() {
    try {
        // Read the technical documentation
        const docData = await fs.readFile('resources/technical-documentation.md', 'utf-8');
        
        const payload = {
            model,
            input: docData,
            stream: false
        };

        const { data, elapsedTime } = await makeOllamaRequest(payload, '/api/embed');
        // console.log("Raw response data:", data);
        console.log("Embedding vector:", data.embeddings);
        console.log("Dimensions:", data.embeddings.length);
        console.log("Elapsed time:", elapsedTime, "seconds");
        printResults(data, elapsedTime);


    } catch (error) {
        console.error('Error:', error);
        process.exit(1);
    }
}

runEmbedTest(); 