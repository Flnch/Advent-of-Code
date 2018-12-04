#!/usr/bin/python3

from string import  ascii_lowercase

lines = []
with open("input.txt") as filehandler:
    for line in filehandler:
        lines.append(line[:len(line) - 1])

# PART ONE

count_two_of_any_letter = 0
count_three_of_any_letter = 0

for line in lines:
    found_exactly_two = False
    found_exactly_three = False
    letter_frequencies = {}
    for letter in ascii_lowercase:  # Initialize all letters with 0
        letter_frequencies[letter] = 0
    for letter in line:  # Count actual letters
        letter_frequencies[letter] += 1
    # print(letter_frequencies)
    for letter in letter_frequencies:  # Search for exactly two or three
        if letter_frequencies[letter] == 2:
            found_exactly_two = True
        if letter_frequencies[letter] == 3:
            found_exactly_three = True
    if found_exactly_two:
        count_two_of_any_letter += 1
    if found_exactly_three:
        count_three_of_any_letter += 1

print("Count two: {}\nCount three: {}\n{} * {} = {}".format(count_two_of_any_letter, count_three_of_any_letter, count_two_of_any_letter, count_three_of_any_letter, count_two_of_any_letter * count_three_of_any_letter))

# PART TWO

for index, line in enumerate(lines):
    for compare_line in lines[index + 1:]:
        found_one_different_char = False
        differ_pos = None
        for char_index, char in enumerate(line):
            if char != compare_line[char_index]:
                if not found_one_different_char:
                    found_one_different_char = True
                    differ_pos = char_index
                else:  # Found a second char that differs
                    found_one_different_char = False
                    break
        if found_one_different_char:
            print("Line \"{}\" and \"{}\" differ only by one letter at the same position. The common letters are {}.".format(line, compare_line, line[:differ_pos] + line[differ_pos + 1:]))
