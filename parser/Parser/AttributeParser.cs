using System;
using Microsoft.OpenApi.Models;
using Models;

namespace Parser
{
    public static class AttributeParser
    {
        public static UriAttribute ParseAttribute(OpenApiParameter parameter)
        {
            if (parameter.In == ParameterLocation.Path || parameter.In == ParameterLocation.Query)
            {
                if (parameter.Schema == null || parameter.Schema.Type == null && parameter.Schema.Format == null)
                {
                    throw new ArgumentException("We do not know anything useful about passed URI parameter.");
                }

                UriAttribute attribute = new UriAttribute(parameter.Name, parameter.Required)
                {
                    ExampleValue = ContentParser.GetStringExampleFromContent(parameter.Example, parameter.Examples) ??
                                   ContentParser.GetSingleExample(parameter.Schema?.Example) ??
                                   PrimitiveDataTypeExampleGenerator.GenerateExampleValueByType(parameter.Schema.Type, parameter.Schema.Format),
                    Type = parameter.Schema.Type,
                    Format = parameter.Schema.Format
                };
                return attribute;
            }
            return null;
        }
    }
}
