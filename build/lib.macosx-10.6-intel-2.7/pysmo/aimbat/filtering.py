import numpy as np
from scipy import signal
import math

"""when the user is picking"""
def filtering_time_freq(originalTime, originalSignalTime, delta, filterType, highFreq, lowFreq, order):
	originalFreq, originalSignalFreq = time_to_freq(originalTime, originalSignalTime, delta)

	# make filter, default is bandpass
	MULTIPLE = 0.7*max(np.abs(originalSignalFreq))
	NYQ, Wn, B, A, adjusted_w, adjusted_h = get_filter_params(delta, lowFreq, highFreq, filterType, order, MULTIPLE)

	# apply filter
	filteredSignalTime = signal.lfilter(B, A, originalSignalTime)

	# convert filtered time signal -> frequency signal
	filteredSignalFreq = np.fft.fft(filteredSignalTime)

	return filteredSignalTime, filteredSignalFreq, adjusted_w, adjusted_h

def get_filter_params(delta, lowFreq, highFreq, filterType, order, MULTIPLE=3000):
	NYQ = 1.0/(2*delta)
	Wn = [lowFreq/NYQ, highFreq/NYQ]
	B, A = signal.butter(order, Wn, analog=False, btype='bandpass')
	if filterType=='lowpass':
		Wn = lowFreq/NYQ
		B, A = signal.butter(order, Wn, analog=False, btype='lowpass')
	elif filterType=='highpass':
		Wn = highFreq/NYQ
		B, A = signal.butter(order, Wn, analog=False, btype='highpass')

	w, h = signal.freqz(B, A)
	adjusted_w = w*(NYQ/np.pi)
	adjusted_h = MULTIPLE*np.abs(h)

	return NYQ, Wn, B, A, adjusted_w, adjusted_h

def filtering_time_signal(originalSignalTime, delta, lowFreq, highFreq, filterType, order, MULTIPLE):
	NYQ, Wn, B, A, w, h = get_filter_params(delta, lowFreq, highFreq, filterType, order, MULTIPLE)
	filteredSignalTime = signal.lfilter(B, A, originalSignalTime)
	return filteredSignalTime

def time_to_freq(originalTime, originalSignalTime, delta):
	originalFreq = np.fft.fftfreq(len(originalTime), delta) 
	originalSignalFreq = np.fft.fft(originalSignalTime) 
	return originalFreq, originalSignalFreq























