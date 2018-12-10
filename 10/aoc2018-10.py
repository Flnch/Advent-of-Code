#!/usr/bin/python3
import re
import numpy


class Point:
    def __init__(self, xpos, ypos, x_velocity, y_velocity):
        self.xpos = int(xpos)
        self.ypos = int(ypos)
        self.x_velocity = int(x_velocity)
        self.y_velocity = int(y_velocity)

    def move(self):
        """
        Move this point for one second
        :return:
        """
        self.xpos += self.x_velocity
        self.ypos += self.y_velocity


def print_points(list_of_points, min_x, max_x, min_y, max_y):
    """
    Print a list of points.
    :param list_of_points:
    :param min_x:
    :param max_x:
    :param min_y:
    :param max_y:
    :return:
    """
    def map_coordinate(min_value, coordinate):
        """
        Maps the single coordinate to a scale beginning with 0.
        :param min_value: Minimum value along this axis, of which the zero point needs to be redefined.
        :return: New coordinate value
        """
        return coordinate - min_value  # In fact, add "min_value" if it is negative and subtract it otherwise

    x_interval = abs(max_x - min_x) + 1  # Number of horizontal points
    y_interval = abs(max_y - min_y) + 1  # Number of vertical points
    array = numpy.chararray((y_interval, x_interval))
    array.fill('.')
    for point in list_of_points:
        x = map_coordinate(min_x, point.xpos)
        y = map_coordinate(min_y, point.ypos)
        array[y, x] = '#'
    for y in range(y_interval):
        for x in range(x_interval):
            print(array[y, x].decode('UTF-8'), end='')
        print()  # Newline


pattern = re.compile("""
position=<
\s*
(-?\d+)  # An optional leading minus and a number
,\s*
(-?\d+)
>[ ]velocity=<
\s*
(-?\d+)
,\s*
(-?\d+)
>
""", re.VERBOSE)

points = []
with open('input.txt') as fh:
    for line in fh:
        data = pattern.match(line).groups()
        point = Point(data[0], data[1], data[2], data[3])
        points.append(point)

smallest_x = 1000000
smallest_y = 1000000
greatest_x = -1000000
greatest_y = -1000000
x_margin = 100  # Margin where we want to print
y_margin = x_margin
for second in range(1, 100000):
    smallest_x = 1000000
    smallest_y = 1000000
    greatest_x = -1000000
    greatest_y = -1000000
    for point in points:
        # Update smallest / greatest values
        if point.xpos < smallest_x:
            smallest_x = point.xpos
        if point.xpos > greatest_x:
            greatest_x = point.xpos
        if point.ypos < smallest_y:
            smallest_y = point.ypos
        if point.ypos > greatest_y:
            greatest_y = point.ypos
        # Move point
        point.move()
    if abs(greatest_x - smallest_x) <= x_margin and abs(greatest_y - smallest_y) <= y_margin:  # Print field if we are in the defined margins
        print("Second {}:".format(second))
        print_points(points, smallest_x, greatest_x, smallest_y, greatest_y)  # After the correct print this call crashes the script
