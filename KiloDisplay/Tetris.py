#Based on: https://gist.github.com/kch42/565419


from random import randrange as rand

import bibliopixel.colors as colors
from bibliopixel.animation import BaseGameAnim
import math
from random import randint
import bibliopixel.util as util


# The configuration
cell_size =	18
cols =		25
rows =		50
maxfps = 	30

colors = [
(0,   0,   0  ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
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
    board = [ [ 0 for x in xrange(cols) ]
            for y in xrange(rows) ]
    board += [[ 1 for x in xrange(cols)]]
    return board

class Tetris(BaseGameAnim):
    def __init__(self, led, inputDev):
        super(Tetris, self).__init__(led, inputDev)

        self.width = cell_size*(cols+6)
        self.height = cell_size*rows
        self.rlim = cell_size*cols
        self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in xrange(cols)] for y in xrange(rows)]

        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
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
        self._key_actions = {
            # 'ESCAPE':	self.quit,
            'LEFT':		lambda:self.move(-1),
            'RIGHT':	lambda:self.move(+1),
            'DOWN':		lambda:self.drop(True),
            'UP':		self.rotate_stone,
            # 'p':		self.toggle_pause,
            'FIRE':	self.start_game,
            # 'RETURN':	self.insta_drop
        }

        self.gameover = False
        self.paused = False
        self.board = new_board()
        self.new_stone()
        self.level = 1
        self.score = 0
        self.lines = 0
        self._last_up = False
        self._last_move = {"RIGHT": False, "LEFT": False}

        self.setSpeed("drop", 5)
        self.setSpeed("move", 2)
        # pygame.time.set_timer(pygame.USEREVENT+1, 1000)

    def disp_msg(self, msg, topleft):
        pass
        # x,y = topleft
        # for line in msg.splitlines():
        # 	self.screen.blit(
        # 		self.default_font.render(
        # 			line,
        # 			False,
        # 			(255,255,255),
        # 			(0,0,0)),
        # 		(x,y))
        # 	y+=14

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
                    self._led.set(off_x+x,off_y+y,colors[val])
                    # pygame.draw.rect(self.screen,colors[val],
                    # 	pygame.Rect(
                    # 		(off_x+x) *
                    # 		  cell_size,
                    # 		(off_y+y) *
                    # 		  cell_size,
                    # 		cell_size,
                    # 		cell_size),0)

    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        # if self.lines >= self.level*6:
        # 	self.level += 1
        # 	newdelay = 1000-50*(self.level-1)
        # 	newdelay = 100 if newdelay < 100 else newdelay
        # 	pygame.time.set_timer(pygame.USEREVENT+1, newdelay)

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
                    for i, row in enumerate(self.board[:-1]):
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
            self.center_msg("""Game Over!\nYour score: %d Press space to continue""" % self.score)
        else:
            if self.paused:
                self.center_msg("Paused")
            else:
                # pygame.draw.line(self.screen,
                #     (255,255,255),
                #     (self.rlim+1, 0),
                #     (self.rlim+1, self.height-1))
                self.disp_msg("Next:", (self.rlim+cell_size,2))
                self.disp_msg("Score: %d\n\nLevel: %d\\nLines: %d" % (self.score, self.level, self.lines),(self.rlim+cell_size, cell_size*5))
                self.draw_matrix(self.bground_grid, (0,0))
                self.draw_matrix(self.board, (0,0))
                self.draw_matrix(self.stone,
                    (self.stone_x, self.stone_y))
                self.draw_matrix(self.next_stone,
                    (cols+1,2))

        for key in self._keys:
            if key == "UP":
                if not self._last_up and self._keys[key]:
                    self._key_actions[key]()
                self._last_up = self._keys[key]
            elif key == "LEFT" or key == "RIGHT":
                if self.checkSpeed("move"):
                    if self._last_move[key] or self._keys[key]:
                        self._key_actions[key]()
                    else:
                        self._last_move[key] = self._keys[key]
            elif self._keys[key]:
                self._key_actions[key]()


        if self.checkSpeed("drop"):
            self.drop(False)

        self._step += amt
        # for event in pygame.event.get():
        # 	if event.type == pygame.USEREVENT+1:
        # 		self.drop(False)
        # 	elif event.type == pygame.QUIT:
        # 		self.quit()
        # 	elif event.type == pygame.KEYDOWN:
        # 		for key in key_actions:
        # 			if event.key == eval("pygame.K_"
        # 			+key):
        # 				key_actions[key]()
        #
        # dont_burn_my_cpu.tick(maxfps)
