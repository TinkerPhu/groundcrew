using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.MSBuild;
using System.Threading.Tasks;

public class DebugCompilation
{
    public static async Task<List<string>> ListAllTypes(string solutionPath)
    {
        var types = new List<string>();

        using (var workspace = MSBuildWorkspace.Create())
        {
            var solution = await workspace.OpenSolutionAsync(solutionPath);
            foreach (var project in solution.Projects)
            {
                var compilation = await project.GetCompilationAsync();
                if (compilation == null) continue;

                Console.WriteLine($"Project: {project.Name}");


                foreach (var symbol in compilation.GlobalNamespace.GetNamespaceMembers())
                {
                    PrintNamespaceTypes(compilation, symbol, "", types);
                }
            }
        }
        return types;
    }

    private static void PrintNamespaceTypes(Compilation compilation, INamespaceSymbol namespaceSymbol, string indent, List<string> types)
    {
        Console.WriteLine($"{indent}Namespace: {namespaceSymbol.Name}");

        foreach (var type in namespaceSymbol.GetTypeMembers())
        {
            //Console.WriteLine($"{indent}  Type: {type.ToDisplayString()}");
            types.Add(type.ToDisplayString());

            var foundType = compilation.GetTypeByMetadataName(type.ToDisplayString());
            if (foundType != null)
            {
                Console.WriteLine($"found {type}");
            }
        }

        foreach (var nestedNamespace in namespaceSymbol.GetNamespaceMembers())
        {
            PrintNamespaceTypes(compilation, nestedNamespace, indent + "  ", types);
        }
    }
}
