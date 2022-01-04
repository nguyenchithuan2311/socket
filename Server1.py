import socket
import threading
import json
import os
import time
import requests

from pattern1 import *

usernameList=[""]
passwordList=[""]

class server:
    def __init__(self):
        #Server setup
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5050
        self.address = (self.host, self.port)
        self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketServer.bind(self.address)
        self.online = bool
        self.clients = set()
      

        #Notify on terminal
        print(f"Server is at HOST: {self.address[0]}")
        print(f"Server is at PORT: {self.address[1]}")
    
    def updata_data_every_1hous(self):
        start_time=time.time()#lấy thời thời gian
        while True:
            end_time=time.time()
            if (round(end_time-start_time) % 2== 0):
                response={}
                response=requests.get('https://coronavirus-19-api.herokuapp.com/countries')
                with open('covid1.json', 'w') as f:
                    json.dump(response.json(), f) 

    def connect(self):
        self.socketServer.listen()

        #Start a thread that handle server itself
        self.online = False
        client = self.socketServer
        address = self.address
       
        handleClientThread = threading.Thread(target=self.handleClient, args=(client, address,))
        handleClientThread.start()
    
        #Starting thread to accept connect from client
        while True :
            client, address = self.socketServer.accept()
            self.clients.add(client)
            handleClientThread = threading.Thread(target=self.handleClient, args=(client, address,))
            handleClientThread.start()
            handupdate=threading.Thread(target=self.updata_data_every_1hous, args=())
            handupdate.start()
            
    def handleClient(self, client, address):
            
        if client == self.socketServer and address == self.address :
            cmd = str(input(""))
            if cmd == "!DISCONNECT" :
                self.send_all()
                os._exit(0)

        #Handle client
        else:
            print(f"Address {address} connected!")
            while True:
                #Recieve request excepting disconnection
                try:
                    msg = client.recv(1024)
                except:
                    print(f"[{address}] {DISCONNECT_RES['respone']}")
                    self.clients.remove(client)
                    client.close()
                    break
                msg = recv_repr(msg)
                print(f"Address {address} " + msg['request'])

                #Login 
                if(msg['request'] == LOGIN_REQ['request']):
                    print(LOGIN_REQ['request'])
                    result = self.checkLogin(msg['username'])
                    if (result != False):
                        #Login success
                        LOGIN_RES['username'] = msg['username']
                        LOGIN_RES['password'] = msg['password']

                        LOGIN_MSG = send_repr(LOGIN_RES)
                        client.send(LOGIN_MSG)
                        client.send(LOGIN_MSG)

                    else:
                        #Login fail
                        LOGIN_MSG = send_repr(FALSE_RES)
                        client.send(LOGIN_MSG)
                        client.send(LOGIN_MSG)
                        

                #Register
                if(msg['request'] == REGISTER_REQ['request']):
                    result = self.checkExistedUser(msg['username'])
                    if(result == False):
                        #Register success
                        self.register(msg['username'], msg['password'])
                        REGISTER_RES['username'] = msg['username']
                        REGISTER_RES['password'] = msg['password']
                        print("okeeee")
                        REGISTER_MSG = send_repr(REGISTER_RES)
                        client.send(REGISTER_MSG)
                        client.send(REGISTER_MSG)
                        
                    else:
                        #Register fail
                        REGISTER_MSG = send_repr(FALSE_RES)
                        client.send(REGISTER_MSG)
                        client.send(REGISTER_MSG)

                #Search 
                response={}
                response=requests.get('https://coronavirus-19-api.herokuapp.com/countries')
                with open('covid1.json', 'w') as f:
                    json.dump(response.json(), f)
                if (msg['request'] == SEARCH_REQ['request']):
                    check=self.checkSearch(msg['country'])
                    if(check==True):
                        with open('covid1.json') as wr:
                            customer=json.load(wr)
                        for p in range(223):
                            if(msg['country']==customer[p]['country']):
                                SEARCH_RES['country'] = customer[p]['country']
                                SEARCH_RES['cases'] = customer[p]['cases']
                                SEARCH_RES['todayCases'] =customer[p]['todayCases']
                                SEARCH_RES['deaths'] = customer[p]['deaths']
                                SEARCH_RES['todayDeaths'] = customer[p]['todayDeaths']
                                SEARCH_RES['recovered'] = customer[p]['recovered']
                                SEARCH_RES['active'] = customer[p]['active']
                                SEARCH_RES['critical'] = customer[p]['critical']
                                SEARCH_RES['casesPerOneMillion'] = customer[p]['casesPerOneMillion']
                                SEARCH_RES['deathsPerOneMillion'] = customer[p]['deathsPerOneMillion']
                                SEARCH_RES['totalTests'] = customer[p]['totalTests']
                                SEARCH_RES['testsPerOneMillion'] = customer[p]['testsPerOneMillion']
                        #Handle multi searching
                        MSG_res = send_repr(SEARCH_RES)
                        client.send(MSG_res)
                        SEARCHED_MSG = client.recv(1024)
                        SEARCHED_MSG = recv_repr(SEARCHED_MSG)
                    else:
                        MSG_res = send_repr(FALSE_SEARCH)
                        client.send(MSG_res)
                        SEARCHED_MSG = client.recv(1024)
                        SEARCHED_MSG = recv_repr(SEARCHED_MSG)

                        
                    if (SEARCHED_MSG['request'] == SEARCHED_REQ['request']):
                        client.send(MSG_res)
                    SEARCHED_MSG = client.recv(1024)
                    SEARCHED_MSG = recv_repr(SEARCHED_MSG)

                    #Report that searching is end
                    DONE_MSG = send_repr(SEARCH_DONE)
                    client.send(DONE_MSG)
                    client.send(DONE_MSG)


                #Disconnect_Client
                if(msg['request'] == DISCONNECT_REQ['request']):
                    DISCONNECT_RES['username'] = msg['username']

                    #Report disconnection
                    print(f"[{address[1]}] [{msg['username']}] {DISCONNECT_REQ['request']}")

                    #Remove client 
                    self.clients.remove(client)
                    client.close()
                    break
                   
    def send_all(self):
        #Send message to all clients
        MSG = send_repr(DISCONNECT_ALL)
        for c in self.clients:
            c.send(MSG)

    def checkLogin(self, username):
        #Check if a login request is legal
        for row in usernameList:
            if row== username:
                return True
                  
        return False
    
    def checkSearch(seft,search):
        with open('covid1.json') as wr:
            customer=json.load(wr)
        for p in range(223):
            if(search==customer[p]['country']):
                return True
        return False

    def checkExistedUser(self, username):
        #Check if a username is existed
        for row in usernameList:
            if row==username:
                return True
        return False

    def register(self, username,password):
        #Insert new account to database
        usernameList.append(username)
        passwordList.append(password)



#----------Main program----------#
sv = server()
sv.connect()