FROM openjdk:11
COPY . /usr/src/saxon
WORKDIR /usr/src/saxon
CMD ["java", "-jar", "saxon9he.jar", "-s:reports.junit.xml", "-xsl:xunit_to_html.xsl"]
