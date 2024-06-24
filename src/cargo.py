from abc import ABC
import random

class Branch:
    def __init__(self):
        self.name = "ветка"
        self.size = random.randint(100,500)
class Leaf:
    def __init__(self):
        self.name = "листик"
        self.size = random.randint(100,500)