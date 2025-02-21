using System.Text.Json;

namespace CodeExtractor.App
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // Ensure correct arguments
            if (args.Length != 2)
            {
                PrintHelp();
                Environment.Exit(1);
            }

            string filePath = args[0];
            string nodeType = args[1];

            // Validate if file exists
            if (!File.Exists(filePath))
            {
                Console.Error.WriteLine($"Error: The file '{filePath}' does not exist.");
                Environment.Exit(1);
            }

            try
            {
                Dictionary<string, object> typeResults = new Dictionary<string, object>();
                var nodeTypes = nodeType.Split(',');
                foreach (var type in nodeTypes)
                {
                    // Call the method
                    Dictionary<string, object> result = CodeExtractor.ExtractFromFile(filePath, type);

                    typeResults[type] = result;
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