# Weather Report Using ToolCall

(Add introduction)

## Features

- Provides ToolCall option for the LLM, letting the model decide if such tool is needed depending on the question
- Executes the ToolCall funtion locally. In this example, it is a Weather API
- Fetches temperature, humidity, sunrise/sunset, wind, and more
- LLM will be asked again with the same question, while providing the output of the ToolCall to aid in its answer

## Requirements

- Python 3.10.6 (or above)
- [Ollama](https://ollama.com) 0.9.0
- pull LLM model "llama 4", or use [other models](https://ollama.com/blog/streaming-tool) that supports tool calling (after pulling, update the value of llm_model accordingly)

Install Python library dependencies:
```bash
pip install requests ollama
```

