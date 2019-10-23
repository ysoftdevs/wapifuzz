using System;
using System.Globalization;
using System.IO;
using System.Text;
using Microsoft.OpenApi.Any;
using Microsoft.OpenApi.Writers;

namespace Parser
{
    public static class OpenApiAnyConvertor
    {
        public static string GetPrimitiveValue(IOpenApiAny value)
        {
            IOpenApiPrimitive primitive = (IOpenApiPrimitive) value;

            switch (primitive.PrimitiveType)
            {
                case PrimitiveType.String:
                    OpenApiString stringValue = (OpenApiString) primitive;
                    return stringValue.Value;
                case PrimitiveType.Boolean:
                    OpenApiBoolean booleanValue = (OpenApiBoolean) primitive;
                    return booleanValue.Value.ToString();
                case PrimitiveType.Integer:
                    OpenApiInteger integerValue = (OpenApiInteger) primitive;
                    return integerValue.Value.ToString();
                case PrimitiveType.Long:
                    OpenApiLong longValue = (OpenApiLong) primitive;
                    return longValue.Value.ToString();
                case PrimitiveType.Float:
                    OpenApiFloat floatValue = (OpenApiFloat) primitive;
                    return floatValue.Value.ToString(CultureInfo.InvariantCulture);
                case PrimitiveType.Double:
                    OpenApiDouble doubleValue = (OpenApiDouble) primitive;
                    return doubleValue.Value.ToString(CultureInfo.InvariantCulture);
                case PrimitiveType.Byte:
                    OpenApiByte byteValue = (OpenApiByte) primitive;
                    return Encoding.Default.GetString(byteValue.Value);
                case PrimitiveType.Binary:
                    OpenApiBinary binaryValue = (OpenApiBinary) primitive;
                    StringBuilder builder = new StringBuilder();
                    foreach (byte byteVal in binaryValue.Value)
                    {
                        builder.Append(Convert.ToString(byteVal, 2).PadLeft(8, '0'));
                    }
                    return builder.ToString();
                case PrimitiveType.Date:
                    OpenApiDate dateValue = (OpenApiDate) primitive;
                    return dateValue.Value.ToString(CultureInfo.InvariantCulture);
                case PrimitiveType.DateTime:
                    OpenApiDateTime dateTimeValue = (OpenApiDateTime) primitive;
                    return dateTimeValue.Value.ToString(CultureInfo.InvariantCulture);
                case PrimitiveType.Password:
                    OpenApiPassword passwordValue = (OpenApiPassword) primitive;
                    return passwordValue.Value;
                default:
                    throw new NotImplementedException("This data example type is not supported yet!");
            }
        }

        public static string GetJsonValue(IOpenApiAny value)
        {
            StringBuilder builder = new StringBuilder();
            value.Write(new OpenApiJsonWriter(new StringWriter(builder)), OpenApiDocumentParser.Version);
            return builder.ToString();
        }
    }
}
