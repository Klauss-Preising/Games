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
        self.jumpCount = 8
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        draw.circle(win, self.color, (self.x,self.y), self.radius)


class enemy(object):
    walkRight = [image.load("images/R" + str(i) + "E.png") for i in range(1, 12)]
    walkLeft = [image.load("images/L" + str(i) + "E.png") for i in range(1, 12)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0


def redrawGameWindow():
    win.blit(bg, (0, 0))
    man.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    foo.draw(win)
    display.update()


# mainloop
man = player(200, 410, 64, 64)
bullets = []
foo = enemy(100, 410, 64, 64, 300)
run = True
while run:
    clock.tick(27)

    for e in event.get():
        if e.type == QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = key.get_pressed()

    if keys[K_SPACE]:
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), -1 if man.left else 1))


    if keys[K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not (man.isJump):
        if keys[K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -8:
            man.y -= (man.jumpCount * abs(man.jumpCount)) * 0.5
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 8

    redrawGameWindow()



quit()
