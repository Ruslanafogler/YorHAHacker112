from cmu_112_graphics import *
import math

#DEFINE CLASSES
class Moveable:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class EnemyA(Moveable):
     def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 20
        self.centerLength = 12.5


     def redrawAll(self, canvas):
         canvas.create_polygon(
                            self.x-self.centerLength, self.y-self.centerLength,
                            self.x, self.y-2*self.centerLength,
                            self.x+self.centerLength, self.y-self.centerLength,
                            self.x+self.centerLength, self.y + self.centerLength,
                            self.x-self.centerLength, self.y+self.centerLength,
                            fill='#3a3b3c'
                            )


class EnemyB(Moveable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.enemyR = 15
        

    def redrawAll(self, canvas):
        canvas.create_oval(self.x - self.enemyR, self.y-self.enemyR,
                    self.x + self.enemyR, self.y + self.enemyR, fill='#242526')



class Obstacle:
    pass



class Player(Moveable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 20
        self.centerDownLength = 20
        self.centerUpLength = 40
        self.angle = 0

        self.x1, self.y1 = self.x-self.width, self.y
        self.x2, self.y2 = self.x, self.y - self.centerUpLength
        self.x3, self.y3 = self.x + self.width, self.y
        self.x4, self.y4 = self.x, self.y + self.centerDownLength



    def redrawAll(self, canvas, mouseX, mouseY):
        self.x1, self.y1 = self.x-self.width, self.y
        self.x2, self.y2 = self.x, self.y - self.centerUpLength
        self.x3, self.y3 = self.x + self.width, self.y
        self.x4, self.y4 = self.x, self.y + self.centerDownLength
        
        canvas.create_polygon(self.x1, self.y1,
                              self.x2, self.y2,
                              self.x3, self.y3,
                              self.x4, self.y4, 
                              fill='white')
        
                              
        canvas.create_text(100, 100, 
        text=f'{Player.getPlayerAngle(self, mouseX, mouseY)*180/math.pi}')
        

        # test = True
        # if(test):
        #     Player.rotateShape(self, angle)
        # else:
        #     x1, y1, x2, y2, x3, y3, x4, y4 = Player.rotateShape(self, mouseX, mouseY)
        
        # canvas.create_polygon(x1, y1,
        #                       x2, y2,
        #                       x3, y3,
        #                       x4, y4)
        

    def moveX(self, x):
        self.x+=x

    def moveY(self, y):
        self.y+=y
    
        
    def getPlayerAngle(self, mouseX, mouseY):
        angle = (Player.getAngle(self.x, self.y, mouseX, mouseY) + math.pi/2) % (math.pi*2)
        print(angle*180/math.pi)
        return angle

    def rotateShape(self, angle):
        originX = self.x
        originY = self.y
        self.x1, self.y1 = Player.do2dRotation(originX, originY, self.x1, self.y1, angle)
        self.x2, self.y2 = Player.do2dRotation(originX, originY, self.x2, self.y2, angle)
        self.x3, self.y3 = Player.do2dRotation(originX, originY, self.x3, self.y3, angle)
        self.x4, self.y4 = Player.do2dRotation(originX, originY, self.x4, self.y4, angle)
        self.angle = angle
        

        
        

        
    #dumb methods
    @staticmethod
    def getDistance(x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def getAngle(x, y, x1, y1):
        angle = math.atan2(y1-y, x1-x)
        return angle

    def do2dRotation(ox, oy, x,y, angle):
        rotationMatrix = [[math.cos(angle), -math.sin(angle)],
                            [math.sin(angle), math.cos(angle)]]
        newX = ox + math.cos(angle)*(x - ox) + (-math.sin(angle))*(y - oy)
        newY = oy + (math.sin(angle))*(x - ox) + (math.cos(angle))*(y - oy)
        return newX,newY 





class Projectile:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color



class Map:
    def __init__(self, width, height):
        self.margin = 100
        self.width = 500
        self.height = 500

    def redrawAll(self, canvas):
        canvas.create_rectangle(
            self.margin, self.margin,
            self.margin+self.width, self.margin+self.width,
            fill='#bfba9e',
            width = 0
        )













#RUN APP

def appStarted(app):
    app.width = 700
    app.height = 700
    app.player = Player(350, 350)
    app.map = Map(500, 500)

    app.enemies = []
    app.enemies.append(EnemyA(200, 200))
    app.enemies.append(EnemyB(450, 450))
    app.mouseX = 0
    app.mouseY = 0
    

def redrawAll(app, canvas):
    # app.player.rotateShape(app.player.getPlayerAngle(app.mouseX, app.mouseY))
    canvas.create_rectangle(0,0, app.width, app.height, fill='#7f7c69',)
    app.map.redrawAll(canvas)
    app.player.redrawAll(canvas, app.mouseX, app.mouseY)
    for enemy in app.enemies:
        enemy.redrawAll(canvas)
    canvas.create_line(app.player.x,app.player.y,app.mouseX,app.mouseY)
    canvas.create_line(app.player.x,app.player.y, app.player.x, 50)

def keyPressed(app, event):
    playerMovement = 15
    if(event.key == 'a'):
        app.player.moveX(-playerMovement)
    if(event.key == 'd'):
        app.player.moveX(playerMovement)
    if(event.key == 'w'):
        app.player.moveY(-playerMovement)
    if(event.key == 's'):
        app.player.moveY(playerMovement)
    if(event.key == 'r'):
        app.player.rotateShape(math.pi/180)

def mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

# def timerFired(app):
#     app.player.rotateShape(math.pi/180)
    
        
def runDaApp():
    runApp(width=700, height=700)

runDaApp()


        
