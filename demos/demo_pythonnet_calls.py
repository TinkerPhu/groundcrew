#HINT to myself, try again with suggestions from https://github.com/pythonnet/pythonnet/issues/2464

import ctypes
import clr
import os
import sys

# dotnet framework runtime
from pythonnet import load
load("netfx")
#load("coreclr")


from System.Collections.Generic import Dictionary
from System.Collections.Generic import List
from System.IO.Ports import Parity, StopBits, Handshake
from System import String, Int32, UInt32, UInt16, Object, Single, Double, Boolean
from System.Net import IPAddress
from System.Threading import CancellationToken
from System.IO import File

def get_existing_abs_path(any_path:str)->str:
    abs_path = os.path.abspath(os.path.normpath(any_path))
    if not os.path.exists(abs_path):
        raise Exception(f"File does not exist: {abs_path}")
    return abs_path

def load_assembly(assembly_path:str)->None:
    import sys
    import os
    import clr
    # Load the compiled C# assembly
    abs_assembly_path = get_existing_abs_path(assembly_path)

    sys.path.append(os.path.dirname(abs_assembly_path))

    assembly_name = os.path.splitext(os.path.basename(abs_assembly_path))[0]
    clr.AddReference(assembly_name)


load_assembly("./dotNet/ClassLibrary1/bin/Debug/net7.0/ClassLibrary1.dll")
#load_assembly("./dotNet/ClassLibrary1/bin/publish/ClassLibrary1.dll")


#print(sys.modules.keys())

from ClassLibrary1NS import Class1
res = Class1.hello()

from ClassLibrary1NS import DemoClass
res = DemoClass.hello()
res = DemoClass.hello22()
res = DemoClass.helloT()
res = DemoClass.helloS()
if res != '345':
    raise Exception("wrong return value from helloS")

from ClassLibrary1NS import CodeVisitorNew
codevisitor = CodeVisitorNew("Class")

# from ClassLibrary1NS import CodeExtractor
# dic = CodeExtractor.ExtractFromFile("../../../CodeExtractor.cs","Class")

# load_assembly("./dotNet/CodeExtractor/bin/Debug/net8.0/CodeExtractor.dll")
load_assembly("./dotNet/ConsoleApp1/bin/publish/ConsoleApp1.exe")
from ConsoleApp1NS import Class2
res = Class2.helloWorld()
from ConsoleApp1NS import CodeExtractorApp
res = CodeExtractorApp.ExtractFromFile("../../../CodeExtractor.cs","Class")


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