from dotenv import load_dotenv
load_dotenv("..")

import json

from groundcrew.toolfolder.time_tools import tool_functions as time_tool_functions


user_query_dicts = [
    {"query":"what's the current time?"               , "tool_calls": [{"name": "get_time", "arguments": {}}]}, 
    {"query":"what is 234 + 345?"                     , "tool_calls": [{"name": "add_numbers", "arguments": {"x": 234, "y": 345}}]}, 
    {"query":"is there an animal with fur and beak?"  , "tool_calls": None}
    ]

def assert_tool_calls(query, expected, chosen_tools):
        
    if chosen_tools is not None:
        modified_chosen_tools = json.loads(json.dumps(chosen_tools))
        for obj in modified_chosen_tools:
            obj.pop('reason', None)
    else:
        modified_chosen_tools = None

    if modified_chosen_tools != expected:
        if modified_chosen_tools is not None:
            print(f"unexpected tool call for query '{query}': {chosen_tools}")
        else:
            print(f"wrong tool_calls for query '{query}': {chosen_tools}")
    else:
        print(f"correct tool choice")   




from groundcrew.llm.llm_model import ollama_model

llm = ollama_model()
llm.setup()

for function in time_tool_functions:
    llm.register_tool_function(function)


models = llm.get_models()
for model in models:
    print(f"\n\n### {model} ###")
    for query_dict in user_query_dicts:
        query = query_dict["query"]

        answer, chosen_tools = llm.single_completion(query, model)

        if chosen_tools is None:
            continue

        for tool in chosen_tools:
            tool_answer = llm.call_tool(tool)
            print(tool_answer)

        assert_tool_calls(query, query_dict["tool_calls"], chosen_tools)
       

        
print("\n\n*** all done ***")