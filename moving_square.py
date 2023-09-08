from typing import Any
from cmu_graphics import *
import cmu_graphics.cmu_graphics as cg
import math


class Vector2D:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __str__(self):		# when used as a string Vector2D is represented as "(x.xx, y.yy)"
		return "({:.2f}, {:.2f})".format(self.x, self.y)
	
	def __mul__(self, factor):		# scale vector by multiplying
		return Vector2D(self.x*factor, self.y*factor)
	
	def __truediv__(self, factor):	# scale vector by dividing
		return Vector2D(self.x/factor, self.y/factor)
	
	def __getmagnitude(self):
		return math.sqrt(self.x**2 + self.y**2)	# pythagorean theorem
	
	def normalize(self):
		mag = self.magnitude	# temporary variable
		if mag > 0:		# avoid division by zero
			self.x /= mag	# by scaling x and y, magnitude will also be scaled by the same factor
			self.y /= mag	# in this case, dividing the magnitude by itself will make it 1
	
	magnitude = property(__getmagnitude)



def onKeyHold(key):
	move_vector = Vector2D(0, 0)
	x_stopped = False	# indicates if a wall is hit on the x axis
	y_stopped = False	# indicates if a wall is hit on the y axis
	
	
	if 'right' in key or 'd' in key:
		if square.right >= 400:
			square.right = 400
			x_stopped = True
		else:
			move_vector.x += 1
	if 'left' in key or 'a' in key:
		if square.left <= 0:
			square.left = 0
			x_stopped = True
		else:
			move_vector.x -= 1
	if 'down' in key or 's' in key:
		if square.bottom >= 400:
			square.bottom = 400
			y_stopped = True
		else:
			move_vector.y += 1
	if 'up' in key or 'w' in key:
		if square.top <= 0:
			square.top = 0
			y_stopped = True
		else:
			move_vector.y -= 1
	
	
	if x_stopped:
		move_vector.x = 0
	if y_stopped:
		move_vector.y = 0
	
	move_vector.normalize()	# math stuff, makes speed the same in any direction
	move_vector *= move_speed	# adjustable speed
	
	square.centerX += move_vector.x	# slide to the left, slide to the right
	square.centerY += move_vector.y	# cha cha real smooth

def onStep():
	global step_counter
	step_counter += 1
	
	if step_counter >= app.stepsPerSecond/8:
		step_counter = 0
		trail.append(Circle(square.centerX, square.centerY, square_w/3, fill="lightGrey", opacity=100))
		square.toFront()
		for i in trail:
			if i.opacity <= 0:
				i.visible = False
				trail.pop(0)
			else:
				i.opacity -= 10
				i.radius *= 0.95
		


app.stepsPerSecond = 60
step_counter = 0
trail = []
move_speed = 2
square_x = 200
square_y = 200
square_w = 20
square_h = 20
square = Rect(square_x-(square_w/2), square_y-(square_h/2), square_w, square_h)


cg.run()