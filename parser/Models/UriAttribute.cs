using System;

namespace Models
{
    public class UriAttribute
    {
        public string Name { get; }
        public bool Required { get; }
        public string ExampleValue { get; set; }

        public string Type { get; set; }
        public string Format { get; set; }

        public UriAttribute(string name, bool required)
        {
            Name = name;
            Required = required;
        }

        public override string ToString()
        {
            return $"Name: {Name}{Environment.NewLine}Required: {Required}{Environment.NewLine}Example value: {ExampleValue}";
        }
    }
}
