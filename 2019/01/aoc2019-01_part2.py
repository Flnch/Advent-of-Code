#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3

def calcFuelForModule(mass):
    """Calculate the needed fuel for a module of mass `mass`, the resulting fuel needed for the fuel(s) and return the total fuel sum."""
    totalFuel = 0
    mass = int(mass)
    nextFuel = mass // 3 - 2
    while nextFuel > 0:
        totalFuel += nextFuel
        nextFuel = nextFuel // 3 - 2
    return totalFuel

sum = 0
with open("input.txt") as fh:
    for line in fh: # A `line` corresponds to the mass of one module
        sum += calcFuelForModule(line)
print("Result: {}".format(sum))
