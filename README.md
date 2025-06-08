
# AI Assistant Using ToolCall Function

This project bridges the gap between AI language models and real-world data. By connecting an Ollama-served LLM with a weather API, it demonstrates how LLMs can call external tools to provide accurate, up-to-date information on demand. 

It's a hands-on example of LLM tool use, perfect for developers exploring agent-style workflows.


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
pip install -U requests ollama
```


## How It Works

### Model Analysis
The message is sent to the LLM via ollama.Client.chat(), along with a list of available tools (in this example case there is only one tool). The model determines it needs external data and issues a tool_call for the get_weather function.

### Tool Execution
The script intercepts the tool call, extracts the city_name argument, and performs the API call. 

### Result Integration
The weather data is formatted and returned to the model as a "tool" response. A second chat() call is made, passing this result so the model can incorporate it into its final reply.

### Final Output
The model produces a natural-language answer that includes the current weather conditions. 

## Customization

- Change the model name in the model='llama 4' line to any other local Ollama-compatible model

- Add more tools in the tools list can allow the model to acquire accurate real-time data is different domains








