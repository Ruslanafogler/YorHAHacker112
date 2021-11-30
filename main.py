
#cmu 112 graphics from 
from cmu_112_graphics import *
import math
import numpy as np

from classes.Player import Player

from classes.Map import Map
from classes.Bullet import PlayerBullet, EnemyBullet
from classes.powerUps import getAbilitiesAndParameters

from classes.config import COLORS


#Game inspired by N.Automata Hacking and Hades Gameplay!



def appStarted(app):
    app.width = 900
    app.height = 900
    app.timerDelay = 5

    app.boxSize = 45
    app.gridSize = 15
    app.fromRestart = True


    initApp(app, app.fromRestart)



def initApp(app, fromRestart):
    app.playerBullets = []
    app.playerDirection = (1, 0)
    
    if(fromRestart):
        app.level = 1
        app.chambers = 0
        app.playerPowerUps = []
        app.playerHealth = 50
        app.maxPlayerHealth = 50


    app.map = Map(app.width, app.height, app.gridSize, app.boxSize, 
                  app.playerHealth, app.maxPlayerHealth, app.playerPowerUps, 
                  app.chambers)
        
    app.gameOver = False
    app.completedMap = False
    app.displayTimerScreen = 50

    app.drawPowerUpScreen = False
    app.headerFontX0, app.headerFontY0 = app.width//2, 60
    app.headerFontSize = 50
    app.screenPowerUps = []
    app.powerUpRectBounds = []
    
    app.generatingMap = False

    app.mouseX = 0
    app.mouseY = 0



#######################################
#DRAWING STUFF
def redrawAll(app, canvas):
    if(app.drawPowerUpScreen):
        drawPowerUpScreen(app, canvas)
    elif(app.gameOver):
        drawGameOverScreen(app, canvas)
    elif(app.generatingMap):
        drawGenMapScreen(app, canvas)
    elif(not app.generatingMap):
        drawGameplayScreen(app, canvas)



