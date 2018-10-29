from pygame import *
init()
mixer.pre_init(44100, 16, 2, 4096)
# size = (500, 500)
size = width, height = 500, 480

# creates a window
win = display.set_mode(size)

# setting caption
display.set_caption("Game: movement")

clock = time.Clock()

bulletSound = mixer.Sound('bullet.wav')

music = mixer.music.load('images/music.mp3')
mixer.music.play(-1)

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
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

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

        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # draw.rect(win, (250, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 8
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width() / 2), 200))
        display.update()
        i = 0
        while i < 300:
            time.delay(10)
            i += 1
            for e in event.get():
                if e.type == QUIT:
                    i = 301
                    quit()

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
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

        self.hitCounter = 0

    def draw(self, win):
        self.move()
        if self.visible and (self.health > 0):
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            draw.rect(win, (250, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50//10) * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # draw.rect(win, (250, 0, 0), self.hitbox, 2)

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

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        self.hitCounter += 1


def redrawGameWindow():
    win.blit(bg, (0, 0))
    man.draw(win)
    text = foop.render("Score:" + str(foo.hitCounter), 1, (0, 0, 0))
    win.blit(text,  (360, 10))
    for bullet in bullets:
        bullet.draw(win)
    foo.draw(win)
    display.update()


# mainloop
foop = font.SysFont("comicsans", 30, True)
man = player(200, 410, 64, 64)
bullets = []
shoot_cdr = 0
foo = enemy(100, 410, 64, 64, 300)
run = True
while run:
    clock.tick(30)
    if foo.health > 0:
        if man.hitbox[1] < foo.hitbox[1] + foo.hitbox[3] and man.hitbox[1] + man.hitbox[3] > foo.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > foo.hitbox[0] and man.hitbox[0] < foo.hitbox[0] + foo.hitbox[2]:
                man.hit()
                foo.hitCounter -= 5
    if shoot_cdr > 0:
        shoot_cdr += 1
    if shoot_cdr > 5:
        shoot_cdr = 0

    for e in event.get():
        if e.type == QUIT:
            run = False

    for bullet in bullets:
        if foo.health > 0:
            if bullet.y - bullet.radius < foo.hitbox[1] + foo.hitbox[3] and bullet.y + bullet.radius > foo.hitbox[1]:
                if bullet.x + bullet.radius > foo.hitbox[0] and bullet.x - bullet.radius < foo.hitbox[0] + foo.hitbox[2]:
                    foo.hit()
                    bullets.pop(bullets.index(bullet))

        if (bullet.x < 500) and (bullet.x > 0):
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = key.get_pressed()

    if keys[K_SPACE] and shoot_cdr == 0:
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), -1 if man.left else 1))
            bulletSound.play()
        shoot_cdr = 1

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

    if not man.isJump:
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
