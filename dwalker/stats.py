# Forked from https://github.com/TelloSDK/Multi-Tello-Formation
# This fork hosted at https://github.com/scubyd/Multi-Tello-Formation to support Python 3
# Updated and tested with Python 3.7

from datetime import datetime


class Stats:
    def __init__(self, command, tello_id):
        self.command = command
        self.response = None
        self.id = tello_id

        self.start_time = datetime.now()
        self.end_time = None
        self.duration = None
        self.drone_ip = None

    def add_response(self, response, ip):
        if self.response is None:
            self.response = response
            self.end_time = datetime.now()
            self.duration = self.get_duration()
            self.drone_ip = ip

    def get_duration(self):
        diff = self.end_time - self.start_time
        return diff.total_seconds()

    def print_stats(self):
        print('id: %s' % self.id, end='')
        print('command: %s' % self.command, end='')
        print('response: %s' % self.response, end='')
        print('start time: %s' % self.start_time, end='')
        print('end_time: %s' % self.end_time, end='')
        print('duration: %s' % self.duration)

    def got_response(self):
        if self.response is None:
            return False
        else:
            return True

    def return_stats(self):
        stats_str = 'id: %s\n' % self.id
        stats_str += 'command: %s\n' % self.command
        stats_str += 'response: %s\n' % self.response
        stats_str += 'start time: %s\n' % self.start_time
        stats_str += 'end_time: %s\n' % self.end_time
        stats_str += 'duration: %s\n' % self.duration
        return stats_str
