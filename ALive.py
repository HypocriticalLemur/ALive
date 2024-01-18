import pygame
from dataclasses import dataclass
from random import randint
from abc import ABC, abstractmethod
# import numpy as np

@dataclass(slots=True)
class Coordinate:
    x:int
    y:int

class Cell:
    def __init__(self, x:int, y:int, alive:bool):
        self.coord = Coordinate(x,y)
        self.alive = alive
        self.color = (155,155,155)
    def copy(self):
        return Cell(self.coord.x, self.coord.y, self.alive)

class FillFieldStrategy(ABC):
    @abstractmethod
    def FillField (self) -> tuple[list[list[Cell]], float, float]: ...
class FillFieldRandom(FillFieldStrategy):
    def __init__(self, x_size:int, y_size:int, rareness:int = 2):
        self.x_size = x_size
        self.y_size = y_size
        self.rareness = rareness
    def FillField(self):
        # cells:list[list[Cell]] = []
        cells = [[Cell(i,j,randint(0,self.rareness)%self.rareness == 1) for i in range(self.x_size)] for j in range(self.y_size)]#np.zeros((self.x_size, self.y_size), dtype = np.int8)
        return cells, self.x_size, self.y_size
class FillFieldOneLine(FillFieldStrategy):
    def FillField(self):
        # cells = np.zeros((3,3), dtype = np.int8)
        # for i in range(3):
        #     for j in range(3):
        #         cells[i][j] = (i == 1)
        cells = [[Cell(i,j,i==1) for i in range(3)] for j in range(3)]
        return cells, 3, 3
@dataclass(slots=True, unsafe_hash=True)
class MinMax:
    min:float
    max:float
    def within(self, value:float):
        if value > self.min and value < self.max:
            return True
        return False

        

class Game:
    ALIVE_COLOR = (155,155,155)
    def __init__(self, width:int, height:int, fill_field_strategy:FillFieldStrategy, fps:int = 0,
    PIXEL_SIZE:int = 5, min_alive_threshold:float = 1.99, max_alive_threshold:float = 2.99):
        self.cells, self.x_size, self.y_size = fill_field_strategy.FillField()
        self.width, self.height = width, height
        # if fps <= 1e-4:
        #     fps = 60
        self.fps = fps
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.PIXEL_SIZE = PIXEL_SIZE
        self.threshold=MinMax(min_alive_threshold, max_alive_threshold)
    def loop(self):
        quit = False
        while not quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        quit = True
                # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                #         is_blue = not is_blue
            
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]: quit = True
            # pressed = pygame.key.get_pressed()
            # if pressed[pygame.K_ESCAPE]: pygame.quit()
            self.clock.tick(self.fps)
            # pygame.time.delay(int(1000/self.fps))
            self.__make_time_step__()
            self.__check_alive__()
            # iteration += 1
            # print(f"iteration {iteration}")
        pygame.quit()
    def __cell_exists__(self, x:int, y:int):
        if x < 0:
            return False
        if y < 0:
            return False
        if x >= len(self.cells):
            return False
        if y >= len(self.cells[0]):
            return False
        return True
    def __check_neighbours__(self, x:int, y:int):
        neighbours_alive = 0.
        for _i in (-1,0,1):
            for _j in (-1,0,1):
                if _j == 0 and _i == 0:
                    continue
                if self.__cell_exists__(x+_i,y+_j):
                    if self.cells[x+_i][y+_j].alive:
                        if _j != 0 and _i != 0:
                            neighbours_alive += .5
                        else:
                            neighbours_alive += 1.
        return neighbours_alive


    def __check_alive__(self):
        cells_copy:list[list[Cell]] = []#self.cells.copy()
        for i in range(len(self.cells)):
            cells_copy.append([])
            for j in range(len(self.cells[i])):
                cells_copy[i].append(self.cells[i][j].copy())
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                neighbours_alive = self.__check_neighbours__(i,j)
                if cells_copy[i][j].alive:
                    if not self.threshold.within(neighbours_alive):#neighbours_alive < 1:
                    # if not cells_copy[i][j]:
                        # print(f'{i} {j} back to live!')
                        cells_copy[i][j].alive = False
                else:
                    if self.threshold.within(neighbours_alive):
                    # if cells_copy[i][j]:
                        # print(f'{i} {j} go to void')
                        cells_copy[i][j].alive = True
        self.cells = cells_copy.copy()

    def __make_time_step__(self):
        self.screen.fill((0, 0, 0))
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j].alive:
                    _x = i*self.PIXEL_SIZE
                    _y = j*self.PIXEL_SIZE
                    pygame.draw.rect(self.screen, self.cells[i][j].color, pygame.Rect(_x,_y,self.PIXEL_SIZE,self.PIXEL_SIZE))
        pygame.display.flip()
        # pygame.display.update()
def test ():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    done = False
    is_blue = True
    x = 30
    y = 30
    
    clock = pygame.time.Clock()
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    is_blue = not is_blue
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: y -= 3
        if pressed[pygame.K_DOWN]: y += 3
        if pressed[pygame.K_LEFT]: x -= 3
        if pressed[pygame.K_RIGHT]: x += 3
        
        screen.fill((0, 0, 0))
        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
        
        pygame.display.flip()
        clock.tick(60)
def main():
    fill_field_strategy = FillFieldRandom(200,200,40)
    # fill_field_strategy = FillFieldOneLine()
    game = Game(1000,1000,fill_field_strategy,PIXEL_SIZE=5,max_alive_threshold=3.49)
    game.loop()

if __name__ == '__main__':
    main()
    # test()