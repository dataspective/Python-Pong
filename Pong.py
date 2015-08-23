# Derek Fermaint
# 8/23/15
# two-player game of Pong
# Left player uses 'w' key to move paddle up, 's' key to move paddle down
# Right player uses 'up' arrow key to move paddle up and 'down' arrow key for down
import simplegui
import random
import math

# initialize globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# variables
score1 = 0
score2 = 0
paddle1_vel = 0
paddle2_vel = 0
ball_vel = 0
rand_left_right = random.randint(1,2)


# inititializes the velocity of the ball
# creates a velocity velocity and stores the x and y components
def ball_velocity():
    global ball_vel
    ball_vel_num = random.random() + 2
    ball_vel = [ ball_vel_num, ball_vel_num]
    ball_vel_vector = math.sqrt(math.pow(ball_vel[0], 2) + math.pow(ball_vel[1], 2))

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    global RIGHT, LEFT
    
    ball_pos = [ WIDTH / 2, HEIGHT / 2]
    ball_velocity()
    
    if (direction is 1):
        RIGHT = False
        LEFT = True
    elif (direction is 2):
        LEFT = False
        RIGHT = True

# defines event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global rand_left_right, RIGHT, LEFT
    
    #reset the score
    score1 = 0
    score2 = 0
    
    # set paddle positions to middle center, flush with sides
    paddle1_pos = [0, HEIGHT / 2 + 25]
    paddle2_pos = [WIDTH, HEIGHT / 2 + 25]
    
    # set initial paddle velocities
    paddle1_vel = 0
    paddle2_vel = 0
    
    # spawns ball
    spawn_ball(rand_left_right)

# draws the frames
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel
    global RIGHT, LEFT
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if (RIGHT is True):
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    elif(LEFT is True):
        ball_pos[0] -= ball_vel[0]
        ball_pos[1] -= ball_vel[1]
     
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 5, "White", "White")
        
    # update paddle's vertical position, keep paddle on the screen
    if(paddle1_pos[1] - 50 < 0):
        paddle1_pos[1] = 50
        paddle1_vel = 0
    elif(paddle1_pos[1] > HEIGHT):
        paddle1_pos[1] = HEIGHT
        paddle1_vel = 0
    else:
        paddle1_pos[1] += paddle1_vel
    
    if(paddle2_pos[1] - 50 < 0):
        paddle2_pos[1] = 50
        paddle2_vel = 0
    elif(paddle2_pos[1] > HEIGHT):
        paddle2_pos[1] = HEIGHT
        paddle2_vel = 0
    else:
        paddle2_pos[1] += paddle2_vel
    
    # draw paddles
    canvas.draw_line(paddle1_pos, [0, paddle1_pos[1] - 50], PAD_WIDTH, "White")
    canvas.draw_line(paddle2_pos, [WIDTH, paddle2_pos[1] - 50], PAD_WIDTH, "White")
    
    # determine whether paddle and ball collide  
    if(ball_pos[0] + BALL_RADIUS > WIDTH):
        if(ball_pos[1] + BALL_RADIUS > paddle2_pos[1] - 65 and 
           ball_pos[1] + BALL_RADIUS < paddle2_pos[1] + 15):
            ball_vel[0] = -(ball_vel[0] + 1)
        else:
            score1 += 1
            rand_left_right = random.randint(1,2)
            spawn_ball(rand_left_right)
     
    if(ball_pos[0] - BALL_RADIUS < 0):
        if(ball_pos[1] + BALL_RADIUS > paddle1_pos[1] - 65 and 
           ball_pos[1] + BALL_RADIUS < paddle1_pos[1] + 15):
            ball_vel[0] = -(ball_vel[0] + 1)
        else:
            score2 += 1
            rand_left_right = random.randint(1,2)
            spawn_ball(rand_left_right)
            
        
    if(ball_pos[1] + BALL_RADIUS > HEIGHT):
        ball_vel[1] = -ball_vel[1]
    if(ball_pos[1] - BALL_RADIUS < 0):
        ball_vel[1] = -ball_vel[1]
    
    # draw scores
    canvas.draw_text(str(score1), [(WIDTH / 2) - 63, 50], 32, "White")
    canvas.draw_text(str(score2), [(WIDTH / 2) + 50, 50], 32, "White")

# event handlers for keyboard controls
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key is simplegui.KEY_MAP['w']:
        if(paddle1_vel > - 2):
            paddle1_vel -= 4
    if key is simplegui.KEY_MAP["up"]:
        if(paddle2_vel > - 2):
            paddle2_vel -= 4
    if key is simplegui.KEY_MAP['s']:
         if(paddle1_vel < 2):
            paddle1_vel += 4
    if key is simplegui.KEY_MAP["down"]:
        if(paddle2_vel < 2):
            paddle2_vel += 4        

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
button = frame.add_button("Restart", new_game)


# start frame
new_game()
frame.start()
