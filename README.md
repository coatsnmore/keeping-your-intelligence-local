# Keeping Your Intelligence Local (and Cheap)

## Run the Example

1. Startup the Docker Compose stack
```bash
# start ollama and open webui
docker compose -f ollama.yml up -d

# turn off when done
docker compose -f ollama.yml down
```

2. Sign up an account. This stay local. Use `admin@admin.com/admin`
3. Admin > Settings


(First time only) Prime the pump for Ollama serving its API by bootstrapping a model
```bash
docker ps -a
docker exec -it ollama /bin/bash
% ollama pull llama2:7b
```

## Reasoning Test

"Please add a pair of parentheses to the incorrect equation: 1 + 2 * 3 + 4 * 5 + 6 * 7 + 8 * 9 = 479, to make the equation true."

## References

### General Knowledge
* [Blog Article - Reasoning with Ollama](https://heidloff.net/article/reasoning-ollama/)
* [Youtube Video - Matt Berman](https://www.youtube.com/@matthew_berman)
* [Youtube Video - Matt Wolfe](https://www.youtube.com/@mreflow)
* [Youtube Video - Matt Williams](https://www.youtube.com/@technovangelist)

### Technology and Tools
* [QwQ - Qwen with Questions](https://qwenlm.github.io/blog/qwq-32b-preview/)