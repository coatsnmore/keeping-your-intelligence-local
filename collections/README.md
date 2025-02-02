# Bruno Collections for Ollama API

This directory contains Bruno API collections for testing and interacting with the Ollama API.

## Overview

The collections provide a set of pre-configured API requests for common Ollama operations, making it easy to test and explore the API functionality.

## Collections

### Ollama API Collection
Contains requests for:
- Model Management
  - List Models
  - Show Model Details
  - Pull Models
  - Delete Models
- Generation
  - Text Generation
  - Chat Completion
  - Function Calling
  - Structured Output
- Embeddings
  - Generate Embeddings

## Usage

1. Install Bruno:
   ```bash
   npm install -g @usebruno/cli
   ```

2. Run requests from collection root:
   ```bash
   cd collections/Ollama
   bru run --env local
   ```

## Environment Variables

The collection uses the following environment variables:
- `OLLAMA_ENDPOINT`: The Ollama API endpoint (default: http://localhost:11434)

## Related Files

- `.env`: Environment configuration
- `models/`: Modelfiles for custom models
- `prompts/`: Prompt templates
- `requests/`: JSON request templates

## Testing

Use these collections to test:
- Model loading and inspection
- Text generation capabilities
- Function calling
- Structured output formatting
- Embedding generation
- Error handling

## Contributing

Feel free to add new requests or improve existing ones. Please maintain the existing structure and documentation format. 