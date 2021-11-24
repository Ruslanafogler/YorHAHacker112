
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

    app.boxSize = 45
    app.gridSize = 15
    app.gameOver = False


    # app.player = Player(6, 8, app.boxSize)
    app.playerBullets = []
    # app.obstacleList = [Obsddtacle(a+4, 5, app.boxSize) for a in range(4)]
    app.map = Map(app.width, app.height, app.gridSize, app.boxSize)

    app.enemyPath = [(-1, 0), 
    (-1, 0), (0, -1), (-1, 0), (0, -1), (-1, 0), (0, -1), 
    (-1, 0), (0, -1), (-1, 0), (0, -1), (0, -1), (0, -1), (-1, 0),
    (-1, 0), (-1, 0), (0, -1), (-1, 0), (0, -1), (-1, 0), (0, -1), 
    (-1, 0), (0, -1), (-1, 0)]

    
    # app.mapGrid = MapGrid()


    app.mouseX = 0
    app.mouseY = 0


#grids on map inspired by KidsCanCode TilebasedGame pt1
#https://www.youtube.com/watch?v=3UxnelT9aCo&list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i&index=1
def drawBigGrid(app, canvas):
    for x in range(0, app.height, app.boxSize):
        canvas.create_line(x, 0, x, app.height, fill='#ffffff')

    for y in range(0, app.height, app.boxSize):
        canvas.create_line(0, y, app.width, y, fill='#ffffff')

def drawTinyGrid(app, canvas):
    for x in range(0, app.height, app.gridSize):
        canvas.create_line(x, 0, x, app.height, fill='#ffffff')

    for y in range(0, app.height, app.gridSize):
        canvas.create_line(0, y, app.width, y, fill='#83f52c')

def drawPlayerHealth(app, canvas):
    healthDisplayLength = app.boxSize*9
    healthDisplayWidth = app.boxSize

    healthRectLen = app.boxSize*7
    healthRectWidth = 5

    textMargin = 15

    healthBarX0 = app.boxSize//2 + textMargin
    healthBarY0 = app.boxSize//2 - healthRectWidth

    healthBarX1 = app.boxSize//2+15 + healthRectLen
    healthBarY1 = app.boxSize//2 + healthRectWidth




    canvas.create_rectangle(0,0, healthDisplayLength, healthDisplayWidth, fill = '#ffffff', width=0)
    canvas.create_text(app.boxSize//2, app.boxSize//2, text="HP:")
    canvas.create_rectangle(healthBarX0, healthBarY0, healthBarX1, healthBarY1, fill='#dad3c5', width=0)
    if(app.map.player.maxHealth != 0):
        fractionOfHealth = app.map.player.health/app.map.player.maxHealth
        canvas.create_rectangle(healthBarX0, healthBarY0, healthBarX1*(fractionOfHealth), healthBarY1, fill='#98fb98', width=0)



    

def redrawAll(app, canvas):

    if(not app.gameOver):
        
        #canvas.create_rectangle(0,0, app.width, app.height, fill='#7f7c69',)
        app.map.redrawAll(canvas, app.mouseX, app.mouseY)
        # app.mapGrid.redrawAll(canvas)
        for bullet in app.playerBullets:
            bullet.redrawAll(canvas)

        for enemy in app.map.enemyList:
            for bullet in enemy.bullets:
                bullet.redrawAll(canvas)
        # app.player.redrawAll(canvas, app.mouseX, app.mouseY)



        # canvas.create_text(100, 80, text=f'Player Angle {app.map.player.angle * 180/math.pi}')
        # canvas.create_text(100, 110, text=f'pointer Angle {(app.map.player.angle-app.map.player.theta)*180/math.pi}')



        drawBigGrid(app, canvas)
        drawPlayerHealth(app, canvas)
        #drawTinyGrid(app, canvas)
    else:
        canvas.create_rectangle(0,0, app.width, app.height, fill='black',)
        canvas.create_text(app.width//2, app.height//2, text=f'Game Over', fill='white')


def playerFireBullet(app):
    app.playerBullets.append(PlayerBullet(app.map.player.gridX, app.map.player.gridY,
                                          app.map.player.x, app.map.player.y, 
                                            app.boxSize, app.map.player.angle))


def keyPressed(app, event):
    playerMovement = 1
    if(event.key == 'a'):
        app.map.movePlayer(-playerMovement, 0)
    if(event.key == 'd' ):
        app.map.movePlayer(playerMovement, 0)
    if(event.key == 'w'):
        app.map.movePlayer(0, -playerMovement)
    if(event.key == 's'):
        app.map.movePlayer(0, playerMovement)
    if(event.key == 'Space'):
        playerFireBullet(app)
    # if(event.key == 'r'): 
    #     print('called')
    #     app.map.moveEnemy(app.map.enemyList[0], (0, 1))

def mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

def mousePressed(app, event):
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

def timerFired(app):
    if(app.map.player.health <= 0):
        app.gameOver = True

    bulletController(app, app.playerBullets, True)
    for enemy in app.map.enemyList:
        enemy.incTimers()

        #enemy fires at the player:
        if(enemy.shootingTimer > enemy.fireCoolDown):
            enemy.fireBullet(EnemyBullet(enemy.gridX, enemy.gridY,
                                        enemy.x, enemy.y,
                                        enemy.boxSize, enemy.angle,
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



