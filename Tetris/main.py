import random, time, pygame, sys
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (195, 195,   0)
LIGHTYELLOW = (255, 255,  20)
CYAN        = (  0, 155, 155)
LIGHTCYAN   = (  0, 175, 175)
PURPLE      = (128,   0, 128)
LIGHTPURPLE = (175,   0, 175)
ORANGE      = (255,  165,  0)
LIGHTORANGE = (255,  185,  0)


BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW,      CYAN,      PURPLE,      ORANGE)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW, LIGHTCYAN, LIGHTPURPLE, LIGHTORANGE)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

# second attribute is index into color array
PIECES = {'S': (S_SHAPE_TEMPLATE, 1),
          'Z': (Z_SHAPE_TEMPLATE, 2),
          'J': (J_SHAPE_TEMPLATE, 0),
          'L': (L_SHAPE_TEMPLATE, 6),
          'I': (I_SHAPE_TEMPLATE, 4),
          'O': (O_SHAPE_TEMPLATE, 3),
          'T': (T_SHAPE_TEMPLATE, 5)}


def makeTextObjs(text, font, color):
    """
    returns the given text as a displayable object
    """
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    """
    exits the game
    """
    pygame.quit()
    sys.exit()


def isOnBoard(x, y):
    """
    check if given x, y are on the board
    """
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def convertToPixelCoords(boxx, boxy):
    """
    Convert the given xy coordinates of the board to xy
    coordinates of the location on the screen.
    """
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def calculateLevelAndFallFreq(score):
    """
    Based on the score, return the level the player is on and
    how many seconds pass until a falling piece falls one space.
    """
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def getBlankBoard():
    """
    create and return a new blank board data structure
    """
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def generatePieceBuff():
    """
    randomly shuffles the list of 7 pieces
    returns the list of new piece objects
    """
    piece_buffer = list(PIECES)
    random.shuffle(piece_buffer)
    return list(map(lambda x: Piece(x),piece_buffer))


class Piece(object):
    """
    object representing single piece
    init with piece name
    """
    def __init__(self, name):
        self.name = name
        self.shape = PIECES[name][0]
        self.color = PIECES[name][1]
        self.x = int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2)
        self.y = -2 #start above the board (i.e. less theen 0)
        self.rotation = random.randint(0, len(self.shape)-1)

    def isValidPosition(self, board, adjX=0, adjY=0):
        # Return True if the piece is within the board and not colliding
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                isAboveBoard = y + self.y + adjY < 0
                if isAboveBoard or self.shape[self.rotation][y][x] == BLANK:
                    continue
                if not isOnBoard(x + self.x + adjX, y + self.y + adjY):
                    return False
                if board[x + self.x + adjX][y + self.y + adjY] != BLANK:
                    return False
        return True


