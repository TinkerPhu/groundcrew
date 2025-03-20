\[user\] > ~={blue}how is the system message for each call to the llm built?=~
⠸ Thinking...

![[example_llm_call_openai.txt]]
[
	{
		'content': '
			~={red}You are an assistant that answers question about a codebase=~. All of the user\'s questions should be about this particular codebase, and ~={red}you will be given tools=~ that you can use to help you answer questions about the codebase.
			
			
			Your task is to address a question or command from a user in the ~={blue}Question=~ seciton. You will do this in a step by step manner ~={red}by choosing a single Tool=~ and parameters necessary for this task. Only ~={red}include "Tool:"=~ in your answer ~={red}if you are choosing a valid Tool=~ available to you. ~={red}When you have the necessary data=~ to complete your task, ~={red}respond directly=~ to the user with a summary of the steps taken. Do not ask the user for filepaths or filenames. You must use the tools available to you. Your answer must be in one of the following two formats.
			
			(1) If you are choosing the correct Tool and parameters, use the following format. Do not use references to parameter values, you must put the value being passed in the Parameter value section. If passing in code, do not include backticks.
			~={purple}Reason: Describe your reasoning for why this tool was chosen in 3 sentences or less.
			Tool: Tool Name
			Tool query: =~Provide a query to the Tool to get the answer to the question.~={purple}
			Parameter_0: Parameter_0 Name | Parameter value | parameter type
			...
			Parameter_N: Parameter_N Name | Parameter value | parameter type=~
			
			(2) If you are responding directly to the user\'s questions, use this format:
			~={purple}Response: Write your response here. Your response should be limited to 3 sentences or less. If you include code in your response, it should be in a code block like this:
			```python
			# Code goes here
			```=~
			
			
			~={green}\### Tools ###
			=~
			~={green}name: LintFileTool=~
			description: This tool interacts with a linter using natural language, takes a user_prompt
			  and filepath_inexact, fuzzily matches the file path, runs linting processes on the
			  identified file, and uses a large language model to answer the user\'s questions
			  about linting results.
			base_prompt: Your task is to provide information and advice on the linting results
			  for a specific file. Be clear and helpful in your guidance.
			params:
			  filepath_inexact:
				description: An inexact file path to match and identify for linting
				type: str
				required: true
			
			
			~={green}name: SingleDocstringTool=~
			description: This tool generates docstrings for a given code snippet, function, or
			  all functions in a specified file based on different scenarios.
			base_prompt: Based on the code, filename, and function name provided, generate an
			  appropriate docstring.
			params:
			  code:
				description: The code to generate a docstring for, if it is not \'none\'.
				type: str
				required: false
			  filename:
				description: The filename to query for generating docstrings for all functions
				  within, must be \'none\' if not used.
				type: str
				required: false
			  function_name:
				description: The name of the function to generate a docstring for, must be \'none\'
				  if not used.
				type: str
				required: false
			
			
			~={green}name: CodebaseQATool=~
			description: This Tool processes a user_prompt, queries a codebase, and then uses
			  a language model to provide a response that may include code snippets if requested.
			base_prompt: ~={cyan}Your task is to assist by querying the codebase and answer questions
			  based on code snippets.=~
			params:
			  include_code:
				description: Flag indicating whether to include code snippets in the response
				type: bool
				required: true
			
			
			~={green}name: CyclomaticComplexityTool=~
			description: This tool uses the user_prompt along with a specified file path and a
			  choice to sort based on average or maximum complexity, to compute the cyclomatic
			  complexity of a codebase. It then summarizes the most complex files to help answer
			  the user\'s question.
			base_prompt: Your task is to compute the cyclomatic complexity of a given codebase
			  and sort the files based on the specified sorting criterion. Provide a summary of
			  the most complex files to facilitate the understanding of the codebase\'s complexity.
			params:
			  filepath_inexact:
				description: An inexact filepath explicitly requested by the user, or an indication
				  of \'none\' if no specific file path is requested.
				type: str
				required: false
				default: none
			  sort_on:
				description: The criterion for sorting the results, which can be either \'average\'
				  or \'max\' complexity of the file.
				type: str
				required: false
				default: max
			
			
			~={green}name: FindUsageTool=~
			description: This tool answers questions about the usage of a given importable object
			  by listing the files that import the object and the number of times the object is
			  used in each file.
			base_prompt: Provide information on the usage of the specified importable object,
			  including a summary listing the file names and their associated usage counts.
			params:
			  importable_object:
				description: The fully qualified name of a module, function, class, or variable.
				type: str
				required: true
			
			
			~={green}name: GetFileContentsTool=~
			description: This tool takes a user_prompt and filepath_inexact, fuzzy matches the
			  filepath to find the exact file in the project, and retrieves the contents of the
			  file.
			base_prompt: Your task is to answer the question based on the file contents provided.
			params:
			  filepath_inexact:
				description: An inexact path to a file, which will be matched to the correct file
				  path in the project.
				type: str
				required: true
			
			
			~={green}name: InstallationAndUseTool=~
			description: This tool queries documentation files about the installation and execution
			  of the codebase to answer questions based on these documents.
			base_prompt: Your task is to provide information on the installation and use of the
			  codebase by examining relevant documentation files provided.
			params: {}
			
			
			',
		'role': 'system'
	},
	{
		'content': '
			
			~={blue}### Question ###
			how is the system message for each call to the llm built?=~', 
		'role': 'user'
	}
]

