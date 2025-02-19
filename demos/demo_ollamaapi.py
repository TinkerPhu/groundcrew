"""
Demo for ollama API.
"""


from unittest.mock import patch

import os
import pytest
import ollama
import json

from groundcrew.llm import ollamaapi


from ollama import ChatResponse

from ollama import Client

from dotenv import load_dotenv
load_dotenv("..")
host_url = os.environ.get("OLLAMA_API_URL")

client = Client(
  host=host_url,
  headers={'x-some-header': 'some-value'}
)

response: ChatResponse = client.chat(model='gemma2:2b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)


