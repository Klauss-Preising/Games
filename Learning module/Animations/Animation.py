from pygame import *

# size = (500, 500)
size = width, height = 500, 480

# creates a window
win = display.set_mode(size)

# setting caption
display.set_caption("Game: movement")

# setting object settings
x_object = 50
y_object = 400
width_object = 64
height_object = 64
speed_object = 5

isJump = False
jumpCount = 8

left = False
right = False
walkCount = 0

walkRight = [image.load("images/R" + str(i) + ".png") for i in range(1, 10)]
walkLeft = [image.load("images/L" + str(i) + ".png") for i in range(1, 10)]
bg = image.load("images/bg.jpg")
char = image.load("images/standing.png")

clock = time.Clock()



def redrawGameWindow():
    global walkCount

    win.blit(bg, (0,0))

    if walkCount + 1 >= 27:
        walkCount = 0

    if left:
        win.blit(walkLeft[walkCount % len(walkLeft)], (x_object, y_object))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount % len(walkLeft)], (x_object, y_object))
        walkCount += 1
    else:
        win.blit(char, (x_object, y_object))




    display.update()


run = True
while run:

    # delay in ms
    clock.tick(27)

    for e in event.get():
        if e.type == QUIT:
            run = False

    keys = key.get_pressed()

    if keys[K_LEFT] and x_object > speed_object:
        x_object -= speed_object
        left = True
        right = False
    elif keys[K_RIGHT] and x_object < width - width_object - speed_object:
        x_object += speed_object
        left = False
        right = True
    else:
        right = False
        left = False
        walkCount = 0

    if not isJump:
        if keys[K_SPACE]:
            isJump = True
            right = False
            left = False
            walkCount = 0
    else:
        if jumpCount >= -8:
            y_object -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 8

    redrawGameWindow()


quit()
