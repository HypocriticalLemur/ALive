import pygame
from dataclasses import dataclass
from random import randint
from abc import ABC, abstractmethod
import numpy as np

@dataclass(slots=True)
class Coordinate:
    x:int
    y:int

class Cell:
    def __init__(self, x:int, y:int, alive:bool):
        self.coord = Coordinate(x,y)
        self.alive = alive

class FillFieldStrategy(ABC):
    @abstractmethod
    def FillField (self) -> tuple[np.ndarray[np.int8,np.int8], float, float]: ...
class FillFieldRandom(FillFieldStrategy):
    def __init__(self, x_size:int, y_size:int, rareness = 30):
        self.x_size = x_size
        self.y_size = y_size
        self.rareness = rareness
    def FillField(self):
        # cells:list[list[Cell]] = []
        cells = np.zeros((self.x_size, self.y_size), dtype = np.int8)
        for i in range(self.x_size):
            for j in range(self.y_size):
                cells[i][j] = (randint(0,self.rareness)%self.rareness == 1)
        return cells, self.x_size, self.y_size
class FillFieldOneLine(FillFieldStrategy):
    def FillField(self):
        cells = np.zeros((3,3), dtype = np.int8)
        for i in range(3):
            for j in range(3):
                cells[i][j] = (i == 1)
        return cells, 3, 3
@dataclass(slots=True, unsafe_hash=True)
class Threshold:
    min:float
    max:float

        

class Game:
    ALIVE_COLOR = (155,155,155)
    def __init__(self, width, height, fill_field_strategy:FillFieldStrategy, fps:int = 0,
    PIXEL_SIZE = 5, min_alive_threshold = 1.99, max_alive_threashold = 3.49):
        self.cells, self.x_size, self.y_size = fill_field_strategy.FillField()
        self.width, self.height = width, height
        self.fps = fps
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.PIXEL_SIZE = PIXEL_SIZE
        self.threshold=Threshold(min_alive_threshold, max_alive_threashold)
    def __infinite_loop__(self):
        quit = False
        iteration = 0
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
            self.__make_time_step__()
            self.__check_alive__()
            iteration += 1
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
                    if self.cells[x+_i][y+_j]:
                        if _j != 0 and _i != 0:
                            neighbours_alive += .49
                        else:
                            neighbours_alive += 1.
        return neighbours_alive


    def __check_alive__(self):
        cells_copy = self.cells.copy()
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                neighbours_alive = self.__check_neighbours__(i,j)
                if neighbours_alive > self.threshold.min and neighbours_alive < self.threshold.max:
                    # if not cells_copy[i][j]:
                        # print(f'{i} {j} back to live!')
                    cells_copy[i][j] = True
                else:
                    # if cells_copy[i][j]:
                        # print(f'{i} {j} go to void')
                    cells_copy[i][j] = False
        self.cells = cells_copy.copy()

    def __make_time_step__(self):
        self.screen.fill((0, 0, 0))
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j]:
                    _x = i*self.PIXEL_SIZE
                    _y = j*self.PIXEL_SIZE
                    pygame.draw.rect(self.screen, self.ALIVE_COLOR, pygame.Rect(_x,_y,self.PIXEL_SIZE,self.PIXEL_SIZE))
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
    fill_field_strategy = FillFieldRandom(300,300,2)
    # fill_field_strategy = FillFieldOneLine()
    game = Game(500,100,fill_field_strategy)
    game.__infinite_loop__()

if __name__ == '__main__':
    main()
    # test()