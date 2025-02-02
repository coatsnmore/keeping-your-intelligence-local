#!/usr/bin/env node

import { 
    checkModelArgument, 
    makeOllamaRequest, 
    printResults,
    readJsonRequest,
    createRequestHandler
} from './utils.js';

const model = checkModelArgument();

const runStructuredTest = createRequestHandler(async () => {
    const payload = await readJsonRequest('requests/structured-request.json');
    payload.model = model;
    
    const { data, elapsedTime } = await makeOllamaRequest(payload);
    console.log("response:", data);
    printResults(data, elapsedTime);
});

runStructuredTest(); 