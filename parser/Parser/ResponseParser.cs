using System;
using System.Collections.Generic;
using Microsoft.OpenApi.Models;
using Models;

namespace Parser
{
    public static class ResponseParser
    {
        public static Response ParseResponse(KeyValuePair<string, OpenApiResponse> openApiResponse)
        {
            string example = null;
            if (openApiResponse.Value != null)
                example = ExamplesParser.ParseExample(openApiResponse.Value.Content);

            var response = new Response
            {
                Example = example,
                StatusCode = ParseStatusCode(openApiResponse.Key)
            };

            return response;
        }

        static int ParseStatusCode(string responseKey)
        {
            if (responseKey == "default")
            {
                return -1;
            }

            if (!int.TryParse(responseKey, out var statusCode))
            {
                throw new NotImplementedException("Provided status code is not supported: " + responseKey);
            }

            return statusCode;
        }
    }
}
