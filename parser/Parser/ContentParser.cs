using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.OpenApi.Any;
using Microsoft.OpenApi.Models;

namespace Parser
{
    public static class ContentParser
    {
        public static string GetStringExampleFromContent(IOpenApiAny example, IDictionary<string, OpenApiExample> examples)
        {
            return GetSingleExample(example) ?? GetExampleFromExamplesDict(examples);
        }

        public static string GetSingleExample(IOpenApiAny example)
        {
            return example != null ? GetStringFromAnyType(example) : null;
        }

        // If there are more examples, take the first one
        // To the future consider creating request for each example
        static string GetExampleFromExamplesDict(IDictionary<string, OpenApiExample> examples)
        {
            return examples.Count > 0 ? GetSingleExample(examples.First().Value.Value) : null;
        }

        static string GetStringFromAnyType(IOpenApiAny value)
        {
            switch (value.AnyType)
            {
                case AnyType.Primitive:
                    return OpenApiAnyConvertor.GetPrimitiveValue(value);
                case AnyType.Object:
                case AnyType.Array:
                    return OpenApiAnyConvertor.GetJsonValue(value);
                default:
                    throw new NotImplementedException("This data example type is not supported yet!");
            }
        }
    }
}
