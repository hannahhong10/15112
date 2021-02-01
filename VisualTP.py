#This part of the code creates all the visual components of the project that are displayed on the screen.

import librosa
import librosa.core
import numpy as np
import wave
import pygame
import math
import random
import time
import copy

###############################################################################
########################    Visual Portion     ################################
###############################################################################

######################  Basic Rotating Shapes #################################
###############################################################################

class Visuals(object):
    def __init__(app, colors, tempo, vertices = 1):#, number = 0):
        app.clock = pygame.time.Clock()
        app.r = 1
        app.red = 100
        app.blue = 100
        app.green = 100
        app.outline = 1
        app.width = 800
        app.height = 800
        app.cx = app.width // 2
        app.cy = app.height // 2
        app.canvas = pygame.display.set_mode((app.width, app.height))
        app.vertices = int(vertices)
        app.angleChange = (2 * math.pi) / app.vertices
        app.pointList = [ ]
        app.coordinates = [ ]
        app.colorList = colors
        app.counter = 0
        app.tickFactor = tempo * 0.04
    
    def addPointList(app, counter):
        for i in range(app.vertices * 20):
            coords = (app.cx + app.r * math.cos(app.angleChange * i + (2 * math.pi // 5) * counter), 
            app.cy - app.r * math.sin(app.angleChange * i + (2 * math.pi // 5) * counter))
            app.pointList.append(coords)
    
    def updateColors(app):
        if app.counter < len(app.colorList):
            color = app.colorList[app.counter]
            app.counter += 1
            return color
        else:
            return False

    def drawCircle(app):
        colors = app.updateColors()
        if colors != False:
            app.red = colors[0]
            app.green = colors[1]
            app.blue = colors[2]
        pygame.draw.circle(drawCanvas(), ((app.red, app.green, app.blue)),
            ((app.cx, app.cy)), app.r, app.outline)
        pygame.display.update()
    
    def drawIterationCircle(app, cx, cy):
        colors = app.updateColors()
        if colors != False:
            app.red = colors[0]
            app.green = colors[1]
            app.blue = colors[2]
        pygame.draw.circle(app.canvas, ((app.red, app.green, app.blue)),
            ((int(cx), int(cy))), app.r, app.outline)
        pygame.display.update()

    def drawManyCircles(app):
        counter = 0.5
        while app.r <= app.width:
            app.drawCircle()
            counter += 1
            app.r += 1
            pygame.display.update()
            app.clock.tick(app.tickFactor * 3 * counter)
        return app.r

    def drawOutlinedPolygon(app, counter):
        colors = app.updateColors()
        if colors != False:
            app.red = colors[0]
            app.green = colors[1]
            app.blue = colors[2]
        app.addPointList(counter)
        pygame.draw.polygon(drawCanvas(), (app.red, app.green, 
                app.blue), ((app.pointList)), app.outline)

    def drawSolidPolygon(app, counter):
        colors = app.updateColors()
        if colors != False:
            app.red = colors[0]
            app.green = colors[1]
            app.blue = colors[2]
        app.addPointList(counter)
        pygame.draw.polygon(app.canvas, (app.red, app.green, 
                app.blue), ((app.pointList)), 1)

    def drawManyOutlinedPolygons(app):
        counter = 0.5
        while app.r <= app.width + 70:
            app.drawOutlinedPolygon(counter)
            app.pointList = []
            counter += 1
            app.r += 1
            pygame.display.update()
            app.clock.tick(app.tickFactor * 2 * counter)
        return app.r

    def drawManySolidPolygons(app):
        counter = 0.5
        while app.r <= app.width + 125:
            app.drawSolidPolygon(counter)
            app.pointList = []
            counter += 0.5
            app.r += 1
            pygame.display.update()
            app.clock.tick(app.tickFactor * counter)
        return app.r
    
    def getCenterList(app, distance):
        centerList = [ ]
        realDistance = app.r * distance
        if distance == 0:
            circleNumber = 1
        else:
            circleNumber = distance * 6
        angleChange = (math.pi * 2) / (circleNumber)
        for i in range(circleNumber):
            newCx = app.cx + (realDistance * math.cos(angleChange * i))
            newCy = app.cy + (realDistance * math.sin(angleChange * i))
            centerList.append((newCx, newCy))
        return centerList

    def getRealDistance(app, distance):
        return distance * app.r

    def drawCircularFractals(app, radius):
        app.r = radius
        counter = 0
        distance = 0
        realDistance = distance * app.r
        while app.getRealDistance(distance) < 350:
            centerList = app.getCenterList(distance)
            for pair in centerList:
                app.drawIterationCircle(pair[0], pair[1])
                counter += 1
                pygame.display.update()
                app.clock.tick(app.tickFactor * 4)
            distance += 1
        return counter

########################    Recursive Fractals  ##############################
##############################################################################

    def getLength(app, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def getEndpoints(app, length, x1, y1, x2 = None, y2 = None):
        endpointList = [ ]
        angleChange = (2 * math.pi) / app.vertices
        if x2 == None and y2 == None:
            for i in range(0, app.vertices):
                newX = x1 + length * math.cos((-math.pi / 2) + angleChange * i)
                newY = y1 + length * math.sin((-math.pi / 2) + angleChange * i)
                endpointList.append((newX, newY))
        else:
            deltaX = x2 - x1
            deltaY = y2 - y1
            if deltaX == 0:
                oldAngle = math.pi / 2
            else:
                oldAngle = math.atan(deltaY / deltaX)
            for i in range(0, app.vertices):
                newAngle = oldAngle + (angleChange) * i
                newX = length * math.cos((-math.pi / 2) + angleChange * i) + x2
                newY = length * math.sin((-math.pi / 2) + angleChange * i) + y2
                endpointList.append((newX, newY))
        return endpointList

    def drawRecursivePattern(app, length, x1, y1, x2 = None, y2 = None, counter = 0):
        app.coordinates = app.getEndpoints(length, x1, y1, x2, y2)
        if x2 != None and y2 != None:
            if app.getLength(x1, y1, x2, y2) <= (app.vertices * 3):
                return
            else:
                for pair in app.coordinates:
                    if counter == None:
                        colors = app.updateColors()
                        if colors != False:
                            app.red = colors[0]
                            app.green = colors[1]
                            app.blue = colors[2]
                    pygame.draw.line(app.canvas, (app.red, app.green, app.blue), (x2, y2), (pair[0], pair[1]), 2)
                    pygame.display.update()
                    counter =+ 1
                    app.drawRecursivePattern(length // 2, x2, y2, pair[0], pair[1], counter)
        else:
            for pair in app.coordinates:
                colors = app.updateColors()
                if colors != False:
                    app.red = colors[0]
                    app.green = colors[1]
                    app.blue = colors[2]
                pygame.draw.line(app.canvas, (app.red, app.green, app.blue), (x1, y1), (pair[0], pair[1]), 2)
                counter += 1
                pygame.display.update()
                app.drawRecursivePattern(length // 2, app.cx, app.cy, pair[0], pair[1], counter)
        return counter
    
    def drawTransition(app):
        pygame.draw.circle(app.canvas, (0, 0, 0), (app.cx, app.cy), app.r, 1)
        pygame.display.update()

    def createTransition(app):
        counter = 1
        app.r = 1
        app.cx = app.width // 2
        app.cy = app.height // 2
        while app.r <= app.width:
            app.drawTransition()
            counter += 1
            app.r += 1
            app.clock.tick(2 * counter)
            pygame.display.update()

def drawCanvas():
    canvas = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Visual Window')
    canvas.fill((0, 0, 0))
    return canvas