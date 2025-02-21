using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using JetBrains.Annotations;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace CodeExtractor.Tests;

[TestClass]
[TestSubject(typeof(global::CodeExtractor.CSharpComplexityAnalyzer))]
public class CSharpComplexityAnalyzerShould
{
    [TestMethod]
    public void ExtractFromFileShould()
    {
        string code = @"
        public class Example
        {
            public void Test(int x)
            {
                if (x > 0)
                {
                    Console.WriteLine(""Positive"");
                }
                else if (x < 0)
                {
                    Console.WriteLine(""Negative"");
                }
                else
                {
                    Console.WriteLine(""Zero"");
                }
            }
        }";

        SyntaxTree tree = CSharpSyntaxTree.ParseText(code);
        var walker = new CSharpComplexityAnalyzer();
        walker.Visit(tree.GetRoot());

        Assert.AreEqual(3,walker.Complexity);
    }

}
