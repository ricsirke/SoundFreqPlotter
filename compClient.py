from audio import Audio
import socket

END_SIGN = "END"
EQUAL = "="
SEP = ","

class compClient():
	def __init__(self):
		self.PORT_NUMBER = 5555
		self.au = Audio()
		self.conn = None
		
	def connect(self):
		self.comp_conn = socket.create_connection(('localhost', self.PORT_NUMBER))
		self.conf_conn = socket.create_connection(('localhost', self.PORT_NUMBER))
		
	def send_comp_data(self):
		Y_abs = self.au.recordHz()		
		send_data = Y_abs.tostring()
		self.comp_conn.send(send_data + END_SIGN)
		
	def recv_config(self):
		# TODO: make it nonblocking
		# TODO: better mapping of the settings -> this and apply_config	
		recv_data = self.conf_conn.recv(100)
		recv_data = recv_data.split(END_SIGN)[0]
		recv_data = recv_data.split(SEP)
		
		new_conf = {}
		
		for conf in recv_data:
			conf = conf.split(EQUAL)
			setting = conf[0]
			value = conf[1]
			
			new_conf[setting] = value
			
		return new_conf
		
	def apply_recv_config(self):
		config_dict = self.recv_config()
		
		self.au.set_threshold(config_dict['TH'])
		
	def run(self):
	
		recv_data = ""
		
		# auth compnode
		self.comp_conn.send("compnode" + END_SIGN)
		
		while recv_data != "ready":
			recv_data = self.comp_conn.recv(50)
			recv_data = recv_data.split(END_SIGN)[0]
			
		recv_data = ""
		
		# auth settingconn
		self.conf_conn.send("settnode" + END_SIGN)
		
		while recv_data != "ready":
			recv_data = self.comp_conn.recv(50)
			recv_data = recv_data.split(END_SIGN)[0]
		
		# computational loop
		while True:
			self.send_comp_data()
			self.
			