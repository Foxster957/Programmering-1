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

class Projectile:
	def __init__(self, x, y, direction: Vector2D):
		self.obj = Circle(x, y, 3, fill="red")
		self.direction = direction


def new_projectile():
	mouse_direction = Vector2D(mouse_x-square.centerX, mouse_y-square.centerY)	# vector between square and mouse
	mouse_direction.normalize()
	projectiles.append(Projectile(square.centerX, square.centerY, mouse_direction))	# create projectile travelling in mouse_direction


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
	
	if step_counter >= app.stepsPerSecond/10:	# this will execute 10 times per second
		step_counter = 0
		
		trail.append(Circle(square.centerX, square.centerY, square_w/3, fill="grey", opacity=100))
		square.toFront()
		
		for i in trail:			# for each circle in the trail
			if i.opacity > 0:	# as long it is actually visible
				i.opacity -= 20		# decrease opacity and size
				i.radius *= 0.90
			else:
				i.visible = False	# objects with opacity 0 are still rendered, this makes it not
				trail.pop(0)		# remove circle from the trail
	
	for i, p in enumerate(projectiles):
		p.obj.centerX += p.direction.x*projectile_speed		# move projectile
		p.obj.centerY += p.direction.y*projectile_speed
		if p.obj.left>400 or p.obj.right<0 or p.obj.bottom>400 or p.obj.top<0:	# check if outside window
			p.obj.visible = False
			projectiles.pop(i)

def onMouseMove(x, y):
	global mouse_x, mouse_y
	mouse_x, mouse_y = x, y

def onMousePress(x, y):
	new_projectile()

def onKeyPress(key):
	if 'space' in key:
		new_projectile()


app.stepsPerSecond = 60
step_counter = 0
trail, projectiles = [], []
projectile_speed, move_speed = 4, 2
square_x, square_y = 200, 200
square_w, square_h = 20, 20
mouse_x, mouse_y = 0, 0
square = Rect(square_x-(square_w/2), square_y-(square_h/2), square_w, square_h)


cg.run()