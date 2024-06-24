from mushroom import Mushroom
class Anthill:
    def __init__(self,tree):
        self.list_tree = []
        self.x = 1350
        self.y = 500
        self.size = 200
        self.list_room = []
        self.list_ants = []
        self.list_larva = []
        self.list_male_ant = []
        self.count_eat_larva = 0
        self.list_worker_ants = []
        self.list_worker_anthill = []
        self.list_Leaf = []
        self.count_leaf = 0
        self.mushroom = Mushroom()
        self.queen = 0
        self.list_death = []
        self.list_branch = []
        self.tree = tree

    def count_Leaf(self):
        sum = 0
        for i in self.list_Leaf:
            sum += i.size
        return sum


    def update(self):
        pass


