import json
import datetime

#Encode/Decode function
def send_repr(MSG):
    MSG = json.dumps(MSG).encode('utf-8')
    #chuyen MSG từ json sang string sau đó chuyển từ string sang byte để gửi
    return MSG
def recv_repr(MSG):
    MSG = json.loads(MSG.decode('utf-8'))
    #chuyen đã nhận MSG từ byte sang string sau đó chuyển từ string sang json 
    return MSG

#def recv_file(so)

#False pattern
FALSE_RES = {"respone": "!FALSE"}
FALSE_SEARCH={"respone":"!Wrong"}

#Login pattern
LOGIN_REQ = {"username": str, 
             "password": str, 
             "request": "!LOGIN"}
LOGIN_RES = {"username": str,
             "password": str,
             "respone": "!COMPLETE"}

#Register pattern
REGISTER_REQ = {"username": str,  
                "password": str,
                "request": "!REGISTER"}
REGISTER_RES = {"username": str, 
                "password": str,
                "respone": "!COMLETE"}

#Search book pattern 
SEARCH_REQ = {"country": str,
              "cases": str,
              "todayCases": str,
              "deaths": str,
              "todayDeaths": str,
              "recovered": str,
              "active": str,
              "critical": str,
              "casesPerOneMillion": str,
              "deathsPerOneMillion": str,
              "totalTests": str,
              "testsPerOneMillion": str,
              "request": "!SEARCH"}
SEARCH_RES = {"country": str,
              "cases": str,
              "todayCases": str,
              "deaths": str,
              "todayDeaths": str,
              "recovered": str,
              "active": str,
              "critical": str,
              "casesPerOneMillion": str,
              "deathsPerOneMillion": str,
              "totalTests": str,
              "testsPerOneMillion": str,
              "respone": "!DONE"}

#Comple searching pattern
SEARCHED_REQ = {"request": "!COMPLETE"}
SEARCH_DONE = {"respon": "!DONE"}

#Disconnect pattern
DISCONNECT_REQ = {"username": str, 
                  "request": "!DISCONNECT"}
DISCONNECT_RES = {"username": str, 
                  "respone": "!DISCONNECT"}
DISCONNECT_ALL = {"respone": "!SERVER DISCONNECT"}
