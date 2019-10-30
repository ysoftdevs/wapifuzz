using System;
using NUnit.Framework;

namespace Parser.Tests
{
    public class PrimitiveDataTypeExampleGeneratorTests
    {
        [TestCase("integer", null, "42")]
        [TestCase("number", null, "42.0")]
        [TestCase("boolean", null, "True")]
        [TestCase("string", null, "example")]
        [TestCase("string", "byte", "example")]
        [TestCase("string", "binary", "01234567")]
        [TestCase("string", "date", "2002-10-02")]
        [TestCase("string", "date-time", "2002-10-02T10:00:00-05:00")]
        [TestCase("string", "password", "example")]
        [TestCase("array", null, "attr1,attr2")]
        public void ValidCombinationsShouldReturnValidValue(string type, string format, string expected)
        {
            string example = PrimitiveDataTypeExampleGenerator.GenerateExampleValueByType(type, format);
            Assert.AreEqual(expected, example);
        }

        [Test]
        public void InvalidCombinationsShouldThrowAnException()
        {
            Assert.Throws<NotImplementedException>(() => PrimitiveDataTypeExampleGenerator.GenerateExampleValueByType("test", null));
        }
    }
}
 