import ctypes
from pythonnet import load
import clr

# dotnet framework runtime
load("netfx")

from System.Collections.Generic import Dictionary

# Load the compiled C# assembly
assembly_path = "C:/DriveD/Projects/groundcrew/dotNet/CodeExtractor/bin/Debug/net9.0/CodeExtractor.dll"  # Update this path
clr.AddReference(assembly_path)

from CodeExtractor import *



def extract_csharp_from_file(file_path, node_type):
    """
    Calls the C# CodeExtractor function to extract classes/methods from a C# file.
    :param file_path: Path to the C# file.
    :param node_type: Either "Class" or "Method".
    :return: Dictionary of extracted elements.
    """
    results = CodeExtractor.ExtractFromFile(file_path, node_type)

    extracted_data = {}
    for key in results.Keys:
        extracted_data[key] = {
            "text": results[key].Text,
            "start_line": results[key].StartLine,
            "end_line": results[key].EndLine,
            "is_method": results[key].IsMethod,
            "is_class": results[key].IsClass,
        }
    return extracted_data


# Example usage
if __name__ == "__main__":
    csharp_file = "Path/To/CSharpFile.cs"  # Update this path
    extracted_classes = extract_csharp_from_file(csharp_file, "Class")
    extracted_methods = extract_csharp_from_file(csharp_file, "Method")

    print("Extracted Classes:", extracted_classes)
    print("Extracted Methods:", extracted_methods)