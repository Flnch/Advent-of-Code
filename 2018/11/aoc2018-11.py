#!/usr/bin/python3
import numpy


def calc_power_level(x_coord, y_coord, grid_serial_number):
    rack_id = x_coord + 10
    power_level = rack_id * y_coord
    power_level += grid_serial_number
    power_level = power_level * rack_id
    power_level = power_level % 1000 // 100  # Keep only the hundreds digit
    power_level -= 5
    return power_level


grid_serial_number = 5719  # Puzzle input

# PART ONE
grid = numpy.empty((301, 301))  # Note for simplicity we create an array which is one unit greater to use indices beginning at 1
# Calculate all power levels
for x in range(1, 300):
    for y in range(1, 300):
        grid[y, x] = calc_power_level(x, y, grid_serial_number)

# Find maximum 3x3 power level square
largest_total_power = -1000000
largest_coord = (-1, -1)
for x in range(1, 298 + 1):  # Such that the square is entirely within the 300x300 grid
    for y in range(1, 298 + 1):
        total_power = grid[y:y + 3, x:x + 3].sum()
        if total_power > largest_total_power:
            largest_total_power = total_power
            largest_coord = (x, y)
print("The coordinate of the top-left fuel cell of the 3x3 square with the largest total power of {} is {}.".format(largest_total_power, largest_coord))

# PART TWO
largest_total_power = -1000000
largest_coord = (-1, -1)
size = -1
for x_upper_left in range(1, 301):
    print("x_upper_left: ", x_upper_left)  # To see programs progress
    for y_upper_left in range(1, 301):
        add_extra = 0  # Offset for looping over the diagonal
        while x_upper_left + add_extra <= 300 and y_upper_left + add_extra <= 300:  # Still valid coordinates of the 300x300 square (on the diagonal)
            x_lower_right = x_upper_left + add_extra
            y_lower_right = y_upper_left + add_extra
            width = x_lower_right - x_upper_left + 1
            height = y_lower_right - y_upper_left + 1
            total_power = grid[y_upper_left:y_upper_left + height, x_upper_left:x_upper_left + width].sum()
            if total_power > largest_total_power:
                largest_total_power = total_power
                largest_coord = (x_upper_left, y_upper_left)
                size = add_extra + 1
            add_extra += 1
print("The square with the largest total power of {} has identifier {},{},{}.".format(largest_total_power, largest_coord[0], largest_coord[1], size))

