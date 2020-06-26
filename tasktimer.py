"""
Track and manage time spent on tasks.
"""

import argparse
import datetime
import pickle
import time
from os import path

FILENAME = 'tasks.pickle'


class Task:
    """Store and manage information about a particular task."""
    def __init__(self, task_name):
        self.task_name = task_name
        self._time_start = None
        self._elapsed_time = datetime.timedelta(seconds=0)
        self._running = False

    def start(self):
        """Start tracking time."""
        self._time_start = time.time()
        self._running = True

    def stop(self):
        """Stop tracking time."""
        if self._running:
            self.get_time()
            self._running = False

    def get_time(self):
        """Return the elapsed time."""
        if self._running:
            self._elapsed_time += datetime.timedelta(
                seconds=time.time() - self._time_start)
        return self._elapsed_time

    def reset(self):
        """Reset the elapsed time."""
        self._time_start = None
        self._elapsed_time = datetime.timedelta(seconds=0)
        self._running = False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A tool to record and manage time spent on tasks.')
    subparsers = parser.add_subparsers(dest='command')
    task_commands = {
        'create' : 'Create a new task.',
        'read' : 'Read the elapsed time of a task.',
        'start' : 'Start tracking time on a task.',
        'stop' : 'Stop tracking time on a task.',
        'reset' : 'Reset elapsed time on a task.',
        'delete' : 'Delete a task.'
    }
    # Add task commands
    for (command, help_str) in task_commands.items():
        subparser = subparsers.add_parser(
            command, help=help_str)
        subparser.add_argument('task')
    subparsers.add_parser(
        'list', help='List all tasks.')
    args = parser.parse_args()

    # Import list of Tasks from file
    if path.exists(FILENAME):
        with open(FILENAME, 'rb') as f_in:
            tasks = pickle.load(f_in)
    else:
        tasks = {}

    # Execute command
    if args.command == 'create':
        if args.task in tasks:
            print('ERROR: %s already exists' % args.task)
        tasks[args.task] = Task(args.task)
    elif args.command == 'start':
        try:
            tasks[args.task].start()
        except KeyError:
            print('ERROR: %s does not exist' % args.task)
    elif args.command == 'stop':
        try:
            tasks[args.task].stop()
            print(
                '%s has been in progress for %ss' %
                (args.task, tasks[args.task].get_time()))
        except KeyError:
            print('ERROR: %s does not exist' % args.task)
    elif args.command == 'reset':
        try:
            tasks[args.task].reset()
        except KeyError:
            print('ERROR: %s does not exist' % args.task)
    elif args.command == 'delete':
        try:
            del tasks[args.task]
        except KeyError:
            print('ERROR: %s does not exist' % args.task)
    elif args.command == 'list':
        for task in tasks:
            print('%s\t%s' % (task, tasks[task].get_time()))
    else:
        try:
            print(
                '%s has been in progress for %ss' %
                (args.task, tasks[args.task].get_time()))
        except KeyError:
            print('ERROR: %s does not exist' % args.task)

    # Export list of Tasks to file
    with open(FILENAME, 'wb') as f_out:
        pickle.dump(tasks, f_out, pickle.HIGHEST_PROTOCOL)
