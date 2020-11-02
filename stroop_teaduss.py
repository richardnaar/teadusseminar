# sProov
from numpy.random import random
# import numpy as np
import psychopy
# , logging, monitors, sound, locale_setup
from psychopy import gui, visual, core, data, event

import pandas as pd

import os

# expInfo
# get the current directory
dirpath = os.getcwd()

expName = os.path.basename(__file__)
expInfo = {'Participant': '001'}

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel

expInfo['date'] = data.getDateStr()  # add a simple timestamp


expName = os.path.basename(__file__)
psychopyVersion = psychopy.__version__
filename = dirpath + '\\data\\' + \
    expInfo['Participant'] + '_' + expName + '_' + expInfo['date']

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(
    name=expName, version=psychopyVersion,
    extraInfo=expInfo, runtimeInfo=None,
    originPath=dirpath + '\\' + os.path.basename(__file__),
    savePickle=True, saveWideText=True,
    dataFileName=filename)

# condition data
xls_file = pd.ExcelFile('conditions' + '.xlsx')
table = xls_file.parse()

repN = 1  # repeat table repN times
table = pd.concat([table]*repN, ignore_index=True)
# shuffle a whole table
table = table.sample(frac=1).reset_index(drop=False)

clock = core.Clock()

# from psychopy import visual
monSettings = {'size': (800, 600), 'fullscr': False}

win = visual.Window(
    size=monSettings['size'], fullscr=monSettings['fullscr'], screen=0, color='black',
    blendMode='avg', useFBO=False, monitor='testMonitor',
    units='deg', waitBlanking=True)

stroopText = visual.TextStim(win=win,
                             text='text',
                             font='Arial',
                             pos=(0, 0), height=0.7, wrapWidth=20, ori=0,
                             color='white', colorSpace='rgb', opacity=1,
                             languageStyle='LTR',
                             depth=0.0, alignHoriz='center')


def draw_iti(win, iti_dur_default):
    iti_time = clock.getTime()  # win.getFutureFlipTime(clock='ptb')  #
    iti_dur = random() + iti_dur_default
    itiPresented = False
    time = clock.getTime() - iti_time
    while (time) < iti_dur:

        win.flip()
        if not itiPresented:
            thisExp.addData('itiStartTime', clock.getTime())
            itiPresented = True

        time = clock.getTime() - iti_time


def draw_stim(win, stim_dur):
    stim_time = clock.getTime()  #
    stimPresented = False
    time = clock.getTime() - stim_time
    noResp = True
    while (time) < stim_dur and noResp:
        if not stimPresented:
            thisExp.addData('stimStartTime', clock.getTime())
            stimPresented = True

        theseKeys = event.getKeys(keyList=['left', 'down', 'right', 'q'])
        if len(theseKeys) < 1:
            # draw stim and flip
            stroopText.draw()
            win.flip()
        elif theseKeys[0] != 'q':
            RT = clock.getTime() - stim_time
            keyPressed = theseKeys[0]
            if table['respCorr'][trialNumber] == keyPressed:
                correct = 1
            else:
                correct = 0
            noResp = False
        else:
            core.quit()
        time = clock.getTime() - stim_time
        # thisExp == an ExperimentHandler isn't essential but helps with data saving

    if noResp:
        thisExp.addData('RT', 'noResp')
        thisExp.addData('respKey', 'noResp')
        thisExp.addData('correct', 'noResp')
    else:
        thisExp.addData('RT', RT)
        thisExp.addData('respKey', keyPressed)
        thisExp.addData('correct', correct)


# this is the start of the experiment loop
nTrials = len(table)

trialNumber = 0
runExperiment = True
theseKeys = event.getKeys(keyList=['q'])
while runExperiment and (len(theseKeys) < 1):

    trialNumber += 1

    # if it is the end of the experiment loop
    if trialNumber == nTrials:
            # close and quit
            # draw goodby text
        runExperiment = False
        win.close(), core.quit()
    # if it is not the end of the experiment yet
    elif trialNumber == nTrials:
        break

    # draw things here
    stroopText.color = table['rgb'][trialNumber]
    stroopText.text = table['word'][trialNumber]

    draw_stim(win, 3)
    draw_iti(win, 1)

    theseKeys = event.getKeys(keyList=['q'])
    # thisExp == an ExperimentHandler isn't essential but helps with data saving
    thisExp.addData('respCorr', table['respCorr'][trialNumber])
    thisExp.addData('colour', table['colour'][trialNumber])
    thisExp.addData('congruent', table['congruent'][trialNumber])
    thisExp.addData('word', table['word'][trialNumber])

    thisExp.nextEntry()

core.quit()
