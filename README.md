# Keeping Your Intelligence Local (and Cheap)

## Preprequisites

* Command Line Tools (only if you don't use Docker): `jq`, `bc`, `git`, `base64`
* Clone this repo with `git clone https://github.com/coatsnmore/keeping-your-intelligence-local`
* Docker Engine (or Podman)
* Docker Compose or equivalent client (e.g. `docker-compose`, `podman`)
* Docker Socket access (only worry about this if something breaks - OpenWebUI assumes socket access by default)
* general HTTP egress acccess (fetches model and container binaries)

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

## Boostrap Ollama with tinyllama

```bash
# request Ollama to pull down model
./load-model.sh tinyllama
```

## Test Basic Text Prompt against Ollama serving a Tiny Model
```bash
# run a prompt against tinyllama
./test.sh tinyllama
```

## (Optional) Test a Slightly More Capable Model

```bash
# load llama3
./load-model.sh llama3.2:1b

# test llama3
./test.sh llama3.2:1b
```

## Test Vision Model

```bash
# load a vision model
./load-model.sh llava

# let's look at some cats
./cats.sh
```

## Structured Output for Function Calling

```bash
# get some valid JSON
./structured.sh

# inspect the request payload
cat structured-request.json
```

## Embeddings

```bash
# load the embedding model
./load-model.sh all-minilm

# create an embedding from a local file
./embed.sh
```
## Test out Open Web UI

1. Open the Open Web UI application in your browser at [`http://localhost:3000`](http://localhost:3000)
1. Sign up an account. This stays local, but use credentials you don't care about. Use `admin@admin.com/admin`

##  Reasoning Test

"Please add a pair of parentheses to the incorrect equation: 1 + 2 * 3 + 4 * 5 + 6 * 7 + 8 * 9 = 479, to make the equation true."

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