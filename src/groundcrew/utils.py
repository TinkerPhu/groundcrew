"""
Utility functions
"""
import os
import ast
import inspect
import importlib
import re

from typing import Any, Callable

import yaml
import astunparse

from chromadb import Collection

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter

from groundcrew import constants, system_prompts as sp
from groundcrew.llm import llmapi
from groundcrew.llm.llmapi import Message
from groundcrew.dataclasses import Tool


def highlight_code_helper(text: str, colorscheme: str) -> str:
    """
    Highlights code in a given text string.

    Args:
        text (str): The text optionally including code to highlight.
        colorscheme (str): The colorscheme to use for highlighting.
    Returns:
        str: The text with code highlighted.
    """

    start_idx = text.find('```python')
    end_idx = text.find('```', start_idx + 1)

    # No python code found
    if start_idx == end_idx == -1:
        return text

    code = ''
    if '```python' in text:
        code = text.split('```python')[1].split('```')[0]
        code = highlight(
            code,
            PythonLexer(),
            Terminal256Formatter(style=colorscheme, background='dark'))

    return text[:start_idx] + code + text[end_idx + 3:]


def highlight_code(text: str, colorscheme: str) -> str:
    """
    Uses the helper function to highlight code in a given text

    Args:
        text (str): The text optionally including code to highlight.
        colorscheme (str): The colorscheme to use for highlighting.
    Returns:
        str: The text with code highlighted.
    """

    if '```python' not in text:
        return text

    out = highlight_code_helper(text, colorscheme)

    while '```python' in out:
        out = highlight_code_helper(out, colorscheme)

    return out


def build_llm_chat_client(
        model: str = constants.DEFAULT_MODEL) -> Callable[[list[Message]], str]:
    """Make an LLM client that accepts a list of messages and returns a response."""
    if 'gpt' in model:
        client = llmapi.get_llm_client()
        chat_session = llmapi.start_chat(model, client)

        def chat(messages: list[Message]) -> Message:
            return chat_session(messages)
    else:
        client = llmapi.get_llm_client()
        chat_session = llmapi.start_chat(model, client)

        def chat(messages: list[Message]) -> Message:
            return chat_session(messages)
    
    return chat

def build_llm_completion_client(
        model: str = constants.DEFAULT_MODEL) -> Callable[[str], str]:
    """Make an LLM client that accepts a string prompt and returns a response."""
    if 'gpt' in model:
        client = llmapi.get_llm_client()
        completion = llmapi.start_chat(model, client)

        def chat_complete(prompt):
            try:
                messages = [
                    llmapi.SystemMessage("You are a helpful assistant."),
                    llmapi.UserMessage(prompt)
                ]
                response = completion(messages)
                return response.content
            except Exception:
                return ''

    else:
        client = llmapi.get_llm_client()
        completion = llmapi.start_chat(model, client)

        def chat_complete(prompt):
            try:
                messages = [
                    llmapi.SystemMessage("You are a helpful assistant."),
                    llmapi.UserMessage(prompt)
                ]
                response = completion(messages)
                return response.content
            except Exception as ex:
                print("=== Exception === :", ex)
                return ''

    return chat_complete


def setup_and_load_yaml(filepath: str, key: str) -> dict[str, dict[str, Any]]:
    """
    Helper function to set up workspace, create a file if it doesn't exist,
    and load data from a YAML file.

    Args:
        filepath (str): The path to the YAML file.
        key (str): The key to extract data from the loaded YAML file.

    Returns:
        dict: A dictionary containing processed data extracted from the YAML
        file. If the file doesn't exist or the data is None, an empty
        dictionary is returned.
    """

    # Create a file if it doesn't exist
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            pass

    # Load data from the file
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)

    # Process the loaded data
    if data is None:
        return {}

    return {item['name']: item for item in data[key]}


