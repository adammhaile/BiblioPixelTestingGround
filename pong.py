import sys
try:
    from sdl2 import *
    import sdl2.ext as sdl2ext
except ImportError:
    import traceback
    traceback.print_exc()
    sys.exit(1)

WHITE = sdl2ext.Color(255, 255, 255)


class TrackingAIController(sdl2ext.Applicator):
    def __init__(self, miny, maxy):
        super(TrackingAIController, self).__init__()
        self.componenttypes = (PlayerData, Velocity, sdl2ext.Sprite)
        self.miny = miny
        self.maxy = maxy
        self.ball = None

    def process(self, world, componentsets):
        for pdata, vel, sprite in componentsets:
            if not pdata.ai:
                continue

            centery = sprite.y + sprite.size[1] // 2
            if self.ball.velocity.vx < 0:
                # ball is moving away from the AI
                if centery < self.maxy // 2:
                    vel.vy = 3
                elif centery > self.maxy // 2:
                    vel.vy = -3
                else:
                    vel.vy = 0
            else:
                bcentery = self.ball.sprite.y + self.ball.sprite.size[1] // 2
                if bcentery < centery:
                    vel.vy = -3
                elif bcentery > centery:
                    vel.vy = 3
                else:
                    vel.vy = 0


class PlayerData(object):
    def __init__(self):
        super(PlayerData, self).__init__()
        self.ai = False


class CollisionSystem(sdl2ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(CollisionSystem, self).__init__()
        self.componenttypes = (Velocity, sdl2ext.Sprite)
        self.ball = None
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def _overlap(self, item):
        pos, sprite = item[0], item[1]
        if sprite == self.ball.sprite:
            return False

        left, top, right, bottom = sprite.area
        bleft, btop, bright, bbottom = self.ball.sprite.area

        return bleft < right and bright > left and \
            btop < bottom and bbottom > top

    def process(self, world, componentsets):
        collitems = [comp for comp in componentsets if self._overlap(comp)]
        if len(collitems) != 0:
            self.ball.velocity.vx = -self.ball.velocity.vx

            sprite = collitems[0][1]
            ballcentery = self.ball.sprite.y + self.ball.sprite.size[1] // 2
            halfheight = sprite.size[1] // 2
            stepsize = halfheight // 10
            degrees = 0.7
            paddlecentery = sprite.y + halfheight
            if ballcentery < paddlecentery:
                factor = (paddlecentery - ballcentery) // stepsize
                self.ball.velocity.vy = -int(round(factor * degrees))
            elif ballcentery > paddlecentery:
                factor = (ballcentery - paddlecentery) // stepsize
                self.ball.velocity.vy = int(round(factor * degrees))
            else:
                self.ball.velocity.vy = - self.ball.velocity.vy


class MovementSystem(sdl2ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = (Velocity, sdl2ext.Sprite)
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        for velocity, sprite in componentsets:
            swidth, sheight = sprite.size
            sprite.x += velocity.vx
            sprite.y += velocity.vy

            sprite.x = max(self.minx, sprite.x)
            sprite.y = max(self.miny, sprite.y)

            pmaxx = sprite.x + swidth
            pmaxy = sprite.y + sheight
            if pmaxx > self.maxx:
                sprite.x = self.maxx - swidth
            if pmaxy > self.maxy:
                sprite.y = self.maxy - sheight


class Velocity(object):
    def __init__(self):
        super(Velocity, self).__init__()
        self.vx = 0
        self.vy = 0


class SoftwareRenderer(sdl2ext.SoftwareSpriteRenderer):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2ext.fill(self.surface, sdl2ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)


class Player(sdl2ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0, ai=False):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()
        self.playerdata = PlayerData()
        self.playerdata.ai = ai


class Ball(sdl2ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()


def run():
    sdl2ext.init()
    window = sdl2ext.Window("The Pong Game", size=(800, 600))
    window.show()

    world = sdl2ext.World()

    aicontroller = TrackingAIController(0, 600)
    collision = CollisionSystem(0, 0, 800, 600)
    movement = MovementSystem(0, 0, 800, 600)
    spriterenderer = SoftwareRenderer(window)

    world.add_system(aicontroller)
    world.add_system(collision)
    world.add_system(movement)
    world.add_system(spriterenderer)

    factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
    sp_paddle1 = factory.from_color(WHITE, size=(20, 100))
    sp_paddle2 = factory.from_color(WHITE, size=(20, 100))
    sp_ball = factory.from_color(WHITE, size=(20, 20))

    player1 = Player(world, sp_paddle1, 0, 250)
    player2 = Player(world, sp_paddle2, 780, 250, True)

    ball = Ball(world, sp_ball, 390, 290)
    ball.velocity.vx = -3

    collision.ball = ball
    aicontroller.ball = ball

    running = True
    while running:
        events = sdl2ext.get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
                break
            if event.type == SDL_KEYDOWN:
                if event.key.keysym.sym == SDLK_UP:
                    player1.velocity.vy = -3
                elif event.key.keysym.sym == SDLK_DOWN:
                    player1.velocity.vy = 3
            elif event.type == SDL_KEYUP:
                if event.key.keysym.sym in (SDLK_UP, SDLK_DOWN):
                    player1.velocity.vy = 0

        SDL_Delay(10)
        world.process()


if __name__ == "__main__":
    sys.exit(run())
