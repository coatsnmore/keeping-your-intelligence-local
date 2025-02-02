#!/usr/bin/env node

import { checkModelArgument, makeOllamaRequest, logResponse } from './utils.js';

const model = checkModelArgument();
// const OLLAMA_ENDPOINT = 'http://ollama:11434';
const OLLAMA_ENDPOINT = 'http://localhost:11434';

async function inspectModel() {
    const payload = { model };
    const { data } = await makeOllamaRequest(payload, '/api/show');
    logResponse('Model Information', JSON.stringify(data, null, 2));
}

inspectModel(); 