using System.Collections.Generic;
using Microsoft.OpenApi.Any;
using Microsoft.OpenApi.Models;
using NUnit.Framework;

namespace Parser.Tests
{
    public class ContentParserTests
    {
        [Test]
        public void NoExampleFoundShouldReturnNull()
        {
            string parsedExample = ContentParser.GetStringExampleFromContent(null, new Dictionary<string, OpenApiExample>());

            Assert.IsNull(parsedExample);
        }

        [Test]
        public void ParsingValidContentExample()
        {
            string attributeContent = "test";
            OpenApiString example = new OpenApiString(attributeContent);
            Dictionary<string, OpenApiExample> examples = new Dictionary<string, OpenApiExample>();

            string parsedExample = ContentParser.GetStringExampleFromContent(example, examples);

            Assert.AreEqual(attributeContent, parsedExample);
        }

        [Test]
        public void ParsingContentExamples()
        {
            string attributeContent = "test";
            Dictionary<string, OpenApiExample> examples = new Dictionary<string, OpenApiExample>
            {
                {"testKey 1", new OpenApiExample {Value = new OpenApiString(attributeContent)}},
                {"testKey 2", new OpenApiExample {Value = new OpenApiString(attributeContent)}}
            };

            string parsedExample = ContentParser.GetStringExampleFromContent(null, examples);

            Assert.AreEqual(attributeContent, parsedExample);
        }
    }
}
