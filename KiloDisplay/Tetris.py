#Based on: https://gist.github.com/kch42/565419


from random import randrange as rand

import bibliopixel.colors as colors
from bibliopixel.animation import BaseGameAnim
import math
from random import randint
import bibliopixel.util as util


# The configuration
cols =		19
rows =		40
maxfps = 	30

color_map = [
(0,   0,   0  ),
colors.Red,
colors.Orange,
colors.Yellow,
colors.Green,
colors.Blue,
colors.Purple,
colors.Violet,
(35,  35,  35) # Helper color for background grid
]

# Define the shapes of the single parts
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

def rotate_clockwise(shape):
    return [ [ shape[y][x]
            for y in xrange(len(shape)) ]
        for x in xrange(len(shape[0]) - 1, -1, -1) ]

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + off_y ][ cx + off_x ]:
                    return True
            except IndexError:
                return True
    return False

def remove_row(board, row):
    del board[row]
    return [[0 for i in xrange(cols)]] + board

def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1	][cx+off_x] += val
    return mat1

def new_board():
    board =  [[ 0 for x in xrange(cols) ] for y in xrange(rows)]
    return board

class Tetris(BaseGameAnim):
    def __init__(self, led, inputDev):
        super(Tetris, self).__init__(led, inputDev)

        if (self.width, self.height) != (25,50):
            raise Exception("Sorry, this was lazily written to only work on a 25x50 display :(")

        if hasattr(self._input_dev, "setLights") and hasattr(self._input_dev, "setLightsOff"):
            self._input_dev.setLightsOff(5)
            lights = {
                "A": (0,255,0),
                "B": (0,0,0),
                "X": (0,0,0),
                "Y": (255,0,0),
                "FIRE":(255,0,0)
            }
            self._input_dev.setLights(lights)

        self.setSpeed("drop", 6)
        self.rlim = cols

        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]

        self.addKeyFunc("LEFT", lambda:self.move(-1), speed=3, hold=True)
        self.addKeyFunc("RIGHT", lambda:self.move(+1), speed=3, hold=True)
        self.addKeyFunc("DOWN", lambda:self.drop(True), speed=1, hold=True)
        self.addKeyFunc(["UP", "A"], self.rotate_stone, speed=1, hold=False)
        self.addKeyFunc(["FIRE", "Y"], self.insta_drop, speed=1, hold=False)
        self.addKeyFunc("X", self.togglePause, speed=1, hold=False)
        self.init_game()

    def togglePause(self):
        self.paused = not self.paused

    def clearLevelUp(self):
        self.doStart = False
        if self.levelUp:
            self.paused = False
            self.levelUp = False

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.stone_x = int(cols / 2 - len(self.stone[0])/2)
        self.stone_y = 0

        if check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.lines_per_level = 6
        self.gameover = False
        self.win = False
        self.levelUp = True
        self.doStart = False
        self.paused = True
        self.board = new_board()
        self.new_stone()
        self.level = 1
        self.score = 0
        self.lines = 0
        self._last_up = False
        self._lastFire = False
        self._last_move = {"RIGHT": False, "LEFT": False}

    def disp_msg(self, msg, x, y):
        self._led.drawText(msg, x, y, size=0)

    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    self._led.set(off_x+x,off_y+y,color_map[val])

    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*self.lines_per_level:
            self.level += 1
            self.levelUp = True
            self.paused = True
            s = self.getSpeed("drop")
            s -= 1
            if s <= 0:
                self.win = True
            else:
                self.setSpeed("drop", s)

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x

    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.stone_y += 1
            if check_collision(self.board,
                               self.stone,
                               (self.stone_x, self.stone_y)):
                self.board = join_matrixes(
                  self.board,
                  self.stone,
                  (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0
                while True:
                    for i, row in enumerate(self.board):
                        if 0 not in row:
                            self.board = remove_row(
                              self.board, i)
                            cleared_rows += 1
                            break
                    else:
                        break
                self.add_cl_lines(cleared_rows)
                return True
        return False

    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop(True)):
                pass

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        self.doStart = False
        if self.gameover or self.win:
            self.init_game()
            self.gameover = False

    def step(self, amt=1):
        if (self.levelUp or self.gameover or self.win) and (self._lastKeys != self._keys) and any(v == True for v in self._keys.itervalues()):
            self.doStart = True
        if self.doStart:
            if not any(v == True for v in self._keys.itervalues()):
                if self.levelUp:
                    self.clearLevelUp()
                elif self.gameover or self.win:
                    self.start_game()
            else:
                return

        if not self.doStart:
            self.handleKeys()

        self._led.all_off()
        if self.gameover:
            self._led.all_off()
            self._led.drawText("GAME", self.width/2-11, self.height/2-8)
            self._led.drawText("OVER", self.width/2-11, self.height/2+1)
            s = "{}".format(self.score)
            self._led.drawText(s, self.width/2-(len(s)*4)/2+1, self.height/2+9, size=0)
        elif self.win:
            for x in range(self.width):
                c = colors.hue_helper(self.width-x, self.width, self._speedStep*2)
                self._led.drawLine(self.width/2, self.height/2, x, 0, c)
                self._led.drawLine(self.width/2, self.height/2, self.width-1-x, self.height-1, c)
            for y in range(self.height):
                c = colors.hue_helper(y, self.height, self._speedStep*2)
                self._led.drawLine(self.width/2, self.height/2, 0, y, c)
                self._led.drawLine(self.width/2, self.height/2, self.width-1, self.height-1-y, c)

            self._led.drawText("YOU", self.width/2-9, self.height/2-8, color=colors.Black, bg=None)
            self._led.drawText("WIN!", self.width/2-10, self.height/2+1, color=colors.Black, bg=None)
        else:
            if self.paused:
                self._led.all_off()
                if self.levelUp:
                    self._led.drawText("LVL", self.width/2-8, self.height/2-8)
                    l = "{}".format(self.level)
                    self._led.drawText(l, self.width/2-(len(l)*6)/2+1, self.height/2+1)
                else:
                    x = self.width/2-2
                    y = 1
                    self._led.drawText("P", x, y+0)
                    self._led.drawText("A", x, y+8)
                    self._led.drawText("U", x, y+16)
                    self._led.drawText("S", x, y+24)
                    self._led.drawText("E", x, y+32)
                    self._led.drawText("D", x, y+40)

            else:
                self.disp_msg("{}".format(self.score), 1, 1)

                lines_left = self.level*self.lines_per_level - self.lines
                for l in range(lines_left):
                    self._led.set(0, self.height-1-l*2, colors.Red)

                #draw rainbow border
                self._led.drawLine(2,8, cols+3, 8,
                    colorFunc=lambda pos: colors.hue_helper(pos, cols+2, self._speedStep*2))
                self._led.drawLine(2,self.height-1, cols+3, self.height-1,
                    colorFunc=lambda pos: colors.hue_helper(cols+2-pos, cols+2, self._speedStep*2))
                self._led.drawLine(2,9, 2, self.height-2,
                    colorFunc=lambda pos: colors.hue_helper(rows+2-pos, rows, self._speedStep*2))
                self._led.drawLine(cols+3,9, cols+3, self.height-2,
                    colorFunc=lambda pos: colors.hue_helper(pos, rows, self._speedStep*2))

                #draw current board state
                self.draw_matrix(self.board, (3,9))
                #draw current block
                self.draw_matrix(self.stone, (self.stone_x + 3, self.stone_y+9))
                #draw next block
                self.draw_matrix(self.next_stone, (self.width-4, 1))
                #drop block
                if self.checkSpeed("drop"):
                    self.drop(False)

        self._step += amt
