from mushroom import Mushroom
from anthill import Anthill
import random
from ants import Queen, Male_Ant, Larva, Worker, Soldier
import pygame
from trees import Tree

pygame.init()
clock = pygame.time.Clock()



class Simulation:
    def __init__(self):
        self.time = 0
        self.mushroom = Mushroom()
        self.anthill = Anthill(tree=0)
        self.anthill.queen = Queen(self.anthill)
        self.screen = pygame.display.set_mode((1650,900))





    def eat_(self):
        self.anthill.queen.eat()
        for i in self.anthill.list_worker_ants:
            i.eat()
        for i in self.anthill.list_ants:
            i.eat()
        for i in self.anthill.list_worker_anthill:
            i.eat()
        for i in self.anthill.list_male_ant:
            i.eat()

    def create_tree(self):
        self.anthill.list_tree.append(Tree(500,700))
        self.anthill.list_tree.append(Tree(250,450))
        self.anthill.list_tree.append(Tree(750,0))
        self.anthill.list_tree.append(Tree(950, 700))

        self.anthill.list_tree.append(Tree(400,50))



    def create_ants(self):
        k = random.randint(10,11)

        n = 0
        for i in range(k):
            c = random.randint(1,3)
            f = random.randint(1, 100)
            if c == 1:
                n += 1
                self.anthill.list_worker_ants.append(Worker(self.anthill, n,self.anthill.tree))
                self.anthill.list_worker_anthill.append(Worker(self.anthill, n,self.anthill.tree))
            elif c == 2:
                self.anthill.list_ants.append(Soldier(self.anthill))
            else:
                self.anthill.list_male_ant.append(Male_Ant(self.anthill))

    def go_trees(self):
        if len(self.anthill.list_worker_ants) > 1:
            tr = 0
            for i in range(len(self.anthill.list_worker_ants)):
                if self.anthill.list_worker_ants[i].x - self.anthill.list_worker_ants[i-1].x > 30:
                    tr = 1

            for i in range(len(self.anthill.list_worker_ants)):
                x = self.anthill.list_worker_ants[i].tree.x+150
                if self.anthill.list_worker_ants[i].x == x:
                    self.anthill.list_worker_ants[i].point = "tree"

                if self.anthill.list_worker_ants[i].point == "anthill":
                    if i == 0 and self.anthill.list_worker_ants[i+1].x - self.anthill.list_worker_ants[i].x <= 30:
                        self.anthill.list_worker_ants[i].go_to_tree()
                        print("координата " + str(self.anthill.list_worker_ants[i].x))

                    if i != 0:
                        if self.anthill.list_worker_ants[i].x - self.anthill.list_worker_ants[i-1].x > 30 or self.anthill.list_worker_ants[i-1].point == "tree" or tr == 1:
                            self.anthill.list_worker_ants[i].go_to_tree()

    def to_grow_a_mushroom(self):
        for i in self.anthill.list_worker_anthill:
            i.grow_mushroom()

    def death_ants(self):
        for i in self.anthill.list_worker_ants:
            if i.age > 5500:
                i.death()
        for i in self.anthill.list_worker_anthill:
            if i.age > 1500:
                i.death()
        for i in self.anthill.list_male_ant:
            if i.age > 1500:
                i.death()
        for i in self.anthill.list_ants:
            if i.age > 1500:
                i.death()


    def grow_ants(self):
        for i in self.anthill.list_worker_anthill:
            i.to_grow_larva()
        if len(self.anthill.list_male_ant) != 0:
            self.anthill.list_male_ant[0].breed()
            self.anthill.list_male_ant.pop(0)
        self.anthill.queen.lay_an_egg()



        if self.anthill.count_eat_larva > 0:
            for i in self.anthill.list_larva:
                i.eat()
            for i in self.anthill.list_larva:
                if i.age > 100:
                    i.transformation()




    def go_home(self):
        tr = 0
        for i in range(len(self.anthill.list_worker_ants)):
            if self.anthill.list_worker_ants[i-1].x - self.anthill.list_worker_ants[i].x > 30:
                tr = 1

        for i in range(len(self.anthill.list_worker_ants)):
            x = self.anthill.x
            if self.anthill.list_worker_ants[i].x == x:
                self.anthill.list_worker_ants[i].point = "anthill"

            if self.anthill.list_worker_ants[i].point == "tree":
                if i == 0 and self.anthill.list_worker_ants[i].x - self.anthill.list_worker_ants[i+1].x <= 30:
                    self.anthill.list_worker_ants[i].go_Home()

                if i != 0:
                    if self.anthill.list_worker_ants[i-1].x - self.anthill.list_worker_ants[i].x > 30 or self.anthill.list_worker_ants[i-1].point == "anthill" or tr == 1:
                        self.anthill.list_worker_ants[i].go_Home()

    def update(self):
        for i in self.anthill.list_ants:
            i.update()
        for i in self.anthill.list_worker_ants:
            i.update()
        for i in self.anthill.list_worker_anthill:
            i.update()
        for i in self.anthill.list_larva:
            i.update()
        self.mushroom.update()

    def count_ants(self):
        count = 0
        count += len(self.anthill.list_worker_ants)
        count += len(self.anthill.list_ants)
        count += len(self.anthill.list_male_ant)
        return count

    def draw_ants(self):
        for i in self.anthill.list_worker_ants:
            pygame.draw.circle(self.screen, "BLACK",(i.x, i.y), 4)

    def draw_tree(self):
        for i in self.anthill.list_tree:
            tree_image = pygame.image.load("Tree.png").convert()
            tree_image = pygame.transform.scale(tree_image, (200, 200))
            tree_image.set_colorkey((255, 255, 255))

            self.screen.blit(tree_image, (i.x, i.y))



    def draw_text(self,text,x,y):
        font = pygame.font.Font("freesansbold.ttf", 14)
        if text == "Статистика":
            font = pygame.font.Font("freesansbold.ttf", 18)

        text_surface = font.render(text, True, "WHITE")
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def count_branch(self):
        sum = 0
        for i in self.anthill.list_branch:
            sum += i.size
        return sum


    def draw(self):

        bg = pygame.image.load("GrassBackground.png")
        bg = pygame.transform.scale(bg, (1920, 1020))
        self.screen.blit(bg,(0,0))

        self.draw_ants()
        anthill_image = pygame.image.load("AntHill.png").convert()
        anthill_image = pygame.transform.scale(anthill_image, (self.anthill.size, self.anthill.size))
        anthill_image.set_colorkey((255, 255, 255))
        self.screen.blit(anthill_image, (self.anthill.x-150,self.anthill.y-150))
        self.draw_tree()

        pygame.draw.rect(self.screen,"BLACK",(0,700,325,200))
        text = "Статистика"
        self.draw_text(text,150,720)
        text = "Запас веток" + " " + str(self.count_branch())
        self.draw_text(text,150,750)
        text = "Количество еды у личинок" + " " + str(self.anthill.count_eat_larva)
        self.draw_text(text,165,775)
        text = "Количество муравьев" + " " + str(self.count_ants())
        self.draw_text(text,150,800)
        text = "Запас Листьев" + " " + str(self.anthill.count_Leaf())
        self.draw_text(text, 120, 850)
        text = "Запас гриба" + " " + str(self.anthill.mushroom.size)
        self.draw_text(text,125,825)

    def build_anthill(self):
        for i in self.anthill.list_worker_anthill:
            i.build_an_anthill()




    def simulate(self):
        time_eat = 0
        mainloop = True
        self.create_tree()
        self.anthill.tree = random.choice(self.anthill.list_tree)
        self.create_ants()




        while mainloop:
            self.time += 1
            time_eat += 1
            self.anthill.tree = random.choice(self.anthill.list_tree)

            if time_eat > 200:
                time_eat = 0
                self.eat_()

                self.grow_ants()
                self.count_ants()
                self.to_grow_a_mushroom()



            if self.time > 1:
                self.build_anthill()
                self.draw()
                self.go_trees()
                self.go_home()
                self.update()
                self.death_ants()


                self.time = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False
            pygame.display.update()
            clock.tick(60)

        pygame.quit()



simulation = Simulation()
simulation.simulate()

