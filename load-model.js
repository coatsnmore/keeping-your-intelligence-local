#!/usr/bin/env node

import { checkModelArgument } from './utils.js';
import fetch from 'node-fetch';

const model = checkModelArgument();
// const OLLAMA_ENDPOINT = 'http://ollama:11434';
const OLLAMA_ENDPOINT = 'http://localhost:11434';


async function loadModel() {
    try {
        // Pull the model
        console.log(`Pulling model: ${model}`);
        const pullResponse = await fetch(`${OLLAMA_ENDPOINT}/api/pull`, {
            method: 'POST',
            body: JSON.stringify({ model }),
            headers: { 'Content-Type': 'application/json' }
        });

        // Read response as text chunks
        for await (const chunk of pullResponse.body) {
            const text = new TextDecoder().decode(chunk);
            const lines = text.split('\n').filter(line => line.trim());
            
            // Parse and log each line
            for (const line of lines) {
                try {
                    const data = JSON.parse(line);
                    if (data.status) console.log(data.status);
                    if (data.error) throw new Error(data.error);
                } catch (e) {
                    if (e.message !== "Unexpected end of JSON input") {
                        console.error('Parse error:', e);
                    }
                }
            }
        }

        // // List loaded models
        // const tagsResponse = await fetch(`${OLLAMA_ENDPOINT}/api/tags`);
        // const tagsData = await tagsResponse.json();
        // console.log('\nLoaded models:', JSON.stringify(tagsData, null, 2));
    } catch (error) {
        console.error('Error:', error);
        process.exit(1);
    }
}

loadModel(); 