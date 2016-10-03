import socket, time

from numpy import fromstring, linspace
from numpy import sin as npsin
from numpy import fft

from bokeh.plotting import Figure, show
from bokeh.models import ColumnDataSource, HBox, VBoxForm,Button
from bokeh.models.widgets import Slider, TextInput
from bokeh.io import curdoc, vplot
from bokeh.models.renderers import GlyphRenderer



class Ui():
	def __init__(self):		
		self.init_params()
		self.init_plot()
		self.init_controls()
		
	def init_params(self):
		# TODO: same CHUNK_SIZE as in serve.py, should unify the two
		# when connect the first datapieces may be these kind of params
		self.CHUNK_SIZE = 1024
		self.SAMPLE_RATE = 22100
		self.PORT_NUMBER = 5555
		
		self.conn = None
		
	def init_plot(self):
		x = fft.rfftfreq(self.CHUNK_SIZE)*self.SAMPLE_RATE
		x_max = x[-1]
		self.init_y = linspace(0, x_max, len(x))
		y = self.init_y
		source = ColumnDataSource(data=dict(x=x, y=y))
		
		# TODO: range and size (toolbar), maybe could be user settings
		plot = Figure(plot_height=400, plot_width=800, title="freq anal",
					  tools="crosshair,pan,reset,resize,save,wheel_zoom",
					  x_range=[0, x_max], y_range=[0, 15])
					  
		rad = x_max/float(len(x))
		data = plot.circle('x', 'y', source=source, line_color=None, radius=rad)
		self.data_source = data.data_source
		
		# TODO: maybe not the best place
		curdoc().add_root(plot)

	def init_controls(self):
		btnStop = Button(label="Stop", type="danger")
		btnStart = Button(label="Start", type="success")	
		
		btnStop.on_click(self.handle_btnStop_press)
		btnStart.on_click(self.handle_btnStart_press)
				
		curdoc().add_root(btnStop)
		curdoc().add_root(btnStart)
		

		sliderHPThreshold = Slider(start=0, end=500, value=100, step=1, title="High pass threshold")
			
		sliderHPThreshold.on_change('value', self.onChangeHPThreshold)
		curdoc().add_root(vplot(sliderHPThreshold))

		
	# TODO: implement stop listening and close connection
	def handle_btnStop_press(self):
		pass
		
	def handle_btnStart_press(self):
		if not self.conn:
			self.conn_to_serv()
			
		self.listen_to_serv()
		
	def onChangeHPThreshold(self, attr, old, new):
		self.conn.send(new)
	
	def conn_to_serv(self):
		self.conn = socket.create_connection(('localhost', self.PORT_NUMBER))
		
	def listen_to_serv(self):
		prev_chunk = ""
		started = False

		while True:
			data = self.conn.recv(4096)
			data = data.split("END")
			if not started:		
				if len(data) == 2:
					prev_chunk = data[1]
					started = True
			else:
				if len(data) == 2:
					# TODO: ValueError: string size must be a multiple of element size
					# have to sync better, start sign? one char sings?
					try:
						npdata = fromstring(prev_chunk + data[0])
					except ValueError:
						npdata = self.init_y
						started = False
		
					prev_chunk = data[1]
					self.data_source.data["y"] = npdata
					self.data_source._dirty = True
					time.sleep(0.01)
				elif len(data) == 1:
					prev_chunk += data[0]
				else:
					print "unexpected happened"

	
ui = Ui()
