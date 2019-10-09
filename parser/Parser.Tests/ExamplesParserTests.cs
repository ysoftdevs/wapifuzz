using System.Collections.Generic;
using Microsoft.OpenApi.Any;
using Microsoft.OpenApi.Models;
using NUnit.Framework;

namespace Parser.Tests
{
    public class ExamplesParserTests
    {
        [TestCase("application/octet-stream")]
        [TestCase("application/pdf")]
        [TestCase("application/zip")]
        public void ParsingNotSupportedContentTypeShouldReturnNull(string contentType)
        {
            Assert.IsNull(ExamplesParser.ParseExample(new Dictionary<string, OpenApiMediaType> { { contentType, null } }));
        }

        [Test]
        public void ParsingPlainTextContent()
        {
            string plainText = "test";
            Dictionary<string, OpenApiMediaType> content = new Dictionary<string, OpenApiMediaType>
            {
                {"text/plain", new OpenApiMediaType {Example = new OpenApiString(plainText)}}
            };

            string example = ExamplesParser.ParseExample(content);

            Assert.AreEqual(plainText, example);
        }

        [Test]
        public void ParsingJsonContent()
        {
            string jsonTemplate = "{\n  \"testKey1\": \"testValue\",\n  \"testKey2\": \"testValue\"\n}";
            Dictionary<string, OpenApiMediaType> content = new Dictionary<string, OpenApiMediaType>
            {
                {
                    "application/json", new OpenApiMediaType
                    {
                        Example = new OpenApiObject
                        {
                            {"testKey1", new OpenApiString("testValue") },
                            {"testKey2", new OpenApiString("testValue") }
                        }
                    }

                }
            };

            string example = ExamplesParser.ParseExample(content);

            Assert.AreEqual(jsonTemplate, example);
        }
    }
}
