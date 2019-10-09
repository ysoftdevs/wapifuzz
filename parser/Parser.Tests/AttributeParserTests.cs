using System.Collections.Generic;
using Microsoft.OpenApi.Any;
using Microsoft.OpenApi.Models;
using NUnit.Framework;

namespace Parser.Tests
{
    public class AttributeParserTests
    {

        [TestCase(ParameterLocation.Cookie)]
        [TestCase(ParameterLocation.Header)]
        public void ParsingAttributeElsewhereThanInPathOrQueryShouldReturnNull(ParameterLocation parameterLocation)
        {
            OpenApiParameter parameter = new OpenApiParameter {In = parameterLocation};

            var parsedAttribute = AttributeParser.ParseAttribute(parameter);

            Assert.IsNull(parsedAttribute);
        }

        [Test]
        public void ParsingAttributeWithNoTypeOrFormatShouldReturnNull()
        {
            OpenApiParameter parameter = new OpenApiParameter {Schema = new OpenApiSchema {Type = null, Format = null}};

            var parsedAttribute = AttributeParser.ParseAttribute(parameter);

            Assert.IsNull(parsedAttribute);
        }

        [Test]
        public void ParsingPathAttributeWithValidContentExample()
        {
            string attributeContent = "test";
            OpenApiParameter parameter = new OpenApiParameter
            {
                In = ParameterLocation.Path, Schema = new OpenApiSchema {Type = "string", Format = null},
                Example = new OpenApiString(attributeContent)
            };

            var parsedAttribute = AttributeParser.ParseAttribute(parameter);

            Assert.AreEqual(attributeContent, parsedAttribute.ExampleValue);
        }

        [Test]
        public void ParsingQueryAttributeWithValidContentExample()
        {
            string attributeContent = "test";
            OpenApiParameter parameter = new OpenApiParameter
            {
                In = ParameterLocation.Query,
                Schema = new OpenApiSchema { Type = "string", Format = null },
                Example = new OpenApiString(attributeContent)
            };

            var parsedAttribute = AttributeParser.ParseAttribute(parameter);

            Assert.AreEqual(attributeContent, parsedAttribute.ExampleValue);
        }

        [Test]
        public void ParsingAttributeWithValidContentExamples()
        {
            string attributeContent = "test";
            OpenApiParameter parameter = new OpenApiParameter
            {
                In = ParameterLocation.Path, Schema = new OpenApiSchema {Type = "string", Format = null},
                Examples = new Dictionary<string, OpenApiExample>
                {
                    { "testKey 1", new OpenApiExample {Value = new OpenApiString(attributeContent)} },
                    { "testKey 2", new OpenApiExample {Value = new OpenApiString(attributeContent)} }
                }
            };

            var parsedAttribute = AttributeParser.ParseAttribute(parameter);

            Assert.AreEqual(attributeContent, parsedAttribute.ExampleValue);
        }

        [Test]
        public void ParsingAttributeWithInheritingExampleJustFromDataType()
        {
            OpenApiParameter parameter = new OpenApiParameter
            {
                In = ParameterLocation.Path,
                Schema = new OpenApiSchema { Type = "string", Format = null },
                Example = null,
                Examples = new Dictionary<string, OpenApiExample>()
            };

            var parsedAttribute = AttributeParser.ParseAttribute(parameter);

            Assert.IsNotNull(parsedAttribute);
            Assert.IsTrue(!string.IsNullOrEmpty(parsedAttribute.ExampleValue));
        }

        [Test]
        public void CheckThatParsedAttributeHasCorrectlySetDataTypeAndFormat()
        {
            OpenApiParameter parameter = new OpenApiParameter
            {
                In = ParameterLocation.Path,
                Schema = new OpenApiSchema { Type = "string", Format = null },
                Example = null,
                Examples = new Dictionary<string, OpenApiExample>()
            };

            var parsedAttribute = AttributeParser.ParseAttribute(parameter);

            Assert.IsNotNull(parsedAttribute);
            Assert.IsTrue(!string.IsNullOrEmpty(parsedAttribute.ExampleValue));
            Assert.AreEqual(parameter.Schema.Type, parsedAttribute.Type);
            Assert.AreEqual(parameter.Schema.Format, parsedAttribute.Format);
        }
    }
}
