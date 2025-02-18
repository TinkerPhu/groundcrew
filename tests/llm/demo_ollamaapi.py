"""
Demo for ollama API.
"""


from unittest.mock import patch

import pytest
import ollama
import json

from groundcrew.llm import ollamaapi


from ollama import ChatResponse

from ollama import Client
client = Client(
  host='http://10.202.48.60:11434',
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


