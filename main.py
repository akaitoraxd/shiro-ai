import yaml
import os
import json
from openai import OpenAI

# Load character config from YAML file
with open("character_config.yaml", "r") as file:
    char_config = yaml.safe_load(file)

client = OpenAI(api_key=char_config.get('OPEN_AI_KEY'))

# Constant parameters
MODEL = char_config.get('model')
HISTORY_FILE = char_config.get('history_file')
SYSTEM_PROMPT =  [
        {
            "role": "system",
            "content": [
                {
                    "type": "input_text",
                    "text": char_config.get('prompt')
                }
            ]
        }
    ]

# Load memory from file
def load_memory():
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as file:
                return json.load(file)
        return SYSTEM_PROMPT


def save_memory(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=2)

# User input
print("Enter your message:")
user_input = input()

def get_shiro_response(messages):
    response = client.responses.create(
        model=MODEL,
        input=messages,
        max_output_tokens=2048,
        text={"format": {"type": "text"}}
    )
    return response


def llm_response(user_input):
    messages = load_memory()

    messages.append({
        "role": "user",
        "content": [{"type": "input_text", "text": user_input}]
    })

    shiro_response = get_shiro_response(messages)

    messages.append({
        "role": "assistant",
        "content": [{"type": "output_text", "text": shiro_response.output_text}]
    })

    save_memory(messages)
    return shiro_response.output_text

# Printing the response
print(llm_response(user_input))