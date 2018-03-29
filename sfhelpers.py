# -*- coding: utf-8 -*-

"""
Game functions for Superfarmer.
"""

import random
from time import sleep

victory_animal_types = ["R", "S", "P", "C", "H"]
dog_types = ["SD", "LD"]
animal_types = ["R", "S", "P", "C", "H", "SD", "LD"]
animal_values = {"R": 1, "S": 6, "P": 12, "C": 36, "H": 72, "SD": 6, "LD": 36}

exchange_table = """Press keys to exchange animals to rabbits and back.
Lowercase letters to exchange animals to rabbits.
Uppercase letters to exchange rabbits to animals.

A)  6 rabbits -> 1 sheep
S) 12 rabbits -> 1 pig
D) 36 rabbits -> 1 cow
F) 72 rabbits -> 1 horse
G)  6 rabbits -> 1 small dog
H) 36 rabbits -> 1 large dog

Press Enter when finished to roll dice.
"""

animal_names = {"R": "Rabbit",
                "S": "Sheep",
                "P": "Pig",
                "C": "Cow",
                "H": "Horse",
                "SD": "Small Dog",
                "LD": "Large Dog",
                "F": "Fox",
                "W": "Wolf"}


def get_animal_number_string(animal, number):
    name = animal_names[animal]
    if animal != "S":
        name += "s"
    return name + ": " + str(number)


red_die = ["R"] * 6 + ["S"] * 3 + ["P", "C", "W"]
yellow_die = ["R"] * 6 + ["S"] * 3 + ["P", "H", "F"]


def roll():
    "Returns a random animal from both dice."
    return (random.choice(red_die), random.choice(yellow_die))


class Player():
    """Represents each player of the game"""

    def __init__(self, name):
        self.name = name
        self.animals = {animal: 0 for animal in animal_types}

    def __repr__(self):
        return self.name.capitalize()

    def farm_state(self):
        output = list()
        output.append(self.name+'\'s farm:')
        if not any(self.animals.values()):
            output.append("No animals")
        for a in animal_types:
            if self.animals[a]:
                output.append(get_animal_number_string(a, self.animals[a]))
        return output

    def add_animals(self, roll):
        """Add animals to farm based on dice roll."""
        temp = {}
        for animal in [x for x in roll if x in victory_animal_types]:
            temp[animal] = temp[animal] + \
                1 if animal in temp else self.animals[animal] + 1
        for animal in temp:
            self.animals[animal] += temp[animal]//2

    def lose_animals(self, roll):
        """Remove animals from farm based on dice roll."""
        if "F" in roll:
            if self.animals["SD"] > 0:
                self.animals["SD"] -= 1
            else:
                self.animals["R"] = 0
        if "W" in roll:
            if self.animals["LD"] > 0:
                self.animals["LD"] -= 1
            else:
                for animal in animal_types:
                    if animal not in ("SD", "H"):
                        self.animals[animal] = 0

    def update_animals(self, roll):
        if "W" in roll or "F" in roll:
            self.lose_animals(roll)
        if any(a in roll for a in victory_animal_types):
            self.add_animals(roll)

    def check_victory_condition(self):
        """Returns True if the player owns every type of animal necessary to win."""
        return all(self.animals[a_type] > 0 for a_type in victory_animal_types)

    def buy_animal(self, animal):
        val = animal_values[animal]
        if self.animals["R"] >= val:
            self.animals["R"] -= val
            self.animals[animal] += 1

    def sell_animal(self, animal):
        val = animal_values[animal]
        if self.animals[animal] > 0:
            self.animals[animal] -= 1
            self.animals["R"] += val

    @property
    def total_value(self):
        """Total value (in rabbits) of all animals at a player's farm."""
        return sum(self.animals[a]*animal_values[a] for a in animal_types)
