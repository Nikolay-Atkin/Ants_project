import random


class Mushroom:
    def __init__(self):
        self.size = random.randint(1000,2000)
        self.list_leaf = []

    def grow(self):
        if len(self.list_leaf) != 0:
            self.size += self.list_leaf[0].size // 2
            self.list_leaf.pop(0)
            print("запас гриба" + str(self.size))

    def update(self):
        ...