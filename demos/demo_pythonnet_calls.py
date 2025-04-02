# see: https://stackoverflow.com/questions/7367976/calling-a-c-sharp-library-from-python/79550419#79550419


import os


def get_existing_abs_path(any_path:str)->str:
    abs_path = os.path.abspath(os.path.normpath(any_path))
    if not os.path.exists(abs_path): raise Exception(f"File does not exist: {abs_path}")
    return abs_path





from clr_loader import get_coreclr
from pythonnet import set_runtime


conf_path = get_existing_abs_path("./dotNet/published.RefApp/ReferingApp.runtimeconfig.json")
if not os.path.exists(conf_path): raise Exception(f"File does not exist: {conf_path}")

rt = get_coreclr(runtime_config=conf_path)
set_runtime(rt)



def load_assembly(assembly_path:str, expected_namespace: str|None=None)->None:
    import sys
    import os
    import clr
    import importlib
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



load_assembly("./dotNet/published.RefApp/CodeExtractor.dll", 'CodeExtractorNS')

from CodeExtractorNS import CSharpCodeExtractor

def extract_csharp_from_file(file_path, node_type):
    """
    Calls the C# CodeExtractor function to extract classes/methods from a C# file.
    :param file_path: Path to the C# file.
    :param node_type: Either "Class" or "Method".
    :return: Dictionary of extracted elements.
    """
    results = CSharpCodeExtractor.ExtractFromFile(file_path, node_type)

    extracted_data = {}
    for nodes in results:
        print(nodes.Key)
        for node in nodes.Value:
            data = node.Value
            extracted_data[node.Key] = {
                "text": data['Text'],
                "start_line": data['StartLine'],
                "end_line": data['EndLine'],
                "is_method": data['IsMethod'],
                "is_class": data['IsClass'],
            }
    return extracted_data


# Example usage
if __name__ == "__main__":

    def assert_equal(expectation, value, message):
        if expectation != value:
            raise Exception(message)
        

    load_assembly("./dotNet/published.RefApp/ClassLibrary1.dll", 'ClassLibraryNS')

    from ClassLibraryNS import Class1

    assert_equal(12, Class1.hello(), "wrong return value from hello")
    assert_equal('345', Class1.helloS(345), "wrong return value from helloS")



    # import clr
    # from System.Collections.Generic import Dictionary
    # from System.Collections.Generic import List
    # from System import String, Int32, UInt32, UInt16, Object, Single, Double, Boolean
    # from System.Net import IPAddress
    # from System.Threading import CancellationToken
    # from System.IO import File

    # codeextractor = CSharpCodeExtractor()

    # codefileName = get_existing_abs_path("./dotNet/CodeExtractor/CSharpCodeExtractor.cs")
    # res = CSharpCodeExtractor.ExtractFromFile(codefileName,"Class,Method")
    # resMethods = res["Method"]
    # for method in resMethods:
    #     print(method.Key)
    #     print(method.Value["Text"])



    csharp_file = get_existing_abs_path("./dotNet/CodeExtractor/CSharpCodeExtractor.cs")

    extracted_classes = extract_csharp_from_file(csharp_file, "Class")
    extracted_methods = extract_csharp_from_file(csharp_file, "Method")

    print("Extracted Classes:")
    for name,dic in extracted_classes.items():
        print(f"Class {name}:")
        print(dic.get('text'))

    print("Extracted Methods:")
    for name,dic in extracted_methods.items():
        print(f"Method {name}:")
        print(dic.get('text'))