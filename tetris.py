#############################################################################
##     _____                _____           _                _             ##
##    |  __ \              / ____|         | |              | |            ##
##    | |__) |___  _ __   | (___   __ _  __| | _____   _____| | ___   _    ##
##    |  _  // _ \| '_ \   \___ \ / _` |/ _` |/ _ \ \ / / __| |/ / | | |   ##
##    | | \ \ (_) | | | |  ____) | (_| | (_| | (_) \ V /\__ \   <| |_| |   ##
##    |_|  \_\___/|_| |_| |_____/ \__,_|\__,_|\___/ \_/ |___/_|\_\\__, |   ##
##                                                                __/ |    ##
##                                                               |___/     ##
## Description: Tetris Game                                                ##
## Due Date: Wednesday, December 21, 2016                                  ##
##                                                                         ##
#############################################################################

from tetris_classes3 import *
from random import randint
import pygame
import time
pygame.init()

HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT//24
screen=pygame.display.set_mode((WIDTH,HEIGHT))
GREY = (170,170,170)

#image uploads
bgn = pygame.image.load("background.jpg")
bgn = pygame.transform.scale(bgn,(14*GRIDSIZE,22*GRIDSIZE))

ssbgn = pygame.image.load("ssbgn.jpg")
ssbgn = pygame.transform.scale(ssbgn,(WIDTH,HEIGHT))

tetrissign = pygame.image.load("tetrissign.png")

gamescreen = pygame.image.load("gamescreen.jpg")
gamescreen = pygame.transform.scale(gamescreen,(WIDTH,HEIGHT))

dropsound = pygame.mixer.Sound("dropsound.wav")
dropsound.set_volume(0.8)

font = pygame.font.SysFont("Default",32)
font2 = pygame.font.SysFont("Default",20)

pause = False #checks whether pause is enabled

tetrisLast = False #checks whether the last row removal was four rows

gameStart = False #checks whether game has started yet 

gameOver = False #checks if game is over

score = 0

level = 1

delay = 200

time = 0

#---------------------------------------#
COLUMNS = 14                            #
ROWS = 22                               # 
LEFT = 9                                # 
RIGHT = LEFT + COLUMNS                  # 
MIDDLE = LEFT + COLUMNS//2              #
TOP = 1                                 #
FLOOR = TOP + ROWS                      #
#---------------------------------------#

#---------------------------------------#
#   functions                           #
#---------------------------------------#
    
def start_screen():
    screen.blit(ssbgn,(0,0))
    screen.blit(tetrissign,(145,50))
    text5 = font.render("Press 's' to begin playing",1,(255,0,0))
    screen.blit(text5,(280,550))

    pygame.display.update()
    
def redraw_screen():               
    screen.blit(gamescreen,(0,0))

    screen.blit(bgn,(9*GRIDSIZE,GRIDSIZE))
    pygame.draw.rect(screen,(255,255,255),(9*GRIDSIZE-2,GRIDSIZE,14*GRIDSIZE+3,22*GRIDSIZE+2),2)

    for i in range(225,HEIGHT,GRIDSIZE): #vertical lines
        pygame.draw.line(screen,GREY,(i,25),(i,HEIGHT-25),1)
        
    for i in range(25,HEIGHT,GRIDSIZE): #horizontal lines
        pygame.draw.line(screen,GREY,(225,i),(575,i),1)

    text1 = font.render("Score: "+str(score),1,(255,0,0))
    screen.blit(text1,(60,100))

    text2 = font.render("Level: "+str(level),1,(255,0,0))
    screen.blit(text2,(60,140))

    text3 = font2.render("Press 'p' to pause/unpause",1,(255,255,255))
    screen.blit(text3,(605,500))

    text4 = font.render("Time: "+str(int(time))+" s",1,(255,0,0))
    screen.blit(text4,(60,180))

    shape.draw(screen, GRIDSIZE)
    shadow.draw(screen,GRIDSIZE)
    nextShape.draw(screen, GRIDSIZE)
    obstacles.draw(screen,GRIDSIZE)

    pygame.display.update()

def end_screen():
    screen.blit(gamescreen,(0,0))
    text6 = font.render("GAME OVER",1,(255,255,255))
    text7 = font.render("Your score was "+str(score),1,(255,255,255))
    screen.blit(text6,(320,250))
    screen.blit(text7,(300,350))
    pygame.display.update()
        
#---------------------------------------#
#   main program                        #
#---------------------------------------#

shapeNo = randint(1,7)
nextShapeNo = randint(1,7)
shape = Shape(MIDDLE,TOP+1,shapeNo)
shadow = Shape(MIDDLE,TOP+1,shapeNo) 
floor = Floor(LEFT,FLOOR,COLUMNS)
top = Floor(LEFT,TOP,COLUMNS)
leftWall = Wall(LEFT-1, TOP, ROWS)
rightWall = Wall(RIGHT, TOP, ROWS)
obstacles = Obstacles(LEFT,FLOOR)
nextShape = Shape(MIDDLE+11,TOP+4,nextShapeNo)

inPlay = True                                         

