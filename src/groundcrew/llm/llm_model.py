from typing import Callable

class llm_model():

    def __init__(self):
        self.client = None
        pass

    def setup(self):
        pass

    def single_completion(self, query):
        pass

    def register_tool_function(self, func: Callable):
        pass





#===========================================================

import re
#import ast
def extract_json_array(text):
    # Regular expression to find a JSON-like array
    match = re.search(r'(\[\s*\{.*?\}\s*(,\w*)?\])', text, re.DOTALL)
    
    if match:
        json_part = match.group(1)  # Extract JSON array
        if json_part.endswith(",]"):
            json_part = json_part[:-2]+"]"
        if json_part.endswith(", ]"):
            json_part = json_part[:-3]+"]"
        
        try:
            #python_obj = ast.literal_eval(json_part)
            #parsed_json = json.loads(json.dumps(python_obj))  # Parse JSON

            fixed_json = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', json_part)
            parsed_json = json.loads(fixed_json)
            return parsed_json
        except json.JSONDecodeError:
            try:
                fixed_json = re.sub(r"\'([^\']*)\'", r'"\1"', json_part)
                fixed_json = fixed_json.replace("'",'"')
                fixed_json = re.sub(r'\bTrue\b', 'true', fixed_json)
                fixed_json = re.sub(r'\bFalse\b', 'false', fixed_json)
                fixed_json = re.sub(r'\bNone\b', 'null', fixed_json)
                parsed_json = json.loads(fixed_json)
                return parsed_json
            except json.JSONDecodeError:
                print(f"Invalid JSON: '{json_part}'")
                return None  # Invalid JSON
    return None  # No JSON found


import ollama
import os
import requests
import json
from types import SimpleNamespace
from ollama._utils import convert_function_to_tool
from typing import List, Callable
from groundcrew.dataclasses import Colors

