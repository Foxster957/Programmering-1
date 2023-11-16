from cmu_graphics import *
import cmu_graphics.cmu_graphics as cg
import math
from time import perf_counter


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
		self.obj = Polygon(x, y-6, x+3, y+6, x-3, y+6, fill="red", rotateAngle=angleTo(0, 0, direction.x, direction.y))
		self.direction = direction
		self.speed = speed

class Enemy:
	def __init__(self, x, y, color = "steelBlue", health = 3, move_speed = 0):
		self.__x, self.__y = x, y
		self.__health, self.max_health = health, health
		self.__healthbar = Rect(x-13, y+14, 26, 4, fill="lime")
		self.__speed = move_speed
		self.obj = Rect(x-10, y-10, 20, 20, fill=color)
		
	def __get_x(self):
		return self.__x
	def __set_x(self, val):	# update obj and healthbar pos when x is changed
		self.__x = val
		self.obj.centerX = self.x
		self.__healthbar.left = self.x-13
	
	def __get_y(self):
		return self.__y
	def __set_y(self, val):	# update obj and healthbar pos when y is changed
		self.__y = val
		self.obj.centerY = self.y
		self.__healthbar.top = self.y+14
	
	def __get_health(self):
		return self.__health
	def __set_health(self, val):	# update healthbar when health is changed 
		self.__health = val
		
		if self.health > 0:
			self.__healthbar.width = self.health*26/self.max_health
		
		if self.health <= 0:
			score.value = int(score.value)+math.floor(self.max_health/2)
			score.left = 65
			self.visible = False
			enemies.remove(self)
			global kill_count
			kill_count += 1
		elif self.health <= self.max_health/3:
			self.__healthbar.fill = "red"
		elif self.health <= self.max_health/2:
			self.__healthbar.fill = "orange"
	
	def __get_speed(self):
		return self.__speed
	def __set_speed(self, val):
		self.__speed = val
	
	def __get_visible(self):
		return self.obj.visible
	def __set_visible(self, val: bool):	# update obj and healthbar visibility when visible is changed
		self.obj.visible = val
		self.__healthbar.visible = val
	
	def check_for_hits(self):
		for p in projectiles:
			if self.obj.hitsShape(p.obj):
				p.obj.visible = False
				projectiles.remove(p)
				self.health -= 1
		if self.obj.hitsShape(player):
			game_over()
	
	x = property(__get_x, __set_x)
	y = property(__get_y, __set_y)
	health = property(__get_health, __set_health)
	speed = property(__get_speed, __set_speed)
	visible = property(__get_visible, __set_visible)


def new_projectile():
	if title.visible:
		return
	
	mouse_direction = Vector2D(mouse_x - player.centerX, mouse_y - player.centerY)
	mouse_direction.normalize()
	projectiles.append(Projectile(player.centerX, player.centerY, mouse_direction, speed=projectile_speed))
	global last_projectile
	last_projectile = 0

def spawn_enemy(enemy):
	while True:
		rand_x = randrange(20, 381)
		rand_y = randrange(20, 381)
		
		if distance(rand_x, rand_y, player.centerX, player.centerY) < 180:
			pass
		elif get_enemy_proximity(rand_x, rand_y) < 30:
			pass
		else:
			enemies.append(Enemy(rand_x, rand_y, color=enemy[1], health=enemy[2], move_speed=enemy[3]))
			break

def get_enemy_proximity(x, y):
	if enemies == []:
		return math.inf
	else:
		closest_distance = math.inf
		for e in enemies:
			closest_distance = min(distance(x, y, e.x, e.y), closest_distance)
		return closest_distance
				
def game_over():
	global wave_index
	wave_index = -1
	title.visible = True
	title.children[1].value = "Game Over"

def win():
	global wave_index
	wave_index = -1
	title.visible = True
	title.children[1].value = "You Win!"

def new_wave():
	global wave_timer, wave_index, kill_count
	wave_timer = 0
	wave_index += 1
	
	if wave_index >= len(waves):
		win()
	else:
		kill_count = 0
		title.visible = True
		title.children[1].value = "Wave {}".format(wave_index+1)
		player.centerX, player.centerY = start_x, start_y

def onKeyHold(key):
	if title.visible:
		return
	
	move_vector = Vector2D(0, 0)
	x_stopped = False	# indicates if a wall is hit on the x axis
	y_stopped = False	# indicates if a wall is hit on the y axis
	
	if 'right' in key or 'd' in key:
		if player.right >= 400:		# collision with right edge of map
			player.right = 400
			x_stopped = True
		else:
			move_vector.x += 1
	if 'left' in key or 'a' in key:
		if player.left <= 0:	# collision with left edge of map
			player.left = 0
			x_stopped = True
		else:
			move_vector.x -= 1
	if 'down' in key or 's' in key:
		if player.bottom >= 400:	# collision with bottom edge of map
			player.bottom = 400
			y_stopped = True
		else:
			move_vector.y += 1
	if 'up' in key or 'w' in key:
		if player.top <= 0:		# collision with top edge of map
			player.top = 0
			y_stopped = True
		else:
			move_vector.y -= 1
	
	if x_stopped:
		move_vector.x = 0
	if y_stopped:
		move_vector.y = 0
	
	move_vector.normalize()
	move_vector *= move_speed*app.deltaTime*60
	
	player.centerX += move_vector.x	# slide to the left, slide to the right
	player.centerY += move_vector.y	# cha cha real smooth

