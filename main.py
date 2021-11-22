
#cmu 112 graphics from 
from cmu_112_graphics import *
import math
import numpy as np

from classes.Player import Player
from classes.EnemyA import EnemyA
from classes.EnemyB import EnemyB
from classes.Map import Map
from classes.BulletPlayer import PlayerBullet

#Game inspired by N.Automata Hacking and Hades Gameplay!



def appStarted(app):
    app.width = 900
    app.height = 900

    app.boxSize = 45
    app.gridSize = 15


    # app.player = Player(6, 8, app.boxSize)
    app.playerBullets = []
    # app.obstacleList = [Obstacle(a+4, 5, app.boxSize) for a in range(4)]
    app.map = Map(app.width, app.height, app.gridSize, app.boxSize)

    
    # app.mapGrid = MapGrid()

    app.enemies = []
    app.enemies.append(EnemyA(4, 4, app.boxSize))
    app.enemies.append(EnemyB(7, 7, app.boxSize))


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


def gonnaHitWallPlayer(app, moveX, moveY):
    newPlayerCol = app.map.player.gridX+moveX
    newPlayerRow = app.map.player.gridY+moveY
    nextSpotValue = app.map.map[newPlayerRow][newPlayerCol]
    print('player location', app.map.player.gridX, app.map.player.gridY)

    if(nextSpotValue == 1 or
     nextSpotValue == 4):
        return True
    else:
        return False

def getGridLocation(app, i):
    return int(i // app.boxSize)

# def gonnaHitWallBullet(app, bullet):
#     row = int(bullet.y // app.boxSize)
#     col = int(bullet.x // app.boxSize)
#     print('bullet r and c', col, row)
#     spotValue = app.map.map[row][col]
#     if(spotValue == 1 or spotValue == 4):
#         print("BULLET HIT WALL")
#         return True
#     else:
#         return False
    

    

#TEMPORARY
def movePlayer(app, moveX, moveY):
    if(not gonnaHitWallPlayer(app, moveX, moveY)):
        if(app.map.changeViewOffset(moveX, moveY)):
            app.map.player.gridX+=moveX
            app.map.player.gridY+=moveY
        else:
            app.map.player.move(moveX, moveY)
        



    

def redrawAll(app, canvas):
    
    #canvas.create_rectangle(0,0, app.width, app.height, fill='#7f7c69',)
    app.map.redrawAll(canvas, app.mouseX, app.mouseY)
    # app.mapGrid.redrawAll(canvas)
    for bullet in app.playerBullets:
        bullet.redrawAll(canvas)
    # app.player.redrawAll(canvas, app.mouseX, app.mouseY)


    # for enemy in app.enemies:
    #     enemy.redrawAll(canvas)
    canvas.create_text(100, 80, text=f'Player Angle {app.map.player.angle * 180/math.pi}')
    canvas.create_text(100, 110, text=f'pointer Angle {(app.map.player.angle-app.map.player.theta)*180/math.pi}')
    drawBigGrid(app, canvas)
    #drawTinyGrid(app, canvas)


def playerFire(app):
    app.playerBullets.append(PlayerBullet(app.map.player.gridX, app.map.player.gridY,
                                          app.map.player.x, app.map.player.y, 
                                            app.boxSize, app.map.player.angle))


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
        playerFire(app)

def mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

def mousePressed(app, event):
    playerFire(app)

def timerFired(app):
    for bullet in app.playerBullets:
        if(not bullet.linearTravel(app.map.map)):
            app.playerBullets.remove(bullet)
        if(bullet.x < 0 or bullet.y < 0 or bullet.x > app.width or bullet.y > app.height):
            app.playerBullets.remove(bullet)
        
        
    
        
def runDaApp():
    runApp(width=900, height=900)

runDaApp()



