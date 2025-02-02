#!/usr/bin/env node

import { checkModelArgument, makeOllamaRequest } from './utils.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs/promises';

const execAsync = promisify(exec);
const model = 'qwen2.5-coder:0.5b';

async function runCodeGeneration() {
    try {
        const template = `<|im_start|>system
You are a python generator. You do not explain code or provide comments. You only output text and it is always valid python.
<|im_end|>{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}
<|im_end|>{{ end }}<|im_start|>assistant
{{ .Response }}<|im_end|>`;

        const prompt = `Example prompt: "Generate me a valid python script using only built in libraries that says hello world"
Exammple Response:
print("Hello World")

Prompt: Generate me a valid python script using only built in libraries that says hello world and prints out the local time. Only output valid Python. Do not include any other words or explanation.
Response:`;

        const payload = {
            model,
            stream: false,
            prompt,
            template
        };

        const { data } = await makeOllamaRequest(payload);
        // console.log('Response data:', JSON.stringify(data, null, 2));
        // Write the Python code to app.py
        await fs.writeFile('app.py', data.response);

        // Run pylint and python
        try {
            const { stdout, stderr } = await execAsync('pylint app.py');
            console.log('Lint results:', stdout || 'No issues found');
        } catch (error) {
            // pylint exits with non-zero for both errors and warnings
            console.log('Lint results:', error.stdout || error.stderr || error.message);
        }

        const { stdout: pythonOutput } = await execAsync('python app.py');
        console.log('\nProgram output:', pythonOutput);

    } catch (error) {
        console.error('Error:', error);
        process.exit(1);
    }
}

runCodeGeneration(); 