def setup_tools(
        modules_list: list[dict[str, Any]],
        tool_descriptions: dict[str, dict[str, str]],
        collection: Collection,
        llm: Callable,
        working_dir_path: str) -> dict[str, Tool]:
    """
    This function sets up tools by generating a dictionary of Tool objects
    based on the given modules and tool descriptions.

    Args:
        modules_list (list): A list of dictionaries containing modules and the
        functions to be used from those modules.
        tool_descriptions (dict): A dictionary containing descriptions for
        specific tools.

    Returns:
        tools (dict): A dictionary containing Tools with each key being the
        tool name
    """

    # Parameters available to a tool constructor
    params = {
        'collection': collection,
        'llm': llm,
        'working_dir_path': working_dir_path
    }

    tools = {}
    for module_dict in modules_list:
        module_name = module_dict['module']
        module = importlib.import_module(module_name)
        tools_list = module_dict['tools']

        # Loop through tools and generate descriptions
        with open(module.__file__, 'r') as f:
            file_text = ''.join(f.readlines())

        for node in ast.walk(ast.parse(file_text)):
            if isinstance(node, ast.ClassDef) and node.name in tools_list:

                # Actual code of the class
                tool_code = astunparse.unparse(node)

                # Description already generated and in yaml file, so load it.
                if node.name in tool_descriptions:
                    print(f'Loading description for {node.name}...')
                    tool_yaml = yaml.dump(
                        tool_descriptions[node.name], sort_keys=False)

                else:
                    print(f'Generating description for {node.name}...')

                    # Generate description of the Tool in YAML format
                    tool_yaml = convert_tool_str_to_yaml(tool_code, llm)

                    # In case the LLM put ```yaml at the beginning and and ```
                    # at the end
                    if '```yaml' in tool_yaml:
                        tool_yaml = '\n'.join(tool_yaml[1:-1])

                # Convert YAML to a dictionary
                
                try:
                    tool_info_dict = yaml.safe_load(tool_yaml)
                except Exception as ex:
                    print("@@@ exception for yaml.safe_load:", ex)
                    tool_yaml_fixed = try_to_fix_yaml_error(tool_yaml,ex)
                    tool_yaml_post = post_process_yaml_response(tool_yaml_fixed)
                    try:
                        tool_info_dict = yaml.safe_load(tool_yaml_post)
                    except Exception as exex:       
                        print(f"@@@ could not fix yaml: {exex}\n  ==> skipping tool {node.name}")
                        continue

                if isinstance(tool_info_dict, list):
                    tool_info_dict = tool_info_dict[0]

                # Remove the user_prompt from the params in case the LLM added
                # it
                if 'user_prompt' in tool_info_dict['params']:
                    del tool_info_dict['params']['user_prompt']

                params['base_prompt'] = tool_info_dict['base_prompt']

                tool_constructor = getattr(module, node.name)
                tool_params = inspect.signature(tool_constructor).parameters

                args = {}
                for param_name, value in params.items():
                    if param_name in tool_params:
                        args[param_name] = value

                # Create an instance of a tool object
                tool_obj = tool_constructor(**args)

                # Check that the tool object has the correct signature
                tool_err = 'Tool must have a user_prompt parameter'
                assert 'user_prompt' in inspect.signature(
                    tool_obj).parameters, tool_err

                tool_err = f'Tool {tool_obj} must return a string'
                assert inspect.signature(
                    tool_obj).return_annotation is str, tool_err

                # Add the tool to the tools dictionary
                tools[node.name] = Tool(
                    name=node.name,
                    code=tool_code,
                    description=tool_info_dict['description'],
                    base_prompt=tool_info_dict['base_prompt'],
                    params=tool_info_dict['params'],
                    obj=tool_obj)

    return tools


def convert_tool_str_to_yaml(function_str: str, llm: Callable) -> str:
    """
    Convert a given tool string to YAML format using a llm model.

    Args:
        function_str (str): The string representation of a function.

    Returns:
        str: The YAML representation of the given function string.
    """
    return llm(sp.TOOL_GPT_PROMPT + '\n\n' + function_str)


def save_tools_to_yaml(tools: dict[str, Tool], filename: str) -> None:
    """
    Converts a dictionary of tools into YAML format and saves it to a file.

    Args:
        tools (dict): A dictionary containing Tools with each key being the
        tool name
        filename (str): The name of the file to save the YAML data to.

    Returns:
        None
    """

    # Convert the tools dictionary into a list of dictionaries
    tools_list = []
    for tool in tools.values():
        tool_dict = {}
        tool_dict['name'] = tool.name
        tool_dict['description'] = tool.description
        tool_dict['base_prompt'] = tool.base_prompt
        tool_dict['params'] = tool.params
        tools_list.append(tool_dict)

    # Wrap the list in a dictionary with the key 'tools'
    data = {'tools': tools_list}

    # Write the data to the YAML file
    with open(filename, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)
    print(f'Saved {filename}\n')


def post_process_yaml_response(text):
    # Remove spaces before/after newlines and join split characters
    fixed_text = re.sub(r'(?<!\n)\n(?!\n)', '', text)
    
    fixed_text = re.sub(r'\n\n', '', fixed_text)
    
    # Handle unnecessary leading/trailing newlines
    fixed_text = fixed_text.strip()

    m = re.match(r'(``yaml\n((\n|.)*)``)', fixed_text)
    if m:
        fixed_text = m.group(2)
    print("✍")
    return fixed_text

def correct_mapping_values_are_not_allowed_here_yaml(yaml_content, error_message):
    # Extract line and column number from error message
    match = re.search(r"line (\d+), column (\d+):", error_message)
    if not match:
        print("Could not extract line and column from error message.")
        return yaml_content

    line_num, col_num = int(match.group(1)), int(match.group(2))

    # Split YAML into lines
    lines = yaml_content.split("\n")

    # Ensure the line number is within the valid range
    if line_num > len(lines):
        print("Line number out of range.")
        return yaml_content

    # Replace ':' with '.' at the specified column
    line = lines[line_num - 1]  # 0-based index
    if col_num - 1 < len(line) and line[col_num - 1] == ':':
        lines[line_num - 1] = line[:col_num - 1] + ';' + line[col_num:]

    # Join the corrected lines
    return "\n".join(lines)

def try_to_fix_yaml_error(yaml_content, error_message):
    # Apply the correction
    if "mapping values are not allowed here" in str(error_message):
        return correct_mapping_values_are_not_allowed_here_yaml(yaml_content, error_message)
    return yaml_content