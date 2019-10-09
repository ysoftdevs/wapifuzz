using System.Collections.Generic;
using Microsoft.OpenApi.Models;
using NUnit.Framework;
using Models;

namespace Parser.Tests
{
    public class EndpointParserTests
    {
        readonly OpenApiDocument _document = new OpenApiDocument {Paths = new OpenApiPaths()};
        private void AddTwoTestingPaths()
        {
            _document.Paths.Add("/path1", new OpenApiPathItem
            {
                Operations = new Dictionary<OperationType, OpenApiOperation>
                {
                    { OperationType.Get, new OpenApiOperation
                        {
                            Responses = new OpenApiResponses
                            {
                                { "200", new OpenApiResponse()}
                            }
                        }
                    }
                }
            });

            _document.Paths.Add("/path2", new OpenApiPathItem
            {
                Operations = new Dictionary<OperationType, OpenApiOperation>
                {
                    { OperationType.Get, new OpenApiOperation
                        {
                            Responses = new OpenApiResponses
                            {
                                { "201", new OpenApiResponse()}
                            }
                        }
                    }
                }
            });
        }

        [Test]
        public void DocumentWithoutAnyPathsShouldReturnEmptyList()
        {
            List<Endpoint> endpoints = EndpointParser.ParseAllEndpoints(_document);

            Assert.IsEmpty(endpoints);
        }

        [Test]
        public void DocumentWithTwoPathsEachHavingSingleResponseShouldReturnTwoEndpoints()
        {
            AddTwoTestingPaths();

            List<Endpoint> endpoints = EndpointParser.ParseAllEndpoints(_document);

            Assert.AreEqual(2,  endpoints.Count);
        }
    }
}
