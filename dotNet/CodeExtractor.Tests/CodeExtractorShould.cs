using System.IO;
using JetBrains.Annotations;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace CodeExtractor.Tests;

[TestClass]
[TestSubject(typeof(CodeExtractor))]
public class CodeExtractorTestX
{

    [TestMethod]
    public void ExtractFromFileShould()
    {
        var basePath = "../../..";
        var path = Path.Combine(basePath, "ExampleClass.cs");
        
        Assert.IsTrue(File.Exists(path));

        var resultClasses  = CodeExtractor.ExtractFromFile(path, "Class");
        Assert.AreEqual(1, resultClasses.Keys.Count);
        Assert.Contains("ExampleClass", resultClasses.Keys);

        var resultMethods  = CodeExtractor.ExtractFromFile(path, "Method");
        Assert.AreEqual(2, resultMethods.Keys.Count);
        Assert.Contains("ExampleClass.MethodOne", resultMethods.Keys);
        Assert.Contains("ExampleClass.MethodTwo", resultMethods.Keys);
    }
}