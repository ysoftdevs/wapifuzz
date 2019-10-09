using System;
using System.Collections.Generic;
using System.IO;
using Microsoft.OpenApi.Models;
using Models;
using Newtonsoft.Json;
using Parser;

namespace OpenApiParserCLI
{
    static class Program
    {
        static int Main(string[] args)
        {
            if (args.Length != 2)
            {
                Console.WriteLine("Bad arguments provided.");
                PrintHelp();
                return 1;
            }

            string openApiDocFilePath = args[0];
            string outputEndpointsFilePath = args[1];

            if (!ValidateArguments(openApiDocFilePath, outputEndpointsFilePath))
            {
                PrintHelp();
                return 1;
            }

            OpenApiDocument openApiDocument = OpenApiDocumentParser.ParseOpenApiDocument(openApiDocFilePath);
            List<Endpoint> endpoints = EndpointParser.ParseAllEndpoints(openApiDocument);
            string json = JsonConvert.SerializeObject(endpoints, Formatting.Indented);
            File.WriteAllText(outputEndpointsFilePath, json);

            return 0;
        }

        static bool ValidateArguments(string openApiDocFilePath, string outputEndpointsFilePath)
        {
            if (!File.Exists(openApiDocFilePath))
            {
                Console.WriteLine("Cannot find specified OpenApi file");
                return false;
            }

            try
            {
                File.Create(outputEndpointsFilePath).Close();
            }
            catch
            {
                Console.WriteLine("Cannot create output file on defined path.");
                return false;
            }
            return true;
        }

        static void PrintHelp()
        {
            Console.WriteLine("Arguments:");
            Console.WriteLine("1] OpenAPI doc. file");
            Console.WriteLine("2] Output file with JSON endpoints specification");
            Console.WriteLine("Example: parser.exe api.yaml output.json");
        }
    }
}