#draw generate map loading screen
def drawGenMapScreen(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill='black',)
    canvas.create_text(app.width//2, app.height//2, text=f'Generating Map..', fill='white')

#draw game over screen
def drawGameOverScreen(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill='black',)
    canvas.create_text(app.width//2, app.height//2, text=f'Game Over', fill='white')




def getPowerScreenRectCords(app, rectNum):

    
    rectMargin = 45
    rectWidth = app.width - rectMargin*2
    rectHeight = (app.height - rectMargin*2 - 
            app.headerFontSize - app.headerFontY0)//3 - rectMargin

    rectX0 = rectMargin
    rectY0 = (app.headerFontY0 + app.headerFontSize + rectMargin + 
                (rectHeight + rectMargin) * rectNum)
    rectX1 = rectX0 + rectWidth
    rectY1 = rectY0 + rectHeight

    return (rectX0, rectY0, rectX1, rectY1)






    

def clickedInRectangle(x0, y0, x1, y1, mouseX, mouseY):
    return x0 <= mouseX <= x1 and y0 <= mouseY <= y1


#draw choose power up screen
def drawPowerUpScreen(app, canvas):
    # headerFontX0, headerFontY0 = app.width//2, 60
    # headerFontSize = 50
    canvas.create_rectangle(0,0, app.width, app.height, fill='gray',)
    canvas.create_text(app.headerFontX0, app.headerFontY0, 
                    text=f'Power Up', font=f'Myriad {app.headerFontSize} bold', 
                    fill='white')
    
    for powerUpNum in range(3):

        ability = app.screenPowerUps[powerUpNum]
        #ability has 3 parts --> type, description, parameter

        rectX0, rectY0, rectX1, rectY1 = getPowerScreenRectCords(app, powerUpNum)

        
        abilityTextX = (rectX0 + rectX1)//2
        abilityTextY = rectY0 + 60
        abilityText = ability[1]

        parameterTextX = (rectX0 + rectX1)//2
        parameterTextY = (rectY0+rectY1)//2+20
        parameter = ability[2]
        if(parameter != None):
           
            percent = int(parameter/app.map.player.getPowerUpAttr(ability[0])*100)

            if(percent > 0):
                parameterText = f'+ {abs(percent)}%'
            elif(percent < 0):
                parameterText = f'- {abs(percent)}%'
            else:
                parameterText = 'Already maxed out.'


        
        canvas.create_rectangle(rectX0, rectY0, 
                                rectX1, rectY1, 
                                fill=COLORS['offMap'], width = 2)
        canvas.create_text(abilityTextX, abilityTextY, 
                            text=abilityText,font='Myriad 15 bold', fill='white')
        canvas.create_text(parameterTextX, parameterTextY, 
                            text=parameterText, font='Myriad 15 bold',fill='white')

                                

#draw gameplay screen

#gameplay screen
def drawMap(app, canvas):
    app.map.redrawAll(canvas, app.mouseX, app.mouseY)

def drawPlayerBullets(app, canvas):
    for bullet in app.playerBullets:
            bullet.redrawAll(canvas)

def drawEnemyBullets(app, canvas):
    for enemy in app.map.enemyList:
        for bullet in enemy.bullets:
            bullet.redrawAll(canvas)

def drawPlayerHealth(app, canvas):
    app.map.drawPlayerHealth(canvas)

def drawHackingCompleteText(app, canvas):
    canvas.create_text(app.height//2, app.width//2, text='- Hacking Complete -', font='Myriad 50 bold', fill='white')
    canvas.create_text(app.height//2, app.width//2+50, text='- Onto next level -', font='Myriad 15 bold', fill='white')

def drawPlayerProgress(app, canvas):
    margin = 30
    fontSize = 15

    levelTextLen = 40
    levelText = f'Level {app.level}' 
    levelFont = f'Myriad {fontSize+10}'
    
    levelTextX0 = app.width - margin - levelTextLen
    levelTextY0 = margin

    chamberFont = f'Myriad {fontSize}'
    chamberText = f'Chamber {app.chambers}' 
    
    chamberTextX0 = levelTextX0
    chamberTextX1 = levelTextY0 + margin
    

    canvas.create_text(levelTextX0, levelTextY0, text=levelText, font=levelFont, fill='white')
    canvas.create_text(chamberTextX0, chamberTextX1, text=chamberText, font=chamberFont,fill='white')


def drawGameplayScreen(app, canvas):
        drawMap(app, canvas)
        drawPlayerBullets(app, canvas)
        drawEnemyBullets(app, canvas)
        drawBigGrid(app, canvas)
        drawPlayerHealth(app, canvas)
        drawPlayerProgress(app, canvas)
        if(app.completedMap):
            drawHackingCompleteText(app, canvas)


#draw big grid method
#grids on map inspired by KidsCanCode TilebasedGame pt1
#https://www.youtube.com/watch?v=3UxnelT9aCo&list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i&index=1
def drawBigGrid(app, canvas):
    for x in range(0, app.height, app.boxSize):
        canvas.create_line(x, 0, x, app.height, fill='#ffffff')

    for y in range(0, app.height, app.boxSize):
        canvas.create_line(0, y, app.width, y, fill='#ffffff')


########################################
#OTHER METHODS TO HELP WITH STUFF

def playerFireBullet(app):
    app.playerBullets.append(PlayerBullet(app.map.player.x, app.map.player.y, 
                                          app.boxSize, app.map.player.angle, app.map.player.bulletDamage))

def movePlayer(app, dcol, drow):
    app.map.movePlayer(dcol, drow)
    addBulletOffset(app, dcol, drow, app.playerBullets)
    for enemy in app.map.enemyList:
        addBulletOffset(app, dcol, drow, enemy.bullets)


def addBulletOffset(app, dcol, drow, bulletList):
    for bullet in bulletList:
        bullet.x-=dcol*app.boxSize
        bullet.y-=drow*app.boxSize


def advanceToNextRoom(app):
    app.generatingMap = True
    app.playerHealth = app.map.player.health
    app.maxPlayerHealth = app.map.player.maxHealth
    app.chambers+=1

    initApp(app, False)


#########################################
#EVENTS LIKE KEY PRESSING,
def mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

def mousePressed(app, event):
    if(app.drawPowerUpScreen):
        handlePowerScreenMousePressed(app, event)
    else:
        handleGameplayMousePressed(app)
        


def handlePowerScreenMousePressed(app, event):
    
    x = event.x
    y = event.y

    def proceed():
        app.drawPowerUpScreen = False
        app.screenPowerUps = []
        print(app.playerPowerUps)
        advanceToNextRoom(app)


    r1 = getPowerScreenRectCords(app, 0)
    r2 = getPowerScreenRectCords(app, 1)
    r3 = getPowerScreenRectCords(app, 2)

    if(clickedInRectangle(r1[0], r1[1], r1[2], r1[3], x, y)):
        app.playerPowerUps.append(app.screenPowerUps[0])
        proceed()
    elif(clickedInRectangle(r2[0], r2[1], r2[2], r2[3], x, y)):
        app.playerPowerUps.append(app.screenPowerUps[1])
        proceed()
    elif(clickedInRectangle(r3[0], r3[1], r3[2], r3[3], x, y)):
        app.playerPowerUps.append(app.screenPowerUps[2])
        proceed()
       

def handleGameplayMousePressed(app):
    if(app.map.player.canShoot):
            playerFireBullet(app)
            app.map.player.canShoot = False



def keyPressed(app, event):
    playerMovement = 1
    if(event.key == 'a'):
        movePlayer(app, -playerMovement, 0)
        app.playerDirection = (-playerMovement, 0)
    if(event.key == 'd' ):
        movePlayer(app, playerMovement, 0)
        app.playerDirection = (playerMovement, 0)
    if(event.key == 'w'):
        movePlayer(app, 0, -playerMovement)
        app.playerDirection = (0, -playerMovement)
    if(event.key == 's'):
        movePlayer(app, 0, playerMovement)
        app.playerDirection = (0, playerMovement)
    if(event.key == 'Space'):
        if(app.map.player.canDash):
            app.map.player.isDashing = True
            if(not movePlayer(app, app.playerDirection[0]*3, app.playerDirection[1]*3)):
                movePlayer(app, app.playerDirection[0]*2, app.playerDirection[1]*2)
        
        #create a small dashing animation and paramat awer player.isDashing
        #dashing cooldown

##################################################
#TIMER FIRED STUFF
def timerFired(app):
    gameOverController(app)
    screenController(app)
    playerController(app)
    bulletController(app, app.playerBullets, True)
    enemyController(app)



################################################
#CONTROLLERS -- Stuff called under timer fired
def gameOverController(app):
    if(app.map.player.health <= 0):
        app.gameOver = True
        app.map.enemyList = []

def screenController(app):
    if(app.map and not app.generatingMap and not app.gameOver and not app.drawPowerUpScreen and len(app.map.enemyList) == 0):
        app.completedMap = True
        app.displayTimerScreen-=1
    
    if(app.gameOver):
        app.displayTimerScreen-=1
    if(app.gameOver and app.displayTimerScreen < 0):
        app.generatingMap = True
        initApp(app, True)
        
    if(app.completedMap and app.displayTimerScreen < 0):
        app.drawPowerUpScreen = True  
    
    if(app.drawPowerUpScreen and len(app.screenPowerUps) == 0):
        app.screenPowerUps = getAbilitiesAndParameters()
        
           
        #clicking a power up turns     


def playerController(app):
    app.map.player.incTimers()

    if(app.map.player.isDashing):
        app.map.player.dashingDuration+=1
    if(app.map.player.isDashing and app.map.player.dashingDuration > 5):
        app.map.player.isDashing = False  
        app.map.player.canDash = False
        app.map.player.dashingDuration = 0        
    
    if(app.map.player.dashingTimer > app.map.player.dashingCoolDown):
        app.map.player.canDash = True
        app.map.player.dashingTimer = 0

    if(app.map.player.shootingTimer > app.map.player.shootingCoolDown):
        app.map.player.canShoot = True
        app.map.player.shootingTimer = 0
    
    

def bulletController(app, bulletList, isPlayerBullet):
    for bullet in bulletList:
        bulletResult = bullet.linearTravel(app.map.map, app.map.offsetY, app.map.offsetX, isPlayerBullet)
        #if it returns something that's not true, we must have hit something
        if(bulletResult != 'success'):
            if(bulletResult == 'player'):
                bullet.damage(app.map.player)

            elif(isinstance(bulletResult, tuple)):
                enemy = app.map.findEnemy(bulletResult[0], bulletResult[1])
                if(enemy):
                    bullet.damage(enemy)
                else:
                    print('bruh wtf there should be an enemy here')

            if(bullet in bulletList):
                bulletList.remove(bullet)
        if(bullet.x < 0 or bullet.y < 0 or bullet.x > app.width or bullet.y > app.height):
            if(bullet in bulletList):
                bulletList.remove(bullet)    


def enemyController(app):
    for enemy in app.map.enemyList:
        if(enemy.health <= 0):
            app.map.enemyList.remove(enemy)
            app.map.map[enemy.gridY][enemy.gridX] = 0

        
        if(not app.map.player.isDashing):
            enemy.dealCollisionDmg(app.map.player)
        app.map.player.dealCollisionDmg(enemy)

        enemy.incTimers()
        #enemy fires at the player:
        if(enemy.shootingTimer > enemy.fireCoolDown):

            if(enemy.type == 'A'):
                enemy.fireBullet(EnemyBullet(enemy.x, enemy.y,
                                        enemy.boxSize, enemy.angle,
                                        enemy.type))
            else:
                numBullets = 4
                for x in range(numBullets):
                    enemy.fireBullet(EnemyBullet(enemy.x, enemy.y,
                        enemy.boxSize, enemy.angle+math.pi*2/numBullets*x,
                        enemy.type))


            enemy.shootingTimer = 0
        
        bulletController(app, enemy.bullets, False)

        #enemy moves according to their own set of movement lists
        if(enemy.movements):
            if(enemy.movementTimer > enemy.movementCoolDown):
                app.map.enemyAutoTravel(enemy)
                enemy.movementTimer = 0    

        
####################################


def runDaApp():
    runApp(width=900, height=900)

runDaApp()



