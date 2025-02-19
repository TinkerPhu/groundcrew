import re

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

def attempt_to_fix_error(yaml_content, error_message):
    # Apply the correction
    if "mapping values are not allowed here" in error_msg:
        return correct_mapping_values_are_not_allowed_here_yaml(yaml_data, error_msg)
    

    
# Example error message and YAML
error_msg = """mapping values are not allowed here
  in "<unicode string>", line 3, column 66:
     ... provide an answer in this format: 'Installation/Usage of the cod ..."""

yaml_data = """- name: InstallationAndUseTool
    description: This tool answers questions about the installation and execution of the codebase by querying for documentation files.
    base_prompt: Your task is to provide an answer in this format: 'Installation/Usage of the codebase.\\n\\n' , the provided context.  Be descriptive in your answer.
    params:
      working_dir_path:
        description: Path to the working directory of the project.
        type: str
        required: true
      collection:
        description: The collection of documentation and code-related files (e.g., a file system)
        type: Collection
        required: true
      llm:
        description: A large language model (LLM) for answering user questions.
        type: Callable
        required: true"""


fixed_yaml = attempt_to_fix_error(yaml_data, error_msg)

print("Corrected YAML:\n", fixed_yaml)
