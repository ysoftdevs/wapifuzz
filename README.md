[![Build Status](https://travis-ci.com/ysoftdevs/wapifuzz.svg?branch=master)](https://travis-ci.com/ysoftdevs/wapifuzz)

# WapiFuzz - fully autonomous web APIs fuzzer
Fuzzing is a popular testing technique for various error types detection. There are many fuzzing engines and fuzzers which can help people with fuzzing itself. However, there is not currently a tool that can fully automate fuzzing just by providing API specification.

And that is a reason why WapiFuzz was created. We believe that web API documentation is all that fuzzer needs to do his job. WapiFuzz can be easily deployed to almost any continuous integration (CI) service. It is based on popular [Boofuzz](https://github.com/jtpereyda/boofuzz) fuzzer and provides test reports to JUnit XML format.

## What does the WapiFuzz test?
WapiFuzz can find vulnerabilities in following parts of the HTTP request:
- HTTP header
- Path and query attributes
- JSON body primitive types

All requests are automatically generated from provided OpenAPI documentation.

## What types of vulnerabilities does WapiFuzz test?
- Numeric strings (overflows, reserved words, etc.)
- Command injection
- SQL injection
- Path traversal
- Special characters
- Unicode sequences
- XML / XPath attacks

## Requirements for your web API
You can automatically test your web API if it meets the following criteria:
- Documented in OpenAPI 2 or OpenAPI 3
- Consumes and produces only `application/json` or `text/plain` content

If you have your API documented in other documentation formats, you can try to use some converters. There are plenty of converters online and the most common ones are listed here: https://openapi.tools/.

Consuming JSON data is not mandatory a requirement. If your API does not consume JSON, WapiFuzz will still test HTTP header and URI attributes processing of your server.
The fuzzing of the HTTP body part will be limited due to unsupported content format.

## Dependencies
- Python 3 with pip
- .NET Core 2.1
- JRE or Docker
- PowerShell or Bash

## Usage
The only thing you need to do is to create a WapiFuzz config file. You can find a template in the root of the repository in `config_example.json` file. You can just modify this file and then pass its path to the runner script.

You are able to specify the following options in the config file:
- **fixed_url_attributes** -> if you want to set some URL attributes to the static values
- **headers** -> the headers which are sent by each request (useful for an AUTH token insertion)
- **receive_timeout** -> the maximum amount of time waiting for a response (in seconds)
- **reporting_interval** -> progress reporting interval (in seconds)
- **http_fuzzing** -> enabling/disabling fuzzing of a pure HTTP protocol
- **skipping_endpoints_keywords** [list of keywords] -> if a keyword is in some endpoint, this endpoint will be skipped (can be used for skipping auth/logout endpoints)
- **startup_command** (only needed if you want to use process monitor) -> startup command for your tested process / service, see more details in `procmon/README.md`
- **are_non_required_attributes_in_requests** -> set to true, if you want non-required attributes to be part of URL
- **payloads_to_json_primitives_mapping** -> mapping of payload folders to JSON primitives
  - **boolean** -> an array of folder names with payloads which will be used for JSON boolean fuzzing
  - **number** -> an array of folder names with payloads which will be used for JSON number fuzzing
  - **string** -> an array of folder names with payloads which will be used for JSON string fuzzing
- **target** -> information about the tested application
  - **hostname** -> victim hostname or IP address
  - **port** -> victim port
  - **ssl** -> set to `true` for SSL TCP connections, otherwise `false`

Great, WapiFuzz is now ready for fuzzing! Run it by following commands.
### Windows
Execute `run.ps1 -c config_file_path -openapi openapi_doc_file_path [-payloads custom_payloads_file_path]` script in PowerShell.

### Unix
Execute `run.sh config_file_path openapi_doc_file_path [custom_payloads_file_path]` command from Bash.

### Docker
You just need to run the container with the following arguments:

`docker run -p {host_port}:{container_port} -v $(pwd):/usr/local/fuzzer/mnt/ starek4/wapifuzz:latest config.json sqta.yaml [custom_payloads.txt]`

where files `config.json`, `sqta.yaml` and `custom_payloads.txt` need to be stored in the working directory.
You also need to bind port number with the parameter `-p`, which is used for communication with your web API, to the container.
So for example, if your API listens on the port 80, you can simply do `-p 80:80`.

#### Custom payloads file
As you can see in the run script parameters, you can specify your payloads! Just create a text file with your strings (every string should have a separate line) and pass the path to this file via the run script parameters. They will be automatically added to every fuzzed part of the request.


## Where can I find test reports?
When WapiFuzz completes its run, three main report files are generated. If you are using a docker image equally as it is described above, you simply find these three files in your working directory. If you are running WapiFuzz by run scripts, you can find these files in the following paths:

- JUnit File: `./reporter/results.junit.xml`
- HTML report: `./reporter/reports.html`
- Full text log: `./fuzzing.log`

### JUnit report
The first report file is the JUnit file (`./reporter/results.junit.xml`), which contains full test report and logs for failed tests. Almost every CI system provides a way how to present JUnit test reports in a human friendly way.

### HTML report
WapiFuzz also generates nicely formatted HTML test report stored at `./reporter/reports.html`.

### Full text log
Detailed text log with all the information help you to understand what happened during the fuzzing.
