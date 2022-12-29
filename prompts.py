import openai
import requests
import re

import textwrap
from fpdf import FPDF




# Set the API key and model
openai.api_key = "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"
model_engine = "text-davinci-002"

# Set the prompt and temperature
subject = "MATH 1554 Linear Algebra"
prompt = "Create a list of topics you would study in a " + subject + " course in a bulleted format."
print(prompt)

# Make the request to the API
response = openai.Completion.create(
engine=model_engine,
prompt=prompt,
temperature=0,
max_tokens=1000,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)

# Get the generated text
generated_text = response["choices"][0]["text"]

# Print the generated text
#print(generated_text)


topic_pattern = re.compile(("(.)\s?(.+)"))
topics_found = topic_pattern.finditer(generated_text)
topics = []
for topic in topics_found:
    topics.append(topic.group(2).strip())

print(topics)


