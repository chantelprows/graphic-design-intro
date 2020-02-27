# Import a library of functions called 'pygame'
import pygame
import math
from math import pi
import numpy as np

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Point3D:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z

class Line3D():

	def __init__(self, start, end):
		self.start = start
		self.end = end

def loadOBJ(filename):

	vertices = []
	indices = []
	lines = []

	f = open(filename, "r")
	for line in f:
		t = str.split(line)
		if not t:
			continue
		if t[0] == "v":
			vertices.append(Point3D(float(t[1]),float(t[2]),float(t[3])))

		if t[0] == "f":
			for i in range(1,len(t) - 1):
				index1 = int(str.split(t[i],"/")[0])
				index2 = int(str.split(t[i+1],"/")[0])
				indices.append((index1,index2))

	f.close()

	#Add faces as lines
	for index_pair in indices:
		index1 = index_pair[0]
		index2 = index_pair[1]
		lines.append(Line3D(vertices[index1 - 1],vertices[index2 - 1]))

	#Find duplicates
	duplicates = []
	for i in range(len(lines)):
		for j in range(i+1, len(lines)):
			line1 = lines[i]
			line2 = lines[j]

			# Case 1 -> Starts match
			if line1.start.x == line2.start.x and line1.start.y == line2.start.y and line1.start.z == line2.start.z:
				if line1.end.x == line2.end.x and line1.end.y == line2.end.y and line1.end.z == line2.end.z:
					duplicates.append(j)
			# Case 2 -> Start matches end
			if line1.start.x == line2.end.x and line1.start.y == line2.end.y and line1.start.z == line2.end.z:
				if line1.end.x == line2.start.x and line1.end.y == line2.start.y and line1.end.z == line2.start.z:
					duplicates.append(j)

	duplicates = list(set(duplicates))
	duplicates.sort()
	duplicates = duplicates[::-1]

	#Remove duplicates
	for j in range(len(duplicates)):
		del lines[duplicates[j]]

	return lines

def loadHouse():
    house = []
    #Floor
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(5, 0, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 0, 5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(-5, 0, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 0, -5)))
    #Ceiling
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 5, -5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(5, 5, 5), Point3D(-5, 5, 5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(-5, 5, -5)))
    #Walls
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(-5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 5, 5)))
    #Door
    house.append(Line3D(Point3D(-1, 0, 5), Point3D(-1, 3, 5)))
    house.append(Line3D(Point3D(-1, 3, 5), Point3D(1, 3, 5)))
    house.append(Line3D(Point3D(1, 3, 5), Point3D(1, 0, 5)))
    #Roof
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(0, 8, -5)))
    house.append(Line3D(Point3D(0, 8, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(0, 8, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(0, 8, -5)))

    return house

def loadCar():
    car = []
    #Front Side
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-2, 3, 2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(2, 3, 2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(3, 2, 2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 1, 2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(-3, 1, 2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 2, 2)))

    #Back Side
    car.append(Line3D(Point3D(-3, 2, -2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(-2, 3, -2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, -2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 2, -2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(3, 1, -2), Point3D(-3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, -2), Point3D(-3, 2, -2)))

    #Connectors
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-3, 2, -2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 1, -2)))

    return car

def loadTire():
    tire = []
    #Front Side
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-.5, 1, .5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(.5, 1, .5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(1, .5, .5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, -.5, .5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(.5, -1, .5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(-.5, -1, .5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-1, -.5, .5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, .5, .5)))

    #Back Side
    tire.append(Line3D(Point3D(-1, .5, -.5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, -.5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, -.5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, .5, -.5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, -.5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(.5, -1, -.5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, -.5), Point3D(-1, -.5, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, -.5), Point3D(-1, .5, -.5)))

    #Connectors
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-1, .5, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, -.5, -.5)))

    return tire


# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Set the height and width of the screen
size = [512, 512]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Shape Drawing")

#Set needed variables
done = False
clock = pygame.time.Clock()
start = Point(0.0,0.0)
end = Point(0.0,0.0)
linelist = loadHouse()
carlist = loadCar()
tirelist = loadTire()

x = 0
y = 0
z = -5
r = 0

carMatrix = []
def makeMatrix(x_, z_, r_, car=0):
	final = np.matmul(np.matrix(([1, 0, 0, x_],
					  			 [0, 1, 0, 0],
					  	 		 [0, 0, 1, z_],
					  	 		 [0, 0, 0, 1])),
					  np.matrix(([math.cos(math.radians(r_)), 0, -math.sin(math.radians(r_)), 0],
					  			 [0, 1, 0, 0],
								 [math.sin(math.radians(r_)), 0, math.cos(math.radians(r_)), 0],
								 [0, 0, 0, 1])))
	if (car):
		carMatrix.append(final.tolist())
	return final.tolist()

neighborhood = []
def makeItem(start, end, x_, z_, r_, car=0):
	newStart = np.matmul(makeMatrix(x_, z_, r_, car), start)
	newEnd = np.matmul(makeMatrix(x_, z_, r_, car), end)
	newLine = [newStart, newEnd]
	neighborhood.append(newLine)

