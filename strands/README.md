# Tool Use
For tool use, tried:

* llama2

❌ Error: registry.ollama.ai/library/llama2:7b does not support tools (status code: 400)


* deepseek-r1:1.5b

❌ Error: registry.ollama.ai/library/deepseek-r1:1.5b does not support tools (status code: 400)

* qwen3:1.7b

Was able to successfully use calculator tool, but not the file_read or file_write

* gpt-4o-mini

tool=<<function file_read at 0x00000148522F3060>> | unrecognized tool specification
tool=<<function file_write at 0x0000014852637F60>> | unrecognized tool specification
🤖 Interactive Agent Loop
Type 'quit', 'exit', or 'bye'

* 