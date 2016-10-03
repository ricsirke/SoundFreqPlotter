from pyaudio import paInt16
from pyaudio import PyAudio

from msvcrt import getch
from msvcrt import kbhit

from numpy import fromstring, int16, fft, absolute
from numpy import array as nparray
from numpy import log as nplog




# CONTROL
record = True

def quit():
	if kbhit() and ord(getch()) == 113:
		stream.stop_stream()
		stream.close()
		p.terminate()
		return False
	else:
		return True
		

# UTIL
def silence(npdata):
	if max(npdata) < THRESHOLD:
		npdata = nparray([0 for i in range(CHUNK_SIZE)], int16)
	return npdata
		

# CONFIG
THRESHOLD = 300
CHUNK_SIZE = 1024
FORMAT = paInt16
RATE = 22100



# INIT
p = PyAudio()
stream = p.open(format=FORMAT, channels=1, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE)

plot_range = CHUNK_SIZE/2 + 1
		
		
# RECORD
print 'recording started'

while record:
	chunk = stream.read(CHUNK_SIZE)
	npdata = fromstring(chunk, dtype=int16)
	sample_width = p.get_sample_size(FORMAT)
	#print npdata, sample_width
	
	# silence check
	npdata = silence(npdata)
	
	Y = fft.rfft(npdata, CHUNK_SIZE)
	#print X, len(X)
	
	Y_abs = nplog(absolute(Y) + 1)
	
	#print Y_abs, len(Y_abs)
	#print max(Y_abs)
	
	
	record = quit()
	