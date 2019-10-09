using System.Collections.Generic;
using Microsoft.OpenApi.Any;
using Microsoft.OpenApi.Models;
using Models;
using NUnit.Framework;

namespace Parser.Tests
{
    public class RequestParserTests
    {
        [Test]
        public void ValidRequestParsingShouldHaveCorrectValues()
        {
            string summary = "summary";
            string example = "test";

            KeyValuePair<OperationType, OpenApiOperation> operation =
                new KeyValuePair<OperationType, OpenApiOperation>(OperationType.Get, new OpenApiOperation
                {
                    Summary = summary,
                    Parameters = new List<OpenApiParameter> { new OpenApiParameter
                    {
                        In = ParameterLocation.Path,
                        Example = new OpenApiString(example),
                        Schema = new OpenApiSchema {Type = "string", Format = null}
                    } },
                    RequestBody = new OpenApiRequestBody
                    {
                        Content = new Dictionary<string, OpenApiMediaType>
                        {
                            { "text/plain", new OpenApiMediaType
                            {
                                Example = new OpenApiString(example)
                            } }
                        }
                    }
                });


            Request request = RequestParser.ParseRequest(operation);

            Assert.AreEqual(summary, request.Summary);
            Assert.AreEqual(example, request.BodyExample);
            Assert.AreEqual(example, request.UriAttributes[0].ExampleValue);
        }


    }
}
