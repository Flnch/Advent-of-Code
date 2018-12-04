#!/usr/bin/python3

import re


class Claim:
    def __init__(self, nr, left_margin, top_margin, width, height):
        self.overlaps = False  # Indicating whether this "Claim" overlaps with at least one other "Claim".
        self.id = nr
        self.left_margin = left_margin
        self.top_margin = top_margin
        self.width = width
        self.height = height

    def is_in_square_inch(self, xpos, ypos):
        """
        Checks whether the single square inch is contained in this claim.
        :param xpos: Horizontal position, counted beginning at 0
        :param ypos: Vertical position, counted beginning at 0. The fixation point is the upper left corner.
        :return: Truth value
        """
        contained_horizontal = self.left_margin <= xpos <= self.left_margin + self.width - 1
        contained_vertical = self.top_margin <= ypos <= self.top_margin + self.height - 1
        return contained_horizontal and contained_vertical


claims = []
pattern = re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
match = pattern.match(r"#1 @ 257,829: 10x23")

with open('input.txt') as fh:
    for line in fh:
        match_groups = pattern.match(line).groups()
        new_case = Claim(int(match_groups[0]), int(match_groups[1]), int(match_groups[2]), int(match_groups[3]), int(match_groups[4]))
        claims.append(new_case)

# PART 1
# I think a more efficient way would be to go through all claims and their covered positions.

count = 0
for i in range(1001):
    print(i)
    for j in range(1001):
        local_count = 0
        for claim in claims:
            if claim.is_in_square_inch(i, j):
                local_count += 1
                if local_count >= 2:
                    count += 1
                    break
print("Count: {}".format(count))

# PART 2

for i in range(1001):
    print(i)
    for j in range(1001):
        first_overlapping_claim = None
        for claim in claims:
            if claim.is_in_square_inch(i, j):
                if not first_overlapping_claim:  # The first claim lying in this square inch
                    first_overlapping_claim = claim
                else:  # We have an overlap, e.g. there was already one claim also covering this square inch
                    first_overlapping_claim.overlaps = True
                    claim.overlaps = True
for claim in claims:
    if not claim.overlaps:
        print("The claim not overlapping at all has the id {}.".format(claim.id))
