RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
NO_COLOR='\033[0m'

TEST_SCRIPTS=`find . -regex ".*\(test.sh\)"`
TEST_SCRIPTS_COUNT=`find . -regex ".*\(test.sh\)" | wc -l`

SUCCESSFULL=0
FAILED=0

TEST_LOG_FILE=e2e_tests.log

# Clear or create log file
> $TEST_LOG_FILE

echo "Founded ${TEST_SCRIPTS_COUNT} tests. Starting test session. Some tests may wait for some kind of timeout, so please be patient."
for SCRIPT in $TEST_SCRIPTS
do
    echo ${SCRIPT} >> $TEST_LOG_FILE
    printf "${ORANGE} Started testing: ${SCRIPT} ${NO_COLOR}\n"
    $SCRIPT >> $TEST_LOG_FILE 2>&1
    RET_VAL=$?
    if [ $RET_VAL -eq 0 ] ; then
        SUCCESSFULL=$((SUCCESSFULL+1))
        printf "${GREEN}  Test ${SCRIPT} was successfull.${NO_COLOR}\n"
    else
        FAILED=$((FAILED+1))
        printf "${RED}  Test ${SCRIPT} was NOT successfull.${NO_COLOR}\n"
    fi

    # Clean generated files
    cd ../
    make clean > /dev/null 2>&1
    cd - > /dev/null 2>&1

    # Make a newline
    echo ""
    echo "" >> $TEST_LOG_FILE
done

# Print summary
echo ""
echo "--- Summary ---"
echo "Failed: ${FAILED}"
echo "Successfull: ${SUCCESSFULL}"
echo "Total: ${TEST_SCRIPTS_COUNT}"
echo "Success rate: $((100*SUCCESSFULL/TEST_SCRIPTS_COUNT))%"

if [ $SUCCESSFULL -eq $TEST_SCRIPTS_COUNT ] ; then
    exit 0
else
    exit 1
fi