class ollama_model(llm_model):

    def __init__(self, base_message:str|None=None, default_model:str|None=None):
        super().__init__()
        self._ollama_url = os.environ.get("OLLAMA_API_URL")
        self._tool_funcs = {}
        self._tools = []
        self._tool_str = ""
        self._base_message = base_message
        self._default_model = default_model

        if self._base_message is None:
            self._base_message = "You are a friendly assistant that answers user questions."


    def setup(self)->None:
        self._client = ollama.Client(self._ollama_url)

    def get_models(self)->List[str]:
        response = requests.get(f"{self._ollama_url}/api/tags")
        response_obj = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
        model_names = [model.name for model in response_obj.models]
        return model_names
    

    def register_tool_object(self, name, obj, func: Callable)->None:

        tool = convert_function_to_tool(func)
        tool.function.name = name
        #print(tool)
        self._tool_str += f"""
- Tool {tool.function.name}
Name: '{tool.function.name}'
Description: {tool.function.description}
Parameters (given here as object with properties that are the parameters):
    {tool.function.parameters}

"""
        self._tool_funcs[name] = lambda **args: func(obj,**args)
        self._tools.append(tool)
        self._tools_system_prompt = None


    def register_tool_function(self, func: Callable)->None:
        tool = convert_function_to_tool(func)
        #print(tool)
        self._tool_str += f"""
- Tool {tool.function.name}
Name: '{tool.function.name}'
Description: {tool.function.description}
Parameters (given here as object with properties that are the parameters):
    {tool.function.parameters}

"""
        self._tool_funcs[tool.function.name] = func
        self._tools.append(tool)
        self._tools_system_prompt = None



    def call_tool(self, tool)->any:
        tool_name = tool['name']
        if tool_name not in self._tool_funcs:
            raise Exception(f"tool {tool_name} unknown")
        
        func = self._tool_funcs[tool_name]
        arguments = tool["arguments"]
        if 'reason' in arguments:
            arguments.pop('reason', None)

        return func(**arguments)
        

    def single_completion(self, query, model:str|None=None)->tuple:
        print(f"\n=== {query} ===")

        if model is None:
            model = self._default_model
        if model is None:
            raise Exception(f"no model given for query '{query}'")
        
        input_messages=[]

        try:
            tools_system_prompt = self._get_tools_system_prompt()

            input_messages = [ 
                            {'role': 'system', 'content':self._base_message},#+"\n"+tools_system_prompt}, 
                            {'role': 'user', 'content':"### Question ###\n"+query}
                        ]
            
            answer = self._client.chat(model=model,
                                messages=input_messages,
                                tools=self._tools
                )

        except Exception as ex:

            tools_system_prompt = self._get_tools_system_prompt()

            if "does not support tools" in str(ex):

                input_messages = [ 
                    {'role': 'system', 'content':self._base_message+"\n"+tools_system_prompt}, 
                    {'role': 'user', 'content':"### Question ###\n"+query}
                ]
                answer = self._client.chat(model=model,
                                messages=input_messages,
                )
            else:
                print(f"{type(ex).__name__}, model {model.name}: {ex}")
                raise ex



        print(Colors.MAGENTA)
        for input_message in input_messages:
            print("\n"+input_message["role"]+":")
            print(Colors.MAGENTA)
            print(input_message["content"])
        print(Colors.CYAN)
        print("\n"+answer.message["role"]+":")
        print(answer.message["content"])
        print(Colors.ENDC)
        #print(f"\nResponse: {answer.message}\n")

        chosen_tools = None
        if answer.message.tool_calls is not None:
            arr=[]
            for toolcall in answer.message.tool_calls:
                tool_calls_serializable = {"name":toolcall.function.name, "arguments": toolcall.function.arguments}
                parsed_json = json.loads(json.dumps(tool_calls_serializable))
                arr.append(parsed_json)
            chosen_tools = json.loads(json.dumps(arr))
        else:
            chosen_tools = extract_json_array(answer.message.content)
        


        print(chosen_tools)

        return (answer, chosen_tools)

    def _get_tools_system_prompt(self)->str:

        if self._tools_system_prompt is not None:
            return self._tools_system_prompt

        CHOOSE_TOOL_PROMPT1 = """
Your task is to address a question or command from a user in the Question seciton. You will do this in a step by step manner. 
For that, you have at your dispense a set of Tools listed below that provide information for you to answer the Question in detail.
Look at the Tool descriptions and choose one (or more) which seams likely to give you specific information to answer the users query in the Question section. 

# List of Tools:
"""

        CHOOSE_TOOL_PROMPT2 = """

*These are the only Tools available to you.*
If none of the above available Tools seams helpfull, answer they user query directly. In this case you can answer freely (use ```the code block format``` if you cite code) and the instructions below are irrelevant.


# Format of response if chosen Tools:

When chosing Tools, express this by a specificly formated response (format below, inclusive Example), where you state the chosen Tool names and their Arguments. 
It is paramount to use this format. Do not engage in additional explanations.
Do not use references to parameter values, you must put the value being passed in the Parameter value section. 
If passing in code as parameter value, do not include backticks.

The Tool Choice format starts by the literal 'tool_calls:' then followed by a correctly formated JSON string containing a list of Tool calls. 
Each separate Tool call consists of a dictionary with
  - a key "name" with the name of the chosen Tool as value and 
  - a key "arguments" with a dictionary containing the name and values of the arguments to pass to the function. (if you don't know the argument value pass None as value)
  - optional: a reason for choosing this tool

# Example with a given tool description (given tool is fictional, just an Example, not available as choice):

  User query: 'why is the sky blue?'

  Example tool description:
    - Name: 'FetchDocument'
    Description: 'Provides documents containing information regarding a users query'
    Parameters (given here as object with properties that are the parameters):
        type='object', required=['self','query'], properties={'self': Property(type='string', description=''), 'query': Property(type='string', description='user query')}

  Expected response (json string):
    tool_calls: [{"name":"FetchDocument", "arguments": {query: "why is the sky blue?"}, "reason": "the tool is likely to provide documents that explain why the sky is blue"}]

# Do not invent new Tools. Do not ask the user for filepaths or filenames. You must use the tools available to you. The given tools are NOT part of the codebase, only select from them, do not talk about them. Be careful to format in valid JSON format.
"""

        tools_system_prompt = CHOOSE_TOOL_PROMPT1 + self._tool_str + CHOOSE_TOOL_PROMPT2

        self._tools_system_prompt = tools_system_prompt

        return tools_system_prompt