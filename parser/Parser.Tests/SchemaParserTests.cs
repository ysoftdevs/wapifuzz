using System.Collections.Generic;
using System.Linq;
using Microsoft.OpenApi.Any;
using Microsoft.OpenApi.Models;
using NUnit.Framework;

namespace Parser.Tests
{
    public class SchemaParserTests
    {
        [TestCase("application/octet-stream")]
        [TestCase("application/pdf")]
        [TestCase("application/zip")]
        public void ParsingNotSupportedContentTypeShouldReturnNull(string contentType)
        {
            Assert.IsNull(SchemaParser.ParseSchema(new Dictionary<string, OpenApiMediaType> { { contentType, null } }));
        }

        [Test]
        public void SchemaWithRegularProperties()
        {
            string testingPropertyName = "testKey";
            string testingPropertyType = "string";
            string testingPropertyExample = "test";
            string testingPropertyFormat = null;

            Dictionary<string, OpenApiMediaType> content = new Dictionary<string, OpenApiMediaType>
            {
                {
                    "application/json", new OpenApiMediaType
                    {
                        Schema = new OpenApiSchema
                        {
                            Properties = new Dictionary<string, OpenApiSchema>
                            {
                                {
                                    testingPropertyName, new OpenApiSchema
                                    {
                                        Type = testingPropertyType,
                                        Example = new OpenApiString(testingPropertyExample),
                                        Title = testingPropertyName,
                                        Format = testingPropertyFormat
                                    }
                                }
                            }
                        }
                    }
                }
            };

            Dictionary<string, object> parsedSchema = SchemaParser.ParseSchema(content);
            Dictionary<string, object> testingProperty = (Dictionary<string, object>) parsedSchema.First().Value;

            Assert.AreEqual(testingPropertyName, parsedSchema.First().Key);

            Assert.That(testingProperty.ContainsKey("Title"));
            Assert.That(testingProperty.ContainsKey("Type"));
            Assert.That(testingProperty.ContainsKey("Format"));
            Assert.That(testingProperty.ContainsKey("Example"));

            Assert.AreEqual(testingPropertyName, testingProperty["Title"]);
            Assert.AreEqual(testingPropertyType, testingProperty["Type"]);
            Assert.AreEqual(testingPropertyFormat, testingProperty["Format"]);
            Assert.AreEqual(testingPropertyExample, testingProperty["Example"]);
        }

        [Test]
        public void SchemaWithRegularArrayOfDoublesProperty()
        {
            string testingPropertyName = "testKey";
            string testingPropertyType = "array";
            string testingPropertyFormat = null;

            string testingArrayItemType = "double";
            string testingArrayItemFormat = "number";

            Dictionary<string, OpenApiMediaType> content = new Dictionary<string, OpenApiMediaType>
            {
                {
                    "application/json", new OpenApiMediaType
                    {
                        Schema = new OpenApiSchema
                        {
                            Properties = new Dictionary<string, OpenApiSchema>
                            {
                                {
                                    testingPropertyName, new OpenApiSchema
                                    {
                                        Type = testingPropertyType,
                                        Title = testingPropertyName,
                                        Items = new OpenApiSchema { Type = testingArrayItemType, Format = testingArrayItemFormat },
                                        Format = testingPropertyFormat
                                    }
                                }
                            }
                        }
                    }
                }
            };

            Dictionary<string, object> parsedSchema = SchemaParser.ParseSchema(content);
            Dictionary<string, object> testingProperty = (Dictionary<string, object>) parsedSchema.First().Value;
            Dictionary<string, object> arrayTypeDictionary = (Dictionary<string, object>) testingProperty["ArrayItemSchema"];

            Assert.AreEqual(testingPropertyName, parsedSchema.First().Key);

            Assert.That(arrayTypeDictionary.ContainsKey("Type"));
            Assert.That(arrayTypeDictionary.ContainsKey("Format"));

            Assert.AreEqual(testingArrayItemType, arrayTypeDictionary["Type"]);
            Assert.AreEqual(testingArrayItemFormat, arrayTypeDictionary["Format"]);
        }

        [Test]
        public void SchemaWithAdditionalProperties()
        {
            string testingPropertyName = "testKey";
            string testingPropertyType = "boolean";
            bool testingPropertyExample = true;
            string testingPropertyFormat = null;

            Dictionary<string, OpenApiMediaType> content = new Dictionary<string, OpenApiMediaType>
            {
                {
                    "application/json", new OpenApiMediaType
                    {
                        Schema = new OpenApiSchema
                        {
                            AdditionalPropertiesAllowed = true,
                            AdditionalProperties = new OpenApiSchema {Properties = new Dictionary<string, OpenApiSchema>
                            {
                                {
                                    testingPropertyName, new OpenApiSchema
                                    {
                                        Type = testingPropertyType,
                                        Example = new OpenApiBoolean(testingPropertyExample),
                                        Title = testingPropertyName,
                                        Format = testingPropertyFormat
                                    }
                                }
                            }}
                        }
                    }

                }
            };

            Dictionary<string, object> firstAdditionalPropertyDictionary = (Dictionary<string, object>) SchemaParser.ParseSchema(content).First().Value;
            Dictionary<string, object> firstAdditionalPropertyItemDictionary = (Dictionary<string, object>)firstAdditionalPropertyDictionary.First().Value;

            Assert.AreEqual(testingPropertyName, firstAdditionalPropertyDictionary.First().Key);

            Assert.That(firstAdditionalPropertyItemDictionary.ContainsKey("Title"));
            Assert.That(firstAdditionalPropertyItemDictionary.ContainsKey("Type"));
            Assert.That(firstAdditionalPropertyItemDictionary.ContainsKey("Format"));
            Assert.That(firstAdditionalPropertyItemDictionary.ContainsKey("Example"));

            Assert.AreEqual(testingPropertyName, firstAdditionalPropertyItemDictionary["Title"]);
            Assert.AreEqual(testingPropertyType, firstAdditionalPropertyItemDictionary["Type"]);
            Assert.AreEqual(testingPropertyFormat, firstAdditionalPropertyItemDictionary["Format"]);
            Assert.AreEqual(testingPropertyExample.ToString(), firstAdditionalPropertyItemDictionary["Example"]);
        }
    }
}
