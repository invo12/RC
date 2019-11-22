import socket
from header import Header
from package import Package
from GetApiData import  GetAPI
from queue import Queue

#threads
from _thread import *
import threading

API=GetAPI()
OK = 200
ERROR = 404
locations = {}
unit = {}
coada=Queue()
lock = threading.Lock()

def process(addr,data):
    request = 0
    message = ""
    if (locations.get(addr) == None):
        locations[addr] = "Iasi"
        unit[addr] = "metric"
    package.pack = data
    (h, m) = package.getPackageInfo()
    header.setHeaderAttributesFromString(h)
    if (header.getResponseClass() == 0):
        if (header.getResponseCode() == 0):
            request = OK
            message = ""
        elif (header.getResponseCode() == 1):
            if (m.lower() in ["coords", "humidity", "pressure", "temperature", "visibility", "wind", "zone", "all"]):
                data1,response_code_data = API.getWeatherData(locations[addr], unit[addr])
                if(response_code_data == "200"):
                    data=data1
                    if (m.lower() == "coords"):
                        request = OK
                        message = data["coord"]
                    elif (m.lower() == "humidity"):
                        request = OK
                        message = data["main"]["humidity"]
                    elif (m.lower() == "pressure"):
                        request = OK
                        message = data["main"]["pressure"]
                    elif (m.lower() == "temperature"):
                        request = OK
                        message = data["main"]["temp"]
                    elif (m.lower() == "visibility"):
                        request = OK
                        message = data["visibility"]
                    elif (m.lower() == "wind"):
                        request = OK
                        message = data["wind"]
                    elif (m.lower() == "zone"):
                        request = OK
                        message = data["sys"]
                    elif (m.lower() == "all"):
                        request = OK
                        message = data
                else:
                    request = ERROR
                    message = "Server Data could not be accessed or the Location is invalid"
                    print("Error at getting API data")
            else:
                request = ERROR
                message = "Wrong access to resource"
                print("Received a wrong GET request")

        elif (header.getResponseCode() == 2):
            if(m[:9].lower()=="location:"):
                m=m[9:].lower()
                print("The new location is = "+ m + " for address "+ str(addr))
                locations[addr] = m
                request = OK
                message = ""
            else:
                request = ERROR
                print("Received a wrong POST request from address "+ str(addr))
                message = "Wrong Location Request"

        elif (header.getResponseCode() == 3):
            if (unit[addr] == "metric"):
                unit[addr] = "imperial"
                print("Unit switched to imperial for address "+ str(addr))
            else:
                unit[addr] = "metric"
                print("Unit switched to metric for address "+ str(addr))
            request = OK
            message = ''
    else:
        request = ERROR
        message = data
    lock.acquire()
    header.setRequest(request // 100, request % 100)
    package.buildPackage(header.header, str(message))
    s.sendto(package.pack, addr)
    lock.release()



UDP_IP = "127.0.0.1"
UDP_PORT = 80
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # address from internet,for udp
s.bind((UDP_IP, UDP_PORT))
print("Waiting for connections")

package = Package()
header = Header()
while 1:
    data,addr = s.recvfrom(512)
    coada.put((addr,data))
    start_new_thread(process,(addr,data,))
s.close()

