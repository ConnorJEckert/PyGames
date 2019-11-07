import random, time, pygame, sys, copy
from pygame.locals import *

pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 600
STAT_FONT = pygame.font.SysFont("comicsans",50)
BIG_FONT = pygame.font.SysFont('comicsans', 100)

class Tile:
    def __init__(self, row, col, value = 2):
        self.col = col
        self.row = row
        self.width = 95
        self.height = 95
        self.value = value
        self.merged = False

    def upgradeTile(self):
        self.value = self.value * 2
        self.merged = True

    def draw(self, win):
        x, y = calcTopLeftPixel(self.row, self.col)
        pygame.draw.rect(win, getColor(self.value), (x,y,95,95))
        text = STAT_FONT.render(str(self.value), 1, (0,0,0))
        text_rect = text.get_rect(center = (x+95/2,y+95/2))
        win.blit(text,text_rect)

    
class Board:
    def __init__(self):
        self.matrix = [[None]*4 for i in range(4)]

    def draw(self, win):
        pygame.draw.rect(win, (0,0,0), (100, 100, 405, 405))
        for row in range(4):
            for col in range(4):
                if self.matrix[row][col] == None:
                    drawEmptyTile(win, row, col)
                else:
                    self.matrix[row][col].draw(win)

    def insertTile(self, tile):
        self.matrix[tile.row][tile.col] = tile

    def insertRandomTile(self):
        open_row, open_col = self.randomOpenSpace()
        if open_row != -1:
            value = random.choice([2,2,2,2,2,2,2,2,4])
            tile = Tile(open_row, open_col, value)
            self.insertTile(tile)

    def randomOpenSpace(self):
        openSpaces = []
        for row in range(4):
            for col in range(4):
                if self.matrix[row][col] == None:
                    openSpaces.append((row,col))
        if openSpaces != []:
            coords = random.choice(openSpaces)
            return coords[0], coords[1]
        else:
            return -1,-1

    def spacesRemaining(self):
        openSpaces = []
        for row in range(4):
            for col in range(4):
                if self.matrix[row][col] == None:
                    openSpaces.append((row,col))
        return len(openSpaces)

    def shiftLeft(self, score):
        old_matrix = getSimpleMatrix(self.matrix)
        for row in range(4):
            for col in range(1,4):
                if self.matrix[row][col] != None:
                    self.matrix, score = shiftTileLeft(self, self.matrix[row][col], score)
        self.removeMergeFlagAll()
        if old_matrix == getSimpleMatrix(self.matrix):
            return False, score
        return True, score
        

    def shiftRight(self, score):
        old_matrix = getSimpleMatrix(self.matrix)
        for row in range(4):
            for col in range(2,-1,-1):
                if self.matrix[row][col] != None:
                    self.matrix, score = shiftTileRight(self, self.matrix[row][col], score)
        self.removeMergeFlagAll()
        if old_matrix == getSimpleMatrix(self.matrix):
            return False, score
        return True, score

    def shiftDown(self, score):
        old_matrix = getSimpleMatrix(self.matrix)
        for row in range(2,-1,-1):
            for col in range(4):
                if self.matrix[row][col] != None:
                    self.matrix, score = shiftTileDown(self, self.matrix[row][col], score)
        self.removeMergeFlagAll()
        if old_matrix == getSimpleMatrix(self.matrix):
            return False, score
        return True, score

    def shiftUp(self, score):
        old_matrix = getSimpleMatrix(self.matrix)
        for row in range(1,4):
            for col in range(4):
                if self.matrix[row][col] != None:
                    self.matrix, score = shiftTileUp(self, self.matrix[row][col], score)
        self.removeMergeFlagAll()
        if old_matrix == getSimpleMatrix(self.matrix):
            return False, score
        return True, score


    def removeMergeFlagAll(self):
        for row in range(4):
            for col in range(4):
                if self.matrix[row][col] != None:
     
                    self.matrix[row][col].merged = False

def getColor(value):
    if (value == 2):
        return (238, 228, 218)
    elif (value == 4):
        return (237, 224, 200)
    elif (value == 8):
        return (242, 177, 121)
    elif (value == 16):
        return (245, 149, 99)
    elif (value == 32):
        return (246, 124, 95)
    elif (value == 64):
        return (246, 94, 59)
    elif (value == 128):
        return (237, 207, 114)
    elif (value == 256):
        return (237, 204, 97)
    elif (value == 512):
        return (237, 200, 80)
    elif (value == 1024):
        return (237, 197, 63)
    elif (value == 2048):
        return (237, 194, 46)


