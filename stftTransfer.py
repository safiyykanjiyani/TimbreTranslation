import numpy as np
import sys
import os
import math
from scipy.signal import resample
import smstools.dftModel

def stftTransfer(reciever, donor, framerate, size1, N1, size2, N2, hop, smoothing, transfer):

	# donor and reciever are sound files
	# donor transfers timbral characteristics to the reciever
	# framerate is rate of audio



	recieverAnalysisWindow = (int(math.floor((size1.size+1)/2)),int(math.floor(size1.size/2))) # calculating size of analysis window, usually 512
	length = int(reciever.size/hop) # this is the track length of the reciever divided by hop size
	reciever = np.append(np.zeros(recieverAnalysisWindow[1]), reciever) # we create padding so that we can edit and synthesis audio at the beginning
	reciever = np.append(reciever, np.zeros(recieverAnalysisWindow[0])) # and at the end
	recieverSave = recieverAnalysisWindow[1] # this is where we are in analysis window
	size1 = size1 / sum(size1)

	# we know do initialization for donor as well
	donorAnalysisWindow = (int(math.floor((size2.size+1)/2)), int(math.floor(size2.size/2)))
	donorHop = int(donor.size/length) # hop size for donor
	donor = np.append(np.zeros(donorAnalysisWindow[1]), donor)
	donor = np.append(donor, np.zeros(donorAnalysisWindow[0]))
	donorSave = donorAnalysisWindow[0]

	# output population
	output = np.zeros(reciever.size) # our output is a numpy array which we later on make an audio file.
	for i in range(length):

		# initialize progress variables, which account for where we are in the files (saves) as well as the window size (analysisWindow)
		# and together they give us a range to analyze and synthesize on
		recieverProgress1 = recieverSave - recieverAnalysisWindow[0]
		recieverProgress2 = recieverSave + recieverAnalysisWindow[1]
		donorProgress1 = donorSave - donorAnalysisWindow[0]
		donorProgress2 = donorSave + donorAnalysisWindow[1]



		recieverMagnitude, recieverPhase = smstools.dftModel.dftAnal(reciever[recieverProgress1:recieverProgress2], size1, N1) # we use dft.anal to get back the dft of the reciever, which returns a magnitude and phase spectrum
		donorMagnitude, donorPhase = smstools.dftModel.dftAnal(donor[donorProgress1:donorProgress2], size2, N2) # we use dft.anal to get back the dft of the donor, which returns a magnitude and phase spectrum
		#sineMagnitude, sinePhase = smstools.dftModel.dftAnal(sine[sineProgress1:sineProgress2], size2, N2) # we use dft.anal to get back the dft of the sine, which returns a magnitude and phase spectrum


		# this is where editing of the audio happens
		donorMagnitudeEdited = resample(np.maximum(-200, donorMagnitude), int(donorMagnitude.size*smoothing))
		donorMagnitude = resample(donorMagnitudeEdited, recieverMagnitude.size)
		#synthesis = transfer * donorMagnitude - (transfer) * sineMagnitude + (1 - transfer) * recieverMagnitude
		synthesis = transfer * donorMagnitude + (1 - transfer) * recieverMagnitude
		#synthesis = donorMagnitude + recieverMagnitude


		# in the range we are analyzing and editing on,
		# use the synthesized magnitude and the original phase
		# to generate an output
		output[recieverProgress1:recieverProgress2] += hop*smstools.dftModel.dftSynth(synthesis, recieverPhase, size1.size)

		recieverSave = recieverSave + hop
		donorSave = donorSave + donorHop

	#cleanup by removing padding added at the beginning on the reciever
	output = np.delete(output, range(recieverAnalysisWindow[1]))
	output = np.delete(output, range(output.size-recieverAnalysisWindow[0], output.size))
	return output
