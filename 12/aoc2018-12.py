#!/usr/bin/python3
import copy

NO_PLANT = '.'
PLANT = '#'

plants = {}
rules = {}
with open('input.txt') as fh:
    for index, line in enumerate(fh):
        line = line.strip()
        if index == 0:  # First line with initial state
            line = line.replace("initial state: ", "")
            for plant_nr, plant in enumerate(line):
                plants[plant_nr] = plant
        elif index >= 2:  # Line with rule
            left_part = line[0:5]
            right_part = line[9]
            rules[left_part] = right_part
# Add leading and tailing "NO_PLANT"s for the case there is a pattern right in the first iteration at the begin or end
plants[min(plants) - 1] = NO_PLANT
plants[min(plants) - 1] = NO_PLANT
plants[max(plants) + 1] = NO_PLANT
plants[max(plants) + 1] = NO_PLANT

# PART ONE (code is not efficient enough for the second part)


def get_plant_substring(dictionary, min_index, max_index):
    """
    Get the consecutive string of chars with index in [min_index, max_index].
    For non existing indices, the "NO_PLANT" string is added.
    :param dictionary:
    :param min_index:
    :param max_index:
    :return:
    """
    string = ""
    for dict_index in range(min_index, max_index + 1):
        try:
            string += dictionary[dict_index]
        except KeyError:  # Not yet existing index
            string += NO_PLANT
    return string


nr_generations = 20
for generation in range(1, nr_generations + 1):
    new_plants = copy.deepcopy(plants)
    for plant_nr in range(min(plants.keys()), max(plants.keys()) + 1):
        plant_substring = get_plant_substring(plants, plant_nr - 2, plant_nr + 2)
        change = rules[plant_substring]  # Get applicable rule
        new_plants[plant_nr] = change
    print("{:0>3}: {}".format(generation, get_plant_substring(new_plants, min(new_plants.keys()), max(new_plants.keys()))))
    plants = new_plants
    min_plant = min(plants.keys())
    max_plant = max(plants.keys())
    if plants[min_plant] == PLANT or plants[min_plant + 1] == PLANT or plants[min_plant + 2] == PLANT or plants[min_plant + 3] == PLANT or plants[min_plant + 4] == PLANT:  # Add leading empty plants for this case
        for i in range(min_plant - 5, min_plant):
            plants[i] = NO_PLANT
    if plants[max_plant] == PLANT or plants[max_plant - 1] == PLANT or plants[max_plant - 2] == PLANT or plants[max_plant - 3] == PLANT or plants[max_plant - 4] == PLANT:
        for i in range(max_plant + 1, max_plant + 5 + 1):
            plants[i] = NO_PLANT
sum_part1 = 0
for plant in plants:
    if plants[plant] == PLANT:
        sum_part1 += plant
print("After {} generations, the sum of the numbers of all pots which contain a plant is {}.".format(nr_generations, sum_part1))
