from pygame import *

# size = (500, 500)
size = width, height = 500, 500

# creates a window
win = display.set_mode(size)

# setting caption
display.set_caption("Game: movement")

# setting object settings
x_object = 50
y_object = 50
width_object = 40
height_object = 60
speed_object = 5

run = True
while run:

    # delay in ms
    time.delay(60)

    for events in event.get():
        if events.type == QUIT:
            run = False

    keys = key.get_pressed()

    if keys[K_LEFT] and x_object > speed_object:
        x_object -= speed_object
    if keys[K_RIGHT] and x_object < width - width_object - speed_object:
        x_object += speed_object
    if keys[K_UP] and y_object > speed_object:
        y_object -= speed_object
    if keys[K_DOWN] and y_object < height - height_object - speed_object:
        y_object += speed_object

    win.fill((0, 0, 0))
    # surface, color, (x, y, width, height)
    draw.rect(win, (255, 0, 0), (x_object, y_object, width_object, height_object))
    display.update()

quit()
