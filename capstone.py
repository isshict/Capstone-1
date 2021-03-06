# SPGL Minimal Code by /u/wynand1004 AKA @TokyoEdTech
# Requires SPGL Version 0.8 or Above
# SPGL Documentation on Github: https://wynand1004.github.io/SPGL
# Use this as the starting point for your own games

# Import SPGL
import spgl
import random 

# Create Classes
class Player(spgl.Sprite):
	def __init__(self, shape, color, x, y, distance):
		spgl.Sprite.__init__(self, shape, color, x, y)
		self.distance = distance
		self.speed = 0.5
		self.y_destination = 0
		self.powerup = 0
		self.set_image("player.gif", 60, 60)
				
	def move_up(self):
		if self.ycor() < 200:
			#self.goto(self.xcor(), self.ycor()+200)
			self.y_destination += 200
		else:
			self.y_destination = 200
			#self.goto(self.xcor(), 200)
		
	def move_down(self):
		if self.ycor() > -200: 
			#self.sety(self.ycor() - self.speed)
			self.y_destination -= 200
		else:
			#self.goto(self.xcor(), -200)
			self.y_destination = -200
	
	def tick(self):
		# Move right
		self.setx(self.xcor() + self.speed)
		# Distance
		# self.speed so that the distance decreases at a slower rate when the player collides with seaweed
		self.distance -= self.speed


		# Move the player
		if self.ycor() < self.y_destination:
			self.sety(self.ycor() + 10)
		elif self.ycor() > self.y_destination:
			self.sety(self.ycor() - 10)
			
		
	# Fireball shoot function
	def shoot_fireball(self):
		if self.powerup > 0:
			fireball = Fireball("circle", "orangered", player.xcor(), player.ycor())
			self.powerup -= 1
			print(self.powerup)
		
			# Make Fireball move
			fireball.tick()
			
	# Speed Lag
	def speedlag(self):
		self.speed = 0.1
		canvas = spgl.turtle.getcanvas()
		canvas.after(2000, self.speed_to_normal)
		
	def speed_to_normal(self):
		self.speed = 0.5
		
	# Speed up 
	def speedup(self):
		self.speed = 1
		canvas = spgl.turtle.getcanvas()
		canvas.after(2000, self.speed_to_normal)
		
class Obstacle(spgl.Sprite):
	def __init__(self, shape, color, x, y):
		spgl.Sprite.__init__(self, shape, color, x, y)
		self.speed = random.randint(3,6)
		self.lt(180)

	
	def tick(self):
		self.move()
		

			
	def move(self):
		self.fd(self.speed)
		
		# Make the obstacle come back on screen
		if self.xcor() <= -375:
			self.setx(random.randint(400, 600))
			y_cors = [-200, 0, 200]
			self.sety(random.choice(y_cors))
	
#Child Classes
class Shark(Obstacle):
	def __init__(self, shape, color, x, y):
		Obstacle.__init__(self, shape, color, x, y)	
		self.set_image("shark.gif", 40, 40)
		
class Powerup(Obstacle):
	def __init__(self, shape, color, x, y):
		Obstacle.__init__(self, shape, color, x, y)
		self.set_image("powerup.gif", 40, 40)
	
class Seaweed(Obstacle):
	def __init__(self, shape, color, x, y):
		Obstacle.__init__(self, shape, color, x, y)
		self.set_image("seaweed.gif", 40, 40)

# Wave class
class Wave(spgl.Sprite):
	def __init__(self, shape, color, x, y):
		spgl.Sprite.__init__(self, shape, color, x, y)
		self.speed = random.randint(-6, -3)
		self.lt(180)
		
	def tick(self):
			self.move()
		
	def move(self):
		self.fd(self.speed)
		
		if self.xcor() >= 380:
			self.setx(random.randint(-600, -400))
			y_cors = [-200, 0, 200]
			self.sety(random.choice(y_cors))
		
