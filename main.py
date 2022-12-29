import openai
import requests

# Set the API key and model
openai.api_key = "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"
model_engine = "text-davinci-002"

# Set the prompt and temperature
prompt = "Create detailed Lecture Notes for the undergraduate course Physics 1 for the topic Chapter 1 Measurement And Units."
temperature = 1

# Make the request to the API
response = openai.Completion.create(
engine=model_engine,
prompt=prompt,
temperature=temperature,
max_tokens=3800,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)

# Get the generated text
generated_text = response["choices"][0]["text"]

# Print the generated text
print(generated_text)