def onStep():
	app.dt_stop = perf_counter()
	app.deltaTime = app.dt_stop - app.dt_start
	app.dt_start = perf_counter()
	
	global wave_timer, wave_index
	wave_timer += app.deltaTime
	
	if title.visible or wave_index == -1:
		title.toFront()
		
		for i in trail:
			i.visible = False
		trail.clear()
		
		for p in projectiles:
			p.obj.visible = False
		projectiles.clear()
		
		if wave_index != -1 and wave_timer >= 2:
			title.visible = False
			wave_timer = 0
		
		return
	
	
	global last_trail_particle, last_projectile
	last_trail_particle += app.deltaTime
	last_projectile += app.deltaTime
	
	global kill_count
	if kill_count == len(waves[wave_index]):
		wave_timer = -1
		kill_count = -1
	elif kill_count == -1 and wave_timer >= 0:	
			new_wave()
	
	if holding_shoot and last_projectile >= 1/fire_rate:
		new_projectile()
		
	for item in waves[wave_index]:
		if wave_timer >= item[0] and item[0] + app.deltaTime >= wave_timer:
			spawn_enemy(item)
	
	for e in enemies:
		e.check_for_hits()

	if last_trail_particle >= 0.1:
		last_trail_particle = 0
		trail.append(Circle(player.centerX, player.centerY, player_w/3, fill="grey", opacity=100))
		player.toFront()
		
		for i in trail:
			if i.opacity > 0:
				i.opacity -= 20
				i.radius *= 0.90
			else:
				i.visible = False
				trail.pop(0)
	
	for p in projectiles:
		move_vector = p.direction * p.speed * app.deltaTime * 60
		p.obj.centerX += move_vector.x
		p.obj.centerY += move_vector.y
		if p.obj.left > 400 or p.obj.right < 0 or p.obj.bottom > 400 or p.obj.top < 0:
			p.obj.visible = False
			projectiles.remove(p)
	
	for e in enemies:
		player_dir = Vector2D(player.centerX - e.x, player.centerY - e.y)
		player_dir.normalize()
		move_vector = player_dir*e.speed*app.deltaTime*60
		e.x += move_vector.x
		e.y += move_vector.y

def onMouseMove(x, y):
	global mouse_x, mouse_y
	mouse_x, mouse_y = x, y
def onMouseDrag(x, y):
	global mouse_x, mouse_y
	mouse_x, mouse_y = x, y

def onMousePress(x, y):
	new_projectile()
	global holding_shoot
	holding_shoot = True	# workaround cause there's no onMouseHold
def onMouseRelease(x, y):
	global holding_shoot
	holding_shoot = False	# workaround cause there's no onMouseHold

def onKeyPress(key):
	if wave_index == -1 and ('enter' in key):
		for e in enemies:
			e.visible = False
		enemies.clear()
		player.centerX, player.centerY = start_x, start_y
		score.value = "0"
		score.left = 65
		new_wave()
	
	if 'space' in key:
		new_projectile()
		global holding_shoot
		holding_shoot = True	# the mouse hold workaround is there, might as well use it
def onKeyRelease(key):
	if 'space' in key:
		global holding_shoot
		holding_shoot = False	# the mouse hold workaround is there, might as well use it
	

app.stepsPerSecond = 60	# update rate, nothing *should* be hardcoded to this
last_trail_particle = 0	# time since last trail particle was created
last_projectile = 0		# time since last projectile was created
wave_timer = 0		# time since wave started

holding_shoot = False	# workaround cause onMouseHold doesn't exist

projectile_speed, move_speed = 6, 2		# gotta go fast
fire_rate = 3

trail, projectiles, enemies = [], [], []	# some lists
mouse_x, mouse_y = 0, 0	# mouse position

start_x, start_y = 200, 200	# player start pos
player_w, player_h = 20, 20		# player dimensions
player = Rect(start_x-(player_w/2), start_y-(player_h/2), player_w, player_h)

Label("Score: ", 35, 15, size=20, bold=True)
score = Label("0", 65, 15, size=20, bold=True, align="left")

title = Group(Rect(50, 150, 300, 100, fill="grey", opacity=75), Label("", 200, 200, size=46, font="monospace", bold=True))
title.visible = False

kill_count = 0	# to keep track of when all enemies in a wave has been killed
wave_index = -1
waves = [	# [<spawn timecode in seconds>, <color>, <health>, <move speed>]
	[
		[0.5, "steelBlue", 3, 0.5],
		[0.5, "steelBlue", 3, 0.5],
		[5, "steelBlue", 3, 0.5],
		[5, "steelBlue", 3, 0.5],
		[9, "fireBrick", 5, 0.3]
	], [
		[0.5, "steelBlue", 3, 0.5],
		[0.5, "steelBlue", 3, 0.5],
		[1.5, "steelBlue", 3, 0.5],
		[5, "fireBrick", 5, 0.3],
		[8, "steelBlue", 3, 0.5],
		[8, "steelBlue", 3, 0.5],
		[11, "fireBrick", 5, 0.3]
	], [
		[0.5, "steelBlue", 3, 0.5],
		[0.5, "steelBlue", 3, 0.5],
		[3, "fireBrick", 5, 0.3],
		[3, "fireBrick", 5, 0.3],
		[8, "purple", 7, 0.2],
		[11, "fireBrick", 5, 0.3],
		[11, "steelBlue", 3, 0.5],
		[11, "steelBlue", 3, 0.5]
	]
]

app.dt_start = perf_counter()	# used to calculate deltaTime
new_wave()


cg.run()