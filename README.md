[![Build Status](https://travis-ci.com/ysoftdevs/wapifuzz.svg?branch=master)](https://travis-ci.com/ysoftdevs/wapifuzz)

# WapiFuzz - fully autonomous web APIs fuzzer
Fuzzing is popular testing technique for various error types detection. There are many fuzzing engines and fuzzers, which can help you with fuzzing itself. But there is currently no tool which can fully automate fuzzing just by providing API specification.

And that is why WapiFuzz was created. We believe that web API documentation is all that fuzzer needs to do his job. WapiFuzz can be easily deployed to almost any continuous integration (CI) service. It provides rich test reports to JUnit XML format.

## What does the WapiFuzz test?
Current version of WapiFuzz tests following parts of HTTP request to your API:
- HTTP header
- URI attributes of all documented requests
- JSON body primitive types of all documented HTTP body examples

## What types of vulnerabilities does WapiFuzz testing?
- Numeric strings (overflows, reserved words, ...)
- Command injection
- SQL injection
- Path traversal
- Special characters
- Unicode sequences
- XML / XPath attacks

## Requirements for your web API
You can automatically test your web API if it meets following criteria:
- Documented in OpenAPI 2 or OpenAPI 3
- Consumes and produces only `application/json` or `text/plain` content

If you have your API documented in other documentation formats, you can try use some convertor.
There are plenty convertors online. Some of theme are listed here: https://openapi.tools/.

Consuming JSON data is not mandatory requirement. If your API does not consumes JSON, WapiFuzz will still tests HTTP header and URI attributes processing of your server.

## Dependencies
- Python 3
- .NET Core runtime 2.1 and higher
- JRE or Docker
- PowerShell or Bash

## Usage
The only thing you need to do is create config file. You can find template in root of repository in `config_example.json` file. You can just modify this file and then pass it's path to runner script.

In config file you are able to specify following options:
- **fixed_url_attributes** -> if you want to set some attributes to static values
- **headers** -> headers which are sent by each request (useful for AUTH token insertion)
- **polling_interval** -> interval between checks for response (in seconds)
- **response_timeout** -> maximum amount of time waiting for response (in seconds)
- **reporting_interval** -> progress reporting interval (in seconds)
- **http_fuzzing** -> boolean value for enabling / disabling fuzzing of HTTP protocol
- **skipping_endpoints_keywords** [list of string keywords] -> endpoints containing any keyword in it from this list will be skipped (can be used for skipping auth/logout endpoints)
- **startup_command** -> startup command for your tested process / service, see more details in `procmon/README.md`
- **payloads_to_json_primitives_mapping** -> mapping of payloads folders to JSON primitives (see `config_example.json` for an example)
  - **boolean** -> array of folder names with payloads which will be used for JSON boolean primitive fuzzing
  - **number** -> array of folder names with payloads which will be used for JSON number primitive fuzzing
  - **string** -> array of folder names with payloads which will be used for JSON string primitive fuzzing
- **target** -> dictionary with following fields:
  - **hostname** -> victim hostname or IP address
  - **port** -> victim port
  - **ssl** -> boolean value, set to `true` if you want use SSL tcp connection, otherwise `false`

Great, WapiFuzz is now ready for fuzzing! Run it by following commands.
### Windows
Execute `run.ps1 -c config_file_path -openapi openapi_doc_file_path [-payloads custom_payloads_file_path]` script in PowerShell.

### Unix
Execute `run.sh config_file_path openapi_doc_file_path [custom_payloads_file_path]` command from Bash.

### Docker
You just need to run the container with following arguments:

`docker run -p {host_port}:{container_port} -v $(pwd):/usr/local/fuzzer/mnt/ starek4/wapifuzz:latest config.json sqta.yaml [custom_payloads.txt]`

where files `config.json`, `sqta.yaml` and `custom_payloads` needs to be stored in the working directory.
With parameter `-p` you also need to bind port number, which is used for communication with your web API, to the container.
So for example, if your API listen on the port 80, you can simply do `-p 80:80`.

#### Custom payloads file
As you can see in run script parameters, you may even specify your own payloads! Just create text file with your own testing strings (one on each line) and pass path to this file via run script parameters!


## Where I can find test reports?
After WapiFuzz finish, three main report files are generated. If you are using docker image just the way that is described above, you simply find these three files in your working directory.
If you are running WapiFuzz by run scripts, you can find these files in the following paths:

- JUnit File: `./reporter/results.junit.xml`
- HTML report: `./reporter/reports.html`
- Full text log: `./fuzzing.log`

### JUnit report
The first is the JUnit file (`./reporter/results.junit.xml`), which contains full test report and contains logs for failed tests. Almost every CI system provides a way how to present JUnit test reports in some human friendly way.

### HTML report
WapiFuzz also generates nicely formatted HTML test report, stored at `./reporter/reports.html`.

### Additional text logs
WapiFuzz informs you about overall progress at standard output. If you want complete tests logs even
for successfully finished test cases you can find it in log file (`./fuzzing.log`).
