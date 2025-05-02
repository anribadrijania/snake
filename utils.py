import random
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # Set by PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def seeded_random_food(rows, cols, exclude):
    while True:
        pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))
        if pos not in exclude:
            return pos
