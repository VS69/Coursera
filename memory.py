# Mini-project #5 - "Memory"
#
# 'Introduction to Interactive Programming in Python' Course
# RICE University - coursera.org
# by Joe Warren, John Greiner, Stephen Wong, Scott Rixner
#
# Student: Vladimir Salitrinskij

import simplegui
import random

# Load images
image_card_back = simplegui.load_image("https://dl.dropboxusercontent.com/u/40444366/card_back.png?dl=1")
image_cards = simplegui.load_image("https://dl.dropboxusercontent.com/u/40444366/cards.png?dl=1")

# Global variables
CARD_WIDTH = 71
CARD_HEIGHT = 96
CANVAS_WIDTH = CARD_WIDTH * 4 - 1
CANVAS_HEIGHT = CARD_HEIGHT * 4 - 1

# Helper function to initialize globals
def init():
    global state, moves, face_down, cards
    
    x_pos = [37, 110, 183, 256, 329, 402, 475, 548, 621, 694, 767, 840, 913]
    y_pos = (49, 147, 245, 343)
    state = 0
    moves = 0
    
    label.set_text("Moves = " + str(moves))
    
    face_down = []
    for i in range(16):
        face_down.append(True)
    
    cards = []
    i = 0
    while i < 8:
        rnd_x = random.randrange(0, 13)
        if x_pos[rnd_x] != 0:
            cards.append([x_pos[rnd_x], y_pos[random.randrange(0, 4)]])
            x_pos[rnd_x] = 0
            i += 1
    cards += cards
    random.shuffle(cards)

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, moves, first_index, second_index
    
    i = 0
    for r in range(4):
        for c in range(4):
            if CARD_WIDTH * c < pos[0] < CARD_WIDTH * (c + 1) and CARD_HEIGHT * r < pos[1] < CARD_HEIGHT * (r + 1):
                if face_down[i]:
                    face_down[i] = False
                    if state == 0:
                        first_index = i
                    elif state == 1:
                        second_index = i
                        moves += 1
                        label.set_text("Moves = " + str(moves))
                    elif state == 2:
                        if cards[first_index][0] != cards[second_index][0]:
                            face_down[second_index], face_down[first_index] = True, True
                        first_index = i
                        state = 0
                    state += 1
            i += 1

# cards 71x96 pixels in size
def draw(canvas):
    # Draw cards
    for r in range(4):
        for c in range(4):
            if face_down[r * 4 + c]:
                canvas.draw_image(image_card_back,
                                  [CARD_WIDTH // 2, CARD_HEIGHT // 2], [CARD_WIDTH, CARD_HEIGHT],
                                  [CARD_WIDTH * (c + 1) - CARD_WIDTH // 2 - 1, CARD_HEIGHT * (r + 1) - CARD_HEIGHT // 2 - 1],
                                  [CARD_WIDTH, CARD_HEIGHT])
            else:
                canvas.draw_image(image_cards,
                                  [cards[r * 4 + c][0], cards[r * 4 + c][1]], [CARD_WIDTH, CARD_HEIGHT],
                                  [CARD_WIDTH * (c + 1) - CARD_WIDTH // 2 - 1, CARD_HEIGHT * (r + 1) - CARD_HEIGHT // 2 - 1],
                                  [CARD_WIDTH, CARD_HEIGHT])
                

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
