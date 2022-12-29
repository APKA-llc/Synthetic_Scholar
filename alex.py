import openai
import requests

# Set the API key and model
openai.api_key = "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"
model_engine = "text-davinci-002"

# Set the prompt and temperature
prompt = "Write an organized, detailed lecture notes on Orthogonality for the course MATH 1554 Linear Algebra. Include relevant definitions and equations."
temperature = 0.3

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

# Print the generated text
print(response["choices"][0]["text"])