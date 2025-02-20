
using System;
using System.Collections.Generic;
using System.IO;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace CodeExtractor;

public class CodeExtractor
{
    public static Dictionary<string, object> ExtractFromFile(string filePath, string nodeType)
    {
        string code = File.ReadAllText(filePath);
        SyntaxTree tree = CSharpSyntaxTree.ParseText(code);
        CompilationUnitSyntax root = tree.GetCompilationUnitRoot();
        var visitor = new CodeVisitor(nodeType);
        visitor.Visit(root);
        return visitor.Results;
    }
}

public class CodeVisitor : CSharpSyntaxWalker
{
    public Dictionary<string, object> Results { get; private set; } = new();
    private readonly string _nodeType;
    private string _currentClass;

    public CodeVisitor(string nodeType)
    {
        _nodeType = nodeType;
    }

    public override void VisitClassDeclaration(ClassDeclarationSyntax node)
    {
        if (_nodeType == "Class")
        {
            Results[node.Identifier.Text] = new
            {
                Text = node.ToFullString(),
                StartLine = node.GetLocation().GetLineSpan().StartLinePosition.Line + 1,
                EndLine = node.GetLocation().GetLineSpan().EndLinePosition.Line + 1,
                IsMethod = false,
                IsClass = true
            };
        }
        _currentClass = node.Identifier.Text;
        base.VisitClassDeclaration(node);
        _currentClass = null;
    }

    public override void VisitMethodDeclaration(MethodDeclarationSyntax node)
    {
        if (_nodeType == "Method")
        {
            string key = _currentClass != null ? $"{_currentClass}.{node.Identifier.Text}" : node.Identifier.Text;
            Results[key] = new
            {
                Text = node.ToFullString(),
                StartLine = node.GetLocation().GetLineSpan().StartLinePosition.Line + 1,
                EndLine = node.GetLocation().GetLineSpan().EndLinePosition.Line + 1,
                IsMethod = true,
                IsClass = false
            };
        }
        base.VisitMethodDeclaration(node);
    }
}
