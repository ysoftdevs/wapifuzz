FOLDER=$1
MATCH_MESSAGE=$2

# Start server
python3 ./httpd.py "${FOLDER}" &
SERVER_PID=`echo $!`

function trap_sigint()
{
    kill -9 $SERVER_PID
    exit 2
}

trap "trap_sigint" 2

cd ../

# Run fuzzer
./run.sh ./tests/localhost_config.json ./tests/documentation.yaml

# Check logs, if there are tests with failures
cat fuzzing.log | grep "${MATCH_MESSAGE}"
IS_MATCH1=`echo $?`

cat ./reporter/reports.junit.xml | grep "${MATCH_MESSAGE}"
IS_MATCH2=`echo $?`

cat ./reporter/reports.html | grep "${MATCH_MESSAGE}"
IS_MATCH3=`echo $?`

# Kill server
kill -9 $SERVER_PID

if [ $IS_MATCH1 -eq 0 -a $IS_MATCH2 -eq 0 -a $IS_MATCH3 -eq 0 ] ; then
    exit 0
fi

exit 1
