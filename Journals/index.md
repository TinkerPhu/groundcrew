[[example_session]]
[[example_llm_call_openai]]
[[example_llm_call_deepseek]]


#findings 
- the llm is called with the chat function, e.g:
```python
input_messages = [
  {'content': '\nYou are an assistant that answers question about a codebase.', 'role': 'system'}, 
  {'content': '### Question ###\n how is the system message for each call to the llm built?', 'role': 'user'}
]
model='deepseek-r1:32b'

response = client.chat(
                messages=input_messages,
                model=model,
```

- I examined, how tools are included into a llm call:
  groundcrew adds them into the system prompt by just textually describe them and instruct the llm to choose the most appropriate one regarding the given user prompt. This ends up in the messages parameter.
- Other suggestions from the net [[[Tool Calling in LLMs: An Introductory Guide : r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/comments/1fvdtqk/tool_calling_in_llms_an_introductory_guide/)]] are:
> You can call the following scripts in the following way
>  
> !!script!! weather.py (zip code) 
> !!script!! calendar.py 
> !!script!! search.py (search query) 
>  So for example, you can say 
> !!script!! weather.py 12345 
> 
> and you'll get the forecast returned

 '''
- tools can be initialized in the call by