
import requests
from datetime import datetime
import json
import ollama
from ollama import ChatResponse

# --- Weather API tool function ---

################ Important: Replace 'your-weather-api-key' with the actual api key ################
# I used API Ninja's free API here (just needed to sign up an account), if using another API, the API call might be different

API_KEY = 'your-weather-api-key'
HEADERS = {'X-Api-Key': API_KEY}

def get_weather(city_name: str) -> str:
    city_url = f'https://api.api-ninjas.com/v1/city?name={city_name}'
    city_response = requests.get(city_url, headers=HEADERS)
    if city_response.status_code != 200:
        return f"City API error: {city_response.status_code} - {city_response.text}"
    
    city_data = city_response.json()
    if not city_data:
        return f"No results found for city: {city_name}"
    
    lat = city_data[0]['latitude']
    lon = city_data[0]['longitude']

    weather_url = f'https://api.api-ninjas.com/v1/weather?lat={lat}&lon={lon}'
    weather_response = requests.get(weather_url, headers=HEADERS)
    if weather_response.status_code != 200:
        return f"Weather API error: {weather_response.status_code} - {weather_response.text}"

    weather_data = weather_response.json()

    sunrise = datetime.fromtimestamp(weather_data['sunrise']).strftime('%H:%M:%S')
    sunset = datetime.fromtimestamp(weather_data['sunset']).strftime('%H:%M:%S')

    result = (
        f"Weather in {city_name.title()}:\n"
        f"Temperature: {weather_data['temp']} C (Feels like: {weather_data['feels_like']} C)\n"
        f"Cloud cover: {weather_data['cloud_pct']} %\n"
        f"Wind speed: {weather_data['wind_speed']} m/s\n"
        f"Wind direction: {weather_data['wind_degrees']} degrees\n"
        f"Humidity: {weather_data['humidity']} %\n"
        f"Max temperature: {weather_data['max_temp']} C\n"
        f"Min temperature: {weather_data['min_temp']} C\n"
        f"Sunrise: {sunrise}\n"
        f"Sunset: {sunset}"
    )
    return result


# --- Ollama chat interaction with tool integration ---
def main():
    llm_model = 'llama4'
    tools = [get_weather]

    messages = [
        {'role': 'user', 'content': 'What is the weather in London?'}
    ]

    ################ Important: You may need to replace 'http://localhost:11434' with the actual IP address or hostname ################
    # and port of your remote Ollama server
    # For example: ollama_host = 'http://192.168.1.100:11434'

    ollama_host = 'http://localhost:11434' 


    # Initialize the Ollama client with the specified host
    client = ollama.Client(host=ollama_host)

    response: ChatResponse = client.chat( # Call chat on the client instance
        model=llm_model,
        messages=messages,
        tools=tools,
        stream=True
    )

    tool_result = None
    tool_call_id = None

    print("\nModel response:\n")

    for chunk in response:
        if chunk.message.content:
            print(chunk.message.content, end='', flush=True)

        if chunk.message.tool_calls:
            for call in chunk.message.tool_calls:
                tool_call_id = getattr(call, 'id', 'tool-call-1')

                args = call.function.arguments
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        print("\nWarning: Could not parse tool call arguments.")
                        args = {}

                print(f"\n\nTool called: {call.function.name} with args {args}")

                try:
                    if call.function.name == "get_weather":
                        tool_result = get_weather(**args)
                        print(f"Tool result:\n{tool_result}")
                except Exception as e:
                    print(f"Error calling tool: {e}")

    if tool_result is None:
        print("\n\nNo tool was called. Model may have responded directly.")

    if tool_result is not None and tool_call_id is not None:
        followup_messages = messages + [
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": tool_result
            }
        ]

        final_response = client.chat( # Call chat on the client instance again
            model=llm_model,
            messages=followup_messages,
            tools=tools,
            stream=True
        )

        print("\n\nFinal response from model:\n")
        for chunk in final_response:
            if chunk.message.content:
                print(chunk.message.content, end='', flush=True)
        print("\n\n")

if __name__ == "__main__":
    main()







