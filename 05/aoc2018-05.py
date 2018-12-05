#!/usr/bin/python3
from string import ascii_lowercase

DUMMY = '_'


def next_right_position(string, old_pos):
    """
    Go to the next position to the right of "old_pos" that does not equal "DUMMY".
    :param old_pos:
    :param string:
    :return: New position or "None" if we are at the end of "string" or all characters to the right of "old_pos" equal "DUMMY"
    """
    if old_pos >= len(string) - 1:  # "old_pos" is already at the last position
        return None
    else:
        new_pos = old_pos + 1
        while string[new_pos] == DUMMY and new_pos < len(string) - 1:
            new_pos += 1
        if string[new_pos] == DUMMY:  # Every character up to the end of "string" equals "DUMMY"
            return None
        else:
            return new_pos


def next_left_position(string, old_pos):
    """
    Go to the next position to the left of "old_pos" that does not equal "DUMMY"
    :param string:
    :param old_pos:
    :return: New position or "None" if we are at the begin of "string" or all characters to the left of "old_pos" equal "DUMMY"
    """
    if old_pos <= 0:  # "old_pos" is already at the first position
        return None
    else:
        new_pos = old_pos - 1
        while string[new_pos] == DUMMY and new_pos > 0:
            new_pos -= 1
        if string[new_pos] == DUMMY:  # Every character up to the begin of "string" equals "DUMMY"
            return None
        else:
            return new_pos


def react_polymer(polymer):
    """
    React the "polymer", that is two adjacent letters that only differ in their case are removed.
    :param polymer:
    :return: Reacted polymer
    """
    polymer = list(polymer)  # Make a list of characters to allow easy modification of each position of the string
    print(''.join(polymer))
    l_pos = 0
    r_pos = 1
    while l_pos is not None and r_pos is not None and l_pos < len(polymer) - 1 and r_pos < len(polymer):  # Check positions and whether one position was set to "None"
        left = polymer[l_pos]
        right = polymer[r_pos]
        if ((left.islower() and right.isupper()) or (left.isupper() and right.islower())) and left.lower() == right.lower():  # Same type but opposite polarity
            polymer[l_pos] = DUMMY
            polymer[r_pos] = DUMMY
            new_l_pos = next_left_position(polymer, l_pos)
            r_pos = next_right_position(polymer, r_pos)
            if not new_l_pos:  # Going to the left was not possible
                new_l_pos = next_right_position(polymer, l_pos)
                r_pos = next_right_position(polymer, r_pos)  # Shift "r_pos" one further to the right (otherwise "l_pos == r_pos")
            l_pos = new_l_pos
        else:  # Simply move both positions to the right for further search
            l_pos = next_right_position(polymer, l_pos)
            r_pos = next_right_position(polymer, r_pos)
    print(''.join(polymer))
    cleaned_string = (''.join(polymer)).replace(DUMMY, '').strip()
    return cleaned_string


polymer = None
with open("input.txt") as fh:
    polymer = fh.readline()
# polymer = "dabAcCaCBAcCcaDA"  # Example from the assignment

# PART 1
print("========== PART 1 ==========")
part1 = react_polymer(polymer)
print("The cleaned string of length {} is:\n{}".format(len(part1), part1))

print("\n\n========== PART 2 ==========")
best_so_far = len(part1)
for letter_low in ascii_lowercase:
    letter_up = letter_low.upper()
    filtered_polymer = polymer.replace(letter_low, '')
    filtered_polymer = filtered_polymer.replace(letter_up, '')
    reacted_polymer = react_polymer(filtered_polymer)
    length = len(reacted_polymer)
    if length < best_so_far:
        best_so_far = length
part2 = best_so_far
print("\nThe length of the shortest polymer to produce is {}.".format(part2))
