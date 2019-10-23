using System;
using System.Globalization;
using System.Threading;
using Microsoft.OpenApi.Any;
using NUnit.Framework;

namespace Parser.Tests
{
    public class OpenApiAnyConvertorTests
    {
        [SetUp]
        public void SetUp()
        {
            Thread.CurrentThread.CurrentCulture = new CultureInfo("en-US");
        }

        [Test]
        public void ConvertStringPrimitiveShouldReturnCorrectValue()
        {
            string value = "test";

            Assert.AreEqual(value, OpenApiAnyConvertor.GetPrimitiveValue(new OpenApiString(value)));
        }

        [Test]
        public void ConvertBooleanPrimitiveShouldReturnCorrectValue()
        {
            Assert.AreEqual("True", OpenApiAnyConvertor.GetPrimitiveValue(new OpenApiBoolean(true)));
        }

        [Test]
        public void ConvertIntegerPrimitiveShouldReturnCorrectValue()
        {
            Assert.AreEqual("5", OpenApiAnyConvertor.GetPrimitiveValue(new OpenApiInteger(5)));
        }

        [Test]
        public void ConvertBytePrimitiveShouldReturnCorrectValue()
        {
            var primitiveValue = OpenApiAnyConvertor.GetPrimitiveValue(new OpenApiByte(new byte[] { 7, 8 }));
            Assert.AreEqual("\a\b", primitiveValue);
        }

        [Test]
        public void ConvertBinaryPrimitiveShouldReturnCorrectValue()
        {
            var primitiveValue = OpenApiAnyConvertor.GetPrimitiveValue(new OpenApiBinary(new byte[] { 7, 8 }));
            Assert.AreEqual("0000011100001000", primitiveValue);
        }

        [Test]
        public void ConvertDatePrimitiveShouldReturnCorrectValue()
        {
            var primitiveValue = OpenApiAnyConvertor.GetPrimitiveValue(new OpenApiDate(DateTime.UnixEpoch));
            Assert.AreEqual("01/01/1970 00:00:00", primitiveValue);
        }

        [Test]
        public void ConvertDateTimePrimitiveShouldReturnCorrectValue()
        {
            var primitiveValue = OpenApiAnyConvertor.GetPrimitiveValue(new OpenApiDateTime(DateTime.UnixEpoch));
            Assert.AreEqual("01/01/1970 00:00:00 +00:00", primitiveValue);
        }

        [Test]
        public void ConvertObjectShouldReturnCorrectJson()
        {
            string expectedJson = "{\n  \"testKey1\": \"testValue\",\n  \"testKey2\": \"testValue\"\n}";
            var openApiObject = new OpenApiObject
            {
                {"testKey1", new OpenApiString("testValue")},
                {"testKey2", new OpenApiString("testValue")}
            };

            var jsonValue = OpenApiAnyConvertor.GetJsonValue(openApiObject);

            Assert.AreEqual(expectedJson, jsonValue);
        }

        [Test]
        public void ConvertArrayShouldReturnCorrectJson()
        {
            string expectedJson = "[\n  {\n    \"testKey1\": \"testValue\",\n    \"testKey2\": \"testValue\"\n  }\n]";
            var openApiObject = new OpenApiObject
            {
                {"testKey1", new OpenApiString("testValue")},
                {"testKey2", new OpenApiString("testValue")}
            };
            var openApiArray = new OpenApiArray {openApiObject};

            var jsonValue = OpenApiAnyConvertor.GetJsonValue(openApiArray);

            Assert.AreEqual(expectedJson, jsonValue);
        }
    }
}
