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

        self.setSpeed("drop", 8)
        self.rlim = cols
        self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in xrange(cols)] for y in xrange(rows)]

        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]

        self.addKeyFunc("LEFT", lambda:self.move(-1), speed=2, hold=True)
        self.addKeyFunc("RIGHT", lambda:self.move(+1), speed=2, hold=True)
        self.addKeyFunc("DOWN", lambda:self.drop(True), speed=1, hold=True)
        self.addKeyFunc("UP", self.rotate_stone, speed=1, hold=False)
        self.addKeyFunc("FIRE", self.insta_drop, speed=1, hold=False)
        self.init_game()

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
        self.gameover = False
        self.paused = False
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

    def center_msg(self, msg):
        pass
        # for i, line in enumerate(msg.splitlines()):
        # 	msg_image =  self.default_font.render(line, False,
        # 		(255,255,255), (0,0,0))
        #
        # 	msgim_center_x, msgim_center_y = msg_image.get_size()
        # 	msgim_center_x //= 2
        # 	msgim_center_y //= 2
        #
        # 	self.screen.blit(msg_image, (
        # 	  self.width // 2-msgim_center_x,
        # 	  self.height // 2-msgim_center_y+i*22))

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
        if self.lines >= self.level*6:
            self.level += 1
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
        if self.gameover:
            self.init_game()
            self.gameover = False

    def step(self, amt=1):
        self._led.all_off()
        if self.gameover:
            self._led.all_off()
            self._led.drawText("GAME", self.width/2-11, self.height/2-8)
            self._led.drawText("OVER", self.width/2-11, self.height/2+1)
        else:
            if self.paused:
                self.center_msg("Paused")
            else:
                self.disp_msg("L{}".format(self.level), 0, 0)
                # self.disp_msg("Pts: {} Lvl: {} L: %d".format(self.score, self.level, self.lines), 0,0)
                self.draw_matrix(self.bground_grid, (3,9))
                self._led.drawRect(2,8,cols+2,rows+2, color_map[8])
                self.draw_matrix(self.board, (3,9))
                self.draw_matrix(self.stone, (self.stone_x + 3, self.stone_y+9))
                self.draw_matrix(self.next_stone, (self.width-4, 1))
                if self.checkSpeed("drop"):
                    self.drop(False)

        # for key in self._keys:
        #     if key == "UP":
        #         if not self._last_up and self._keys[key]:
        #             self._key_actions[key]()
        #         self._last_up = self._keys[key]
        #     elif key == "LEFT" or key == "RIGHT":
        #         if self.checkSpeed("move"):
        #             if self._last_move[key] or self._keys[key]:
        #                 self._key_actions[key]()
        #             else:
        #                 self._last_move[key] = self._keys[key]
        #     elif key == "FIRE":
        #         if self.gameover:
        #             if self._keys[key]:
        #                 self._lastFire = True
        #                 self.start_game()
        #         else:
        #             if self._keys[key] and not self._lastFire:
        #                 self._key_actions[key]()
        #             self._lastFire = self._keys[key]
        #     elif key in self._key_actions and self._keys[key]:
        #         self._key_actions[key]()

        self.handleKeys()

        self._step += amt
