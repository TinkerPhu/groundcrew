using System.Collections;
using System.Text.Json;
using static CodeExtractor.CSharpCodeExtractor;

namespace CodeExtractor.App
{
    internal class Program
    {
        static async Task Main(string[] args)
        {
            // Ensure correct arguments
            if (args.Length != 2)
            {
                PrintHelp();
                Environment.Exit(1);
            }

            string filePath = args[0];
            string nodeTypes = args[1];

            // Validate if file exists
            if (!File.Exists(filePath))
            {
                Console.Error.WriteLine($"Error: The file '{filePath}' does not exist.");
                Environment.Exit(1);
            }

            try
            {
                // Call the method
                Dictionary<string, object> typeResults = CSharpCodeExtractor.ExtractFromFile(filePath, nodeTypes);

                if(typeResults.ContainsKey(NodeType.Class.ToString()))
                {
                    var classNames = ((Dictionary<string, object>)typeResults[NodeType.Class.ToString()]).Keys;

                    //var res = await DebugCompilation.ListAllTypes("../../../../CodeExtractor.sln");

                    var usages = await CSharpUsageAnalyzer.GetUsage("../../../../CodeExtractor.sln", classNames);

                    foreach (var classInfo in (Dictionary<string, object>)typeResults[NodeType.Class.ToString()])
                    {
                        if (usages.ContainsKey(classInfo.Key))
                        {
                            var classInfoContent = (Dictionary<string, object>)classInfo.Value;
                            classInfoContent["usages"] = usages[classInfo.Key];
                        }
                    }
                }

                string jsonOutput = JsonSerializer.Serialize(typeResults, new JsonSerializerOptions { WriteIndented = true });
                // Convert to JSON and output to stdout
                Console.WriteLine(jsonOutput);
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"Error: {ex.Message}");
                Environment.Exit(1);
            }
        }

        static void PrintHelp()
        {
            Console.WriteLine("Usage: ConsoleApp <filePath> <nodeType>");
            Console.WriteLine("Example: ConsoleApp \"data.xml\" \"element\"");
            Console.WriteLine();
            Console.WriteLine("Arguments:");
            Console.WriteLine("  filePath   - Path to the input file.");
            Console.WriteLine("  nodeType   - Type of node to extract.");
        }
    }
}