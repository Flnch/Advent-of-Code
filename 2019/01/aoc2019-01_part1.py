#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3

sum = 0
with open("input.txt") as fh:
    for line in fh:
        sum += int(line) // 3 - 2
print("Result: {}".format(sum))
