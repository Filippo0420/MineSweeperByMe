import pygame
import random
import tkinter as tk
from tkinter import messagebox
from time import sleep


class square:
    rows = 30
    width = 900
    sizeBtwn = width // rows
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 15)

    def __init__(self, position, window, color = (0, 150, 0), used = False):
        self.pos = position
        self.window = window
        self.color = color
        self.used = used
        self.number = 0
        self.bomb = False
        self.flag = False
        # types bomb, null, number
        pass

    def draw(self, bomb = False, flag = False):
        self.bomb = bomb
        self.flag = flag
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(self.window, self.color, (i * self.sizeBtwn + 1,
                                              j * self.sizeBtwn + 1,
                                              self.sizeBtwn - 2,
                                              self.sizeBtwn - 2))

    def drawUsed(self, color = (51, 102, 0)):
        self.color = color
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(self.window, self.color, (i * self.sizeBtwn + 1,
                                                   j * self.sizeBtwn + 1,
                                                   self.sizeBtwn - 2,
                                                   self.sizeBtwn - 2))

    def clicked(self, flag = False):
        self.flag = flag
        if not self.used:
            if not self.flag:
                if not self.used:
                    self.used = True
                    self.drawUsed()
            if self.flag:
                centre = self.sizeBtwn // 2
                radius = 4
                circleMiddle = (self.pos[0] * self.sizeBtwn + centre, self.pos[1] * self.sizeBtwn + centre)
                pygame.draw.circle(self.window, (100, 10, 200), circleMiddle, radius)
            elif self.bomb:
                centre = self.sizeBtwn // 2
                radius = 4
                circleMiddle = (self.pos[0] * self.sizeBtwn + centre, self.pos[1] * self.sizeBtwn + centre)
                pygame.draw.circle(self.window, (0, 0, 0), circleMiddle, radius)
                message_box('You lost!', 'Play Again')
                reset()
            else:
                text_surface = self.font.render(str(self.number), False, (255, 60, 0))
                self.window.blit(text_surface, (self.pos[0] * self.sizeBtwn + 5, self.pos[1] * self.sizeBtwn))


    def giveNumber(self, number):
        self.number = number



def losujBomby(rows, numOfBombs):
    bombs = []

    while len(bombs) != numOfBombs:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if (x, y) not in bombs:
            bombs.append((x, y))
    return bombs


def giveNumbers(allCubes, bombs):
    global width, rows
    zeros = []
    # sizeBtwn = width // rows
    for cube in allCubes:
        if not cube.bomb:
            cube.giveNumber(checkAround(cube, bombs))
            if cube.number == 0:
                zeros.append(cube.pos)
            #text_surface = font.render(str(cube.number), False, (255, 60, 0))
            #window.blit(text_surface, (cube.pos[0] * sizeBtwn + 5, cube.pos[1] * sizeBtwn))


def drawBoard(width, rows, window):
    global sizeBtwn
    linesColor = (0, 100, 0)
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(window, linesColor, (x, 0), (x, width))
        pygame.draw.line(window, linesColor, (0, y), (width, y))


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

def czyPuste(allCubes, cubeNum):
    global rows

    def czyLewoPuste():
        checkingCube = allCubes[cubeNum - rows]
        checkingCube.clicked()
        if checkingCube.number == 0:
            czyPuste(allCubes, cubeNum - rows)

    def czyPrawoPuste():
        checkingCube = allCubes[cubeNum + rows]
        if checkingCube.number == 0:
            checkingCube.clicked()

    def czyGoraPuste():
        checkingCube = allCubes[cubeNum - 1]
        if checkingCube.number == 0:
            checkingCube.clicked()

    def czyDolPuste():
        checkingCube = allCubes[cubeNum + 1]
        checkingCube.clicked()
        if checkingCube.number == 0:
            czyPuste(allCubes, cubeNum + 1)

    if allCubes[cubeNum].pos[0] == 0:
        if allCubes[cubeNum].pos[1] == rows - 1:
            czyGoraPuste()
        elif allCubes[cubeNum].pos[1] == 0:
            czyDolPuste()
        czyPrawoPuste()

    elif allCubes[cubeNum].pos[0] == rows - 1:
        if allCubes[cubeNum].pos[1] == rows - 1:
            czyGoraPuste()
        elif allCubes[cubeNum].pos[1] == 0:
            czyDolPuste()
        czyLewoPuste()
    elif allCubes[cubeNum].pos[1] == 0:
        czyDolPuste()
        czyLewoPuste()
        czyPrawoPuste()
    elif allCubes[cubeNum].pos[1] == rows - 1:
        czyGoraPuste()
        czyLewoPuste()
        czyPrawoPuste()
    else:
        czyDolPuste()
        czyPrawoPuste()
        czyGoraPuste()
        czyLewoPuste()




def makeCubes(window):
    allCubes = []
    for x in range(rows):
        for y in range(rows):
            allCubes.append(square((x, y), window))
    return allCubes


def drawCubes(allCubes, bombs, width, rows, window):
    for cube in allCubes:
        if cube.pos in bombs:
            cube.draw(bomb = True)
        else:
            cube.draw()
    pass


def getCubeNumFromMousePos(mousePos):
    global sizeBtwn
    position = (mousePos[0] // sizeBtwn, mousePos[1] // sizeBtwn)
    cubeNum = (position[0] + 1) * rows - (rows - (position[1]))
    return cubeNum

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def reset():
    global window, numOfBombs, allCubes, bombs
    window.fill((0, 0, 0))
    drawBoard(width, rows, window)
    allCubes = makeCubes(window)
    bombs = losujBomby(rows, numOfBombs)
    drawCubes(allCubes, bombs, width, rows, window)
    giveNumbers(allCubes, bombs)


def czyWygrana():
    global allCubes, numOfBombs
    sumOfUsedCubes = 0
    for cube in allCubes:
        if cube.used:
            sumOfUsedCubes +=1
    if sumOfUsedCubes == len(allCubes) - numOfBombs:
        win()


def win():
    message_box('You Win!', 'Congratulations!')
    reset()


def main():
    global width, rows, sizeBtwn, numOfBombs, allCubes, bombs, window
    width = 900
    rows = 30
    sizeBtwn = width // rows
    numOfBombs = 100
    pygame.font.init()
    window = pygame.display.set_mode((width, width))
    window.fill((0, 0, 0))
    allCubes = makeCubes(window)
    bombs = losujBomby(rows, numOfBombs)
    flag = True
    clock = pygame.time.Clock()

    drawBoard(width, rows, window)
    drawCubes(allCubes, bombs, width, rows, window)
    giveNumbers(allCubes, bombs)
    while flag:
        for event in pygame.event.get():
            # left mouse button click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                cubeNum = getCubeNumFromMousePos(mouse_position)
                if allCubes[cubeNum].flag:
                    allCubes[cubeNum].draw()
                if allCubes[cubeNum].number == 0:
                    czyPuste(allCubes, cubeNum)
                allCubes[cubeNum].clicked(flag=False)
                czyWygrana()
            # right mouse button click
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_position = pygame.mouse.get_pos()
                cubeNum = getCubeNumFromMousePos(mouse_position)
                if not allCubes[cubeNum].flag and not allCubes[cubeNum].used:
                    allCubes[cubeNum].clicked(flag=True)
                elif not allCubes[cubeNum].used:
                    allCubes[cubeNum].draw()

        pygame.time.delay(20)
        clock.tick(10)

        pygame.display.update()
    pass


main()