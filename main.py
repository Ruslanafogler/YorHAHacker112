
#cmu 112 graphics from 
from cmu_112_graphics import *
import math
import numpy as np

from classes.Player import Player

from classes.Map import Map
from classes.Bullet import PlayerBullet, EnemyBullet


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
    if(fromRestart):
        app.playerHealth = 50
        app.maxPlayerHealth = 50
    
    
    
    app.map = Map(app.width, app.height, app.gridSize, 
                  app.boxSize, app.playerHealth, app.maxPlayerHealth)
        
    app.gameOver = False
    app.completedMap = False
    app.displayTimerScreen = 50

    app.drawPowerUpScreen = False
    app.generatingMap = False

    app.mouseX = 0
    app.mouseY = 0



#grids on map inspired by KidsCanCode TilebasedGame pt1
#https://www.youtube.com/watch?v=3UxnelT9aCo&list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i&index=1
def drawBigGrid(app, canvas):
    for x in range(0, app.height, app.boxSize):
        canvas.create_line(x, 0, x, app.height, fill='#ffffff')

    for y in range(0, app.height, app.boxSize):
        canvas.create_line(0, y, app.width, y, fill='#ffffff')


def redrawAll(app, canvas):

    if(app.drawPowerUpScreen):
        canvas.create_rectangle(0,0, app.width, app.height, fill='black',)
        canvas.create_text(app.width//2, app.height//2, text=f'Power Up', fill='white')
    elif(app.gameOver):
        canvas.create_rectangle(0,0, app.width, app.height, fill='black',)
        canvas.create_text(app.width//2, app.height//2, text=f'Game Over', fill='white')
    elif(app.generatingMap):
        canvas.create_rectangle(0,0, app.width, app.height, fill='black',)
        canvas.create_text(app.width//2, app.height//2, text=f'Generating Map..', fill='white')
    

    elif(not app.generatingMap):
        drawMap(app, canvas)
        drawPlayerBullets(app, canvas)
        drawEnemyBullets(app, canvas)
        drawBigGrid(app, canvas)
        drawPlayerHealth(app, canvas)

        
        if(app.completedMap):
            drawHackingCompleteText(app, canvas)



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




def playerFireBullet(app):
    app.playerBullets.append(PlayerBullet(app.map.player.x, app.map.player.y, 
                                          app.boxSize, app.map.player.angle))

def movePlayer(app, dcol, drow):
    app.map.movePlayer(dcol, drow)
    addBulletOffset(app, dcol, drow, app.playerBullets)
    for enemy in app.map.enemyList:
        addBulletOffset(app, dcol, drow, enemy.bullets)


def addBulletOffset(app, dcol, drow, bulletList):
    for bullet in bulletList:
        bullet.x-=dcol*app.boxSize
        bullet.y-=drow*app.boxSize


def keyPressed(app, event):
    playerMovement = 1
    if(event.key == 'a'):
        movePlayer(app, -playerMovement, 0)
    if(event.key == 'd' ):
        movePlayer(app, playerMovement, 0)
    if(event.key == 'w'):
        movePlayer(app, 0, -playerMovement)
    if(event.key == 's'):
        movePlayer(app, 0, playerMovement)
    if(event.key == 'Space'):
        playerFireBullet(app)


def mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

def advanceToNextRoom(app):
    app.generatingMap = True
    app.playerHealth = app.map.player.health
    app.maxPlayerHealth = app.map.player.maxHealth
    initApp(app, False)



def mousePressed(app, event):
    if(app.drawPowerUpScreen):
        x = event.x
        y = event.y
        if(x > 50 and y > 50):
            app.drawPowerUpScreen = False
            advanceToNextRoom(app)
    else:
        playerFireBullet(app)

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

def drawHackingCompleteText(app, canvas):
    canvas.create_text(app.height//2, app.width//2, text='- Hacking Complete -', font='Myriad 50 bold', fill='white')
    canvas.create_text(app.height//2, app.width//2+50, text='- Onto next level -', font='Myriad 15 bold', fill='white')



def timerFired(app):
    if(app.map.player.health <= 0):
        app.gameOver = True
        app.map.enemyList = []


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
        #clicking a power up turns 


    
    bulletController(app, app.playerBullets, True)
    
    for enemy in app.map.enemyList:
        if(enemy.health <= 0):
            app.map.enemyList.remove(enemy)
            app.map.map[enemy.gridY][enemy.gridX] = 0

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
        
    
        
def runDaApp():
    runApp(width=900, height=900)

runDaApp()



