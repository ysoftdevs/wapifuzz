using System.Collections.Generic;
using Microsoft.OpenApi.Models;
using Models;

namespace Parser
{
    public static class EndpointParser
    {
        public static List<Endpoint> ParseAllEndpoints(OpenApiDocument openApiDocument)
        {
            List<Endpoint> endpoints = new List<Endpoint>();

            foreach (var path in openApiDocument.Paths)
            {
                endpoints.Add(ParseEndpoint(path));
            }
            return endpoints;
        }

        static Endpoint ParseEndpoint(KeyValuePair<string, OpenApiPathItem> path)
        {
            Endpoint endpoint = new Endpoint(path.Key);
            foreach (KeyValuePair<OperationType, OpenApiOperation> operation in path.Value.Operations)
            {
                endpoint.Requests.Add(RequestParser.ParseRequest(operation));
            }
            return endpoint;
        }
    }
}
