using System.Collections.Generic;
using Microsoft.OpenApi.Models;
using Models;

namespace Parser
{
    public static class RequestParser
    {
        public static Request ParseRequest(KeyValuePair<OperationType, OpenApiOperation> operation)
        {
            var request = new Request(operation.Key.ToString())
            {
                Summary = operation.Value.Summary,
                BodyExample = GetBodyExample(operation.Value.RequestBody),
                BodySchema = GetBodySchema(operation.Value.RequestBody),
                UriAttributes = ParseUriAttributes(operation.Value),
                Responses = ParseResponses(operation.Value)
            };

            return request;
        }

        static string GetBodyExample(OpenApiRequestBody body)
        {
            return body != null ? ExamplesParser.ParseExample(body.Content) : null;
        }

        static Dictionary<string, object> GetBodySchema(OpenApiRequestBody body)
        {
            return body != null ? SchemaParser.ParseSchema(body.Content) : null;
        }

        static List<UriAttribute> ParseUriAttributes(OpenApiOperation operation)
        {
            List<UriAttribute> attributes = new List<UriAttribute>();
            foreach (var parameter in operation.Parameters)
            {
                var attribute = AttributeParser.ParseAttribute(parameter);
                if (attribute != null)
                {
                    attributes.Add(attribute);
                }
            }

            return attributes;
        }

        static List<Response> ParseResponses(OpenApiOperation operation)
        {
            List<Response> responses = new List<Response>();
            foreach (var openApiResponse in operation.Responses)
            {
                responses.Add(ResponseParser.ParseResponse(openApiResponse));
            }

            return responses;
        }
    }
}
