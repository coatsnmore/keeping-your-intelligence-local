#!/usr/bin/env node

import { checkModelArgument, makeOllamaRequest, printResults } from './utils.js';
import fs from 'fs/promises';

const model = checkModelArgument();

async function runImageTest() {
    try {
        // Read the base64 image data
        const imageData = await fs.readFile('resources/cats.base64', 'utf-8');
        
        const payload = {
            model,
            stream: false,
            prompt: "What is going on in this picture?",
            images: [imageData.trim()]
        };

        const { data, elapsedTime } = await makeOllamaRequest(payload);
        console.log("response:", data);
        printResults(data, elapsedTime);

    } catch (error) {
        console.error('Error:', error);
        process.exit(1);
    }
}

runImageTest(); 