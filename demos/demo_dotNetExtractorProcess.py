import os; 
import sys; 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from src.groundcrew.code_analyser_csharp import extract_csharp_from_file

# Example usage
file_path = "./dotNet/CodeExtractor/CodeExtractor.cs"
node_type = "Class,Method"

output = extract_csharp_from_file(file_path, node_type)
if output:
    print("Parsed Output:", json.dumps(output, indent=4))
