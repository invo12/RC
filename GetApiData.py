from socket import *
import datetime
import json


class GetAPI():
    def __init__(self):
        #print("Init")
        pass

    def getWeatherData(self,locatie,um):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(("api.openweathermap.org", 80))
        request = "GET /data/2.5/weather?q="+locatie+"&APPID=8a999283783fff58a906c31b2e47a26d&units="+um+" HTTP/1.1\r\nHost: api.openweathermap.org\r\n\r\n"
        s.send(request.encode())
        response = s.recv(4096)
        response = response.decode()
        y = response.rfind('\n')
        jsonData=json.loads(response[y + 1:])
        #print(response[y+1:])
        return jsonData