while inPlay:

    if gameStart==False and gameOver==False:
        for eventA in pygame.event.get():
            if eventA.type == pygame.QUIT:         
                inPlay = False
                    
        if gameStart==False:
            start_screen()

        keys = pygame.key.get_pressed()

        if eventA.type == pygame.KEYDOWN: #if 's' is pressed, game begins
            if eventA.key == pygame.K_s:
                gameStart = True

    if gameStart:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inPlay = False
            
            if event.type == pygame.KEYDOWN and pause==False: #key movements
                
                if event.key == pygame.K_UP: #rotates blocks               
                    shape.rotateClkwise()
                    shadow = Shape(shape.col,shape.row,shapeNo)
                    shadow.shadowRot(shape.shapeRot()) #shadow rotation to match the shape rotation
                    shadow.setClr() #shadow colour to be set to white
                
                    if shape.collides(leftWall) or shape.collides(rightWall) or shape.collides(floor) or shape.collides(obstacles): #if collision occurs during rotation a conflicting rotation occurs
                        shape.rotateCntclkwise()
                        shadow = Shape(shape.col,shape.row,shapeNo)
                        shadow.shadowRot(shape.shapeRot())
                        shadow.setClr()
                        
                        if shape.collides(leftWall) or shape.collides(rightWall) or shape.collides(floor) or shape.collides(obstacles): 
                            shape.rotateClkwise()
                            shadow.rotateClkwise() 

                if event.key == pygame.K_LEFT: #moves blocks left
                    
                    shape.move_left()
                    shadow = Shape(shape.col,shape.row,shapeNo)
                    shadow.shadowRot(shape.shapeRot())
                    shadow.setClr()
                
                    if shape.collides(leftWall) or shape.collides(obstacles):
                        shape.move_right()
                        shadow.move_right()
                        
                if event.key == pygame.K_RIGHT: #moves blocks right
                    shape.move_right()
                    shadow = Shape(shape.col,shape.row,shapeNo)
                    shadow.shadowRot(shape.shapeRot())
                    shadow.setClr()
                    
                    if shape.collides(rightWall) or shape.collides(obstacles):
                        shape.move_left()
                        shadow.move_left()
                if event.key == pygame.K_DOWN:
                    shape.move_down()
                    if shape.collides(floor) or shape.collides(obstacles):
                        shape.move_up()

                if shadow.collides(floor) or shadow.collides(obstacles): 
                    shadow.move_up()

                if event.key == pygame.K_SPACE:
                    while True:
                        shape.move_down()
                        if shape.collides(obstacles) or shape.collides(floor):
                            shape.move_up()
                            break
                        
                if event.key == pygame.K_p: #if p is pressed pause is enabled
                    pause = True

            elif event.type==pygame.KEYDOWN and pause: #if p is pressed after pausing pause is disabled
                if event.key == pygame.K_p:
                    pause = False

        if pause==False: #calculates the time elapsed since the beginning of the game
            if delay == 200:
              time+=0.2

            if delay == 150:
              time+=0.15

            if delay == 100:
              time+=0.1
                
        while True: #moves the shadows down until they hit an obstacle
            shadow.move_down()
            if shadow.collides(floor) or shadow.collides(obstacles):
                shadow.setClr()
                shadow.move_up()
                break
                shadow = Shape(MIDDLE,TOP+1,shapeNo)

        if pause==False: #moves tetris blocks down
            shape.move_down()
            
        if shape.collides(floor) or shape.collides(obstacles): #makes tetris blocks become obstacles if they collide with other obstacles or the floor

            dropsound.play()
            shape.move_up()
            obstacles.append(shape)
            shapeNo = nextShapeNo
            shape = Shape(MIDDLE,TOP+1,shapeNo)
            shadow = Shape(shape.col,TOP+1,shapeNo)
            nextShapeNo = randint(1,7)
            nextShape = Shape(MIDDLE+11,TOP+4,nextShapeNo)

        if shape.collides(top) and shape.collides(obstacles): #if a shape collides with the top of the screen the game is over
            gameOver = True

        fullRows = obstacles.findFullRows(TOP, FLOOR, COLUMNS) # finds the full rows and removes their blocks from the obstacles 
        obstacles.removeFullRows(fullRows)

        if len(fullRows)>=1 and len(fullRows)<4: #calculates the score by determining the length of full rows
            score+= 100*len(fullRows)
            tetrisLast = False
            
        if len(fullRows)==4: #gives 800 points if there are 4 full rows taken out at once
            tetrisLast = True
            score+=800

        if len(fullRows)==4 and tetrisLast: #gives 1200 if 4 full rows are taken out twice in a row
            score+=1200

        if score==500: #increases speed and level if score reaches 500
            level = 2
            delay = 150

        if score==1000: #increases speed and level more if score reaches 1000
            level = 3
            delay = 100

        redraw_screen()

    if gameOver:
        gameStart = False
        end_screen()
        for eventB in pygame.event.get():
            if eventB.type == pygame.QUIT:         
                inPlay = False
        
    pygame.time.delay(delay)

pygame.quit()
    
    