def getSimpleMatrix(matrix):
    output = copy.deepcopy(matrix)
    for row in range(4):
        for col in range(4):
            if matrix[row][col] != None:
                output[row][col] = matrix[row][col].value
    return output


def shiftTileLeft(board, tile, score):
    row = tile.row
    col = tile.col
    while (col > 0):
        spaceLeft = board.matrix[row][col-1]
        if spaceLeft == None:
            board.matrix[row][col] = None
            col -= 1
        elif (spaceLeft.value == tile.value and spaceLeft.merged == False):
            spaceLeft.upgradeTile()
            board.insertTile(spaceLeft)
            board.matrix[row][col] = None
            score += (tile.value*2)
            return board.matrix, score
        else:
            tile.col = col
            board.insertTile(tile)
            return board.matrix, score
    tile.col = col
    board.insertTile(tile)
    return board.matrix, score

def shiftTileRight(board, tile, score):
    row = tile.row
    col = tile.col
    while (col < 3):
        spaceRight = board.matrix[row][col+1]
        if spaceRight == None:
            board.matrix[row][col] = None
            col += 1
        elif (spaceRight.value == tile.value and spaceRight.merged == False):
            spaceRight.upgradeTile()
            board.insertTile(spaceRight)
            board.matrix[row][col] = None
            score += (tile.value*2)
            return board.matrix, score
        else:
            tile.col = col
            board.insertTile(tile)
            return board.matrix, score
    tile.col = col
    board.insertTile(tile)
    return board.matrix, score

def shiftTileUp(board, tile, score):
    row = tile.row
    col = tile.col
    while (row > 0):
        spaceUp = board.matrix[row-1][col]
        if spaceUp == None:
            board.matrix[row][col] = None
            row -= 1
        elif (spaceUp.value == tile.value and spaceUp.merged == False):
            spaceUp.upgradeTile()
            board.insertTile(spaceUp)
            board.matrix[row][col] = None
            score += (tile.value*2)
            return board.matrix, score
        else:
            tile.row = row
            board.insertTile(tile)
            return board.matrix, score
    tile.row = row
    board.insertTile(tile)
    return board.matrix, score

def shiftTileDown(board, tile, score):
    row = tile.row
    col = tile.col
    while (row < 3):
        spaceDown = board.matrix[row+1][col]
        if spaceDown == None:
            board.matrix[row][col] = None
            row += 1
        elif (spaceDown.value == tile.value and spaceDown.merged == False):
            spaceDown.upgradeTile()
            board.insertTile(spaceDown)
            board.matrix[row][col] = None
            score += (tile.value*2)
            return board.matrix, score
        else:
            tile.row = row
            board.insertTile(tile)
            return board.matrix, score
    tile.row = row
    board.insertTile(tile)
    return board.matrix, score

def calcTopLeftPixel(row, col):
    y = (row * 100) + 5 + 100
    x = (col * 100) + 5 + 100
    return x, y

def checkForKeyPress():
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()
            continue
        return event.key
    return None


def showGameOverScreen(win, clock, score):
    win.fill((0,0,0))

    text_render = BIG_FONT.render('Game Over', 1, (255,255,255))
    win.blit(text_render, (int(WIN_WIDTH / 2) - 180, int(WIN_HEIGHT / 2)- 100))

    key_render = STAT_FONT.render('Press any key to play again.', 1, (255,255,255))
    win.blit(key_render, (int(WIN_WIDTH / 2) - 225, int(WIN_HEIGHT / 2) + 80))

    score_text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(score_text, (10, 10))

    while checkForKeyPress() == None:
        pygame.display.update()
        clock.tick()

def draw_window(win, board, score):
    win.fill((187,173,169))
    board.draw(win)
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (10, 10))
    pygame.display.update()

def drawEmptyTile(win, row, col):
    x, y = calcTopLeftPixel(row, col)
    pygame.draw.rect(win, (255,255,255), (x,y,95,95))

def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    board = Board()

    #start the game with two tiles
    board.insertRandomTile()
    board.insertRandomTile()

    run = True
    while run:
        clock.tick(30)
        if board.spacesRemaining() == 0:
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                res = False
                if event.key == K_LEFT:
                    res, score = board.shiftLeft(score)
                elif event.key == K_RIGHT:
                    res, score = board.shiftRight(score)
                elif event.key == K_DOWN:
                    res, score = board.shiftDown(score)
                elif event.key == K_UP:
                    res, score = board.shiftUp(score)
                if res == True:
                    board.insertRandomTile()

        draw_window(win, board, score)
    return win, clock, score

if __name__ == "__main__":
    while True:
        win, clock, score = main()
        showGameOverScreen(win, clock, score)
    pygame.quit()
    quit()

