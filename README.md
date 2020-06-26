# Tasktimer
A simple command line tool to track and manage time spent on various
tasks.

## Usage
Use the command `python tasktimer.py -h` to view help and usage
information.

Some example usage:
```
> python tasktimer.py create atask
> python tasktimer.py read atask
atask has been in progress for 0:00:00s
> python tasktimer.py start atask
> python tasktimer.py stop atask
atask has been in progress for 0:00:02.020019s
> python tasktimer.py list
atask   0:00:02.020019s
> python tasktimer.py reset atask
> python tasktimer.py read atask
atask has been in progress for 0:00:00s
> python tasktimer.py delete atask
```
