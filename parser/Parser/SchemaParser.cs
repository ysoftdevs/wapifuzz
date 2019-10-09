using System.Collections.Generic;
using System.Linq;
using Microsoft.OpenApi.Models;

namespace Parser
{
    public static class SchemaParser
    {
        public static Dictionary<string, object> ParseSchema(IDictionary<string, OpenApiMediaType> contentDict)
        {
            return contentDict.ContainsKey("application/json") ? ParseSchemaProperties(contentDict["application/json"].Schema) : null;
        }

        static Dictionary<string, object> ParseSchemaProperties(OpenApiSchema schema)
        {
            Dictionary<string, object> parsedSchema = new Dictionary<string, object>();

            if (schema.AdditionalPropertiesAllowed && schema.AdditionalProperties != null)
            {
                Dictionary<string, object> nestedSchema = ParseSchemaProperties(schema.AdditionalProperties);

                // Create single object with string key: "AdditionalPropertyExample1" and with nested schema as it is in documentation
                // There can be multiple nested objects, but we want to reduce number of generated test cases
                parsedSchema.Add("AdditionalPropertyExample1", nestedSchema);
            }

            if (schema.AllOf.Count > 0)
            {
                foreach (var openApiSchema in schema.AllOf)
                {
                    Dictionary<string, object> nestedSchema = ParseSchemaProperties(openApiSchema);
                    parsedSchema = MergeTwoDictionaries(nestedSchema, parsedSchema);
                }
            }

            if (schema.OneOf.Count > 0)
            {
                Dictionary<string, object> nestedSchema = ParseSchemaProperties(schema.OneOf.First());
                parsedSchema = MergeTwoDictionaries(nestedSchema, parsedSchema);
            }

            if (schema.AnyOf.Count > 0)
            {
                Dictionary<string, object> nestedSchema = ParseSchemaProperties(schema.AnyOf.First());
                parsedSchema = MergeTwoDictionaries(nestedSchema, parsedSchema);
            }

            if (schema.Properties != null && schema.Properties.Count > 0)
            {
                foreach (var property in schema.Properties)
                {
                    Dictionary<string, object> nestedSchema = ParseSchemaProperties(property.Value);
                    parsedSchema.Add(property.Key, nestedSchema);
                }
            }
            else if (schema.Type != null && schema.Type.ToLower() == "array")
            {
                parsedSchema.Add("Type", schema.Type);
                Dictionary<string, object> arrayItemsSchema = ParseSchemaProperties(schema.Items);
                parsedSchema.Add("ArrayItemSchema", arrayItemsSchema);
            }
            else if (schema.Type != "object")
            {
                parsedSchema.Add("Title", schema.Title);
                parsedSchema.Add("Type", schema.Type);
                parsedSchema.Add("Format", schema.Format);
                parsedSchema.Add("Example", ContentParser.GetSingleExample(schema.Example));
            }

            return parsedSchema;
        }

        static Dictionary<string, object> MergeTwoDictionaries(Dictionary<string, object> first, Dictionary<string, object> second)
        {
            return new List<Dictionary<string, object>> { first, second }.SelectMany(dict => dict).ToDictionary(pair => pair.Key, pair => pair.Value);
        }
    }
}
