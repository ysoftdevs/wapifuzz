API_REQUESTS_JSON=./parser/api.json
JUNIT_TEST_REPORT=./reporter/reports.junit.xml
HTML_TEST_REPORT=./reporter/reports.html
FUZZER_LOG=fuzzing.log

rm ${API_REQUESTS_JSON} ${FUZZER_LOG} ${JUNIT_TEST_REPORT} ${HTML_TEST_REPORT}
rm -rf ./fuzzer/boofuzz-results/
rm -rf ./boofuzz-results/
rm -rf ./env/
