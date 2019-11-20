# Process monitor
Process monitor is optional component of Boofuzz library.
It is a Python 2 script, which can monitor tested process.
This means, it should be running on testing target.
You can find process monitor script in this folder both for Windows and Unix systems.

Process monitor works by communication via port 26002, so all nodes between tested and testing device needs to have open this port.

## What is it good for?
- Restarting tested application after vulberability was triggered
- Additional checks before and after each test if tested process is still running
- Starting tested application when it dies

## Installation
Windows process monitor needs some prerequisites. See official installation instructions here:
https://boofuzz.readthedocs.io/en/latest/user/install.html#extras

## Running of script
Process monitor contains help with arguments description, so just enter `--help` argument and it will print a help for you.

Example command:
`python process_monitor_windows.py -p TestedApplication.exe`


## How to tell WapiFuzz that we want to use process monitor?
If you want to use process monitor and it is running on tested system, just add starting command for your tested service / process into WapiFuzz configuration file. Example configuration key may look like this:
`"startup_command": ["python", "C:\\server\\httpd.py"]`

WapiFuzz then automatically connects with running process monitor script on tested system and will use its features.
