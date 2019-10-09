cd ../

# Run fuzzer
./run.sh ./tests/localhost_config.json ./tests/documentation.yaml 2>&1 | grep "Fuzzing hangs on test case number: 1. See log file for an error message."
RET_VAL=`echo $?`

if [ $RET_VAL -eq 0 ] ; then
    exit 0
fi

exit 1
