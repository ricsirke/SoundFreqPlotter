import threading, socket
import subprocess as sp


#############
## CONTROL ##
#############


PORT_NUMBER = 5555


class Control():
	def __init__(self):
		self.server = None
		self.server_stop = threading.Event()
		
		self.ui = None
		self.ui_stop = threading.Event()
		
		self.run()

		
	def run_server(self):
		from server	import Server
		srv = Server(self.server_stop)
		serv_thread = threading.Thread(target=srv.run, args=())
		serv_thread.start()
		#serv_thread.join() # the main thread waits while the child thread finishes - not for here...
		print "server started"
		
	def run_ui(self):
		command = "bokeh serve ui.py"
		sp.Popen(command, shell=True)
		print "ui started"
		
	def interpret_cmd(self):
		if cmd == "server stop":
				print "stopping server"
				# dummy connection to go through accept's block
				self.conn = socket.create_connection(('localhost', PORT_NUMBER))
				self.server_stop.set()
				print "server stopped"
			
			elif cmd == "ui stop":
				print "stopping ui"
				self.ui_stop.set()
				print "ui stopped"
				
			elif cmd == "server start":
				self.run_server()
				
			elif cmd == "ui start":
				self.run_ui()

	def run(self):
		cmd = ""
		
		while cmd != "quit":
			cmd = raw_input(">> ")
			self.interpret_cmd(cmd)
			
			
				
ctrl = Control()
