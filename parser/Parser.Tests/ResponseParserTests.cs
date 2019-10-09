using System;
using System.Collections.Generic;
using Microsoft.OpenApi.Any;
using Microsoft.OpenApi.Models;
using Models;
using NUnit.Framework;

namespace Parser.Tests
{
    public class ResponseParserTests
    {
        [Test]
        public void ValidResponseParsingShouldHaveCorrectValues()
        {
            int statusCode = 200;
            string example = "example";

            KeyValuePair<string, OpenApiResponse> openApiResponse = new KeyValuePair<string, OpenApiResponse>(statusCode.ToString(), new OpenApiResponse
            {
                Content = new Dictionary<string, OpenApiMediaType>
                {
                    { "text/plain", new OpenApiMediaType
                    {
                        Schema = new OpenApiSchema {Type = "string", Format = null},
                        Example = new OpenApiString(example)
                    } }
                }
            });

            Response response = ResponseParser.ParseResponse(openApiResponse);

            Assert.AreEqual(statusCode, response.StatusCode);
            Assert.AreEqual(example, response.Example);
        }

        [Test]
        public void InvalidResponseStatusCodeShouldThrowException()
        {
            KeyValuePair<string, OpenApiResponse> openApiResponse = new KeyValuePair<string, OpenApiResponse>("invalid", new OpenApiResponse());
            Assert.Throws<NotImplementedException>(() => ResponseParser.ParseResponse(openApiResponse));
        }
    }
}
