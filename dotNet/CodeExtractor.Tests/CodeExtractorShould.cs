using System.IO;
using System.Reflection;
using JetBrains.Annotations;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace CodeExtractor.Tests;

[TestClass]
[TestSubject(typeof(global::CodeExtractor.CodeExtractor))]
public class CodeExtractorTest
{

    [TestMethod]
    public void ExtractFromFileShould()
    {
        var basePath = "../../..";
        var path = Path.Combine(basePath, "ExampleClass.cs");
        
        Assert.IsTrue(File.Exists(path));

        var resultClasses  = global::CodeExtractor.CodeExtractor.ExtractFromFile(path, "Class");
        Assert.AreEqual(1, resultClasses.Keys.Count);
        Assert.Contains("ExampleClass", resultClasses.Keys);

        var resultMethods  = global::CodeExtractor.CodeExtractor.ExtractFromFile(path, "Method");
        Assert.AreEqual(2, resultMethods.Keys.Count);
        Assert.Contains("ExampleClass.MethodOne", resultMethods.Keys);
        Assert.Contains("ExampleClass.MethodTwo", resultMethods.Keys);


        System.Runtime.CompilerServices.NullableContextAttribute x = new System.Runtime.CompilerServices.NullableContextAttribute(1);
        var ass = Assembly.GetAssembly(typeof(System.Runtime.CompilerServices.NullableContextAttribute));
    }
}