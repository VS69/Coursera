# Mini-project #1 - "Rock-paper-scissors-lizard-Spock game"
#
# 'Introduction to Interactive Programming in Python' Course
# RICE University - coursera.org
# by Joe Warren, John Greiner, Stephen Wong, Scott Rixner
#
# Student: Vladimir Salitrinskij

import random

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def number_to_name(number):
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        return "The number is out of range!"
    
def name_to_number(name):
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        return "Invalid name!"

# Function implementation of the game RPSLS

def rpsls(name): 
    # convert name to player_number using name_to_number
    player_number = name_to_number(name)
    
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)
    
    # compute difference of player_number and comp_number modulo five
    difference = (player_number - comp_number) % 5
    
    # use if/elif/else to determine winner
    if difference == 0:
        result = "Player and computer tie!"
    elif difference == 1 or difference == 2:
        result = "Player wins!"
    else:
        result = "Computer wins!"
    
    # convert comp_number to name using number_to_name
    comp_name = number_to_name (comp_number)
    
    # print results
    print "Player chooses", name
    print "Computer chooses", comp_name
    print result
    if name != "scissors":
        print
    
# test my code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
