# Keeping Your Intelligence Local (and Cheap)

## Preprequisites

* Command Line Tools (only if you don't use Docker): `jq`, `bc`, `git`, `base64`, `node`, `curl`
* Docker Engine (or Podman)
* Docker Compose or equivalent client (e.g. `docker-compose`, `podman`)
* Docker Socket access (only worry about this if something breaks - OpenWebUI assumes socket access by default)
* general HTTP egress acccess (fetches model and container binaries)

## Project Structure

```
.
├── collections/     # Bruno API collections for testing
├── models/         # Modelfiles for custom models
├── requests/       # JSON request templates
│   ├── function-calling.json    # Function calling examples
│   └── structured-request.json  # Structured output examples
├── resources/      # Static resources
│   ├── cats.base64             # Test image for vision models
│   ├── cats.jpeg              # Original test image
│   └── technical-documentation.md  # Test document for embeddings
└── src/           # Node.js test scripts
    ├── cats.js         # Vision model testing
    ├── code.js         # Code generation testing
    ├── embed.js        # Embedding generation
    ├── function-calling.js  # Function calling tests
    ├── inspect.js      # Model inspection
    ├── load-model.js   # Model loading utility
    ├── structured.js   # Structured output testing
    ├── test.js         # Basic generation testing
    └── utils.js        # Shared utilities
```

## Clone the Repo

```bash
# Clone this repo with 
git clone https://github.com/coatsnmore/keeping-your-intelligence-local
```

## Run the Docker Compose Stack and Attach to the Workspace Container

```bash
# start ollama, open webui, and a shell environment with some tooling
docker compose up --build -d

# check out the deployed containers
docker ps

# attach to the intelligence container
docker exec -it intelligence /bin/bash

# after you are done, you can turn this off with
# docker compose down
```

## Available Scripts

Run these scripts from within the intelligence container:

```bash
# load the models
npm run load tinyllama
npm run load llava
npm run load all-minilm

# test the model
npm run test tinyllama

# test image recognition
npm run cats llava

# test function calling
npm run function tinyllama

# test structured output
npm run structured

# test embeddings
npm run embed
```


## Open Web UI

1. Open the Open Web UI application in your browser at [`http://localhost:3000`](http://localhost:3000)
1. Sign up an account. This stays local, but use credentials you don't care about. Use `admin@admin.com/admin`

## References

### General Knowledge

* [Blog - Reasoning with Ollama](https://heidloff.net/article/reasoning-ollama/)
* [Youtube - Matt Berman](https://www.youtube.com/@matthew_berman)
* [Youtube - Matt Wolfe](https://www.youtube.com/@mreflow)
* [Youtube - Matt Williams](https://www.youtube.com/@technovangelist)

### Technology and Tools

* [Ollama - API Docs](hhttps://github.com/ollama/ollama/blob/main/docs/api.md)
* [QwQ - Qwen with Questions](https://qwenlm.github.io/blog/qwq-32b-preview/)
* [Ollama with Spring Boot](https://docs.spring.io/spring-ai/reference/api/chat/ollama-chat.html#:~:text=Ollama%20is%20OpenAI%20API%2Dcompatible,openai.)
* [Ollama Function Calling aka Format JSON](https://www.youtube.com/watch?v=RXDWkiuXtG0)


## Some Common Issues

```bash
# clean it up
sudo docker system prune --all --volumes`
```