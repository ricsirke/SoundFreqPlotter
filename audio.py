from numpy import fromstring
from numpy import int16
from numpy import fft
from numpy import absolute
from numpy import array as nparray
from numpy import log as nplog

from pyaudio import paInt16
from pyaudio import PyAudio


class Audio():
	def __init__(self):
		self.THRESHOLD = 200
		self.CHUNK_SIZE = 1024
		self.RATE = 22100

		p = PyAudio()
		self.stream = p.open(format=paInt16, channels=1, rate=self.RATE, input=True, output=True, frames_per_buffer=self.CHUNK_SIZE)
		
	def set_threshold(self, new_th):
		self.THRESHOLD = new_th
		
	def silence(self, npdata):
		if max(npdata) < self.THRESHOLD:
			npdata = nparray([0 for i in range(self.CHUNK_SIZE)], int16)
		return npdata
		
	def recordHz(self):
		chunk = self.stream.read(self.CHUNK_SIZE)
		npdata = fromstring(chunk, dtype=int16)
		#sample_width = p.get_sample_size(FORMAT)
		
		npdata = self.silence(npdata)
		Y = fft.rfft(npdata, self.CHUNK_SIZE)
		
		Y_abs = nplog(absolute(Y) + 1)
		return Y_abs