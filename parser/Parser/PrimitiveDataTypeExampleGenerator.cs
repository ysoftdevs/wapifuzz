using System;
using System.Text;

namespace Parser
{
    // Data types for Open API 2 and OpenAPI 3 are basically the same:
    // https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md
    // https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md
    public static class PrimitiveDataTypeExampleGenerator
    {
        public static string GenerateExampleValueByType(string type, string format)
        {
            switch (type)
            {
                case "integer":
                    return "42";
                case "number":
                    return "42.0";
                case "boolean":
                    return "True";
                case "array":
                    return "attr1,attr2";
                case "string":
                {
                    const string example = "example";
                    switch (format)
                    {
                        case null:
                            return example;
                        case "byte":
                            var plainTextBytes = Encoding.UTF8.GetBytes(example);
                            return Encoding.Default.GetString(plainTextBytes);
                        case "binary":
                            return "01234567";
                        case "date":
                            return "2002-10-02";
                        case "date-time":
                            return "2002-10-02T10:00:00-05:00";
                        case "password":
                            return example;
                    }

                    break;
                }
            }

            throw new NotImplementedException("Unrecognized value data type! Check the OpenAPI documentation for new types!");
        }
    }
}
