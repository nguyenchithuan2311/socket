import socket
import threading
from pattern1 import*
import json
import User 
import os
import shlex

# gate to connect/ auto
PORT = 5050
# auto get host from your computer
HOST = socket.gethostbyname(socket.gethostname())
# takes exactly one argument (2 given) .Therefor, we have a tuple/ This is an array
ADDR = (HOST, PORT)
#socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = str
flag = True
flag_search = True
host = str
port = int



class client:
    def __init__(self):
        #Client setup
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5050
        self.address = (self.host, self.port)
    
    def create_connection(self):
        while True:
            try:
                #Create connection
                self.host = input("Enter HOST: ")
                self.port = int(input("Enter PORT: "))
                self.address = (self.host, self.port)
                self.load_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.load_client.connect(self.address)
                break
            except:
                print("CAN NOT connect to the server!")
        # notice on terminal
        print(f"[CONNECT] in HOST: {self.host}")
        print(f"[CONNECT] in HOST: {self.port}")
    
    def create_auth_thread(self):
        
        #Start a thread that handle client
        handle_auth_thread = threading.Thread(target=self.__handle_auth, args=())
            
        handle_auth_thread.start()
        
        #Start a thread that handle server disconnect
        handle_server_dis_thread = threading.Thread(target=self.__handle_server_dis, args=())
        handle_server_dis_thread.start()

    def __handle_server_dis(self):
        #Always recieve request from server
        while True:
            LISTEN_MSG = self.load_client.recv(1024)
            try:
                
                LISTEN_MSG = recv_repr(LISTEN_MSG)
                if (LISTEN_MSG['respone'] != SEARCH_DONE['respone']):
                    if (flag_search == False):
                        SEARCHED_MSG = send_repr(SEARCHED_REQ)
                        self.load_client.send(SEARCHED_MSG)
                if(LISTEN_MSG['respone'] == DISCONNECT_ALL['respone']):
                    print(LISTEN_MSG['respone'])
                    return

            except:
                if (LISTEN_MSG != "DONE"):
                    if (flag_search == False):
                        SEARCHED_MSG = send_repr(SEARCHED_REQ)
                        self.load_client.send(SEARCHED_MSG)
                #continue

            if (flag == False):
                return
            
                

    def __handle_auth(self):
        #Login/Register
        global username 
        while True:
            choice = input("LOGIN or REGISTER (l/r):")
            if(choice == "l"):
                self.login()
                break
            if(choice == "r"):
                self.register()
                break
    

    
# LOGIN -----------------------------------------------------------------
    def login(self):
        global username
        while True:
            # send
            LOGIN_REQ = User.login()
            MSG = send_repr(LOGIN_REQ)
            
            try:
                self.load_client.send(MSG)
            except:
                os._exit(0)

            MSG = self.load_client.recv(1024)
            MSG = recv_repr(MSG)

            if(MSG['respone'] == LOGIN_RES['respone']):
                DATA = MSG
                username = DATA['username']
                print(f"WELCOME {username}!")
                self.create_task_thread()
                return

            print("Wrong!")
            self.__handle_auth()

# REGISTER -----------------------------------------------------------------
    def register(self):
        global username
        while True:
            # send
            REGISTER_REQ = User.register()
            msg = send_repr(REGISTER_REQ)

            try:
                self.load_client.send(msg)
            except:
                os._exit(0)

            msg = self.load_client.recv(1024)
            msg = recv_repr(msg)

            if(msg['respone'] == REGISTER_RES['respone']):
                username = msg['username']
                print(f"REGIST COMPLTETE {username}!")
                print("Please login to continue")
                self.login()
                return

            print("Your username is existed! Please choose another username")

    def create_task_thread(self):
        #Start a thread that handle task
        handle_task_thread = threading.Thread(
            target=self.__handle_task, args=())
        handle_task_thread.start()

    def __handle_task(self):
        global DATA
        global username
        global flag_search
        global flag
        while True:
            MSG = ""
            if(flag == True):
                MSG = input("Enter task (search/end): ")

            #Client disconnect
            if(MSG == "end"):
                DISCONNECT_REQ['username'] = username
                MSG = send_repr(DISCONNECT_REQ)
                self.load_client.send(MSG)
                os._exit(0)
            #Search
            if (MSG == "search"):
                clear = lambda: os.system('cls')
                clear()
                flag_search = False
                SEARCH_MSG = input("Enter keyword: ")
                SEARCH_MSG = shlex.split(SEARCH_MSG)
                SEARCH_REQ['country'] = SEARCH_MSG[0]
                SEARCH_REQ['cases'] = ""
                SEARCH_REQ['todayCases'] = ""
                SEARCH_REQ['deaths'] = ""  
                SEARCH_REQ['todayDeaths'] = "" 
                SEARCH_REQ['recovered'] = "" 
                SEARCH_REQ['active'] = "" 
                SEARCH_REQ['critical'] = "" 
                SEARCH_REQ['casesPerOneMillion'] = "" 
                SEARCH_REQ['deathsPerOneMillion'] = ""
                SEARCH_REQ['totalTests'] = ""
                SEARCH_REQ['testsPerOneMillion'] = ""
                SEARCH_MSG = send_repr(SEARCH_REQ)
                try:
                    self.load_client.send(SEARCH_MSG)
                except:
                    os._exit(0)
                
                while True:
                    SEARCH_MSG = self.load_client.recv(1024)
                    SEARCH_MSG = recv_repr(SEARCH_MSG)
                    if(SEARCH_MSG['respone'] == FALSE_SEARCH['respone']):
                        print("No Country")
                        SEARCH_MSG=send_repr(SEARCH_REQ)
                        self.load_client.send(SEARCH_MSG)
                        break
                    else:
                        print('country: ' + SEARCH_MSG['country'])
                        print('cases: ' + str(SEARCH_MSG['cases']))
                        print('todayCases: '+str(SEARCH_MSG['todayCases']))
                        print('deaths: '+str(SEARCH_MSG['deaths']))  
                        print('todayDeaths: '+str(SEARCH_MSG['todayDeaths']))
                        print('recovered: '+str(SEARCH_MSG['recovered']))
                        print('active: '+str(SEARCH_MSG['active'] )) 
                        print('critical: '+str(SEARCH_MSG['critical']))
                        print('casesPerOneMillion: '+str(SEARCH_MSG['casesPerOneMillion']) )
                        print('deathsPerOneMillion: '+str(SEARCH_MSG['deathsPerOneMillion'] ))
                        print('totalTests: '+str(SEARCH_MSG['totalTests'] ))
                        print('testsPerOneMillion: '+str(SEARCH_MSG['testsPerOneMillion'] ))
                        SEARCH_MSG=send_repr(SEARCH_REQ)
                        self.load_client.send(SEARCH_MSG)
                        break
                        
                #Choose
            while True:
                MSG = ""
                MSG = input("back to main(b): ")
                if (MSG == "b"):
                    break             
                    

#----------Main program----------#        
if(__name__=="__main__"):
    cl = client()
    cl.create_connection()
    cl.create_auth_thread()