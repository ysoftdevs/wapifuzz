# Process monitor
The process monitor is an optional component of the Boofuzz library.
It is a Python 2 script, which can monitor the tested process.
This means the script is run on the testing target system.
You can find process monitor script in this folder for both Windows and Unix systems.

Process monitor works by communication via port 26002, therefore all nodes between tested and testing systems need to have opened this port.

## What is it good for?
- Restarting tested application after the vulnerability was triggered
- Additional checks happening before and after each test to confirm the appropriate tested process is still running
- Starting tested application when it dies

## Installation
For the Windows platform, two prerequisites need to be installed before running process monitor.
See official installation instructions here:
https://boofuzz.readthedocs.io/en/latest/user/install.html#extras

## Running of a script
Process monitor contains help with arguments description, thus just type `--help` as an argument and it will print help for you.

Example command:
`python process_monitor_windows.py -p TestedApplication.exe`


## How to connect WapiFuzz with process monitor?
If you want to connect WapiFuzz with process monitor and process monitor has been already running on a tested system, just add starting command for your tested service/process into the WapiFuzz configuration file. Example configuration key can look like this:
`"startup_command": ["python", "C:\\server\\httpd.py"]`

WapiFuzz then automatically connects with the running process monitor script on the tested system and it will use its features.
