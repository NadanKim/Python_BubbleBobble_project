from pico2d import *
import random

class SKULL():
    TYPE = 'SKULL'
    DIRECT_LEFT, DIRECT_RIGHT, DIRECT_UP, DIRECT_DOWN = 0, 1, 2, 3
    STATE_WALK, STATE_ANGRY, STATE_AFRAID, STATE_DEAD = 3, None, None, 1
    STATE_STUCK_GREEN, STATE_STUCK_YELLOW, STATE_STUCK_RED, STATE_PON, STATE_NONE = None, None, None, None, 99
    PIXEL_PER_METER = (10.0 / 0.3)
    MOVE_SPEED_KMPH = 6.0
    FLY_SPEED_KMPH = 6.0
    XSIZE, YSIZE = 50, 70
    sprite = None
    appearSound = None

    def __init__(self, x, y):
        self.stayTime = 6.0
        self.x = x
        self.y = y
        self.playerX = 0
        self.playerY = 0
        self.moveSpeedPPS = self.change_moveSpeed(self.MOVE_SPEED_KMPH)
        self.flySpeedPPS = self.change_moveSpeed(self.FLY_SPEED_KMPH)
        self.direct = random.randint(0, 1)
        self.directTemp = self.direct
        self.yDirect = random.randint(2, 3)
        self.state = self.STATE_WALK
        self.frame, self.totalFrame = 0, 0
        self.actionPerTime = 1.0 / 1.5
        self.frameTime = 0.0
        self.stateTemp = None
        if SKULL.sprite == None:
            SKULL.sprite = load_image('sprite\\Enemy\\skull.png')
        if SKULL.appearSound == None:
            SKULL.appearSound = load_wav('GameSound\\Surround\\SkullAppear.wav')
            SKULL.appearSound.set_volume(32)
        self.xSprite = 16
        self.ySprite = 16
        self.numSprite = 12
        self.appearSound.play()


    def change_moveSpeed(self, MOVE_SPEED_KMPH):
        moveSpeedMPM = MOVE_SPEED_KMPH * 1000.0 / 60.0
        moveSpeedMPS = moveSpeedMPM / 60.0
        return moveSpeedMPS * self.PIXEL_PER_METER


    def get_bb(self):
        return self.x - self.XSIZE * 2 / 5, self.y - self.YSIZE / 2, self.x + self.XSIZE * 2 / 5, self.y + self.YSIZE /2


    def get_bb_left(self):
        return self.x - self.XSIZE * 2 / 5


    def get_bb_right(self):
        return self.x + self.XSIZE * 2 / 5


    def get_bb_top(self):
        return self.y + self.YSIZE /2


    def get_bb_bottom(self):
        return self.y - self.YSIZE / 2


    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def set_player_loc(self, x, y):
        self.playerX = x
        self.playerY = y


    def handle_walk(self):
        if self.x < self.playerX:
            self.direct = self.DIRECT_RIGHT
        else:
            self.direct = self.DIRECT_LEFT
        if self.y < self.playerY:
            self.yDirect = self.DIRECT_UP
        else:
            self.yDirect = self.DIRECT_DOWN
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x - self.moveSpeedPPS * self.frameTime)
            if self.x == self.XSIZE/2 + 50:
                self.direct = self.DIRECT_RIGHT
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime)
            if self.x == 1200 - self.XSIZE/2 - 50:
                self.direct = self.DIRECT_LEFT
        if self.yDirect == self.DIRECT_UP:
            self.y = self.y + self.moveSpeedPPS * self.frameTime
            if 675 < self.y - self.YSIZE:
                self.y = -self.YSIZE/2
        elif self.yDirect == self.DIRECT_DOWN:
            self.y = self.y - self.moveSpeedPPS * self.frameTime
            if self.y + self.YSIZE < 0:
                self.y = 675



    def handle_angry(self):
        pass


    def handle_afraid(self):
        pass


    def handle_dead(self):
        if 10 <= self.totalFrame:
            self.state = self.STATE_NONE


    def handle_stuck(self):
        pass


    def handle_pon(self):
        pass


    def handle_none(self):
        pass


    handle_state = {
        STATE_WALK: handle_walk,
        STATE_ANGRY: handle_angry,
        STATE_AFRAID: handle_afraid,
        STATE_DEAD: handle_dead,
        STATE_STUCK_GREEN: handle_stuck,
        STATE_STUCK_YELLOW: handle_stuck,
        STATE_STUCK_RED: handle_stuck,
        STATE_PON: handle_pon,
        STATE_NONE: handle_none
    }


    def update(self, frameTime):
        self.frameTime = frameTime
        #change frames
        self.totalFrame += self.numSprite * self.actionPerTime * self.frameTime
        self.frame = int(self.totalFrame) % self.numSprite
        #change state
        if self.stayTime == 0:
            self.handle_state[self.state](self)
        else:
            self.stayTime -= frameTime
            if self.stayTime < 0:
                self.stayTime = 0


    def draw(self):
        self.sprite.clip_draw(self.xSprite * self.frame, self.ySprite * (self.state - (self.direct % 2)), self.xSprite, self.ySprite, self.x, self.y, self.XSIZE, self.YSIZE)


    def isPop(self):
        if self.state == self.STATE_NONE:
            return True
        else:
            return False