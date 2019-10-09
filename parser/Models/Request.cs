using System.Collections.Generic;
using System.Text;

namespace Models
{
    public class Request
    {
        public string Method { get; }
        public string Summary { get; set; }
        public List<UriAttribute> UriAttributes { get; set; }
        public List<Response> Responses { get; set; }
        public string BodyExample { get; set; }

        public Dictionary<string, object> BodySchema { get; set; }

        public Request(string method)
        {
            Method = method;
        }

        public override string ToString()
        {
            StringBuilder builder = new StringBuilder();
            builder.Append("Type: ");
            builder.AppendLine(Method);
            builder.Append("Summary: ");
            builder.AppendLine(Summary);
            builder.AppendLine("Uri Attributes: ");
            foreach (var attribute in UriAttributes)
            {
                builder.AppendLine(attribute.ToString());
            }
            builder.AppendLine("Responses: ");
            foreach (var response in Responses)
            {
                builder.AppendLine(response.ToString());
            }
            builder.Append("BodyExample: ");
            builder.AppendLine(BodyExample);
            return builder.ToString();
        }
    }
}