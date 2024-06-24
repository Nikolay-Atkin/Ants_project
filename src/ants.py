from abc import ABC
from trees import Tree
from cargo import Leaf,Branch
import random


class Ant(ABC):
    def __init__(self, anthill):
        self.point = "anthill"
        self.anthill = anthill
        self.alive = 1
        self.condition = 1
        self.size = 0
        self.age = 0
        self.x = anthill.x
        self.y = anthill.y
        self.x_ = anthill.x
        self.y_ = anthill.y
        self.x_home = self.anthill.x
        self.y_home = self.anthill.y


    def eat(self):
        if self.anthill.mushroom.size > 500:
            if self.anthill.mushroom.size >= 1:
                self.anthill.mushroom.size -= 1
        else:
            self.death()

    def death(self):
        self.anthill.list_death.append(Ant_death(self.x,self.y,self.size))
        print("муравей погиб")

        if self in self.anthill.list_worker_ants:
            self.anthill.list_worker_ants.remove(self)
        if self in self.anthill.list_ants:
            self.anthill.list_ants.remove(self)
        if self in self.anthill.list_worker_anthill:
            self.anthill.list_worker_anthill.remove(self)
        if self in self.anthill.list_male_ant:
            self.anthill.list_male_ant.remove(self)


    def update(self):
        pass

    def move(self):
        pass

    def go_Home(self):
        if self.x_home < self.x:
            move = -1
        else:
            move = 1
        if self.x_home != self.x:
            self.x += move
            self.y = self.y_ + (self.x - self.x_)*(self.y_home - self.y_) / (self.x_home - self.x_)

        if self.x == self.x_home:
            print("муравей номер ")
            self.x_ = self.x
            self.y_ = self.y


class Queen(Ant):
    def __init__(self, anthill):
        super().__init__(anthill)
        self.breed = False

    def eat(self):
        if self.anthill.mushroom.size >= 30:
            self.starvation = False
        self.anthill.mushroom.size -= 30


    def lay_an_egg(self):
        if self.breed == True:
            k = random.randint(5,20)
            for i in range(k):
                self.anthill.list_larva.append(Larva(self.anthill))
            self.breed = False


    def update(self):
        self.age += 1

class Soldier(Ant):
    def __init__(self, anthill):
        super().__init__(anthill)

    def update(self):
        self.age += 1

class Worker(Ant):
    def __init__(self, anthill, number,tree):
        super().__init__(anthill)
        self.size = 1
        self.number = number
        self.cargo = None
        self.x_home = self.anthill.x
        self.y_home = self.anthill.y
        self.tree = tree

    def append_leaf(self):
        self.anthill.mushroom.list_leaf.append(self.anthill.list_Leaf[0])


    def grow_mushroom(self):
        if len(self.anthill.list_Leaf) > 0:
            self.append_leaf()
            self.anthill.list_Leaf.pop(0)
            self.anthill.mushroom.grow()

    def build_an_anthill(self):
        if len(self.anthill.list_branch) > 0 and self.anthill.size < 1001:
            self.anthill.size += 1
            self.anthill.list_branch.pop(0)

    def collect_leaves(self):
        self.cargo = Leaf()

    def collect_branch(self):
        self.cargo = Branch()

    def go_to_tree(self):
        k = random.randint(1,2)
        if self.anthill.size == 1000:
            k = 1
        x_tree = self.tree.x+150
        y_tree = self.tree.y+150

        self.x_ = self.anthill.x
        self.y_ = self.anthill.y
        if self.x < x_tree:
            move = +5
        else:
            move = -5
        if x_tree != self.x:
            self.x += move
            self.y = self.y_ + (self.x - self.x_) * (y_tree - self.y_) / (x_tree - self.x_)

        if self.x == x_tree:
            if k == 1:
                self.collect_leaves()
            if k == 2:
                self.collect_branch()
            self.x_ = self.x
            self.y_ = self.y





    def to_grow_larva(self):
        k = random.randint(1, 3)
        self.size += k
        self.anthill.mushroom.size -= 10
        self.anthill.count_eat_larva += 10


    def put_cargo(self):
        if self.cargo:
            self.anthill.list_Leaf.append(self.cargo)
        self.cargo = None

    def put_branch(self):
        if self.cargo:
            self.anthill.list_branch.append(self.cargo)
        self.cargo = None


    def go_Home(self):
        self.x_home = self.anthill.x
        self.y_home = self.anthill.y
        self.x_ = self.tree.x+150
        self.y_ = self.tree.y+100

        if self.x_home < self.x:
            move = -5
        else:
            move = +5
        if self.x_home != self.x:
            self.x += move
            self.y = self.y_ + (self.x - self.x_)*(self.y_home - self.y_) / (self.x_home - self.x_)



        if self.x == self.x_home:
            sum = 0

            if self.cargo.name == "листик":
                self.put_cargo()
            else:
                self.put_branch()
            for i in range(len(self.anthill.list_Leaf)):
                sum += self.anthill.list_Leaf[i].size
            print("запас листьев: " + str(sum))

            self.point = "anthill"
            self.x_ = self.x
            self.y_ = self.y

    def draw(self):
        ...


    def update(self):
        self.age += 1

class Male_Ant(Ant):
    def __init__(self, anthill):
        super().__init__(anthill)
        self.wings = True

    def breed(self):
        self.anthill.queen.breed = True
        self.wings = False

    def update(self):
        pass

class Larva:
    def __init__(self, anthill):
        self.anthill = anthill
        self.age = 0
        self.size = 0

    def eat(self):
        if self.anthill.count_eat_larva > 1:
            self.anthill.count_eat_larva -= 1

    def transformation(self):
        if len(self.anthill.list_larva) > 0:
            k = random.randint(1,2)
            if self.size == 3:
                self.anthill.list_ants.append(Soldier(self.anthill))
            elif self.size == 2:
                self.anthill.list_male_ant.append(Male_Ant(self.anthill))
            else:
                self.anthill.list_worker_ants.append(Worker(self.anthill, len(self.anthill.list_worker_anthill) + 1,self.anthill.tree))
            if k == 2:
                self.anthill.list_worker_anthill.append(Worker(self.anthill, len(self.anthill.list_worker_anthill) + 1,self.anthill.tree))
                self.anthill.list_larva.pop(0)
            if len(self.anthill.list_larva) > 0:
                self.anthill.list_larva.pop(0)

    def update(self):
        self.age += 1

class Ant_death:
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size
