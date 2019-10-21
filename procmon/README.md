# Process monitor
Process monitor is Python 2 script, which can monitor tested process.
This means, it should be running on testing target.
You can find process monitor script in this folder both for Windows and Unix systems.

Process monitor works by communication via port 26002, so all nodes between tested and testing device needs to have open this port.

## What is it good for?
Well, process monitor is used for the following benefits:
- Restarting tested application after failure
- Checks before and after each test if process is still running
- Starting tested application when it dies cause of testing payload
- Generating dump file for each application crash

## Installation
Windows process monitor needs some prerequisites. See installation instructions here:
https://boofuzz.readthedocs.io/en/latest/user/install.html#extras

## Running of script
Process monitor contains help with arguments description, so just enter `--help` argument and it will print a help for you.

Example command:
`python process_monitor_windows.py -p TestedApplication.exe`


## How to tell WapiFuzz that we want to monitor process?
If you want to use process monitor, just add starting command for your tested service / process into WapiFuzz configuration file. Example configuration key should look like this:
`"startup_command": ["python", "C:\\server\\httpd.py"]`

WapiFuzz then automatically connect with running process monitor script on tested system and will use its features.
