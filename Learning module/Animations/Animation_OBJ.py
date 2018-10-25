from pygame import *

# size = (500, 500)
size = width, height = 500, 480

# creates a window
win = display.set_mode(size)

# setting caption
display.set_caption("Game: movement")

walkRight = [image.load("images/R" + str(i) + ".png") for i in range(1, 10)]
walkLeft = [image.load("images/L" + str(i) + ".png") for i in range(1, 10)]
bg = image.load("images/bg.jpg")
char = image.load("images/standing.png")

clock = time.Clock()


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(char, (self.x, self.y))


def redrawGameWindow():
    win.blit(bg, (0, 0))
    man.draw(win)

    display.update()


# mainloop
man = player(200, 410, 64, 64)
run = True
while run:
    clock.tick(27)

    for e in event.get():
        if e.type == QUIT:
            run = False

    keys = key.get_pressed()

    if keys[K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
    elif keys[K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
    else:
        man.right = False
        man.left = False
        man.walkCount = 0

    if not (man.isJump):
        if keys[K_SPACE]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            man.y -= (man.jumpCount * abs(man.jumpCount)) * 0.5
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()



quit()
