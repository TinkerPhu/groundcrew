from dotenv import load_dotenv
load_dotenv("..")

import json


from groundcrew.toolfolder.code_analysis_tools import tool_functions as code_tool_functions


user_query_dicts = [
    {"query":"how is the system message for each call to the llm built?"                         , "tool_calls": [{"name": "CodebaseQATool", "arguments": {"user_prompt": "explain how the system message for each LLM call is constructed within the system", "include_code": True}}]}, 
    {"query":"how exactly is the system message for each call to the llm built in the codebase?" , "tool_calls": [{"name": "CodebaseQATool", "arguments": {"user_prompt": "explain the process of constructing system messages for each LLM call within the codebase", "include_code": True }}]}, 
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
        if modified_chosen_tools is None:
            print(f"Assertion: wrong tool_calls for query '{query}': {chosen_tools}")
        else:
            print(f"Assertion: unexpected tool call for query '{query}': {chosen_tools}")
    else:
        print(f"correct tool choice")   




from groundcrew.llm.llm_model import ollama_model

#llmO = ollama_model(base_message="You are a specialist for code analysis. The user will ask questions to a codebase that is available to you by utilizing tools you are given. Using them will give you the required information to answer the query. Do not speculate about the codebase, use the tools to request details.")
llm = ollama_model(base_message="You are an assistant that answers question about a codebase. All of the user's questions should be about this particular codebase, and you will be given tools that you can use to help you answer questions about the codebase.")
# llmO = ollama_model(base_message="You are an assistant that answers question about a codebase. All of the user's questions should be about this particular codebase, and you will be given tools that you can use to help you answer questions about the codebase."+"""
# Look at the Tool descriptions and choose one (or more) which seams likely to give you specific information to answer the users query in the Question section. 
# """)
llm.setup()


for function in code_tool_functions:
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
            try:
                tool_answer = llm.call_tool(tool)
                print(tool_answer)
            except Exception as ex:
                print(ex)

        assert_tool_calls(query, query_dict["tool_calls"], chosen_tools)

        
print("\n\n*** all done ***")