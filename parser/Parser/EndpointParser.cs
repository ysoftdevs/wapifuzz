using System;
using System.Collections.Generic;
using System.Linq;
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
                endpoints.Add(ParseEndpoint(path, GetBasePath(openApiDocument)));
            }
            return endpoints;
        }

        static Endpoint ParseEndpoint(KeyValuePair<string, OpenApiPathItem> path, string basePath)
        {
            Endpoint endpoint = new Endpoint(basePath + path.Key);
            foreach (KeyValuePair<OperationType, OpenApiOperation> operation in path.Value.Operations)
            {
                endpoint.Requests.Add(RequestParser.ParseRequest(operation));
            }
            return endpoint;
        }

        static string GetBasePath(OpenApiDocument openApiDocument)
        {
            string basePath = string.Empty;
            if (openApiDocument.Servers.Any())
            {
                basePath = new Uri(openApiDocument.Servers.First().Url).AbsolutePath;
            }

            if (basePath == "/")
                basePath = string.Empty;

            return basePath;
        }
    }
}
