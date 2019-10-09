using System;
using System.Collections.Generic;
using System.IO;
using Microsoft.OpenApi;
using Microsoft.OpenApi.Models;
using Microsoft.OpenApi.Readers;

namespace Parser
{
    public static class OpenApiDocumentParser
    {
        public static OpenApiSpecVersion Version;
        public static OpenApiDocument ParseOpenApiDocument(string openApiDocFilePath)
        {
            OpenApiDocument openApiDocument;
            using (FileStream stream = File.Open(openApiDocFilePath, FileMode.Open))
            {
                openApiDocument = new OpenApiStreamReader().Read(stream, out var diagnostic);

                StoreDocumentVersion(diagnostic.SpecificationVersion);
                PrintParsingErrors(diagnostic.Errors);
            }
            return openApiDocument;
        }

        static void PrintParsingErrors(IList<OpenApiError> errors)
        {
            foreach (var openApiError in errors)
            {
                Console.WriteLine("WARNING: Following parsing error occurs: " + openApiError.Message);
            }
        }

        static void StoreDocumentVersion(OpenApiSpecVersion version)
        {
            Version = version;
        }
    }
}
