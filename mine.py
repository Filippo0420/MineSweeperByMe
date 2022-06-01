import pygame
import  random
from time import sleep


class square:
    rows = 20
    width = 700

    def __init__(self, position, color = (50, 205, 50), used = True):
        self.pos = position
        self.type = type
        self.color = color
        self.used = used
        self.bomb = False
        # types bomb, null, number
        pass

    def draw(self, window, bomb = False):
        self.bomb = bomb
        dis = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(window, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if self.bomb:
            centre = dis // 2
            radius = 6
            circleMiddle = (i * dis + centre, j * dis + centre)
            pygame.draw.circle(window, (0, 0, 0), circleMiddle, radius)

    def clicked(self):
        if self.used:
            self.used = False
        pass



def losujBomby(rows, numOfBombs):
    bombs = []

    while len(bombs) != numOfBombs:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if (x, y) not in bombs:
            bombs.append((x, y))
    return bombs


def giveNumbers(window, allCubes, bombs):
    global width, rows
    sizeBtwn = width // rows
    my_font = pygame.font.SysFont('Arial', 13)
    for cube in allCubes:
        if not cube.bomb:
            text_surface = my_font.render(str(checkAround(cube, bombs)), False, (200, 100, 0))
            window.blit(text_surface, (cube.pos[0] * sizeBtwn + 5, cube.pos[1] * sizeBtwn))


def drawBoard(width, rows, window):
    sizeBtwn = width // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(window, (34, 139, 34), (x, 0), (x, width))
        pygame.draw.line(window, (34, 139, 34), (0, y), (width, y))


def checkAround(cube, bombs):
    global rows
    bombAround = 0

    def checkLeft():
        bombAround = 0
        # left
        if (cube.pos[0] - 1, cube.pos[1]) in bombs:
            bombAround += 1
        # left up
        if (cube.pos[0] - 1, cube.pos[1] - 1) in bombs:
            bombAround += 1
        # left down
        if (cube.pos[0] - 1, cube.pos[1] + 1) in bombs:
            bombAround += 1
        return bombAround

    def checkRight():
        bombAround = 0
        # right
        if (cube.pos[0] + 1, cube.pos[1]) in bombs:
            bombAround += 1
        # right up
        if (cube.pos[0] + 1, cube.pos[1] - 1) in bombs:
            bombAround += 1
        # right down
        if (cube.pos[0] + 1, cube.pos[1] + 1) in bombs:
            bombAround += 1
        return bombAround

    def checkDown():
        bombAround = 0
        # down
        if (cube.pos[0], cube.pos[1] + 1) in bombs:
            bombAround += 1
        return bombAround

    def checkUp():
        bombAround = 0
        # up
        if (cube.pos[0], cube.pos[1] - 1) in bombs:
            bombAround += 1
        return bombAround

    bombAround += checkUp() + checkDown() + checkRight() + checkLeft()
    return bombAround


def makeCubes():
    allCubes = []
    for x in range(rows):
        for y in range(rows):
            allCubes.append(square((x, y)))
    return allCubes


def drawCubes(allCubes, bombs, width, rows, window):
    sizeBtwn = width // rows

    for cube in allCubes:
        if cube.pos in bombs:
            cube.draw(window, bomb = True)
        else:
            cube.draw(window)
    print(len(allCubes))
    pass


def main():
    global width, rows
    width = 700
    rows = 20
    numOfBombs = 30
    pygame.font.init()
    window = pygame.display.set_mode((width, width))
    window.fill((0, 0, 0))
    allCubes = makeCubes()
    bombs = losujBomby(rows, numOfBombs)
    flag = True
    while flag:
        drawBoard(width, rows, window)
        drawCubes(allCubes, bombs, width, rows, window)
        giveNumbers(window, allCubes, bombs)
        pygame.display.update()
        sleep(1000)
    pass


main()