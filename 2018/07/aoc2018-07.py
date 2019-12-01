#!/usr/bin/python3
import re
from string import ascii_uppercase


pattern = re.compile(r"""
Step[ ]
([A-Z])
[ ]must[ ]be[ ]finished[ ]before[ ]step[ ]
([A-Z])
[ ]can[ ]begin.
""", re.VERBOSE)

prerequisites = {}
for letter in ascii_uppercase:  # Assume all letters are contained in our input
    prerequisites[letter] = []
with open('input.txt') as fh:
    for line in fh:
        line = line.strip()
        (condition, step) = pattern.match(line).groups()
        old_list = prerequisites.get(step, [])
        old_list.append(condition)
        prerequisites[step] = old_list

# PART 1


def remove_prerequisite(prerequisites, step_to_delete):
    """
    Remove "step" from all conditions in "prerequisites".
    :param step_to_delete:
    :param prerequisites:
    """
    for step in prerequisites:
        old_list = prerequisites[step]
        try:
            old_list.remove(step_to_delete)
        except ValueError:  # The "step_to_delete" was no element of the list
            pass
        prerequisites[step] = old_list


# part1 = ""
# already_processed = []  # List of already processed steps
# ready = False
# while not ready:
#     found_one = False  # Whether we found a still not processed step
#     for step in sorted(prerequisites.keys()):  # Search for step with no prerequisites
#         condition = prerequisites[step]
#         if not condition and step not in already_processed:  # Empty list and step not already processed
#             part1 += step
#             already_processed.append(step)
#             remove_prerequisite(prerequisites, step)
#             found_one = True
#             break
#     if not found_one:  # There is nothing left to process
#         ready = True
# print("Part 1 solution: {}".format(part1))

# PART 2


def compute_working_time(letter):
    """
    Computes the working time for a uppercase letter.
    :param letter:
    :return: Working time
    """
    return ord(letter) - 4  # Calculate using ASCII index


def work_one_second(workers, worker_works_at, prerequisites):
    """
    Every non-idle worker works one second.
    If one worker finishes his work, this step is removed from the "prerequisites".
    :param prerequisites:
    :param worker_works_at:
    :param workers:
    :return: Whether some worker finished his work during this one second
    """
    finished_some_work = False
    for worker in workers:
        if workers[worker] > 0:
            workers[worker] -= 1
            if workers[worker] <= 0:  # This last second of work finished the workers work
                remove_prerequisite(prerequisites, worker_works_at[worker])
                finished_some_work = True
    return finished_some_work


def wait_for_free_worker(workers, worker_works_at, prerequisites):
    """
    Wait until at least one worker is free.
    :param prerequisites:
    :param worker_works_at:
    :param workers:
    :return: New workers list and number of second(s) we needed to wait
    """
    waiting_time = 0
    while not (workers[0] <= 0 or workers[1] <= 0 or workers[2] <= 0 or workers[3] <= 0):
        waiting_time += 1
        work_one_second(workers, worker_works_at, prerequisites)
    return workers, waiting_time


def begin_work(workers, work_seconds, worker_works_at, step):
    """
    Set a free worker to work that takes "work_seconds".
    Assign him the work "step".
    Before calling it is assumed that one worker is free!
    :param step:
    :param worker_works_at:
    :param work_seconds:
    :param workers:
    :return:
    """
    for worker in workers:
        if workers[worker] <= 0:
            workers[worker] = work_seconds
            worker_works_at[worker] = step
            break


def workers_busy(workers):
    """
    Determines whether at least one worker is busy.
    :param workers:
    :return:
    """
    for worker in workers:
        if workers[worker] > 0:
            return True
    return False


def nr_of_free_workers(workers):
    """
    Determines the number of free workers.
    :param workers:
    :return: Number of free / available workers
    """
    nr = 0
    for worker in workers:
        if workers[worker] <= 0:
            nr += 1
    return nr


workers = {0: 0, 1: 0, 2: 0, 3: 0}  # Four workers, each 0 seconds of work left
worker_works_at = {}  # Mapping worker to step he processes
second = 0  # Time during the next step
already_processed = []  # List of already processed steps
ready = False
while not ready or workers_busy(workers):
    found_one = False  # Whether we found a still not processed step
    workers, waiting_time = wait_for_free_worker(workers, worker_works_at, prerequisites)
    second += waiting_time
    for _ in range(nr_of_free_workers(workers)):  # Search for work for all free workers
        for step in sorted(prerequisites.keys()):  # Search for step with no prerequisites
            condition = prerequisites[step]
            if not condition and step not in already_processed:  # Empty list (no more precondition for this step) and step not already processed
                already_processed.append(step)
                begin_work(workers, compute_working_time(step), worker_works_at, step)
                found_one = True
                break
    some_worker_finished_work = work_one_second(workers, worker_works_at, prerequisites)
    second += 1
    if not found_one and not some_worker_finished_work:  # There is nothing left to process and no worker finished his work during the last iteration
        ready = True
    else:
        ready = False
print("Part 2 solution: {}".format(second - 1))  # Subtract 1 because "second" indicates the time of the next iteration that would happen