def makeWheel(start, end, x, z):
	mat = np.matmul(carMatrix[0], np.matrix(([1, 0, 0, x],
											 [0, 1, 0, 0],
											 [0, 0, 1, z],
											 [0, 0, 0, 1]))).tolist()
	newStart = np.matmul(mat, start)
	newEnd = np.matmul(mat, end)
	newLine = [newStart, newEnd]
	neighborhood.append(newLine)

for s in linelist:
	startVector = [s.start.x, s.start.y, s.start.z, 1]
	endVector = [s.end.x, s.end.y, s.end.z, 1]

	makeItem(startVector, endVector, 0, 0, 0)
	makeItem(startVector, endVector, 20, 0, 0)
	makeItem(startVector, endVector, -20, 0, 0)
	makeItem(startVector, endVector, 0, 40, 180)
	makeItem(startVector, endVector, 20, 40, 180)
	makeItem(startVector, endVector, -20, 40, 180)
	makeItem(startVector, endVector, -35, 20, -90)

for c in carlist:
	startVector = [c.start.x, c.start.y, c.start.z, 1]
	endVector = [c.end.x, c.end.y, c.end.z, 1]
	makeItem(startVector, endVector, 0, 25, 0, 1)

for t in tirelist:
	startVector = [t.start.x, t.start.y, t.start.z, 1]
	endVector = [t.end.x, t.end.y, t.end.z, 1]

	makeWheel(startVector, endVector, 2, -2)
	makeWheel(startVector, endVector, -2, -2)
	makeWheel(startVector, endVector, 2, 2)
	makeWheel(startVector, endVector, -2, 2)

	carMatrix.pop()

#Loop until the user clicks the close button.
while not done:

	# This limits the while loop to a max of 100 times per second.
	# Leave this out and we will use all CPU we can.
	clock.tick(100)

	# Clear the screen and set the screen background
	screen.fill(BLACK)

	#Controller Code#
	#####################################################################

	for event in pygame.event.get():
		if event.type == pygame.QUIT: # If user clicked close
			done=True

	pressed = pygame.key.get_pressed()

	if pressed[pygame.K_a]:
		z = z - math.sin(math.radians(r))
		x = x + math.cos(math.radians(r))

	if pressed[pygame.K_d]:
		z = z + math.sin(math.radians(r))
		x = x - math.cos(math.radians(r))

	if pressed[pygame.K_w]:
		z = z - math.cos(math.radians(r))
		x = x - math.sin(math.radians(r))

	if pressed[pygame.K_s]:
		z = z + math.cos(math.radians(r ))
		x = x + math.sin(math.radians(r))

	if pressed[pygame.K_r]:
		y = y - 1

	if pressed[pygame.K_f]:
		y = y + 1

	if pressed[pygame.K_q]:
		r = r - 1

	if pressed[pygame.K_e]:
		r = r + 1

	if pressed[pygame.K_h]:
		x = 0
		y = 0
		z = -5
		r = 0

	#Viewer Code#
	#####################################################################
	worldToCam = np.matmul(np.matrix(([math.cos(math.radians(r)), 0, -math.sin(math.radians(r)), 0],
						 			  [0, 1, 0, 0],
						 		  	  [math.sin(math.radians(r)), 0, math.cos(math.radians(r)), 0],
						 		  	  [0, 0, 0, 1])),
						   np.matrix(([1, 0, 0, x],
								      [0, 1, 0, y],
								      [0, 0, 1, z],
								      [0, 0, 0, 1])))

	zoom = 1/(math.tan(math.radians(45)))
	third = 101/99
	fourth = -200/99
	clip = np.matrix(([zoom, 0, 0, 0],
					  [0, zoom, 0, 0],
					  [0, 0, third, fourth],
					  [0, 0, 1, 0]))

	toScreen = np.matrix(([256, 0, 256],
						  [0, -256, 256],
						  [0, 0, 1]))

	for s in neighborhood:
		start = np.matmul(worldToCam, s[0]).tolist()
		end = np.matmul(worldToCam, s[1]).tolist()

		start = np.matmul(clip, start[0]).tolist()
		end = np.matmul(clip, end[0]).tolist()

		a = start[0]
		b = end[0]
		drawline = 1
		if (a[0] < -a[3]):
			if (b[0] < -b[3]):
				drawline = 0
		if (a[1] < -a[3]):
			if (b[1] < -b[3]):
				drawline = 0
		if (a[0] > a[3]):
			if (b[0] > b[3]):
				drawline = 0
		if (a[1] > a[3]):
			if (b[1] > b[3]):
				drawline = 0
		if (a[2] > a[3]):
			if (b[2] > b[3]):
				drawline = 0
		if (a[2] < -a[3]) or (b[2] < -b[3]):
			drawline = 0

		if (drawline == 1):
			w = a[3]
			wb = b[3]
			a = np.array(a) / w
			b = np.array(b) / wb

			da = [a[0], a[1], a[3]]
			db = [b[0], b[1], b[3]]

			start = np.matmul(toScreen, da).tolist()
			end = np.matmul(toScreen, db).tolist()
			sCopy = [start[0], end[0]]

			pygame.draw.line(screen, RED, (sCopy[0][0], sCopy[0][1]), (sCopy[1][0], sCopy[1][1]))

	# Go ahead and update the screen with what we've drawn.
	# This MUST happen after all the other drawing commands.
	pygame.display.flip()


# Be IDLE friendly
pygame.quit()
