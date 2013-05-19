# Mini-project #2 - "Guess the number"
#
# 'Introduction to Interactive Programming in Python' Course
# RICE University - coursera.org
# by Joe Warren, John Greiner, Stephen Wong, Scott Rixner
#
# Student: Vladimir Salitrinskij

# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables used in your code
num_range = 0  # given range
rem_guess = 0	# the number of allowed guesses
number = 0		# secret computer number
user_num = 0	# user number

# define event handlers for control panel

def range100():
    # button that changes range to range [0,100) and restarts
    global num_range
    global rem_guess
    global number
    
    num_range = 100
    rem_guess = math.ceil(math.log(num_range, 2))
    number = random.randrange(0, num_range)
    
    print "New game. Range is from 0 to", num_range
    print "Number of remaining guesses is", rem_guess, "\n"

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range
    global rem_guess
    global number
    
    num_range = 1000
    rem_guess = math.ceil(math.log(num_range, 2))
    number = random.randrange(0, num_range)
    
    print "New game. Range is from 0 to", num_range
    print "Number of remaining guesses is", rem_guess, "\n"

def input_guess(guess):
    global user_num
    global rem_guess
    
    # exception handling, if the input simbols - not number
    try:
        user_num = int(guess)
    except ValueError:
        print "'%s' - You entered invalid characters!\n" %guess
        return
    
    # range checking
    if user_num < 0 or user_num >= num_range:
        print "You entered number is out of range!\n"
        return
    
    rem_guess -= 1
    
    print "Guess was", user_num
    print "Number of remaining guesses is", rem_guess
    
    if rem_guess > 0:
        if number == user_num:
            print "Correct!\n"
            if num_range == 100:
                range100()
            else:
                range1000()
        elif number > user_num:
            print "Higher!\n"
        else:
            print "Lower!\n"
    else:
        if number == user_num:
            print "Correct!\n"
        else:
            print "You ran out of guesses. The number was", number, "\n"
        if num_range == 100:
            range100()
        else:
            range1000()

# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)

range100()

# start frame
frame.start()
