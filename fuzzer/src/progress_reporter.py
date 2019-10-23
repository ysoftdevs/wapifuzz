import os
import threading
import sys
import datetime
from configuration_manager import ConfigurationManager

DID_FUZZING_STARTED_CHECKS_TIME_INTERVAL_IN_SECONDS = 5
HANGED_TIMEOUT = 120


def close_testing_and_kill_fuzzer(junit_logger, session):
    if is_fuzzing_hanged(session):
        junit_logger.close_test()
        os._exit(1)


def report_progress(session, junit_logger):
    if did_fuzzing_already_started(session) > 0:

        if is_fuzzing_hanged(session):
            message = create_hanged_message(session)
            print(message, file=sys.stderr)
            threading.Timer(HANGED_TIMEOUT, close_testing_and_kill_fuzzer, [junit_logger, session]).start()

        if is_fuzzing_still_in_progress(session):
            plan_another_report(session, junit_logger, ConfigurationManager.get_reporting_interval())

        message = create_report_message(session)
        print(message, file=sys.stderr)
    else:
        plan_another_report(session, junit_logger, DID_FUZZING_STARTED_CHECKS_TIME_INTERVAL_IN_SECONDS)


def plan_another_report(session, junit_logger, reporting_interval):
    threading.Timer(reporting_interval, report_progress, [session, junit_logger]).start()


def did_fuzzing_already_started(session):
    return session.total_num_mutations > 0


def is_fuzzing_hanged(session):
    hanged = is_fuzzing_hanged.previous_mutant_index == session.total_mutant_index
    is_fuzzing_hanged.previous_mutant_index = session.total_mutant_index
    return hanged


is_fuzzing_hanged.previous_mutant_index = -1


def is_fuzzing_still_in_progress(session):
    return session.total_num_mutations != session.total_mutant_index


def create_report_message(session):
    percentage = session.total_mutant_index / session.total_num_mutations * 100
    percentage = str(round(percentage, 2))

    message = str(datetime.datetime.now()) + ": "
    message += "Proceeded " + str(session.total_mutant_index) + " of "
    message += str(session.total_num_mutations) + " (" + percentage + "%) test cases"

    return message


def create_hanged_message(session):
    test_case_number = str(session.total_mutant_index)
    return "Fuzzing hangs on test case number: " + test_case_number + ". See log file for an error message."
