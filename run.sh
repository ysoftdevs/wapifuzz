#!/bin/bash

USAGE="Usage: `basename $0` config_file_path open_api_doc_file_path [custom_payloads_file]"

# We want at least 2 parameters
if [ ${#} -lt 2 ]
then
    echo $USAGE >&2
    exit 1
fi

# Load script arguments
WAPIFUZZ_CONFIG=$1
OPENAPI_DOCUMENTATION=$2
CUSTOM_PAYLOADS_FILE=$3

# Define binary binaries paths
PIP3_BIN=pip3
PYTHON3_BIN=python3
DOTNET_BIN=dotnet
JAVA=java
DOCKER=docker

# Define paths inside directory
JUNIT_TEST_REPORT_FILENAME=reports.junit.xml
HTML_TEST_REPORT_FILENAME=reports.html

PARSER_FOLDER=./parser/OpenApiParserCLI/
API_REQUESTS_JSON=./parser/api.json
JUNIT_TEST_REPORT="./reporter/$JUNIT_TEST_REPORT_FILENAME"
HTML_TEST_REPORT="./reporter/$HTML_TEST_REPORT_FILENAME"
FUZZER_LOG=fuzzing.log
XUNIT2HTML_XSL=./reporter/xunit_to_html.xsl
SAXON9HE=./reporter/saxon9he.jar

# If we are in Docker container, write output files into mounted folder and append this folder before input files paths
if [ "$container" = "true" ]; then
    echo "Founded mounted Docker directory, you can find WapiFuzz artifacts in your working directory."
    WAPIFUZZ_CONFIG="./mnt/$WAPIFUZZ_CONFIG"
    OPENAPI_DOCUMENTATION="./mnt/$OPENAPI_DOCUMENTATION"

    if [ ! -z "$CUSTOM_PAYLOADS_FILE" ]; then
        CUSTOM_PAYLOADS_FILE="./mnt/$CUSTOM_PAYLOADS_FILE"
    fi

    FUZZER_LOG="./mnt/$FUZZER_LOG"
    JUNIT_TEST_REPORT="./mnt/$JUNIT_TEST_REPORT_FILENAME"
    HTML_TEST_REPORT="./mnt/$HTML_TEST_REPORT_FILENAME"
fi

# Check if config file and documentation file are valid files
if [ ! -f "$WAPIFUZZ_CONFIG" ]
then
    echo "Configuration file path is not valid!" >&2
    echo $USAGE >&2
    exit 1
fi

if [ ! -f "$OPENAPI_DOCUMENTATION" ]
then
    echo "OpenApi documentation file path is not valid!" >&2
    echo $USAGE >&2
    exit 1
fi

# Define docker images tags
REPORTER_IMAGE_TAG=wapifuzz:reporter

# Pilenine execution
echo "Started parsing"
${DOTNET_BIN} run -p ${PARSER_FOLDER} ${OPENAPI_DOCUMENTATION} ${API_REQUESTS_JSON} || { echo 'Parsing of documentation failed! Fuzzing will not be started.' ; exit 1; }
echo "Parsing finished"

echo "Installing virtualenv and dependencies for fuzzer"
${PIP3_BIN} install virtualenv
${PYTHON3_BIN} -m virtualenv env
echo "Started fuzzing"
. ./env/bin/activate ; \
pip install --upgrade pip ; pip install git+https://github.com/jtpereyda/boofuzz.git ; pip install junit-xml ; \
python fuzzer/wapifuzz.py ${WAPIFUZZ_CONFIG} ${API_REQUESTS_JSON} ${JUNIT_TEST_REPORT} ${CUSTOM_PAYLOADS_FILE} > ${FUZZER_LOG}
FUZZER_ERROR_CODE=$?
if [ "$FUZZER_ERROR_CODE" -eq "2" ]; then
   echo "Fuzzing failed. Trying to generate HTML result of procceeded test cases.";
fi
deactivate
echo "Fuzzing finished"

echo "Starting generating HTML test report"
if type "$JAVA" > /dev/null; then
    ${JAVA} -jar ${SAXON9HE} -o:${HTML_TEST_REPORT} -s:${JUNIT_TEST_REPORT} -xsl:${XUNIT2HTML_XSL} || { echo 'HTML test report via installed Java binary cannot be produced. There was an error during parsing JUnit input file.' ; exit 1; }
elif type "$DOCKER" > /dev/null; then
    ${DOCKER} build reporter -t ${REPORTER_IMAGE_TAG} || { echo 'HTML test report cannot be produced. Docker cannot build image.' ; exit 1; }
    ${DOCKER} run ${REPORTER_IMAGE_TAG} > ${HTML_TEST_REPORT} || { echo 'HTML test report cannot be produced. Docker run failed.' ; exit 1; }
else
    echo 'HTML test report cannot be produced. Missing JRE or Docker binary. Need to provide at least one of them. You can specify their binary paths in the beggining of this script.'
    exit 1
fi
echo "Ending generating HTML test report"

if [ "$FUZZER_ERROR_CODE" -eq "1" ]; then
   echo "There were some failures! Returning non-zero return value.";
   exit -1;
fi
