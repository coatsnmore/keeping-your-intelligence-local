#!/usr/bin/env node

import { 
    makeOllamaRequest, 
    printResults,
    readResourceFile,
    createRequestHandler,
    logResponse
} from './utils.js';

// const model = checkModelArgument();
// const model = 'qwen2.5-coder:0.5b';
const model = 'all-minilm';

const runEmbedTest = createRequestHandler(async () => {
    const docData = await readResourceFile('resources/technical-documentation.md');
    
    const payload = {
        model,
        input: docData,
        stream: false
    };

    const { data, elapsedTime } = await makeOllamaRequest(payload, '/api/embed');
    logResponse('Embedding vector', data.embeddings);
    logResponse('Dimensions', data.embeddings.length);
    logResponse('Elapsed time', `${elapsedTime} seconds`);
    printResults(data, elapsedTime);
});

runEmbedTest(); 