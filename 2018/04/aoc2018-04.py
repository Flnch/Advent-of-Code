#!/usr/bin/python3

import re
from enum import Enum, auto
from functools import total_ordering

pattern_shift = re.compile(r"""
\[
(\d{4})
-
(\d{2})
-
(\d{2})
[ ]
(\d{2})
:
(\d{2})
\]
[^#]*   # Match anything besides '#'
[#]
(\d+)
\D*     # Match any non-digit character
""", re.VERBOSE)

pattern_falls = re.compile(r"""
\[
(\d{4})
-
(\d{2})
-
(\d{2})
[ ]
(\d{2})
:
(\d{2})
\]
[ ]
falls
[ ]
asleep
\D*     # Match any non-digit character
""", re.VERBOSE)

pattern_wakes = re.compile(r"""
\[
(\d{4})
-
(\d{2})
-
(\d{2})
[ ]
(\d{2})
:
(\d{2})
\]
[ ]
wakes
[ ]
up
\D*     # Match any non-digit character
""", re.VERBOSE)


class Action(Enum):
    SHIFT_BEGIN = auto()
    FALLS_ASLEEP = auto()
    WAKES_UP = auto()


@total_ordering
class Event:
    def __init__(self, line):
        action, match = self.parse_line(line)
        match_groups = match.groups()
        self.action = action
        # Set shared variables (date stamp)
        self.year = int(match_groups[0])
        self.month = int(match_groups[1])
        self.day = int(match_groups[2])
        self.hour = int(match_groups[3])
        self.minute = int(match_groups[4])
        # Set special variables (only case is guard id)
        if action == Action.SHIFT_BEGIN:
            self.guard_id = match_groups[5]

    def __str__(self):
        string = "[{:04d}-{:02d}-{:02d} {:02d}:{:02d}]".format(self.year, self.month, self.day, self.hour, self.minute)
        if self.action == Action.SHIFT_BEGIN:
            string += " Guard #{} begins shift".format(self.guard_id)
        elif self.action == Action.FALLS_ASLEEP:
            string += " falls asleep"
        elif self.action == Action.WAKES_UP:
            string += " wakes up"
        return string

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):  # Test for x < y, based on date stamp
        if not isinstance(other, Event):
            return NotImplemented
        else:  # Check all True cases, default to False
            if self.year < other.year:
                return True
            elif self.year == other.year:
                if self.month < other.month:
                    return True
                elif self.month == other.month:
                    if self.day < other.day:
                        return True
                    elif self.day == other.day:
                        if self.hour < other.hour:
                            return True
                        elif self.hour == other.hour:
                            if self.minute < other.minute:
                                return True
        return False

    def __eq__(self, other):  # Test for x == y, based on date stamp
        if not isinstance(other, Event):
            return NotImplemented
        else:
            return self.year == other.year and self.month == other.month and self.day == other.day and self.hour == other.hour and self.minute == other.minute

    @staticmethod
    def parse_line(line):
        match = pattern_shift.match(line)
        action = Action.SHIFT_BEGIN
        if not match:
            match = pattern_falls.match(line)
            action = Action.FALLS_ASLEEP
        if not match:
            match = pattern_wakes.match(line)
            action = Action.WAKES_UP
        if not match:
            raise ValueError("Input line \"{}\" does not match any pattern.".format(line))
        return action, match


events = []
with open('input.txt') as fh:
    for line in fh:
        events.append(Event(line))
events.sort()
print("Events in sorted order:\n")
for event in events:
    print(event)

guards_asleep_time = {}  # Maps guard ids to their cumulative asleep time
current_guard_id = None
current_sleep_time = 0
falls_asleep_minute = None
guard_minutes = {}  # Dictionary for each guard containing a dictionary for each minute
for event in events:
    if event.action == Action.SHIFT_BEGIN and current_guard_id:  # Do not set in "guards_asleep_time" in first iteration
        guards_asleep_time[current_guard_id] = guards_asleep_time.get(current_guard_id, 0) + current_sleep_time
    if event.action == Action.SHIFT_BEGIN:  # Reset variables
        current_guard_id = event.guard_id
        current_sleep_time = 0
    elif event.action == Action.FALLS_ASLEEP:
        falls_asleep_minute = event.minute
    elif event.action == Action.WAKES_UP:
        current_sleep_time += event.minute - 1 - falls_asleep_minute
        for minute in range(falls_asleep_minute, event.minute):
            minutes = guard_minutes.get(current_guard_id, {})
            minutes[minute] = minutes.get(minute, 0) + 1
            guard_minutes[current_guard_id] = minutes

max_key_asleep_time = max(guards_asleep_time, key=lambda i: guards_asleep_time[i])
max_value_asleep_time = guards_asleep_time[max_key_asleep_time]
max_key_1487 = max(guard_minutes[max_key_asleep_time], key=lambda i: guard_minutes[max_key_asleep_time][i])
max_value_1487 = guard_minutes[max_key_asleep_time][max_key_1487]
print("\nThe most minutes asleep has guard #{0} with {1} minutes. He spents minute {4} asleep most. {0}*{4} = {3}".format(max_key_asleep_time, max_value_asleep_time, max_value_1487, int(max_key_asleep_time) * max_key_1487, max_key_1487))

guard_id_part2 = None
minute_part2 = -1
max_value_part2 = -1
for guard_id in guard_minutes:
    minutes_guard_id = guard_minutes[guard_id]
    max_key = max(minutes_guard_id, key=lambda i: minutes_guard_id[i])
    max_value = minutes_guard_id[max_key]
    if max_value > max_value_part2:
        guard_id_part2 = guard_id
        minute_part2 = max_key
        max_value_part2 = max_value
print("Of all guards, the guard most frequently asleep on the same minute is guard #{0} on minute {1} with {3} times asleep. {0}*{1} = {2}".format(guard_id_part2, minute_part2, int(guard_id_part2) * minute_part2, max_value_part2))
