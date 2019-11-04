# Params definition
param
(
    [Parameter(Mandatory=$true)][string]$config,
    [Parameter(Mandatory=$true)][string]$openapi,
    [Parameter(Mandatory=$false)][string]$payloads
)

$ErrorActionPreference = "Stop"

# Check if config file and documentation file are valid files
if (!(Test-Path $config))
{
    Write-Error "Configuration file path is not valid!"
    exit
}

if (!(Test-Path $openapi))
{
    Write-Error "OpenApi documentation file path is not valid!"
    exit
}

# Define binary binaries paths
$PY='py'
$PYTHON3='-3'
$PIP3='-3', '-m', 'pip'
$DOTNET='dotnet'
$JAVA='java'
$DOCKER='docker'

# Define paths inside directory
$PARSER_FOLDER="./parser/OpenApiParserCLI/"
$API_REQUESTS_JSON="./parser/api.json"
$FUZZER_LOG="fuzzing.log"
$JUNIT_TEST_REPORT="./reporter/reports.junit.xml"
$HTML_TEST_REPORT="./reporter/reports.html"
$XUNIT2HTML_XSL="./reporter/xunit_to_html.xsl"
$SAXON9HE="./reporter/saxon9he.jar"

# Define docker images tags
$REPORTER_IMAGE_TAG="wapifuzz:reporter"

# Setting encofing for Python
$env:PYTHONIOENCODING = "UTF-8"


# Pilenine execution
Write-Host "--- Parsing openAPI documentation to JSON endpoints file ---"
& $DOTNET run -p ${PARSER_FOLDER} ${openapi} ${API_REQUESTS_JSON}
if(-Not ($?))
{
    Write-Host "Parsing of documentation failed! Fuzzing will not be started."
    exit 1
}

Write-Host "--- Starting fuzzing ---"
Write-Host "Creating virtual environment for Python 3"
& $PY $PIP3 install virtualenv
& $PY $PYTHON3 -m virtualenv env
.\env\Scripts\activate

Write-Host "Upgrade Python 3 pip (needed for crypto lib)"
pip install --upgrade pip

Write-Host "Installing specific dependencies"
pip install git+https://github.com/jtpereyda/boofuzz.git
pip install junit-xml
Write-Host "Starting fuzz testing"
python ./fuzzer/src/wapifuzz.py ${config} ${API_REQUESTS_JSON} ${JUNIT_TEST_REPORT} ${payloads} > $FUZZER_LOG
$FUZZER_ERROR_CODE=$LASTEXITCODE
if ($FUZZER_ERROR_CODE -eq 2)
{
    Write-Host "Fuzzing failed. HTML report will not be produced."
    exit 1
}
Write-Host "Ending fuzz testing"

Write-Host "Destroying virtual environment for Python 3"
deactivate
Remove-Item -LiteralPath ./env/ -Force -Recurse -ErrorAction SilentlyContinue
Write-Host "--- Ending fuzzing ---"

Write-Host "--- Starting generating HTML test report ---"
if (Get-Command $JAVA -errorAction SilentlyContinue)
{
    & $JAVA -jar ${SAXON9HE} -o:${HTML_TEST_REPORT} -s:${JUNIT_TEST_REPORT} -xsl:${XUNIT2HTML_XSL}
    if(-Not ($?))
    {
        Write-Host "HTML test report via installed Java binary cannot be produced. There was an error during parsing JUnit input file."
        exit 1
    }
}
elseif (Get-Command $DOCKER -errorAction SilentlyContinue)
{
    & $DOCKER build reporter -t ${REPORTER_IMAGE_TAG}
    if(-Not ($?))
    {
        Write-Host "HTML test report cannot be produced. Docker cannot build image."
        exit 1
    }
    & $DOCKER run ${REPORTER_IMAGE_TAG} > ${HTML_TEST_REPORT}
    if(-Not ($?))
    {
        Write-Host "HTML test report cannot be produced. Docker run failed."
        exit 1
    }
}
else
{
    Write-Host "HTML test report cannot be produced. Missing JRE or Docker binary. Need to provide at least one of them. You can specify their binary paths in the beggining of this script."
    exit 1
}
Write-Host "--- Ending generating HTML test report ---"

if ($FUZZER_ERROR_CODE -eq 1)
{
    Write-Host "There were some failures! Returning non-zero return value."
    exit 1
}
