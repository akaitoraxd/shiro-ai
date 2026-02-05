import yaml

from openai import OpenAI

# Load character config from YAML file
with open("character_config.yaml", "r") as file:
    char_config = yaml.safe_load(file)

client = OpenAI(api_key=char_config.get('OPEN_AI_KEY'))

# User input
print("Enter your message:")
user_input = input()

# Create a response
response = client.responses.create(
    model=char_config.get('model'),
    input= user_input
)

# Printing the response
print(response.output_text)