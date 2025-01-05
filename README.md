# Keeping Your Intelligence Local (and Cheap)

## Preprequisites
* Command Line Tools: `jq`, `bc`, `git`
* Clone this repo with `git clone https://github.com/coatsnmore/keeping-your-intelligence-local`
* Docker Engine
* Docker Compose or equivalent client (e.g. `docker-compose`)

## Run the Docker Compose Stack
```bash
# start ollama and open webui
docker compose up -d

# check out the deployed containers
docker ps

# later, you can turn this off with
docker compose down
```

## Boostrap and Test Ollama

```bash
# boostrap Ollama by loading a model
./bootstrap.sh

# run the test script
./test.sh
```

## Test out Open Web UI
1. Open the Open Web UI application in your browser at [`http://localhost:3000`](http://localhost:3000)
1. Sign up an account. This stay local. Use `admin@admin.com/admin`

## Reasoning Test

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