# Fire ball class	
class Fireball(spgl.Sprite):
	def __init__(self, shape, color, x, y):
		spgl.Sprite.__init__(self, shape, color, x, y)
		self.speed = 6
		self.lt(0)
		self.frame = 0
		self.frames = ["fireball1.gif", "fireball2.gif", "fireball3.gif"]
	
	def tick(self):
		self.move()
		
		# Animate the fireballs
		self.frame += 1
		if self.frame > len(self.frames)-1:
			self.frame = 0
			
		self.set_image(self.frames[self.frame], 40, 40)
		
		
	def move(self):
		self.fd(self.speed)
		
		if self.xcor() >= 380:
			self.destroy()

# Create Functions

# Initial Game setup
game = spgl.Game(800, 600, "blue", "Capstone Project by Sarah T-B", 0)

# Create Sprites
player = Player("triangle", "mediumvioletred", -350, 0, 700.00)
sharks = []
powerups = []
seaweeds = []
y_cors = [-200, 0, 200]

# Create multiple sprites per class
for i in range(0,2):
	shark = Shark("square", "dimgray", random.randint(350, 600), random.choice(y_cors))
	sharks.append(shark)
	powerup = Powerup("square", "gold", random.randint(350, 600), random.choice(y_cors))
	powerups.append(powerup)
	seaweed = Seaweed("square", "seagreen", random.randint(350, 600), random.choice(y_cors))
	seaweeds.append(seaweed)
	
wave = Wave("square", "white", random.randint(-600, -350), random.choice(y_cors))

	
	
# Create Labels
distance_label = spgl.Label("Distance From Shore: {} // Fireballs: {}".format(player.distance, player.powerup), "white", -380, 280)

# Set Keyboard Bindings
game.set_keyboard_binding(spgl.KEY_UP, player.move_up)
game.set_keyboard_binding(spgl.KEY_DOWN, player.move_down)
game.set_keyboard_binding(spgl.KEY_SPACE, player.shoot_fireball)

while True:
	game_over = False
    # Call the game tick method
	game.tick()

	# Move Obstacles
	for shark in sharks:
		shark.tick()
	for powerup in powerups:
		powerup.tick()
	for seaweed in seaweeds:
		seaweed.tick()

	wave.tick()
		
	player.tick()
	
	# Update Label 
	distance_label.update("Distance From Shore: {} // Fireballs: {}".format(player.distance, player.powerup))
	
	# Check for collisions
	for sprite in game.sprites:
		if isinstance(sprite, Shark):
			if game.is_collision(sprite, player):
				sprite.goto(random.randint(350, 600), random.choice(y_cors))
				print("GAME OVER: SHARK COLLISION")
				game_over = True

		if isinstance(sprite, Powerup):
			if game.is_collision(sprite, player):
				sprite.goto(random.randint(350, 600), random.choice(y_cors))
				print("POWERUP COLLISION")
				player.powerup = 5

		if isinstance(sprite, Seaweed):
			if game.is_collision(sprite, player):
				sprite.goto(random.randint(350, 600), random.choice(y_cors))
				print("SEAWEED COLLISION")
				player.speedlag()
		
		if isinstance(sprite, Wave):
			if game.is_collision(sprite, player):
				sprite.goto(random.randint(-600, -350), random.choice(y_cors))
				print("WAVE COLLISION")
				player.speedup()

	# Check for Power-up and Shark Collisions
	for sprite1 in game.sprites:
		if isinstance(sprite1, Shark):
			for sprite2 in game.sprites:
				if isinstance(sprite2, Fireball):
					if game.is_collision(sprite1, sprite2):
						sprite1.goto(random.randint(350, 600), random.choice(y_cors))
						sprite2.destroy()
						print("SHARK AND FIREBALL")
	
	# Game over when Distance is 0
	if player.distance == 0 :
		print("GAME CLEAR")
		game_over = True

	# End game
	if game_over:
		break

	game.print_game_info()
	