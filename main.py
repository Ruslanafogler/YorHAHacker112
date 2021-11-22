
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


def gonnaHitWall(app, moveX, moveY):
    newPlayerCol = app.map.player.rowX+moveX
    newPlayerRow = app.map.player.rowY+moveY
    nextSpotValue = app.map.map[newPlayerRow][newPlayerCol]
    print('player location', app.map.player.rowX, app.map.player.rowY)

    if(nextSpotValue == 1 or
     nextSpotValue == 4):
        return True
    else:
        return False


#TEMPORARY
def movePlayer(app, moveX, moveY):
    if(not gonnaHitWall(app, moveX, moveY)):
        if(app.map.changeViewOffset(moveX, moveY, app.map.player.rowX, app.map.player.rowY)):
            app.map.player.rowX+=moveX
            app.map.player.rowY+=moveY
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
        app.playerBullets.append(PlayerBullet(app.map.player.x, app.map.player.y, app.map.player.angle))
    # if(event.key == 'r'):
    #     app.player.rotateShape(math.pi/180*5)
    # if(event.key == 't'):
    #     pass
   
def mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

# def mousePressed(app, event):
#     app.playerBullets.append(PlayerBullet(app.player.x, app.player.y, app.player.angle))

def timerFired(app):
    for bullet in app.playerBullets:
        if(bullet.x < 0 or bullet.y < 0 or bullet.x > app.width or bullet.y > app.height):
            app.playerBullets.remove(bullet)
        bullet.linearTravel()
        
    
        
def runDaApp():
    runApp(width=900, height=900)

runDaApp()



