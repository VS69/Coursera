# Mini-project #7 - Spaceship
#
# 'Introduction to Interactive Programming in Python' Course
# RICE University - coursera.org
# by Joe Warren, John Greiner, Stephen Wong, Scott Rixner
#
# Student: Vladimir Salitrinskij

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
UP = 0.12       # pixel/sec.
DOWN = 0.4 / 60 # 40% decrease in sec 
ANGL_VEL = math.pi / 30 # one turn in second
CLCK_WISE = {simplegui.KEY_MAP["left"] : False, simplegui.KEY_MAP["right"] : True}
R_AV_LIM = (-math.pi / 15, math.pi / 15)
R_V_LIM = (-5, 5)

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated
    
    def get_center(self):
        return self.center
    
    def get_size(self):
        return self.size
    
    def get_radius(self):
        return self.radius
    
    def get_lifespan(self):
        return self.lifespan
    
    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([WIDTH / 10 * 4, HEIGHT / 10 * 4], [WIDTH / 10 * 8, HEIGHT / 10 * 8])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris1_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([WIDTH / 4, HEIGHT / 4], [WIDTH / 2, HEIGHT / 2])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_size = info.get_size()
        self.image_center = info.get_center()
        self.image_center_go = [self.image_center[0] + self.image_size[0], self.image_center[1]]
        self.radius = info.get_radius()
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, self.image_center_go, self.image_size, 
                          self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)
    
    def update(self):
        self.vel[0] *= (1 - DOWN)
        self.vel[1] *= (1 - DOWN)
        
        if self.thrust:
            vector = angle_to_vector(self.angle)
            self.vel[0] += UP * vector[0]
            self.vel[1] += UP * vector[1]
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
    
    def change_angle_vel(self, is_clckws, down):
        if down:
            if is_clckws:
                self.angle_vel += ANGL_VEL
            else:
                self.angle_vel -= ANGL_VEL
        else:
            if is_clckws:
                self.angle_vel -= ANGL_VEL
            else:
                self.angle_vel += ANGL_VEL
    
    def thrust_switch(self):
        self.thrust = not self.thrust
        if self.thrust:
            ship_thrust_sound.play()
            sound.start()
        else:
            sound.stop()
            ship_thrust_sound.rewind()
    
    def shoot(self):
        global a_missile
        vector = angle_to_vector(self.angle)
        begin_x = self.pos[0] + (self.image_size[0] / 2) * angle_to_vector(my_ship.angle)[0]
        begin_y = self.pos[1] + (self.image_size[1] / 2) * angle_to_vector(my_ship.angle)[1]
        vel_x = angle_to_vector(self.angle)[0] * 15
        vel_y = angle_to_vector(self.angle)[1] * 15
        a_missile = Sprite([begin_x, begin_y], [vel_x, vel_y], 0, 0, missile_image, missile_info, missile_sound)

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_size = info.get_size()
        self.image_center = info.get_center()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
    
        if sound:
            sound.rewind()
            sound.play()
    
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % WIDTH
        self.angle += self.angle_vel

# Function "draw"
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                    [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                    [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])
    
    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # draw lives and score
    canvas.draw_text("Lives", [20, 30], 22, "White")
    canvas.draw_text(str(lives), [20, 55], 22, "White")
    
    canvas.draw_text("Score", [720, 30], 22, "White")
    canvas.draw_text(str(score), [720, 55], 22, "White")

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()

def sound_restart():
    ship_thrust_sound.rewind()
    ship_thrust_sound.play()

# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    vel_x = random.random() * (R_V_LIM[1] - R_V_LIM[0]) + R_V_LIM[0]
    vel_y = random.random() * (R_V_LIM[1] - R_V_LIM[0]) + R_V_LIM[0]
    vel_angle = random.random() * (R_AV_LIM[1] - R_AV_LIM[0]) + R_AV_LIM[0]
    angle = random.random() * 2 * math.pi
    a_rock = Sprite([WIDTH * random.random(), HEIGHT * random.random()], [vel_x, vel_y], angle, vel_angle, asteroid_image, asteroid_info)

#key handlers
def down(key):
    if key in CLCK_WISE.keys():
        my_ship.change_angle_vel(CLCK_WISE[key], True)
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_switch()
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        
def up(key):
    if key in CLCK_WISE.keys():
        my_ship.change_angle_vel(CLCK_WISE[key], False)  
    if key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_switch()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([-10, -10], [0, 0], my_ship.angle, 0, missile_image, missile_info, missile_sound)    

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(down)
frame.set_keyup_handler(up)

timer = simplegui.create_timer(1000.0, rock_spawner)
sound = simplegui.create_timer(25000.0, sound_restart)

# get things rolling
timer.start()
frame.start()
