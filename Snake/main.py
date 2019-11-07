import random, time, pygame, sys
from pygame.locals import *


WIN_WIDTH = 600
WIN_HEIGHT = 600
TILE_DIM = 20
TOP_BUFF = 6
LEFT_BUFF = 6

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans",50)
BIG_FONT = pygame.font.SysFont('comicsans', 100)

class Snake:
    def __init__(self, x, y):
        self.head = (x,y)
        self.body = [(x,y)]




class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [[None]*width for i in range(height)]
        self.food = None
        self.direction = "s"
        self.snake = [(0,0)]
        self.upgrade = False

    def snakeAlive(self):
        for coord in self.snake:
            col = coord[0]
            row = coord[1]
            if col < 0 or col > self.width-1:
                return False
            if row < 0 or row > self.height-1:
                return False
            if self.snake.count(coord) > 1:
                return False
            return True

    def moveSnake(self):
        head = self.snake[0]
        if self.direction == "s":
            new_head = (head[0], head[1]+1)
        elif self.direction == "n":
            new_head = (head[0], head[1]-1)
        elif self.direction == "e":
            new_head = (head[0]+1, head[1])
        elif self.direction == "w":
            new_head = (head[0]-1, head[1])
        self.snake = [new_head] + self.snake
        if self.upgrade == True:
            self.upgrade = False
            self.applySnake()
            self.placeNewFood()
        else:
            self.snake.pop(len(self.snake)-1)
            self.applySnake()

    def applySnake(self):
        #clear old snake
        for row in range(self.height):
            for col in range(self.width):
                if self.matrix[row][col] == "~":
                    self.matrix[row][col] = None
        #put new snake
        for row in range(self.height):
            for col in range(self.width):
                if (col, row) in self.snake:
                    if self.matrix[row][col] == "*":
                        self.upgrade = True
                    self.matrix[row][col] = "~"


    def placeNewFood(self):
        open_row, open_col = self.randomOpenSpace()
        self.matrix[open_row][open_col] = "*"

    def randomOpenSpace(self):
        open_spaces = []
        for row in range(self.height):
            for col in range(self.width):
                if self.matrix[row][col] == None:
                    open_spaces.append((row,col))
        rand_space = random.choice(open_spaces)
        return rand_space[0], rand_space[1]

    def draw(self, win):
        for row in range(self.height):
            for col in range(self.width):
                x, y = calcTopLeftPixel(row, col)
                if self.matrix[row][col] == None:
                    pygame.draw.rect(win, (0,0,0), (x,y,TILE_DIM,TILE_DIM))
                elif self.matrix[row][col] == "*": #food
                    pygame.draw.rect(win, (150,0,0), (x,y,TILE_DIM,TILE_DIM))
                elif self.matrix[row][col] == "~": #snake
                    pygame.draw.rect(win, (0,150,0), (x,y,TILE_DIM,TILE_DIM))


def calcTopLeftPixel(row, col):
    y = (row * TILE_DIM) + (1*row) + TOP_BUFF
    x = (col * TILE_DIM) + (1*col) + LEFT_BUFF
    return x, y

def draw_window(win, board):
    win.fill((80,80,80))
    board.draw(win)
    pygame.display.update()

def showGameOverScreen(win, clock, score):
    win.fill((0,0,0))

    text_render = BIG_FONT.render('Game Over', 1, (255,255,255))
    win.blit(text_render, (int(WIN_WIDTH / 2) - 180, int(WIN_HEIGHT / 2)- 100))

    key_render = STAT_FONT.render('Press any key to play again.', 1, (255,255,255))
    win.blit(key_render, (int(WIN_WIDTH / 2) - 225, int(WIN_HEIGHT / 2) + 80))

    score_text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(score_text, (int(WIN_WIDTH / 2) -50, int(WIN_HEIGHT / 2)))

    while checkForKeyPress() == None:
        pygame.display.update()
        clock.tick()

def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()
            return event.key
    return None

def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    board = Board(28,28)
    board.applySnake()
    board.placeNewFood()

    alive = True
    while alive:
        clock.tick(10)
        score = len(board.snake)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    board.direction = "w"
                elif event.key == K_RIGHT:
                    board.direction = "e"
                elif event.key == K_DOWN:
                    board.direction = "s"
                elif event.key == K_UP:
                    board.direction = "n"
        board.moveSnake()
        alive = board.snakeAlive()
        draw_window(win, board)
    return win, clock, score



if __name__ == "__main__":
    while True:
        win, clock, score = main()
        showGameOverScreen(win, clock, score)
    pygame.quit()
    quit()
