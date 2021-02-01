#This audio file analyzes the amplitudes, and frequencies of the music at specific points in time.

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
########################     Audio Portion     ################################
###############################################################################

class Audio(object):
    def __init__(app, filename):
        app.filename = str(filename)
        app.ampLength = None
        app.frames = []
        app.data, app.sr = librosa.load(app.filename)
        app.fileLength = librosa.core.get_duration(filename = app.filename)

    def getAmpIncrement(app, event, timerDict, dataLength):
        if event == 0:
            time = timerDict[0]
        elif 1 <= event <= 6:
            time = timerDict[1]
        elif 7 <= event <= 12:
            time = timerDict[2]
        else:
            key = event - 10
            time = timerDict[key]
        timeFraction = time / app.fileLength
        return math.ceil(dataLength * timeFraction)

    def analyzeAmplitude(app, radDict, eventsList, timerDict):
        dataLength = len(app.data)
        app.data = abs(app.data)
        startingPoint = 0
        endPoint = None
        ampList = [ ]
        for event in eventsList:
            dataSplit = app.getAmpIncrement(event, timerDict, dataLength)
            endPoint = startingPoint + dataSplit
            timeframe = app.data[startingPoint:endPoint]
            if event == 0:
                rad = radDict[0]
            elif 1 <= event <= 6:
                rad = radDict[1]
            elif 7 <= event <= 12:
                rad = radDict[2]
            elif 13 <= event <= 18:
                key = event - 10
                rad = radDict[key]
            else:
                rad = radDict[9]
            ampIncrement = math.floor((len(timeframe) // rad))
            ampListAddition = timeframe[::ampIncrement]
            ampList.append(ampListAddition)
            startingPoint = endPoint
        lo = min(app.data)
        hi = max(app.data)
        return ampList, lo, hi

    def getFrequencyData(app):
        data = np.abs(librosa.core.stft(app.data))
        colData = len(data[0])
        rate = (colData // app.fileLength)
        rowData = len(data)
        return data, rowData, colData, rate