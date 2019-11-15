import socket
from header import Header
from package import Package
from GetApiData import  GetAPI

API=GetAPI()
OK = 200
ERROR_FILE_NOT_FOUND = 404
ERROR = 500
locations = {}
unit = {}
def process(addr,requestClass,requestCode,m):
    data = 0
    if(requestClass == 0):
        if(requestCode == 0):
            return (OK,"")
        elif(requestCode == 1):
            if(m in ["Coords","Humidity","Pressure","Temperature","Visibility","Wind","Zone","All"]):
                data = API.getWeatherData(locations[addr], unit[addr])
            else:
                return (ERROR,"")
            if(m == "Coords"):
                return (OK,data["coord"])
            elif(m == "Humidity"):
                return (OK,data["main"]["humidity"])
            elif (m == "Pressure"):
                return (OK,data["main"]["pressure"])
            elif (m == "Temperature"):
                return (OK,data["main"]["temp"])
            elif (m == "Visibility"):
                return (OK,data["visibility"])
            elif (m == "Wind"):
                return (OK,data["wind"])
            elif (m == "Zone"):
                return (OK,data["sys"])
            elif (m == "All"):
                return (OK,data)
        elif (requestCode == 2):
            locations[addr] = m
            return (OK,'')
        elif (requestCode == 3):
            if(unit[addr] == "metric"):
                unit[addr] = "imperial"
            else:
                unit[addr] = "metric"
            return (OK,'')
    else:
        return (ERROR,data)

UDP_IP = "127.0.0.1"
UDP_PORT = 80
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # address from internet,for udp
s.bind((UDP_IP, UDP_PORT))

print("Wait connections")

package = Package()
header = Header()
while 1:
    data,addr = s.recvfrom(1024)
    if (locations.get(addr) == None):
        locations[addr] = "Iasi"
        unit[addr] = "metric"
    package.pack = data
    (h,m) = package.getPackageInfo()
    header.setHeaderAttributesFromString(h)
    request,a = process(addr, header.getResponseClass(), header.getResponseCode(), m)
    header.setRequest(request//100,request%100)
    package.buildPackage(header.header,str(a))
    s.sendto(package.pack,addr)
conn.close()


