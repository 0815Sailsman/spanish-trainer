import math
import random


def crash():
    p = math.pi
    while True:
        print(str(p))
        p = p * random.randint(1, 100)
        p = p / random.randint(1, 100)

crash()