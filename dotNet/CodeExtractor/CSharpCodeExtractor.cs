using System.Collections.Generic;
using System.IO;
using System.Reflection;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;


namespace CodeExtractor;

public partial class CSharpCodeExtractor
{
    public static Dictionary<string, object> ExtractFromFile(string filePath, string nodeTypes)
    {
        var nodeTypeSet = new HashSet<string>(nodeTypes.Split(','));
        return ExtractFromFile(filePath, nodeTypeSet);
    }

    public static Dictionary<string, object> ExtractFromFile(string filePath, ICollection<string> nodeTypes)
    {
        string code = File.ReadAllText(filePath);
        SyntaxTree tree = CSharpSyntaxTree.ParseText(code);
        CompilationUnitSyntax root = tree.GetCompilationUnitRoot();
        var visitor = new CodeVisitor(nodeTypes);
        visitor.Visit(root);

        return visitor.Results;
    }

    public class CodeVisitor : CSharpSyntaxWalker
    {
        public Dictionary<string, object> Results { get; private set; } = new();
        private readonly ICollection<string> _nodeTypes;
        private string _currentNamespace;
        private string _currentClass;

        public CodeVisitor(ICollection<string> nodeTypes)
        {
            _nodeTypes = nodeTypes;
        }

        public override void VisitNamespaceDeclaration(NamespaceDeclarationSyntax node)
        {
            _currentNamespace = node.Name.ToString();
            base.VisitNamespaceDeclaration(node);
            _currentNamespace = null;
        }

        public override void VisitClassDeclaration(ClassDeclarationSyntax node)
        {
            string className = node.Identifier.Text;
            string fullyQualifiedName = _currentNamespace != null ? $"{_currentNamespace}.{className}" : className;
            if (_nodeTypes.Contains(NodeType.Class.ToString()))
            {
                var classes = ProvideResultDictionary(Results, NodeType.Class.ToString());
                classes[fullyQualifiedName] = new
                {
                    Text = node.ToFullString(),
                    StartLine = node.GetLocation().GetLineSpan().StartLinePosition.Line + 1,
                    EndLine = node.GetLocation().GetLineSpan().EndLinePosition.Line + 1,
                    IsMethod = false,
                    IsClass = true
                }.ToDictionary();
            }
            _currentClass = fullyQualifiedName;
            base.VisitClassDeclaration(node);
            _currentClass = null;
        }
        public override void VisitMethodDeclaration(MethodDeclarationSyntax node)
        {
            if (_nodeTypes.Contains(NodeType.Method.ToString()))
            {
                var methods = ProvideResultDictionary(Results, NodeType.Method.ToString());
                string methodName = node.Identifier.Text;
                string fullyQualifiedMethodName = _currentClass != null ? $"{_currentClass}.{methodName}" : methodName;

                var methodInfo = new
                {
                    Text = node.ToFullString(),
                    StartLine = node.GetLocation().GetLineSpan().StartLinePosition.Line + 1,
                    EndLine = node.GetLocation().GetLineSpan().EndLinePosition.Line + 1,
                    IsMethod = true,
                    IsClass = false
                }.ToDictionary();
                methods[fullyQualifiedMethodName] = methodInfo;
                if (_currentClass != null && Results.ContainsKey(NodeType.Class.ToString()))
                {
                    var classesDict = (Dictionary<string, object>) Results[NodeType.Class.ToString()];
                    var classDict = (Dictionary<string, object>) classesDict[_currentClass];
                    var classMethods = ProvideResultDictionary(classDict, NodeType.Method.ToString());
                    classMethods[methodName] = methodInfo;
                }
            }

            base.VisitMethodDeclaration(node);
        }

        private Dictionary<string, object> ProvideResultDictionary(Dictionary<string, object> container, string nodeType)
        {
            Dictionary<string, object> resultDictionary;
            if (container.ContainsKey((nodeType)))
            {
                resultDictionary = (Dictionary<string, object>)container[nodeType];
            }
            else
            {
                resultDictionary = new Dictionary<string, object>();
                container[nodeType] = resultDictionary;
            }

            return resultDictionary;
        }
    }
}