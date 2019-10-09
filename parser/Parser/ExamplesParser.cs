using System.Collections.Generic;
using Microsoft.OpenApi.Models;

namespace Parser
{
    public static class ExamplesParser
    {
        static readonly List<string> SupportedContentTypes = new List<string> { "application/json", "text/plain" };

        public static string ParseExample(IDictionary<string, OpenApiMediaType> contentDict)
        {
            foreach (var supportedContentType in SupportedContentTypes)
            {
                if (contentDict.ContainsKey(supportedContentType))
                    return GetSpecificContentTypeExample(contentDict, supportedContentType);
            }

            return null;
        }

        static string GetSpecificContentTypeExample(IDictionary<string, OpenApiMediaType> contentDict, string contentType)
        {
            var content = contentDict[contentType];
            return GetRealExample(content) ?? GetExampleFromSchema(content);
        }

        static string GetRealExample(OpenApiMediaType content)
        {
            return ContentParser.GetStringExampleFromContent(content.Example, content.Examples);
        }

        static string GetExampleFromSchema(OpenApiMediaType content)
        {
            return content.Schema != null ? ContentParser.GetStringExampleFromContent(content.Schema.Example, new Dictionary<string, OpenApiExample>()) : null;
        }
    }
}
