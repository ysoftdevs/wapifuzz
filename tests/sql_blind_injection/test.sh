# Start server which does not send any response
python3 "$(dirname "${BASH_SOURCE[0]}")/web_and_sql_server.py" &
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

# Check logs, if there are tests with failure
cat fuzzing.log | grep "Timeout or closed connection"
IS_MATCH1=`echo $?`

cat ./reporter/reports.junit.xml | grep "Timeout or closed connection"
IS_MATCH2=`echo $?`

cat ./reporter/reports.html | grep "Timeout or closed connection"
IS_MATCH3=`echo $?`

# Kill server
kill -9 $SERVER_PID

if [ $IS_MATCH1 -eq 0 -a $IS_MATCH2 -eq 0 -a $IS_MATCH3 -eq 0 ] ; then
    exit 0
fi

exit 1
