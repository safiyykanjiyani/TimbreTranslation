import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy.signal as sig
import scipy.optimize as opt
import plot_wave
import smstools.stft

def getData(path):
    soundfile = wave.open(path, 'rb') #open file in read mode
    parameters = soundfile.getparams() #returns a namedtuple() (nchannels, sampwidth, framerate, nframes, comptype, compname),
    nchannels, sampwidth, framerate, nframes = parameters[:4] #we only care about nchannels, bitrate, speed of play, and length
    soundframes = np.fromstring(soundfile.readframes(nframes), dtype=np.short) #put it into a numpy array
    soundfile.close()

    return soundframes, nchannels, sampwidth, framerate, nframes

def plotWave(soundfile, framerate, nframes):
    plot = plt.figure() #create a matplot
    plt.plot(np.arange((1, nframes + 1)* 1./ rate)), soundfile) #populate data of soundfile, given length of soundfile and pacing
    plot.show() #open window to show


if __name__ == '__main__':

    path = '/output_sounds/oboeviolin.wav'

    soundframes, nchannels, sampwidth, framerate, nframes = getData(path)
