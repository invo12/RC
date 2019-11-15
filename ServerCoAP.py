import socket
from header import Header
from package import Package
from GetApiData import  GetAPI

#threads
from _thread import *
import threading

API=GetAPI()
OK = 200
ERROR_FILE_NOT_FOUND = 404
ERROR = 500
locations = {}
unit = {}
#py ServerCoAP.py
lock = threading.Lock()
def process(addr,data):
    print("yes")
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
            if (m in ["Coords", "Humidity", "Pressure", "Temperature", "Visibility", "Wind", "Zone", "All"]):
                data = API.getWeatherData(locations[addr], unit[addr])
            else:
                request = ERROR
                message = ""
            if (m == "Coords"):
                request = OK
                message = data["coord"]
            elif (m == "Humidity"):
                request = OK
                message = data["main"]["humidity"]
            elif (m == "Pressure"):
                request = OK
                message = data["main"]["pressure"]
            elif (m == "Temperature"):
                request = OK
                message = data["main"]["temp"]
            elif (m == "Visibility"):
                request = OK
                message = data["visibility"]
            elif (m == "Wind"):
                request = OK
                message = data["wind"]
            elif (m == "Zone"):
                request = OK
                message = data["sys"]
            elif (m == "All"):
                request = OK
                message = data
        elif (header.getResponseCode() == 2):
            locations[addr] = m
            request = OK
            message = ""
        elif (header.getResponseCode() == 3):
            if (unit[addr] == "metric"):
                unit[addr] = "imperial"
            else:
                unit[addr] = "metric"
            request = OK
            message = ''
    else:
        request = ERROR
        message = data
    header.setRequest(request // 100, request % 100)
    package.buildPackage(header.header, str(message))
    s.sendto(package.pack, addr)
    lock.release()


UDP_IP = "127.0.0.1"
UDP_PORT = 80
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # address from internet,for udp
s.bind((UDP_IP, UDP_PORT))
print("Wait connections")

package = Package()
header = Header()
while 1:
    data,addr = s.recvfrom(1024)
    lock.acquire()
    start_new_thread(process,(addr,data,))
s.close()

