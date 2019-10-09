using System;

namespace Models
{
    public class Response
    {
        public int StatusCode { get; set; }
        public string Example { get; set; }

        public override string ToString()
        {
            return $"Status code: {StatusCode}{Environment.NewLine}Example: {Example}";
        }
    }
}
