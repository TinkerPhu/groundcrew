using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.MSBuild;
using Microsoft.CodeAnalysis.FindSymbols;
using System.Linq;

namespace CodeExtractor;

public class CSharpUsageAnalyzer
{
    public static async Task<Dictionary<string, object>> GetUsage(string solutionPath, string className)
    {
        return await SearchInSoultion(solutionPath, (solution, compilation, results) => AppendUsages(solution,compilation, className, results));
    }
    public static async Task<Dictionary<string, object>> GetUsage(string solutionPath, ICollection<string> classNames)
    {
        return await SearchInSoultion(solutionPath, (solution, compilation, results) =>
        {
            foreach (var className in classNames)
            { 
                AppendUsages(solution, compilation, className, results);
            }
            return Task.CompletedTask;
        });
    }
    public static async Task<Dictionary<string, object>> SearchInSoultion(string solutionPath, Func<Solution, Compilation, Dictionary<string, object>, Task> appendResults)
    {
        solutionPath = Path.GetFullPath(solutionPath);

        if (!File.Exists(solutionPath))
        {
            Console.Error.WriteLine($"Error: The solution file '{solutionPath}' does not exist.");
            Environment.Exit(1);
        }

        var usages = new Dictionary<string, object>();

        using (var workspace = MSBuildWorkspace.Create())
        {
            var solution = await workspace.OpenSolutionAsync(solutionPath);
            foreach (var project in solution.Projects)
            {
                var compilation = await project.GetCompilationAsync();
                if (compilation == null) continue;

                await appendResults(solution, compilation, usages);
            }
        }
        return usages;
    }

    private static async Task AppendUsages(Solution solution, Compilation compilation, string className, Dictionary<string, object> usages)
    {
        var classSymbol = compilation.GetTypeByMetadataName(className);
        if (classSymbol == null)
        {
            return;
        }

        try
        {
            // Find references to the class
            //Console.WriteLine("before mysterious skip");

            // The line below causes uncatchable Exceptions, do not use it!
            // var references = await SymbolFinder.FindReferencesAsync(classSymbol, solution);
            
            // use workaround instead!

            var referencesTask = SymbolFinder.FindReferencesAsync(classSymbol, solution);
            referencesTask.Wait();
            var references = referencesTask.Result;


            //Console.WriteLine("after mysterious skip");


            foreach (var reference in references)
            {
                foreach (var location in reference.Locations)
                {
                    var filePath = location.Location.SourceTree?.FilePath;
                    if (filePath == null) continue;

                    List<object> usageList;
                    if (!usages.ContainsKey(className))
                    {
                        usageList = new List<object>();
                        usages[className] = usageList;
                    }
                    else
                    {
                        usageList = (List<object>) (usages[className]);
                    }

                    usageList.Add(
                            new
                            {
                                Path = filePath,
                                Pos = location.Location.SourceSpan,
                                Count = 0
                            }//.ToDictionary()
                        );
                }
            }
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine(ex.Message);
        }
        finally
        {
            //Console.WriteLine("finally");
        }
    }
}