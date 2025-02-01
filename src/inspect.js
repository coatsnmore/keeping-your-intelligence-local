#!/usr/bin/env node

import { checkModelArgument } from './utils.js';
import fetch from 'node-fetch';

const model = checkModelArgument();
// const OLLAMA_ENDPOINT = 'http://ollama:11434';
const OLLAMA_ENDPOINT = 'http://localhost:11434';

async function inspectModel() {
    try {
        const response = await fetch(`${OLLAMA_ENDPOINT}/api/show`, {
            method: 'POST',
            body: JSON.stringify({ model }),
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();
        console.log(JSON.stringify(data, null, 2));
        
        // if (data.model_info) {
        //     console.log('\nContext Length:', data.model_info.context_length);
        // }
    } catch (error) {
        console.error('Error:', error);
        process.exit(1);
    }
}

inspectModel(); 