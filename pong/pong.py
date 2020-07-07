# Simple pong in Python 3 for beginers 
# @Dennis van den Berg
# Prt 1: Getting started 

# With turtle you can make some basic graphics
import turtle
import os

window = turtle.Screen()
window.title("Pong by @Dennis")
window.bgcolor("Black")
window.setup(width=800, height=600)
window.tracer(0) 	# Stop the window of updating th whole time, so we can run the game faster

# Score
score_a = 0
score_b = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()	# I don't know exacly but it has something to do with drawing a line 
paddle_a.goto(-350, 0)
paddle_a.down = False
paddle_a.up = False

# Paddle B 
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()	# I don't know exacly but it has something to do with drawing a line 
paddle_b.goto(350, 0)
paddle_b.down = False
paddle_b.up = False

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()	# I don't know exacly but it has something to do with drawing a line 
ball.goto(0, 0)
ball.dx = 0.3 # dx and dy define the movement of the ball by 2 px at each update
ball.dy = -0.3

# Functions 
# Paddle A
def paddle_a_set_up():
	paddle_a.up = True

def paddle_a_unset_up():
	paddle_a.up= False

def paddle_a_up():
	y = paddle_a.ycor()
	if y < 250:
		y += 0.5
	paddle_a.sety(y)

def paddle_a_set_down():
	paddle_a.down = True

def paddle_a_unset_down():
	paddle_a.down= False

def paddle_a_down():
	y = paddle_a.ycor()
	if y > -250:
		y -= 0.5
	paddle_a.sety(y)

# Paddle B
def paddle_b_set_up():
	paddle_b.up = True

def paddle_b_unset_up():
	paddle_b.up= False

def paddle_b_up():
	y = paddle_b.ycor()
	if y < 250:
		y += 0.5
	paddle_b.sety(y)

def paddle_b_set_down():
	paddle_b.down = True

def paddle_b_unset_down():
	paddle_b.down= False

def paddle_b_down():
	y = paddle_b.ycor()
	if y > -250:
		y -= 0.5
	paddle_b.sety(y)

# Pen (to draw the scores)
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0 | Player B: 0", align="center", font=('Courier', 24, 'normal'))


# Keyboard binding
window.onkeypress(paddle_a_set_up, "w")
window.onkeyrelease(paddle_a_unset_up, "w")

window.onkeypress(paddle_a_set_down, "s")
window.onkeyrelease(paddle_a_unset_down, "s")

window.onkeypress(paddle_b_set_up, "Up")
window.onkeyrelease(paddle_b_unset_up, "Up")

window.onkeypress(paddle_b_set_down, "Down")
window.onkeyrelease(paddle_b_unset_down, "Down")

window.listen()

# Main game loop
while True:
	window.update()
	# Move paddle A
	if paddle_a.up:
		paddle_a_up()
	if paddle_a.down:
		paddle_a_down()
	if paddle_b.up:
		paddle_b_up()
	if paddle_b.down:
		paddle_b_down()

	# Move the Ball
	ball.setx(ball.xcor() + ball.dx)
	ball.sety(ball.ycor() + ball.dy)

	# Border Checking
	if ball.ycor() > 290:
		ball.sety(290)
		ball.dy *= -1
		os.system("aplay bounce.wav&")

	if ball.ycor() < -290:
		ball.sety(-290)
		ball.dy *= -1
		os.system("aplay bounce.wav&")

	if ball.xcor() > 390: 
		ball.goto(0, 0)
		ball.dx *= -1
		score_a += 1
		os.system("aplay point.wav&")
		pen.clear()
		pen.write("Player A: {} | Player B: {}".format(score_a,score_b), align="center", font=('Courier', 24, 'normal'))

	if ball.xcor() < -390: 
		ball.goto(0, 0)
		ball.dx *= -1
		score_b += 1
		os.system("aplay point.wav&")
		pen.clear()
		pen.write("Player A: {} | Player B: {}".format(score_a,score_b), align="center", font=('Courier', 24, 'normal'))

	# Paddle and Ball collisions 
	if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40):
		ball.setx(340)
		ball.dx *= -1
		os.system("aplay bounce.wav&")

	if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40):
		ball.setx(-340)
		ball.dx *= -1
		os.system("aplay bounce.wav&")