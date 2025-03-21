def LintFileTool(user_prompt:str, filepath_inexact:str):
    """This tool interacts with a linter using natural language, and provides answers about the results of linting for a file.
    
    base_prompt: Your task is to answer questions using about linting results for a file. Be descriptive in your answer.

    args:
        user_prompt (str): contains usually questions to a source file and its code cleannes.
        filepath_inexact (str): This is an inexact file path which can be fuzzy matched to find an exact file path for the project. Linters usually operate per file so this granularity makes sense.

    returns:
        lining results for the file
    """
    return f"called LintFileTool(user_prompt={user_prompt}, filepath_inexact={filepath_inexact})"
    pass


def SingleDocstringTool(user_prompt:str,
            code: str,
            filename: str = None,
            function_name: str = None):
    """This tool takes user prompts and code snippets to generate docstrings for functions or specific files.
    
    base_prompt: Your task is to generate a detailed docstring based on the provided information.

    args:
        user_prompt (str): contains usually questions to a source file and its functionality.
        code (str): source code to create documentation for
        filename (str): filename of the code
        function_name (str): function name of the code if only a function is given

    returns:
        documentation of the provided code with focus on the users prompt requirements.
    """
    return f"called SingleDocstringTool(user_prompt={user_prompt}, code={code}, function_name={function_name})"
    pass


def CodebaseQATool(user_prompt: str, include_code: bool=False):
    """This tool takes a user_prompt, queries a codebase for information, and generates a response using a language model.

    base_prompt: Your task is to answer the question given the data above. Be descriptive in your answer.

    args:
        user_prompt (str): contains general questions to the codebase, e.g. functionality and its location, the whereabouts of a certain function or variables, the call structures.
        include_code (bool): set true to add code snippeds in the answer

    returns:
        Answer to the question in the users prompt
    """
    return f"called CodebaseQATool(user_prompt={user_prompt}, include_code={include_code})"
    pass



def CyclomaticComplexityTool(user_prompt: str,
            filepath_inexact: str = 'none',
            sort_on: str = 'max'):
    """This tool takes a user_prompt, finds the most complex files in the codebase, and answers questions about those files.

    base_prompt: Analyze the complexity of the codebase to answer questions about it.

    args:
        user_prompt (str): contains information on what aspect in the code complexity is of interest. 
        filepath_inexact (str): If not 'none', provides a filepath that should be used for analysis.
        sort_on (str): Sort result based on the "average" or "max" complexity of the file.

    returns:
        Summary and analysis of the complex files in the codebase.
    """
    return f"called CyclomaticComplexityTool(user_prompt={user_prompt}, filepath_inexact={filepath_inexact}, sort_on={sort_on})"
    pass



def FindUsageTool(user_prompt: str, importable_object: str):
    """This tool takes a user_prompt and importable_object, finds the usage of the object in files, then uses a large language model to answer questions about the usage.

    base_prompt: Answer questions using about the usage of the given importable object. Be descriptive in your answer.

    args:
        user_prompt (str): describes what usage is to be searched for. 
        importable_object (str): Name of the module, function, class, or variable whose usage you want to explore. It should be a fully qualified name, e.g. 'numpy.random' or 'numpy.random.randint'.

    returns:
        a list of code passages (filename and line number) where the usages have been found.
    """
    return f"called FindUsageTool(user_prompt={user_prompt}, importable_object={importable_object})"
    pass

def GetFileContentsTool(filepath_inexact: str, user_prompt: str="summarize the purpose of the source code."):
    """This tool interacts with the contents of a specific file.

    base_prompt: Answer questions about a specific file.
    
    args:
        filepath_inexact: File path to look for in the code base. The file path can be inexact
        user_prompt (str): question about a source file

    returns:
        the answer to the user prompt.
    """
    return f"called GetFileContentsTool(user_prompt={user_prompt}, filepath_inexact={filepath_inexact})"
    pass



def InstallationAndUseTool(user_prompt: str):
    """This tool answers questions about the installation and execution of the codebase by querying for documentation files.
    
    base_prompt: Your task is to provide an informative answer based on the provided information and context.
    
    args:
        user_prompt (str): question about installation and execution

    returns:
        the answer to the user prompt.
    """
    return f"called InstallationAndUseTool(user_prompt={user_prompt})"
    

tool_functions = [
    LintFileTool,
    SingleDocstringTool,
    CodebaseQATool,
    CyclomaticComplexityTool,
    FindUsageTool,
    GetFileContentsTool,
    InstallationAndUseTool
]