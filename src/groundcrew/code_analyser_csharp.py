import subprocess
import json
import os

_CodeExtractorAppExecutablePath = "./dotNet/binaries/CodeExtractor.App.exe"

def extract_csharp_from_file(file_path, node_type):
    file_path = existing_abs_path(file_path)
    results = call_console_program_and_capture_output(_CodeExtractorAppExecutablePath, file_path, node_type)
    return results

def call_console_program_and_capture_output(executable_path, *args):
    try:
        executable_path = existing_abs_path(executable_path)
        # Run the C# program as a subprocess
        cmd_line = [executable_path, *args]
        result = subprocess.run(
            cmd_line, 
            capture_output=True, 
            text=True
        )

        # Check for errors
        if result.returncode != 0:
            print("Error:", result.stderr)
            return None

        # Parse and return JSON output
        return json.loads(result.stdout)

    except Exception as e:
        print("Exception occurred:", str(e))
        return None

def existing_abs_path(any_path:str)->str:
    abs_path = os.path.abspath(os.path.normpath(any_path))
    if not os.path.exists(abs_path):
        raise Exception(f"File does not exist: {abs_path}")
    return abs_path


if __name__ == "__main__":
    # Example usage
    file_path = "./dotNet/CodeExtractor/CodeExtractor.cs"
    node_type = "Class,Method"

    output = extract_csharp_from_file(file_path, node_type)
    if output:
        print("Parsed Output:", json.dumps(output, indent=4))