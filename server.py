import socket, select, sys
from thread import *

from audio import Audio

# TODO: freq computing should be client too - have to mark it - first everybody say something about itself
# TODO: config params (eg. threshold) should be sent to this computing client

# TODO: on closing connection the audio stream should be destroyed 

class Server():
	def __init__(self, stop_event):
		self.stop_event = stop_event
		self.init_socket()
		
	def init_socket(self):
		host = '' # accept any address
		port = 5555 # server port
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		try:
			self.sock.bind((host, port))
		except socket.error as e:
			print str(e)

		self.sock.listen(5) # number of max listeners
		
	def run(self):
		while not self.stop_event.is_set():
			
			conn, addr = self.sock.accept() # wait untill someone connects - blocking
			
			print "connected to: " + addr[0] + ":" + str(addr[1])
			
			start_new_thread(self.on_client, (conn,))
			
		print "server stopped"
		self.sock.close()


	def on_client(self, conn):
		#conn.setblocking(0)
		au = Audio()
		while True:
			Y_abs = au.recordHz()
			
			send_data = Y_abs.tostring()
			conn.send(send_data + "END")
			
		conn.close()