ChatCompletionMessage(
    content='
	     Tool: ~={green}CodebaseQATool=~
         Tool query: ~={blue}Explain how the system message is constructed for each call to the language model in the codebase.=~
         Parameter_0: include_code | true | bool',
    refusal=None, 
    role='assistant', 
    audio=None, 
    function_call=None, 
    tool_calls=None, 
    annotations=[]
    )
    
🗨  openapi LLM(gpt-4-1106-preview)
⠋ Running CodebaseQATool. Please standby while I run the tool CodebaseQATool...
("Explain how the system message is constructed for each call to the language model in the codebase.", {'include_code': True})

⠹ Running CodebaseQATool

[
    {
        'content': 'You are a helpful assistant.', 
        'role': 'system'
    },
    {
        'content': '~={pink}Name: src/groundcrew/tools.py: :CodebaseQATool.__init__ (method)=~
            Type: method
            Full Text:     def __init__(self, base_prompt: str, collection: Collection, llm: Callable):
                    """
                    Initialize the CodebaseQATool with a base prompt, a code collection,
                    and a language model.
                    
                    Args:
                        base_prompt (str): The base prompt to prepend to all queries.
                        collection (Collection): The code collection or database to query
                        for code-related information.
                        llm (Callable): The language model to use for generating
                        code-related responses.
                    """
                    self.base_prompt = base_prompt + sp.CODEQA_PROMPT
                    self.collection = collection
                    self.llm = llm
            Document: The provided Python code snippet appears to be the initialization method of a class named `CodebaseQATool`, which is intended to work with a code collection and utilize a language model to generate code-related responses. This class depends on external entities such as `Collection` and some callable `llm`, which suggests the class interacts with a database or collection of code snippets and a language model, respectively. The `__init__` method sets up the object with a `base_prompt` that is enhanced by appending `sp.CODEQA_PROMPT`, a given `collection`, and a `llm` function or method provided as arguments. The comments within the code describe the purpose of each argument, ensuring the `CodebaseQATool` is properly initialized with necessary data and functionality for its operation. No explicit functions or methods are shown outside of the `__init__` method in this snippet, but the initialization of the class is crucial for the tool\'s ability to interact with a codebase and provide responses via a language model.
            Start Line: 335
            End Line: 349
            ~={pink}--------=~
            
            ~={pink}Name: src/groundcrew/tools.py: :CodebaseQATool (class)=~
            Type: class
            Full Text: class CodebaseQATool:
                """
                Tool for querying a codebase and generating responses using a language
                model.  Inherits from ToolBase and implements the abstract methods for
                specific codebase querying functionality.
                """
                def __init__(self, base_prompt: str, collection: Collection, llm: Callable):
                    """
                    Initialize the CodebaseQATool with a base prompt, a code collection,
                    and a language model.
            
                    Args:
                        base_prompt (str): The base prompt to prepend to all queries.
                        collection (Collection): The code collection or database to query
                        for code-related information.
                        llm (Callable): The language model to use for generating
                        code-related responses.
                    """
                    self.base_prompt = base_prompt + sp.CODEQA_PROMPT
                    self.collection = collection
                    self.llm = llm
            
                def __call__(self, ~={blue}user_prompt=~: str, include_code: bool) -> str:
                    """
                    Processes a given prompt, queries the codebase, and uses the language
                    model to generate a response.
            
                    Args:
                        prompt (str): The prompt to process.
                        include_code (bool): Flag to include code in the response.
            
                    Returns:
                        str: The generated response from the language model.
                    """
                    chunks = query_codebase(~={blue}user_prompt=~, self.collection)
            
                    prompt = \'\'
                    for chunk in chunks:
                        prompt += code.format_chunk(chunk, include_text=include_code)
                        prompt += \'--------\
            \
            \'
            
                    prompt += self.base_prompt + \'\
            ### Question ###\
            \'
                    prompt += f\'{user_prompt
                    }\
            \
            \'
            
                    return self.llm(prompt)
            Document: The above Python code defines a class named `CodebaseQATool`, which is designed to facilitate querying a codebase and generating responses using a language model. This class requires a base prompt string, a collection object representing the codebase, and a callable representing the language model (`llm`). The class has an `__init__` method to initialize these dependencies and a `__call__` method that takes in a user\'s prompt and a boolean indicating whether to include code in the response; it constructs a comprehensive prompt with codebase chunks and passes it to the language model to generate a response. The actual querying of the codebase (`query_codebase`) and formatting of code chunks (`code.format_chunk`) appear to be handled by functions not defined within this snippet but are expected to exist in the module. The comments and docstrings provide insight into the class\'s purpose and usage, emphasizing its role in interfacing between a user\'s queries and the automated generation of code-related answers.
            Start Line: 329
            End Line: 373
            ~={pink}--------=~
            
            ~={pink}Name: src/groundcrew/agent.py: :Agent.print_message_history (method)=~
            Type: method
            Full Text:     def print_message_history(self, messages):
                    print(\'\
            \', \'*\' * 50, \'\
            \')
                    for message in messages:
                        if message.role == \'user\':
                            color = Colors.GREEN
                        elif message.role == \'system\':
                            color = Colors.RED
                        elif message.role == \'assistant\':
                            color = Colors.BLUE
            
                        print(\'Role:\', message.role)
                        print(color)
                        print(message.content)
                        print(Colors.ENDC)
                    print(\'\
            \', \'*\' * 50, \'\
            \')
            Document: The provided Python code snippet is a method definition (`print_message_history`) within a class presumed to be part of a module called `groundcrew`. The method takes a list of `messages` as an argument and prints each message to the console, formatted by the role of the sender. There is a dependency on a presumed external class or enum `Colors` which is used to color-code the output according to whether the message is from a \'user\' (green), \'system\' (red), or \'assistant\' (blue); this `Colors` class defines these color constants and a reset value (ENDC). There are no comments or docstrings present in the snippet to provide additional context. The method concludes by printing a series of asterisks before and after the message history to delineate the printed messages visually in the console output.
            Start Line: 336
            End Line: 350
            ~={pink}--------
            
            Name: src/groundcrew/tools.py: :CodebaseQATool.__call__ (method)=~
            Type: method
            Full Text:     def __call__(self, user_prompt: str, include_code: bool) -> str:
                    """
                    Processes a given prompt, queries the codebase, and uses the language
                    model to generate a response.
            
                    Args:
                       
             prompt (str): The prompt to process.
                        include_code (bool): Flag to include code in the response.
            
                    Returns:
                        str: The generated response from the language model.
                    """
                    chunks = query_codebase(user_prompt, self.collection)
            
                    prompt = \'\'
                    for chunk in chunks:
                        prompt += code.format_chunk(chunk, include_text=include_code)
                        prompt += \'--------\
            \
            \'
            
                    prompt += self.base_prompt + \'\
            ### Question ###\
            \'
                    prompt += f\'{user_prompt}\
            \
            \'
            
                    return self.llm(prompt)
            Document: This Python code snippet defines a `__call__` method within a `tools.py` module that is likely part of a larger class meant for interacting with a codebase. It is dependent on external functions such as `query_codebase` and `code.format_chunk` which are not defined in this snippet, indicating the code relies on other parts of the application or external libraries. The method takes a user prompt and a boolean to determine whether to include code in the response, processing the prompt to generate and return a response using a language model referred to as \'llm\'. It builds the input for the language model by querying the codebase for relevant chunks of information, formatting them, and concatenating them with a base prompt and the user\'s question. The comments and docstring provide clear instructions on the method\'s usage, input arguments (`user_prompt` and `include_code`), and the expected string output.
            Start Line: 351
            End Line: 373
            ~={pink}--------
            
            Name: src/groundcrew/tools.py::SingleDocstringTool.__init__ (method)=~
            Type: method
            Full Text:     def __init__(self, base_prompt: str, collection: Collection, llm: Callable):
                    """
                    Initialize the SingleDocstringTool with a base prompt, a code
                    collection, and a language model.
            
                    Args:
                        base_prompt (str): The base prompt to prepend to all queries.
                        collection (Collection): The code collection or database to query
                        for code-related information.
                        llm (Callable): The language model to use for generating
                        code-related responses.
                    """
                    self.base_prompt = base_prompt
                    self.collection = collection
                    self.llm = llm
            
                    # Adding additional instructions
                    self.base_prompt = base_prompt + sp.DOCSTRING_PROMPT
            Document: The given Python code snippet defines the initialization method `__init__` for a class named `SingleDocstringTool`, which is not explicitly declared within the snippet but can be inferred from the method\'s context. This method takes three arguments: `base_prompt` (a string for creating prompts), `collection` (an instance of `Collection`, suggesting a dependency on a module that contains this class which is used to handle a code database), and `llm` (a callable representing a language model, indicating dependency on a machine learning or language processing library).
            
            The `__init__` method sets up the class instance by assigning the provided arguments to instance variables, and then it appends a constant `DOCSTRING_PROMPT` from an object `sp` to `base_prompt`. This constant is likely defined elsewhere and used to standardize prompts for the language model. The comments and docstrings explain that the purpose of the `SingleDocstringTool` is to work with a base prompt to make queries and generate code-related responses using a language model, suggesting its utility in tasks related to code analysis, documentation, or similar activities involving a code collection.
            Start Line: 191
            End Line: 208
            ~={pink}--------=~
            
~={cyan}Your task is to assist by querying the codebase and answer questions based on code snippets.Your answer should only include information that pertains to the question.=~
            ~={blue}### Question ###
            Explain how the system message is constructed for each call to the language model in the codebase.=~
        
        ', 
        'role': 'user'
    }
]

ChatCompletionMessage(
	content="The system message sent to the language model in the codebase is constructed within the `__call__` method of the `CodebaseQATool` class, as shown in the provided code snippets. Here's a step-by-step explanation of how the system message is constructed for each call to the language model:
		
		1. The `__call__` method receives a `user_prompt` as a string and an `include_code` Boolean flag as parameters.
		
		2. The method begins by querying the codebase for related code segments using the `query_codebase` function. This function takes the `user_prompt` and the `collection` attribute (which is the reference to the code collection/database) and returns a list of code chunks relevant to the user's query.
		
		3. An empty string `prompt` is initialized to start constructing the system message.
		
		4. For each code chunk in the list returned by `query_codebase`, the `format_chunk` function from the `code` module is called with the chunk and the `include_text` parameter set to the value of `include_code`. This function likely formats the code chunk for inclusion, depending on whether code should be included in the response or not.
		
		5. The formatted code chunk and a separation line ('--------\
		\
		') are appended to the `prompt` string with each iteration, building a section of the prompt that contains all the codebase information deemed relevant.
		
		6. After all code chunks have been formatted and appended, the base prompt (which has been concatenated with `sp.CODEQA_PROMPT` during initialization) is appended to the `prompt` string. This is followed by the string '\
		### Question ###\
		', which likely serves as a delimiter or marker to indicate the start of the actual user query.
		
		7. The user's original prompt (`user_prompt`) is then appended to the `prompt` string followed by two newline characters to ensure proper formatting.
		
		8. Finally, the entire constructed `prompt` string is passed to the language model callable (`llm`) which is invoked to generate a response.
		
		9. The response from the language model callable is then returned from the `__call__` method.
		
		In summary, the system message for each call to the language model is a meticulously constructed combination of formatted code chunks from the codebase, along with a base prompt enhanced by a specific prompt addition (e.g., `sp.CODEQA_PROMPT`), and the user's query itself, formatted and ready to be processed by the language model.", 
    refusal=None, 
    role='assistant', 
    audio=None, 
    function_call=None, 
    tool_calls=None, 
    annotations=[]
)

🗨  openapi LLM(gpt-4-1106-preview)
⠋ Thinking...


[
    {
        'content': '
            You are an assistant that answers question about a codebase. All of the user\'s questions should be about this particular codebase, and you will be given tools that you can use to help you answer questions about the codebase.
            
            
            Your task is to address a question or command from a user in the Question seciton. You will do this in a step by step manner by choosing a single Tool and parameters necessary for this task. Only include "Tool:" in your answer if you are choosing a valid Tool available to you. When you have the necessary data to complete your task, respond directly to the user with a summary of the steps taken. Do not ask the user for filepaths or filenames. You must use the tools available to you. Your answer must be in one of the following two formats.
            
            (1) If you are choosing the correct Tool and parameters, use the following format. Do not use references to parameter values, you must put the value being passed in the Parameter value section. If passing in code, do not include backticks.
            Reason: Describe your reasoning for why this tool was chosen in 3 sentences or less.
            Tool: Tool Name
            Tool query: Provide a query to the Tool to get the answer to the question.
            Parameter_0: Parameter_0 Name | Parameter value | parameter type
            ...
            Parameter_N: Parameter_N Name | Parameter value | parameter type
            
            (2) If you are responding directly to the user\'s questions, use this format:
            Response: Write your response here. Your response should be limited to 3 sentences or less. If you include code in your response, it should be in a code block like this:
            ```python
            # Code goes here
            ```
            
            
            ### Tools ###
            name: LintFileTool
            description: This tool interacts with a linter using natural language, takes a user_prompt
              and filepath_inexact, fuzzily matches the file path, runs linting processes on the
              identified file, and uses a large language model to answer the user\'s questions
              about linting results.
            base_prompt: Your task is to provide information and advice on the linting results
              for a specific file. Be clear and helpful in your guidance.
            params:
              filepath_inexact:
                description: An inexact file path to match and identify for linting
                type: str
                required: true
            
            
            name: SingleDocstringTool
            description: This tool generates docstrings for a given code snippet, function, or
              all functions in a specified file based on different scenarios.
            base_prompt: Based on the code, filename, and function name provided, generate an
              appropriate docstring.
            params:
              code:
                description: The code to generate a docstring for, if it is not \'none\'.
                type: str
                required: false
              filename:
                description: The filename to query for generating docstrings for all functions
                  within, must be \'none\' if not used.
                type: str
                required: false
              function_name:
                description: The name of the function to generate a docstring for, must be \'none\'
                  if not used.
                type: str
                required: false
            
            
            name: CodebaseQATool
            description: This Tool processes a user_prompt, queries a codebase, and then uses
              a language model to provide a response that may include code snippets if requested.
            base_prompt: Your task is to assist by querying the codebase and answer questions
              based on code snippets.
            params:
              include_code:
                description: Flag indicating whether to include code snippets in the response
                type: bool
                required: true
            
            
            name: CyclomaticComplexityTool
            description: This tool uses the user_prompt along with a specified file path and a
              choice to sort based on average or maximum complexity, to compute the cyclomatic
              complexity of a codebase. It then summarizes the most complex files to help answer
              the user\'s question.
            base_prompt: Your task is to compute the cyclomatic complexity of a given codebase
              and sort the files based on the specified sorting criterion. Provide a summary of
              the most complex files to facilitate the understanding of the codebase\'s complexity.
            params:
              filepath_inexact:
                description: An inexact filepath explicitly requested by the user, or an indication
                  of \'none\' if no specific file path is requested.
                type: str
                required: false
                default: none
              sort_on:
                description: The criterion for sorting the results, which can be either \'average\'
                  or \'max\' complexity of the file.
                type: str
                required: false
                default: max
            
            
            name: FindUsageTool
            description: This tool answers questions about the usage of a given importable object
              by listing the files that import the object and the number of times the object is
              used in each file.
            base_prompt: Provide information on the usage of the specified importable object,
              including a summary listing the file names and their associated usage counts.
            params:
              importable_object:
                description: The fully qualified name of a module, function, class, or variable.
                type: str
                required: true
            
            
            name: GetFileContentsTool
            description: This tool takes a user_prompt and filepath_inexact, fuzzy matches the
              filepath to find the exact file in the project, and retrieves the contents of the
              file.
            base_prompt: Your task is to answer the question based on the file contents provided.
            params:
              filepath_inexact:
                description: An inexact path to a file, which will be matched to the correct file
                  path in the project.
                type: str
                required: true
            
            
            name: InstallationAndUseTool
            description: This tool queries documentation files about the installation and execution
              of the codebase to answer questions based on these documents.
            base_prompt: Your task is to provide information on the installation and use of the
              codebase by examining relevant documentation files provided.
            params: {}
            
            
            ', 
        'role': 'system'
    },
    {
        'content': '
	        
	        ### Question ###
	        ~={blue}how is the system message for each call to the llm built?=~', 
        'role': 'user'
    },
    {
        'content': 'Tool: CodebaseQATool
            Tool query: ~={blue}Explain how the system message is constructed for each call to the language model in the codebase=~.
            Parameter_0: include_code | true | bool', 
        'role': 'assistant'
    },
    {
        'content': "Tool response
            The system message sent to the language model in the codebase is constructed within the `__call__` method of the `CodebaseQATool` class, as shown in the provided code snippets. Here's a step-by-step explanation of how the system message is constructed for each call to the language model:
            
            1. The `__call__` method receives a `user_prompt` as a string and an `include_code` Boolean flag as parameters.
            
            2. The method begins by querying the codebase for related code segments using the `query_codebase` function. This function takes the `user_prompt` and the `collection` attribute (which is the reference to the code collection/database) and returns a list of code chunks relevant to the user's query.
            
            3. An empty string `prompt` is initialized to start constructing the system message.
            
            4. For each code chunk in the list returned by `query_codebase`, the `format_chunk` function from the `code` module is called with the chunk and the `include_text` parameter set to the value of `include_code`. This function likely formats the code chunk for inclusion, depending on whether code should be included in the response or not.
            
            5. The formatted code chunk and a separation line ('--------\
            \
            ') are appended to the `prompt` string with each iteration, building a section of the prompt that contains all the codebase information deemed relevant.
            
            6. After all code chunks have been formatted and appended, the base prompt (which has been concatenated with `sp.CODEQA_PROMPT` during initialization) is appended to the `prompt` string. This is followed by the string '\
            ### Question ###\
            ', which likely serves as a delimiter or marker to indicate the start of the actual user query.
            
            7. The user's original prompt (`user_prompt`) is then appended to the `prompt` string followed by two newline characters to ensure proper formatting.
            
            8. Finally, the entire constructed `prompt` string is passed to the language model callable (`llm`) which is invoked to generate a response.
            
            9. The response from the language model callable is then returned from the `__call__` method.
            
            In summary, the system message for each call to the language model is a meticulously constructed combination of formatted code chunks from the codebase, along with a base prompt enhanced by a specific prompt addition (e.g., `sp.CODEQA_PROMPT`), and the user's query itself, formatted and ready to be processed by the language model.
            
            ### Question ###
            ~={blue}how is the system message for each call to the llm built?=~
            
            ~={red}If you can answer the complete question, do so using the output from the Tool Response. If you cannot answer the complete question, choose a Tool.=~
            ", 
        'role': 'user'
    }
]


ChatCompletionMessage(
    content="Response: The system message sent to the language model for each call is made in the `__call__` method of the `CodebaseQATool` class. This process involves:
        
        1. Receiving a `user_prompt` and an `include_code` flag.
        2. Querying the codebase with `query_codebase` for relevant code segments using the `user_prompt`.
        3. Formatting the code chunks using the `format_chunk` function and appending them to an initial prompt string.
        4. Appending the base prompt and user's query to the constructed message.
        5. Sending this complete prompt string to the language model to generate a response.", 
    refusal=None, 
    role='assistant', 
    audio=None, 
    function_call=None, 
    tool_calls=None, 
    annotations=[]
)

🗨  openapi LLM(gpt-4-1106-preview)

 **************************************************
