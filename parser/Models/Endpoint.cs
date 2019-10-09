using System.Collections.Generic;
using System.Text;

namespace Models
{
    public class Endpoint
    {
        public string Uri { get; }
        public List<Request> Requests { get; } = new List<Request>();

        public Endpoint(string uri)
        {
            Uri = uri;
        }

        public override string ToString()
        {
            StringBuilder builder = new StringBuilder();
            builder.Append("Uri: ");
            builder.AppendLine(Uri);
            builder.AppendLine("Requests: ");
            foreach (var request in Requests)
            {
                builder.AppendLine(request.ToString());
            }
            return builder.ToString();
        }
    }
}
