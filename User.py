import datetime
import json
from pattern1 import *



# client ------------------------------------------
def login():
    LOGIN_REQ['username'] = input("Enter USERNAME: ")
    LOGIN_REQ['password'] = input("Enter PASSWORD: ")
    #cryptography = input(
       # "Do you want to encrypt message before sending? (y/n): ")
    
       # if (cryptography == 'y'):
            #LOGIN_REQ['cryptography'] = True
            #c_pwd = encrypt_str(pwd)
            #LOGIN_REQ['password'] = c_pwd
            #break
       # if (cryptography == 'n'):
            #LOGIN_REQ['cryptography'] = False
      
    return LOGIN_REQ

def register():
    REGISTER_REQ['username'] = input("Enter USERNAME: ")
    while True:
        password = input("Enter PASSWORD: ")
        password_again = input("Enter PASSWORD again: ")
        if(password == password_again):
            pwd = password
            REGISTER_REQ['password'] = pwd
            return REGISTER_REQ
        print("Password not match!")
        
