#!/usr/bin/env node

import { checkModelArgument, makeOllamaRequest, printResults } from './utils.js';

const model = checkModelArgument();

async function runTest() {
    
    const payload = {
        model: model,
        stream: false,
        prompt: "What are mirror neurons and how do they relate to empathy in primates?"
    };

    const { data, elapsedTime } = await makeOllamaRequest(payload);
    console.log("response:", data);
    printResults(data, elapsedTime);
}

runTest(); 