#HINT to myself, try again with suggestions from https://github.com/pythonnet/pythonnet/issues/2464

import ctypes
import os
import sys
import importlib

# dotnet framework runtime
import pythonnet
from pythonnet import load
info = pythonnet.get_runtime_info()
#load("netfx")
from clr_loader import get_coreclr
from pythonnet import set_runtime

conf_path = os.path.abspath(os.path.normpath("./dotNet/published.RefApp/ReferingApp.runtimeconfig.json"))
if not os.path.exists(conf_path): raise Exception(f"File does not exist: {conf_path}")

rt = get_coreclr(runtime_config=conf_path)
set_runtime(rt)

#load("coreclr", runtime_config=conf_path)
#load("netfx", runtime_config=conf_path)

info = pythonnet.get_runtime_info()
import clr
info = pythonnet.get_runtime_info()

from System.Collections.Generic import Dictionary
from System.Collections.Generic import List
#from System.IO.Ports import Parity, StopBits, Handshake
from System import String, Int32, UInt32, UInt16, Object, Single, Double, Boolean
from System.Net import IPAddress
from System.Threading import CancellationToken
from System.IO import File

def get_existing_abs_path(any_path:str)->str:
    abs_path = os.path.abspath(os.path.normpath(any_path))
    if not os.path.exists(abs_path): raise Exception(f"File does not exist: {abs_path}")
    return abs_path

def load_assembly(assembly_path:str, expected_namespace: str|None=None)->None:
    import sys
    import os
    import clr
    # Load the compiled C# assembly
    abs_assembly_path = get_existing_abs_path(assembly_path)

    sys.path.append(os.path.dirname(abs_assembly_path))

    assembly_name = os.path.splitext(os.path.basename(abs_assembly_path))[0]
    clr.AddReference(assembly_name)

    if expected_namespace:
        importlib.import_module(expected_namespace)
        module_names = list(sys.modules.keys())
        if expected_namespace not in module_names:
            print(sys.modules.keys())
            print(module_names)
            raise Exception(f"could not load namespace {expected_namespace}")
        

def assert_equal(expectation, value, message):
    if expectation != value:
        raise Exception(message)


load_assembly("./dotNet/published.RefApp/ClassLibrary1.dll", 'ClassLibraryNS')


from ClassLibraryNS import Class1



assert_equal(12, Class1.hello(), "wrong return value from hello")
assert_equal('345', Class1.helloS(345), "wrong return value from helloS")

from ClassLibraryNS import CodeVisitor

lis = List[String]()
lis.Add("Class")
codevisitor = CodeVisitor(lis)


load_assembly("./dotNet/published.RefApp/CodeExtractor.dll", 'CodeExtractorNS')


from CodeExtractorNS import CSharpCodeExtractor

codeextractor = CSharpCodeExtractor()

res = CSharpCodeExtractor.ExtractFromFile("../../../CodeExtractor.cs","Class")


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