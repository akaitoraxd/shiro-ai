import yaml
import os
import json
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Load character config from YAML file
with open("character_config.yaml", "r") as file:
    char_config = yaml.safe_load(file)

client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

# Constant parameters
MAX_MESSAGE = 20
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
            try:
                with open(HISTORY_FILE, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return SYSTEM_PROMPT.copy()
        return SYSTEM_PROMPT.copy()

# Save memory to file
def save_memory(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=2)

# Trim memory so the file and tokens doesn't explode
def trim_memory(messages):
    system = messages[0]
    rest = messages[1:]
    rest = rest[-MAX_MESSAGE:]
    return [system] + rest

# Sending prompt to Shiro and getting response
def get_shiro_response(messages):
    response = client.responses.create(
        model=MODEL,
        input=messages,
        max_output_tokens=2048,
        text={"format": {"type": "text"}}
    )
    return response

# Handle literraly everything
def llm_response(user_input):
    messages = load_memory()

    # So she can tell time lmao (To be honest I don't know why I make this)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_input_time = f"[User input received at {current_time}] {user_input}"

    messages.append({
        "role": "user",
        "content": [{"type": "input_text", "text": user_input_time}]
    })

    shiro_response = get_shiro_response(messages)

    messages.append({
        "role": "assistant",
        "content": [{"type": "output_text", "text": shiro_response.output_text}]
    })
    messages = trim_memory(messages)
    save_memory(messages)
    return shiro_response.output_text

# Main loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    print("Shiro:", llm_response(user_input))