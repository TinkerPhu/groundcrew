import re

def post_process_yaml_response(text):
    # Remove spaces before/after newlines and join split characters
    fixed_text = re.sub(r'(?<!\n)\n(?!\n)', '', text)
    
    fixed_text = re.sub(r'\n\n', '', fixed_text)
    
    # Handle unnecessary leading/trailing newlines
    fixed_text = fixed_text.strip()

    m = re.match(r'(``yaml\n((\n|.)*)``)', fixed_text)
    if m:
        fixed_text = m.group(2)
    
    return fixed_text

# Example
broken_yaml = '`\n`\ny\na\nm\nl\n\n\n \n \n-\n \nn\na\nm\ne\n:\n \nF\ni\nn\nd\nU\ns\na\ng\ne\nT\no\no\nl\n\n\n \n \n \n \nd\ne\ns\nc\nr\ni\np\nt\ni\no\nn\n:\n \nT\nh\ni\ns\n \nt\no\no\nl\n \na\nn\ns\nw\ne\nr\ns\n \nq\nu\ne\ns\nt\ni\no\nn\ns\n \na\nb\no\nu\nt\n \nt\nh\ne\n \nu\ns\na\ng\ne\n \no\nf\n \na\n \ng\ni\nv\ne\nn\n \ni\nm\np\no\nr\nt\na\nb\nl\ne\n \no\nb\nj\ne\nc\nt\n.\n \n\n\n \n \n \n \nb\na\ns\ne\n_\np\nr\no\nm\np\nt\n:\n \nA\nn\ns\nw\ne\nr\n \nq\nu\ne\ns\nt\ni\no\nn\ns\n \nu\ns\ni\nn\ng\n \na\nb\no\nu\nt\n \nt\nh\ne\n \nu\ns\na\ng\ne\n \no\nf\n \na\n \ng\ni\nv\ne\nn\n \ni\nm\np\no\nr\nt\na\nb\nl\ne\n \no\nb\nj\ne\nc\nt\n.\n \n\n\n \n \n \n \np\na\nr\na\nm\ns\n:\n\n\n \n \n \n \n \n \ni\nm\np\no\nr\nt\na\nb\nl\ne\n_\no\nb\nj\ne\nc\nt\n:\n\n\n \n \n \n \n \n \n \n \nd\ne\ns\nc\nr\ni\np\nt\ni\no\nn\n:\n \nN\na\nm\ne\n \no\nf\n \nt\nh\ne\n \nm\no\nd\nu\nl\ne\n,\n \nf\nu\nn\nc\nt\ni\no\nn\n,\n \nc\nl\na\ns\ns\n,\n \no\nr\n \nv\na\nr\ni\na\nb\nl\ne\n \nt\no\n \ne\nx\na\nm\ni\nn\ne\n.\n \n \n\n\n \n \n \n \n \n \n \n \nt\ny\np\ne\n:\n \ns\nt\nr\n\n\n \n \n \n \n \n \n \n \nr\ne\nq\nu\ni\nr\ne\nd\n:\n \nt\nr\nu\ne\n\n\n`\n`'
fixed_yaml = post_process_yaml_response(broken_yaml)
print(fixed_yaml)

good_yaml = "  - name: LintFileTool\n    description: This tool helps users understand linting results by providing a user-friendly interface to ask questions and obtain specific information about the file. \n    base_prompt: The linter's output is provided. Use the following prompt to find out what needs fixing in the code, including any possible syntax errors. Be detailed in your answer.\n    params:\n      filepath_inexact:\n        description: File path for the file, fuzzy matching will be used to find exact match. \n        type: str\n        required: true  \n     \n\n\n\n\n"
untouched_yaml = post_process_yaml_response(good_yaml)
print(untouched_yaml)