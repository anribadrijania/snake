import random

def seeded_random_food(rows, cols, exclude):
    while True:
        pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))
        if pos not in exclude:
            return pos
