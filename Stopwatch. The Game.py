# Mini-project #3 - "Stopwatch: The Game"
#
# 'Introduction to Interactive Programming in Python' Course
# RICE University - coursera.org
# by Joe Warren, John Greiner, Stephen Wong, Scott Rixner
#
# Student: Vladimir Salitrinskij

import simplegui

# define global variables
games = 0  		# the number of games
win_games = 0		# the number of games won
clock = 0			# timer
msec = 0			# millisecond
stop_clock = False	# Stop or Start timer?

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    # Split into minute, second and millisecond
    global msec
    
    minute = t // 1000
    sec = (t - minute * 1000) // 10
    msec = (t - minute * 1000) % 10
    
    if sec < 10:
        return str(minute) + ":0" + str(sec) + "." + str(msec)
    else:
        return str(minute) + ":" + str(sec) + "." + str(msec)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global stop_clock
    
    if stop_clock == False:
        timer.start()
        stop_clock = True

def stop():
    global games, win_games, stop_clock
    
    if stop_clock == True:
        timer.stop()
        stop_clock = False
        
        games += 1
        if msec == 0:
            win_games += 1

def reset():
    global games, win_games, clock, msec, stop_clock
    
    if stop_clock == True:
        timer.stop()
        stop_clock = False
    
    games = 0
    win_games = 0
    clock = 0
    msec = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global clock
    
    clock += 1
    # 60 sec == 1 min
    if clock - clock // 1000 * 1000 == 600:
        clock += 400

# define draw handler
def draw(canvas):
    canvas.draw_text(str(win_games)+"/"+str(games), [150, 20], 20, "Green")
    canvas.draw_text(format(clock),[70, 110], 28, "White")

# create frame and timer
frame = simplegui.create_frame("Stopwatch: The Game", 200, 200)
timer = simplegui.create_timer(100, tick)

# register event handlers
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

# register draw handler    
frame.set_draw_handler(draw)

# start frame
frame.start()
