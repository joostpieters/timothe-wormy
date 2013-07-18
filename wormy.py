import random,pygame,sys
from pygame.locals import *
fps = 15
windowwidth = 640
windowheight = 480
cellsize = 20
cellwidth = int(windowwidth/cellsize)
cellheight = int(windowheight/cellsize)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
darkgreen = (0,155,0)
darkgray = (40,40,40)
BGCOLOR = 
gameOverColor = black

up = 'up'
down = 'down'
left = 'left'
right = 'right'

head = 0  # this is the index of the worms head

def main():
	global FPSCLOCK,DISPLAYSURF,BASICFONT
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((windowwidth,windowheight))
	BASICFONT = pygame.font.Font('freesansbold.ttf',18)
	pygame.display.set_caption('wormy')
	showStartScreen()
	while True:
		runGame()
		showGameOverScreen()

def runGame():
	score=0
	# set a random startpoint
	startx = random.randint(5,cellwidth-6)
	starty = random.randint(5,cellheight-6)
	wormCoords = [{'x': startx, 'y': starty},
	               {'x':startx-1,'y':starty},
	               {'x':startx-2,'y':starty}]
	direction = right

	apple = getRandomLocation()

	while True:    # main game loop
		for event in pygame.event.get():

			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == K_LEFT and direction != right:
				 	direction = left
				elif event.key == K_RIGHT and direction != left:
				 	direction = right
				elif event.key == K_UP and direction != down:
				 	direction = up
				elif event.key == K_DOWN and direction != up:
				 	direction = down
				elif event.key == K_ESCAPE:
				 	terminate()
		
		# check if the worm has hit the edge
		if wormCoords[head]['x'] == -1:
			wormCoords[head]['x'] = cellwidth-1
		if wormCoords[head]['x'] == cellwidth:
			wormCoords[head]['x'] = 0
		if wormCoords[head]['y'] == cellheight:
			wormCoords[head]['y'] = 0
		if wormCoords[head]['y'] == -1:
			wormCoords[head]['y'] = cellheight-1
	
		# check if the worm has hit itself
		for wormBody in wormCoords[1:]:
			if wormBody['x'] == wormCoords[head]['x'] and wormBody['y'] == wormCoords[head]['y']:
				return

		# check if worm has eaten an apple
		if apple['x'] == wormCoords[head]['x'] and apple['y'] == wormCoords[head]['y']:
			apple = getRandomLocation()
			score = score + 1
		elif random.randint(0,1000)>5:
			del wormCoords[-1]   # remove the tail segment

		# move the worm by adding a segment in the direction it is moving
		headCoords = wormCoords[head]
		if direction == up:
			newhead = {'x': headCoords['x'],'y':headCoords['y']-1}
		elif direction == down:
			newhead = {'x': headCoords['x'],'y':headCoords['y']+1}
		elif direction == left:
			newhead = {'x': headCoords['x']-1,'y':headCoords['y']}
		elif direction == right:
			newhead = {'x': headCoords['x']+1,'y':headCoords['y']}
		wormCoords.insert(0,newhead)

		DISPLAYSURF.fill(BGCOLOR)
		drawGrid()
		drawWorm(wormCoords)
		drawApple(apple)
		drawScore(score)
		pygame.display.update()
		FPSCLOCK.tick(fps)
		DISPLAYSURF.fill(gameOverColor)
def drawPressKeyMsg():
	pressKeySurf = BASICFONT.render('press a key to play',True,darkgray)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.topleft = (windowwidth-200,windowheight-30)
	DISPLAYSURF.blit(pressKeySurf,pressKeyRect)

def checkForKeyPress():
	if len(pygame.event.get(QUIT))>0:
		terminate()
	keyupEvents = pygame.event.get(KEYUP)
	if len(keyupEvents) == 0:
		return None
	if keyupEvents[0].key == K_ESCAPE:
		terminate()
	return keyupEvents[0]

def showStartScreen():
	titleFont = pygame.font.Font('freesansbold.ttf', 100)
	titleSurf1 = titleFont.render('Wormy!', True, white, darkgreen)
	titleSurf2 = titleFont.render('Wormy!', True, green)
	degrees1=0
	degrees2=0
	while True:
		DISPLAYSURF.fill(BGCOLOR)
		rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
		rotatedRect1 = rotatedSurf1.get_rect()
		rotatedRect1.center = (windowwidth/2, windowheight/2)
		DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)
		rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
		rotatedRect2 = rotatedSurf2.get_rect()
		rotatedRect2.center = (windowwidth/2, windowheight/2)
		DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)
		drawPressKeyMsg()
		if checkForKeyPress():
			pygame.event.get()
			return
		pygame.display.update()
		FPSCLOCK.tick(fps)
		degrees1 += 3
		degrees2 += 7

def terminate():
	pygame.quit()
	sys.exit()

def getRandomLocation():
	return {'x': random.randint(0, cellwidth-1),
	        'y': random.randint(0, cellheight-1)}

def showGameOverScreen():
	gamefont = pygame.font.Font('freesansbold.ttf',150)
	gamesurf = gamefont.render('game',True,white)
	oversurf = gamefont.render('over',True,white)
	gamerect = gamesurf.get_rect()
	gamerect.midtop = (windowwidth/2,10)
	DISPLAYSURF.blit(gamesurf,gamerect)
	overrect = oversurf.get_rect()
	overrect.midtop = (windowwidth/2,gamerect.height+10+25)
	DISPLAYSURF.blit(oversurf,overrect)
	drawPressKeyMsg()
	pygame.display.update()
	pygame.time.wait(500)
	checkForKeyPress()
	while True:
		if checkForKeyPress():
			pygame.event.get()
			return

def drawScore(score):
	surf = BASICFONT.render('score: %s' % (score),True,white)
	rect = surf.get_rect()
	rect.topleft = (windowwidth-120,10)
	DISPLAYSURF.blit(surf,rect)

def drawWorm(c5):
	for coord in c5:
		x = coord['x'] * cellsize
		y = coord['y'] * cellsize
		rect = pygame.Rect(x,y,cellsize,cellsize)
		pygame.draw.rect(DISPLAYSURF,darkgreen,rect)
		innerrect = pygame.Rect(x+4, y+4, cellsize-8, cellsize-8)
		pygame.draw.rect(DISPLAYSURF,green,innerrect)

def drawApple(apple):
	x = apple['x'] * cellsize
	y = apple['y'] * cellsize
	rect = pygame.Rect(x,y,cellsize,cellsize)
	pygame.draw.rect(DISPLAYSURF,red,rect)

def drawGrid():
	for x in range(0,windowwidth,cellsize):
		pygame.draw.line(DISPLAYSURF,darkgray,(x,0),(x,windowheight))
	for y in range(0,windowheight,cellsize):
		pygame.draw.line(DISPLAYSURF,darkgray,(0,y),(windowwidth,y))

if __name__ == '__main__':
	main()
	