class App(object):

    def __init__(self):
        """
        sets needed global variables at the start of the app
        """
        pygame.init()
        pygame.display.set_caption('Tetris')
        self.fps_clock = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        self.basic_font = pygame.font.Font('freesansbold.ttf', 18)
        self.big_font = pygame.font.Font('freesansbold.ttf', 100)
        self.board = None
        self.falling_piece = None
        self.piece_buffer = None
        self.score = 0
        self.level, self.fall_freq = calculateLevelAndFallFreq(self.score)


    def game_loop(self):
        """
        main game loop
        """
        self.board = getBlankBoard()

        self.last_move_down_time = time.time()
        self.last_move_sideways_time = time.time()
        self.last_fall_time = time.time()

        self.moving_down = False # note: there is no movingUp variable
        self.moving_left = False
        self.moving_right = False

        self.piece_buffer = generatePieceBuff()
        self.falling_piece = self.popFromPieceBuffer()
        self.next_piece = self.popFromPieceBuffer()

        while True:
            if self.falling_piece == None:
                # no falling piece in play, start a new piece at the top
                self.falling_piece = self.next_piece
                self.next_piece = self.popFromPieceBuffer()
                # reset last fall time for new piece
                self.last_fall_time = time.time()
                if not self.falling_piece.isValidPosition(self.board):
                    return # if cant fit new piece on top then game over
            self.checkForQuit()
            for event in pygame.event.get(): # event handling loop
                self.do_event(event)
            self.do_update()
            self.do_render() # drawing everything on the screen


    def do_event(self, event):
        """
        handles user input
        """
        self.checkForQuit()
        if event.type == KEYUP:
            if (event.key == K_p):
                # Pausing the game
                self.display_surface.fill(BGCOLOR)
                self.showTextScreen('Paused') # pause until a key press
                self.last_fall_time = time.time()
                self.last_move_down_time = time.time()
                self.last_move_sideways_time = time.time()
            elif (event.key == K_LEFT or event.key == K_a):
                self.moving_left = False
            elif (event.key == K_RIGHT or event.key == K_d):
                self.moving_right = False
            elif (event.key == K_DOWN or event.key == K_s):
                self.moving_down = False

        elif (event.type == KEYDOWN):
            #moving piece sideways
            if (event.key == K_LEFT or event.key == K_a) and self.falling_piece.isValidPosition(self.board, adjX=-1):
                    self.falling_piece.x -= 1
                    self.moving_left = True
                    self.moving_right = False
                    self.last_move_sideways_time = time.time()
            elif (event.key == K_RIGHT or event.key == K_d) and self.falling_piece.isValidPosition(self.board, adjX=1):
                    self.falling_piece.x += 1
                    self.moving_left = False
                    self.moving_right = True
                    self.last_move_sideways_time = time.time()

            # rotating the piece (if there is room to rotate)
            elif (event.key == K_UP or event.key == K_w):
                self.falling_piece.rotation = (self.falling_piece.rotation + 1) % len(self.falling_piece.shape)
                if not self.falling_piece.isValidPosition(self.board):
                    self.falling_piece.rotation = (self.falling_piece.rotation - 1) % len(self.falling_piece.shape)
            elif (event.key == K_q): # rotate the other direction
                self.falling_piece.rotation = (self.falling_piece.rotation - 1) % len(self.falling_piece.shape)
                if not isValidPosition(self.board):
                    self.falling_piece.rotation = (self.falling_piece.rotation + 1) % len(self.falling_piece.shape)
            # making the piece fall faster with the down key
            elif (event.key == K_DOWN or event.key == K_s):
                    self.moving_down = True
                    if self.falling_piece.isValidPosition(self.board, adjY=1):
                        self.falling_piece.y += 1
                    self.last_move_down_time = time.time()
            # move the current piece all the way down
            elif event.key == K_SPACE:
                self.moving_down = False
                self.moving_left = False
                self.moving_right = False
                for i in range(1, BOARDHEIGHT):
                    if not self.falling_piece.isValidPosition(self.board, adjY=i):
                        break
                self.falling_piece.y += i - 1

    def do_update(self):
        """
        updates the game logic based on the user input of do_event
        """

        # handle moving the piece because of user input
        if (self.moving_left or self.moving_right) and time.time() - self.last_move_sideways_time > MOVESIDEWAYSFREQ:
            if self.moving_left and self.falling_piece.isValidPosition(self.board, adjX=-1):
                self.falling_piece.x -= 1
            elif self.moving_right and self.falling_piece.isValidPosition(self.board, adjX=1):
                self.falling_piece.x += 1
            self.last_move_sideways_time = time.time()

        # handle moving the piece down becauase of user input
        if self.moving_down and time.time() - self.last_move_down_time > MOVEDOWNFREQ and self.falling_piece.isValidPosition(self.board, adjY=1):
            self.falling_piece.y += 1
            self.last_move_down_time = time.time()

        # let the piece fall if it is time to fall
        if time.time() - self.last_fall_time > self.fall_freq:
            # see if the piece has landed
            if not self.falling_piece.isValidPosition(self.board, adjY=1):
                # falling piece has landed, set it on the board
                self.addToBoard(self.falling_piece)
                self.score += self.removeCompleteLines()
                self.level, self.fall_freq = calculateLevelAndFallFreq(self.score)
                self.falling_piece = None
            else:
                # piece did not land, just move the piece down
                self.falling_piece.y += 1
                self.last_fall_time = time.time()

    def do_render(self):
        """
        displays changes to user
        """
        self.display_surface.fill(BGCOLOR)
        self.drawBoard()
        self.drawStatus()
        self.drawNextPiece(self.next_piece)
        if self.falling_piece != None:
            self.drawPiece(self.falling_piece)
        pygame.display.update()
        self.fps_clock.tick(FPS)


    def checkForKeyPress(self):
        """
        Go through event queue looking for a KEYUP event.
        Grab KEYDOWN events to remove them from the event queue.
        """
        self.checkForQuit()
        for event in pygame.event.get([KEYDOWN, KEYUP]):
            if event.type == KEYDOWN:
                continue
            return event.key
        return None


    def showTextScreen(self, text):
        """
        This function displays large text in the
        center of the screen until a key is pressed.
        Draw the text drop shadow
        """
        titleSurf, titleRect = makeTextObjs(text, self.big_font, TEXTSHADOWCOLOR)
        titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
        self.display_surface.blit(titleSurf, titleRect)

        # Draw the text
        titleSurf, titleRect = makeTextObjs(text, self.big_font, TEXTCOLOR)
        titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
        self.display_surface.blit(titleSurf, titleRect)

        # Draw the additional "Press a key to play." text.
        pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', self.basic_font, TEXTCOLOR)
        pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
        self.display_surface.blit(pressKeySurf, pressKeyRect)

        while self.checkForKeyPress() == None:
            pygame.display.update()
            self.fps_clock.tick()


    def checkForQuit(self):
        """
        check for quit events or the escape key
        """
        for event in pygame.event.get(QUIT): # get all the QUIT events
            terminate()
        for event in pygame.event.get(KEYUP): # get all the KEYUP events
            if event.key == K_ESCAPE:
                terminate()
            pygame.event.post(event) # put the other KEYUP event objects back

    def popFromPieceBuffer(self):
        if len(self.piece_buffer) == 1:
            popped = self.piece_buffer.pop(0)
            self.piece_buffer = generatePieceBuff()
        else:
            popped = self.piece_buffer.pop(0)
        return popped

    def isCompleteLine(self, y):
        # Return True if the line filled with boxes with no gaps.
        for x in range(BOARDWIDTH):
            if self.board[x][y] == BLANK:
                return False
        return True


    def removeCompleteLines(self):
        # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
        numLinesRemoved = 0
        y = BOARDHEIGHT - 1 # start y at the bottom of the board
        while y >= 0:
            if self.isCompleteLine(y):
                # Remove the line and pull boxes down by one line.
                for pullDownY in range(y, 0, -1):
                    for x in range(BOARDWIDTH):
                        self.board[x][pullDownY] = self.board[x][pullDownY-1]
                # Set very top line to blank.
                for x in range(BOARDWIDTH):
                    self.board[x][0] = BLANK
                numLinesRemoved += 1
                # Note on the next iteration of the loop, y is the same.
                # This is so that if the line that was pulled down is also
                # complete, it will be removed.
            else:
                y -= 1 # move on to check next row up
        return numLinesRemoved

    def drawNextPiece(self, piece):
        # draw the "next" text
        nextSurf = self.basic_font.render('Next:', True, TEXTCOLOR)
        nextRect = nextSurf.get_rect()
        nextRect.topleft = (WINDOWWIDTH - 120, 80)
        self.display_surface.blit(nextSurf, nextRect)
        # draw the "next" piece
        self.drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)

    def drawStatus(self):
        # draw the score text
        scoreSurf = self.basic_font.render('Score: %s' % self.score, True, TEXTCOLOR)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 150, 20)
        self.display_surface.blit(scoreSurf, scoreRect)

        # draw the level text
        levelSurf = self.basic_font.render('Level: %s' % self.level, True, TEXTCOLOR)
        levelRect = levelSurf.get_rect()
        levelRect.topleft = (WINDOWWIDTH - 150, 50)
        self.display_surface.blit(levelSurf, levelRect)

    def drawBox(self, boxx, boxy, color, pixelx=None, pixely=None):
        """
        draw a single box (each tetromino piece has four boxes)
        at xy coordinates on the board. Or, if pixelx & pixely
        are specified, draw to the pixel coordinates stored in
        pixelx & pixely (this is used for the "Next" piece).
        """
        if color == BLANK:
            return
        if pixelx == None and pixely == None:
            pixelx, pixely = convertToPixelCoords(boxx, boxy)
        pygame.draw.rect(self.display_surface, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
        pygame.draw.rect(self.display_surface, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


    def drawPiece(self, piece, pixelx=None, pixely=None):
        """
        draw the piece
        """
        shapeToDraw = piece.shape[piece.rotation]
        if pixelx == None and pixely == None:
            # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
            pixelx, pixely = convertToPixelCoords(piece.x, piece.y)
        # draw each of the boxes that make up the piece
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if shapeToDraw[y][x] != BLANK:
                    self.drawBox(None, None, piece.color, pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))



    def drawBoard(self):
        """
        draw boarder around the board and the individual boxes on the board
        """
        # draw the border around the board
        pygame.draw.rect(self.display_surface, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)
        # fill the background of the board
        pygame.draw.rect(self.display_surface, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
        # draw the individual boxes on the board
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                self.drawBox(x, y, self.board[x][y])


    def addToBoard(self, piece):
        """
        fill in the board based on piece's location, shape, and rotation
        """
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if piece.shape[piece.rotation][y][x] != BLANK:
                    self.board[x + piece.x][y + piece.y] = piece.color


    def main(self):
        self.showTextScreen('Tetris')
        while True:
            self.game_loop()
            self.showTextScreen("Game Over")
        terminate()


if __name__ == '__main__':
    App = App()
    App.main()
