import librosa
import librosa.core
import numpy as np
import wave
import pygame
import math
import random
import time
import copy
from VisualTP import *
from AudioTP import *

#This is the main part of the code that contains the code for the User Interface and converts the
#audio data into attributes of the visual patterns. It also syncs up the music and visuals.

###############################################################################
####################         User Interface         ###########################
###############################################################################

class TextBox(object):
    def __init__(app):
        app.backgroundColor = (0, 0, 0)
        app.font = 'arialrounded'

    def drawTextBox(app, canvas, cx, cy, width, height):
        dwidth = width // 2
        dheight = height // 2
        pygame.draw.rect(canvas, (app.backgroundColor), ((cx - dwidth), (cy - dheight), width, height))
        pygame.draw.rect(canvas, (200, 0, 0), ((cx - dwidth), (cy - dheight), width, height), 5)

    def updateLetter(self, canvas, string):
        pygame.font.init()
        font = pygame.font.SysFont('arialrounded', 30)

class OpenScreen(object):
    def __init__(app):
        app.width = 800
        app.height = 800
        app.cx = app.width // 2
        app.cy = app.height // 2
        app.canvas = pygame.display.set_mode((app.width, app.height))
        app.canvas.fill((0, 0, 0))
# https://www.freepik.com/free-vector/red-sound-wave-equalizer-vector-design_3833274.htm#page=1&query=sound%20bars&position=7
        app.backDrop = pygame.image.load('Music_Background.png')

    def createFirstScreen(app, number):
        app.canvas.blit(app.backDrop, (0, 0))
        r = app.width // 6
        if number == 1:
            pygame.draw.rect(app.canvas, ((180, 0, 0)), ((app.width * 3 // 7) - 50, app.height * 0.75, app.width // 4, app.height // 8), 5)
            pygame.display.update()
        elif number == 3:
            pygame.draw.rect(app.canvas, ((180, 0, 0)), (app.width // 5, app.height * 0.75, app.width // 5, app.height // 7), 5)
            pygame.draw.rect(app.canvas, ((180, 0, 0)), (app.width * 3 // 5, app.height * 0.75, app.width // 5, app.height // 7), 5)
            pygame.display.update()
        pygame.display.update()

    def createFirstScreenText(app):
        app.createFirstScreen(1)
        pygame.font.init()
        font = pygame.font.SysFont('arialrounded', 30)
        titleFont = pygame.font.SysFont('arialrounded', 60)
        playText = font.render('START', False, ((255, 255, 255)))
        titleText = titleFont.render('VISUAL HARMONIES', False, ((230, 0, 0)))
        app.canvas.blit(playText, (app.width // 2 - 58, app.height * 0.79))
        app.canvas.blit(titleText, ((app.width / 10, app.height * 0.20)))
        pygame.display.update()
    
    def typing(app):
        pygame.font.init()
        font = pygame.font.SysFont('arialrounded', 30)
        wavTitle = ''
        while len(wavTitle) < 32:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    charName = str(pygame.key.name(event.key))
                    if charName == 'return':
                        try:
                            duration = librosa.core.get_duration(filename = wavTitle)
                            app.drawLoadingScreen(duration, wavTitle)
                            return
                        except:
                            errorFont = pygame.font.SysFont('arialrounded', 15)
                            errorText = errorFont.render('Error: No File Found', False, ((200, 200, 200)))
                            app.canvas.blit(errorText, (((app.width * 3 // 7) - 15, app.height * 0.90)))
                            pygame.display.update()
                    elif charName == 'backspace':
                        length = len(wavTitle)
                        wavTitle = wavTitle[0:length - 1]
                        wavText = font.render(wavTitle, False, ((200, 200, 200)))
                        app.createSecondScreen()
                        app.canvas.blit(wavText, ((app.width * 1 / 7, app.height * 0.83)))
                        pygame.display.update()
                    elif charName == 'space':
                        wavTitle += ' '
                        wavText = font.render(wavTitle, False, ((200, 200, 200)))
                        app.canvas.blit(wavText, ((app.width * 1 / 7, app.height * 0.83)))
                        pygame.display.update()
                    else:
                        wavTitle += charName
                        wavText = font.render(wavTitle, False, ((200, 200, 200)))
                        app.canvas.blit(wavText, ((app.width * 1 / 7, app.height * 0.83)))
                        pygame.display.update()

    def createSecondScreen(app, boolean = False):
        app.createFirstScreen(2)
        pygame.font.init()
        font = pygame.font.SysFont('arialrounded', 30)
        instructionText = font.render('Please enter a .wav file:', False, ((230, 0, 0)))
        textBox = TextBox()
        textBox.drawTextBox(app.canvas, app.cx, app.height * 0.85, 600, 50)
        app.canvas.blit(instructionText, ((app.width / 7, app.height * 0.20)))
        pygame.display.update()
        if boolean == True:
            app.typing()

    def drawEndScreen(app):
        app.createFirstScreen(3)
        pygame.font.init()
        font = pygame.font.SysFont('arialrounded', 30)
        titleFont = pygame.font.SysFont('arialrounded', 40)
        recordText = font.render('NEW FILE', False, ((255, 255, 255)))
        playText = font.render('CLOSE', False, ((255, 255, 255)))
        titleText = titleFont.render('VISUALS OVER', False, ((230, 0, 0)))
        app.canvas.blit(recordText, (app.width // 5 + 8, app.height * 0.79))
        app.canvas.blit(playText, (app.width * 3 // 5 + 27, app.height * 0.79))
        app.canvas.blit(titleText, ((app.width / 10, app.height * 0.20)))
        pygame.display.update()

    def drawLoadingScreen(app, duration, wavTitle):
        pygame.font.init()
        font = pygame.font.SysFont('arialrounded', 30)
        loadingText = font.render('CALIBRATING', False, ((180, 0, 0)))
        drawCanvas().blit(loadingText, ((app.width // 2 - 110, app.height // 2)))
        pygame.display.update()
        audioFile = Audio(wavTitle)
        tempo = getTempo(wavTitle)
        timerDict, radDict = getDicts(tempo)
        freqData, rowData, colData, rate = audioFile.getFrequencyData()
        eventsList = makeEventsList(timerDict, duration, freqData, rowData, colData, rate)
        ampList, lo, hi = audioFile.analyzeAmplitude(radDict, eventsList, timerDict)
        colorList = returnColorList(wavTitle, ampList, lo, hi)
        startFont = pygame.font.SysFont('arialrounded', 30)
        startText = font.render('FINISHED CALIBRATING', False, ((230, 0, 0)))
        drawCanvas().blit(startText, (app.width // 2 - 180, app.height // 2))
        pygame.display.update()
        initVisual(tempo, eventsList, radDict, wavTitle, ampList, colorList)
        app.drawEndScreen()

    def clickLastButton(app):
        button = True
        while button == True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    place = pygame.mouse.get_pos()
                    if (app.width // 5) <= place[0] <= (2 * app.width // 5) and (app.height * 
                        0.75) <= place[1] <= (app.height * 0.75 + app.height // 7):
                        app.createSecondScreen(True)
                    elif (app.width * 3 // 5) <= place[0] <= (app.width * 4 // 5) and (app.height * 
                        0.75) <= place[1] <= (app.height * 0.75 + app.height // 7):
                        button = False
                        pygame.quit()
                        quit()

    def clickButton(app):
        button = True
        while button == True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    place = pygame.mouse.get_pos()
                    if (app.width * 3 // 7) - 50 <= place[0] <= ((app.width * 3 // 7) - 50 + app.width // 4) and (app.height * 
                        0.75) <= place[1] <= (app.height * 0.75 + app.height // 8):
                        button = False
                        app.createSecondScreen(True)

            pygame.draw.rect(app.canvas, ((180, 0, 0)), ((app.width * 3 // 7) - 50, app.height * 0.75, app.width // 4, app.height // 8), 5)


###############################################################################
####################   Combine Audio and Visual     ###########################
###############################################################################

def getTempo(filename):
    y, sr = librosa.load(filename)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    return tempo

def drawCanvas():
    canvas = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Visual Window')
    canvas.fill((0, 0, 0))
    return canvas

def createCircle(colors, tempo):
    startTime = time.time()
    circle = Visuals(colors, tempo)
    rad = circle.drawManyCircles()
    endTime = time.time()
    totalTime = endTime - startTime
    return (totalTime, rad)

def createOutlinedPolygons(colors, vertices, tempo):
    startTime = time.time()
    polygon = Visuals(colors, tempo, vertices)
    rad = polygon.drawManyOutlinedPolygons()
    endTime = time.time()
    totalTime = endTime - startTime
    return (totalTime, rad)

def createSolidPolygons(colors, vertices, tempo):
    startTime = time.time()
    solPoly = Visuals(colors, tempo, vertices)
    rad = solPoly.drawManySolidPolygons()
    solPoly.createTransition()
    endTime = time.time()
    totalTime = endTime - startTime
    return (totalTime, rad)

def drawFractals(colors, vertices):
    recursion = Visuals(colors, 1, vertices)
    rad = recursion.drawRecursivePattern(recursion.width // 5, recursion.cx, recursion.cy)
    recursion.createTransition()

def drawCircleFractals(colors, tempo):
    startTime = time.time()
    fractals = Visuals(colors, tempo)
    radius = int((1 / tempo) * 10000)
    rad = fractals.drawCircularFractals(radius)
    fractals.createTransition()
    endTime = time.time()
    totalTime = endTime - startTime
    return (totalTime, rad)

def makeBinList(timerDict, duration, freqData, rowData, colData, rate):
    totalTime = 0
    for i in range(9):
        totalTime += timerDict[i]
    averageTimePerEvent = totalTime / 9
    eventNumber = int(duration // averageTimePerEvent)
    eventsList = [ ]
    time = 0
    for i in range(eventNumber):
        listAppend = getBin(time, freqData, rowData, colData, rate)
        time += (totalTime / eventNumber)
        eventsList.append(listAppend)
    total = 0
    for i in range(len(eventsList)):
        total += eventsList[i]
    average = total / (len(eventsList))
    eventsCopy = copy.copy(eventsList)
    for value in eventsCopy:
        if value - average > 200:
            eventsList.remove(value)
    hi = max(eventsList)
    lo = min(eventsList)
    return lo, hi

def makeEventsList(timerDict, duration, freqData, rowData, colData, rate):
    lo, hi = makeBinList(timerDict, duration, freqData, rowData, colData, rate)
    totalTime = 0
    eventsList = [ ]
    eventsDict = {'circle': 0, 'OP3': 1, 'OP4': 2, 'OP5': 3, 'OP6': 4, 'OP7': 5, 'OP8': 6,
    'SP3': 7, 'SP4': 8, 'SP5': 9, 'SP6': 10, 'SP7': 11, 'SP8': 12, 'F3': 13,
    'F4': 14, 'F5': 15, 'F6': 16, 'F7': 17, 'F8': 18, 'FCircle': 19}
    while totalTime <= duration:
        if totalTime - duration > 6:
            eventsList.pop()
        pattern = random.randint(0, 8)
        if pattern == 0:
            eventsList.append(eventsDict['circle'])
            totalTime += timerDict[0]
        elif pattern == 1 or pattern == 2:
            vertices = getVertex(totalTime, freqData, rowData, colData, rate, lo, hi)
            key = 'OP' + str(vertices)
            eventsList.append(eventsDict[key])
            totalTime += timerDict[1]
        elif pattern == 3 or pattern == 4:
            vertices = getVertex(totalTime, freqData, rowData, colData, rate, lo, hi)
            key = 'SP' + str(vertices)
            eventsList.append(eventsDict[key])
            totalTime += timerDict[2]            
        elif pattern == 5 or pattern == 6:
            vertices = getVertex(totalTime, freqData, rowData, colData, rate, lo, hi)
            key = 'F' + str(vertices)
            eventsList.append(eventsDict[key])
            totalTime += timerDict[vertices]
        else:
            eventsList.append(eventsDict['FCircle'])
            totalTime += timerDict[9]
    return eventsList

def getBin(time, freqData, rowData, colData, rate):
    colIndex = math.floor(time * rate)
    if colIndex > colData:
        colIndex = colData - 1
    highestValue = -1
    for i in range(rowData):
        currValue = freqData[i, colIndex]
        if currValue > highestValue:
            highestI = i
            highestValue = currValue
    return highestI

def getVertex(time, freqData, rowData, colData, rate, lo, hi):
    binIndex = getBin(time, freqData, rowData, colData, rate)
    percentThrough = 1 - ((binIndex - lo) / 100)#(hi - lo))
    vertices = int((percentThrough * 5) + 3)
    if percentThrough < 0:
        vertices = 3
    return vertices

def getDicts(tempo):
    red = (255, 0, 0)
    timerDict = dict()
    radDict = dict()
    timerDict[0], radDict[0] = createCircle([red], tempo)
    timerDict[1], radDict[1] = createOutlinedPolygons([red], 4, tempo)
    timerDict[2], radDict[2] = createSolidPolygons([red], 4, tempo)
    timerDict[3], radDict[3] = 5, 3
    timerDict[4], radDict[4] = 5.1, 4
    timerDict[5], radDict[5] = 8.2, 5
    timerDict[6], radDict[6] = 14, 6
    timerDict[7], radDict[7] = 6.9, 7
    timerDict[8], radDict[8] = 9.1, 8
    timerDict[9], radDict[9] = drawCircleFractals([red], tempo)
    return (timerDict, radDict)

#this function would get the colors when given an amplitude
def getColors(amplitude, firstQuartile, secondQuartile, thirdQuartile, rate):
    if amplitude <= firstQuartile:
        red = int(abs(amplitude) * rate)
        if red > 255:
            red = 255
        green = 0
        blue = 255
        return ((red, green, blue))
    elif firstQuartile < amplitude < secondQuartile:
        red = 0
        green = 255
        newAmp = amplitude - firstQuartile
        blue = 255 - (newAmp * rate)
        if blue < 0:
            blue = 0
        return ((red, green, blue))
    elif secondQuartile <= amplitude <= thirdQuartile:
        newAmp = amplitude - secondQuartile
        red = int(newAmp * rate)
        if red > 255:
            red = 255
        green = 255 - int(newAmp * rate)
        if green < 0:
            green = 0
        blue = 0
        return ((red, green, blue))
    elif amplitude > thirdQuartile:
        red = 255
        newAmp = amplitude - thirdQuartile
        green = int(newAmp * rate)
        if green > 255:
            green = 255
        blue = 0
        return ((red, green, blue))

def returnColorList(filename, ampList, lo, hi):
    increment = (hi - lo) / 4
    firstQuartile = lo + increment
    secondQuartile = firstQuartile + increment
    thirdQuartile = secondQuartile + increment
    rate = 255 // (increment)
    colorList = [ ]
    for l in ampList:
        shapeColorList = [ ]
        for entry in l:
            rbgVal = getColors(entry, firstQuartile, secondQuartile, thirdQuartile, rate)
            shapeColorList.append(rbgVal)
        colorList.append(shapeColorList)
    return colorList

def initVisual(tempo, eventsList, radDict, filename, ampList, colorList):
    audioFile = Audio(filename)
    wf = wave.open(audioFile.filename, 'rb')
    frequency = wf.getframerate()
    pygame.mixer.quit()
    pygame.mixer.init(frequency = frequency)
    pygame.mixer.music.load(audioFile.filename)
    pygame.mixer.music.set_volume(0.04)
    pygame.mixer.music.play()
    for i in range(len(eventsList)):
        key = eventsList[i]
        if eventsList[i] == 0:
            createCircle(colorList[i], tempo)
        elif 1 <= key <= 6:
            vertex = key + 2
            createOutlinedPolygons(colorList[i], vertex, tempo)
        elif 7 <= key <= 12:
            vertex = key - 4
            createSolidPolygons(colorList[i], vertex, tempo)
        elif 13 <= key <= 18:
            vertex = key - 10
            drawFractals(colorList[i], vertex)
        else:
            drawCircleFractals(colorList[i], tempo)
        
def main():
    pygame.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            quit()
    screen = OpenScreen()
    screen.createFirstScreenText()
    screen.clickButton()
    screen.clickLastButton()

if __name__ == '__main__':
    main()