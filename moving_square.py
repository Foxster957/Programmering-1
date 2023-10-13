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
	def __init__(self, x, y, direction: Vector2D, speed = 4):
		self.obj = Circle(x, y, 3, fill="red")
		self.direction = direction
		self.speed = speed

class Enemy:
	def __init__(self, x, y, color = "navy", health = 3):
		self.__x, self.__y = x, y
		self.__health, self.max_health = health, health
		self.__healthbar = Rect(x-13, y+14, 26, 4, fill="lime")
		self.obj = Rect(x-10, y-10, 20, 20, fill=color)
		
	def get_x(self):
		return self.__x
	def set_x(self, val):	# update obj and healthbar pos when x is changed
		self.__x = val
		self.obj.centerX = self.x
		self.__healthbar.left = self.x-13
	
	def get_y(self):
		return self.__y
	def set_y(self, val):	# update obj and healthbar pos when y is changed
		self.__y = val
		self.obj.centerY = self.y
		self.__healthbar.top = self.y+14
	
	def get_health(self):
		return self.__health
	def set_health(self, val):	# update healthbar when health is changed 
		self.__health = val
		
		if self.health > 0:
			self.__healthbar.width = self.health*26/self.max_health
		
		if self.health <= self.max_health/3:
			self.__healthbar.fill = "red"
		elif self.health <= self.max_health/2:
			self.__healthbar.fill = "orange"
	
	def get_visible(self):
		return self.obj.visible
	def set_visible(self, val: bool):	# update obj and healthbar visibility when visible is changed
		self.obj.visible = val
		self.__healthbar.visible = val
	
	x = property(get_x, set_x)
	y = property(get_y, set_y)
	health = property(get_health, set_health)
	visible = property(get_visible, set_visible)


def new_projectile():
	mouse_direction = Vector2D(mouse_x-square.centerX, mouse_y-square.centerY)	# vector between square and mouse
	mouse_direction.normalize()		# make vector length 1
	projectiles.append(Projectile(square.centerX, square.centerY, mouse_direction))	# create projectile travelling in mouse_direction
	global last_projectile
	last_projectile = 0

def onKeyHold(key):
	move_vector = Vector2D(0, 0)
	x_stopped = False	# indicates if a wall is hit on the x axis
	y_stopped = False	# indicates if a wall is hit on the y axis
	
	if 'right' in key or 'd' in key:
		if square.right >= 400:		# collision with right edge of map
			square.right = 400
			x_stopped = True
		else:
			move_vector.x += 1
	if 'left' in key or 'a' in key:
		if square.left <= 0:	# collision with left edge of map
			square.left = 0
			x_stopped = True
		else:
			move_vector.x -= 1
	if 'down' in key or 's' in key:
		if square.bottom >= 400:	# collision with bottom edge of map
			square.bottom = 400
			y_stopped = True
		else:
			move_vector.y += 1
	if 'up' in key or 'w' in key:
		if square.top <= 0:		# collision with top edge of map
			square.top = 0
			y_stopped = True
		else:
			move_vector.y -= 1
	
	if x_stopped:
		move_vector.x = 0	# don't move on x axis if you can't
	if y_stopped:
		move_vector.y = 0	# don't move on y axis if you can't
	
	move_vector.normalize()	# math stuff, makes speed the same in any direction
	move_vector *= move_speed	# adjustable speed
	
	square.centerX += move_vector.x	# slide to the left, slide to the right
	square.centerY += move_vector.y	# cha cha real smooth

def onStep():
	global last_trail_particle, last_projectile
	last_trail_particle += 1	# step counters
	last_projectile += 1
	
	if hold_shoot and last_projectile >= 30:	# shoot once each 30 steps when holding shoot
		new_projectile()
	
	if len(enemies) == 0:	# if there are no enemies, make a new one
		while True:
			rand_x = randrange(20, 381)
			rand_y = randrange(20, 381)
			if distance(rand_x, rand_y, square.centerX, square.centerY) >= 30:	# make sure enemy is not too close to player
				enemies.append(Enemy(rand_x, rand_y, health=4))
				break
	
	for p_index, p in enumerate(projectiles):	# go through all projectiles and enemies and check for hits
		for e_index, e in enumerate(enemies):
			if p.obj.hitsShape(e.obj):
				p.obj.visible = False	# "delete" projectile
				projectiles.pop(p_index)	# remove from list of projectiles
				e.health -= 1
				if e.health <= 0:
					e.visible = False	# "delete" enemy
					enemies.pop(e_index)	# remove from list of enemies
	
	if last_trail_particle >= app.stepsPerSecond/10:	# add trail particle (10 times per second)
		last_trail_particle = 0
		trail.append(Circle(square.centerX, square.centerY, square_w/3, fill="grey", opacity=100))
		square.toFront()
		
		for i in trail:			# for each circle in the trail
			if i.opacity > 0:	# as long it is actually visible
				i.opacity -= 20		# decrease opacity and size
				i.radius *= 0.90
			else:
				i.visible = False	# objects with opacity 0 are still rendered, this makes it not
				trail.pop(0)		# remove circle from the trail
	
	for i, p in enumerate(projectiles):		# move projectiles
		p.obj.centerX += p.direction.x*p.speed
		p.obj.centerY += p.direction.y*p.speed
		if p.obj.left>400 or p.obj.right<0 or p.obj.bottom>400 or p.obj.top<0:	# check if outside window
			p.obj.visible = False
			projectiles.pop(i)

def onMouseMove(x, y):
	global mouse_x, mouse_y
	mouse_x, mouse_y = x, y	# current mouse pos is always stored in mouse_x and mouse_y
def onMouseDrag(x, y):
	global mouse_x, mouse_y
	mouse_x, mouse_y = x, y	# onMouseMove won't trigger if mouse button is held, so this updates pos too
def onMousePress(x, y):
	new_projectile()	# spawn one projectile when pressed
	global hold_shoot
	hold_shoot = True	# workaround cause there's no onMouseHold
def onMouseRelease(x, y):
	global hold_shoot
	hold_shoot = False	# workaround cause there's no onMouseHold
def onKeyPress(key):
	if 'space' in key:	# spawn one projectile when pressed
		new_projectile()
		global hold_shoot
		hold_shoot = True	# the mouse hold workaround is already there, might as well use it twice
def onKeyRelease(key):
	if 'space' in key:
		global hold_shoot
		hold_shoot = False	# the mouse hold workaround is already there, might as well use it twice


app.stepsPerSecond = 60
last_trail_particle = 0	# time since last trail particle was created
last_projectile = 0		# time since last projectile was created
hold_shoot = False	# workaround cause onMouseHold doesn't exist
trail, projectiles, enemies = [], [], []	# some lists
projectile_speed, move_speed = 4, 2		# gotta go fast
square_x, square_y = 200, 200	# player start pos
square_w, square_h = 20, 20		# player dimensions
mouse_x, mouse_y	# mouse position
square = Rect(square_x-(square_w/2), square_y-(square_h/2), square_w, square_h)	# player object


cg.run()