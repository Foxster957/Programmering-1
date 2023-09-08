from cmu_graphics import *
import math

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def normalize(vector):
    vectorMag = math.sqrt(vector.x**2 + vector.y**2)  # pythagorean theorem to calculate vector magnitude
    
    if vectorMag > 0:   # check to avoid division by zero
        vector.x = vector.x/vectorMag   # 
        vector.y = vector.y/vectorMag
    
    return vector


def onKeyHold(key):
    xChanged = False
    yChanged = False
    moveVector = Vector2D(0, 0)
    
    if 'up' in key or 'w' in key:
        if app.square.top <= 0:
            app.square.top = 0
            yChanged = True
        else:
            moveVector.y -= 1
        
    if 'down' in key or 's' in key:
        if app.square.bottom >= 400:
            app.square.bottom = 400
            yChanged = True
        else:
            moveVector.y += 1
        
    if 'left' in key or 'a' in key:
        if app.square.left <= 0:
            app.square.left = 0
            xChanged = True
        else:
            moveVector.x -= 1
        
    if 'right' in key or 'd' in key:
        if app.square.right >= 400:
            app.square.right = 400
            xChanged = True
        else:
            moveVector.x += 1
    
    
    if xChanged:
        moveVector.x = 0
    if yChanged:
        moveVector.y = 0
    
    
    moveVector = normalize(moveVector)
    
    app.square.centerX += moveVector.x*app.moveSpeed
    app.square.centerY += moveVector.y*app.moveSpeed
    

app.stepsPerSecond = 120
app.moveSpeed = 2
app.squareX = 200
app.squareY = 200
app.squareW = 20
app.squareH = 20
app.square = Rect(app.squareX-app.squareW/2, app.squareY-app.squareH/2, app.squareW, app.squareH)


cmu_graphics.run()