import socket
import time
from concurrent.futures.thread import ThreadPoolExecutor

from header import Header
from package import Package
from GetApiData import GetAPI
from queue import Queue

# threads
from _thread import *
import threading


class ServerCOAP():
    def __init__(self, ip, port,graphicalInterface):
        self.OK = 200
        self.ERROR = 404
        self.locations = {}
        self.unit = {}
        self.addrAnswer={}
        self.RST={}
        self.coada = Queue()
        self.UDP_IP = ip
        self.UDP_PORT = int(port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.UDP_IP, self.UDP_PORT))
        self.version = 0
        self.lock = threading.Lock()
        self.ShutdownServer = 0
        self.DelayFlag = 0
        self.ResetFlag = 0
        self.GUI=graphicalInterface
        graphicalInterface.print(self.UDP_IP,"Server init, waiting for start command")

    def SetDelayFlag(self, df):
        self.DelayFlag = df

    def SetResetFlag(self, rf):
        self.ResetFlag = rf

    def SetVersion(self, vrs):
        self.version = int(vrs)

    # setare Flag shutdown
    def ShutDownServer(self):
        self.ShutdownServer = 1
        self.s.sendto("shutdown".encode(), (self.UDP_IP, self.UDP_PORT))

    # verificare daca avem loc in coada serverului. Daca da, cererea se pune in coada. Daca nu,se raspunde cu un
    # pachet de tip RST
    def StartServer(self):
        self.ShutdownServer = 0
        start_new_thread(self.QueueExtractAndSolve, ())
        start_new_thread(self.ServerLoop, ())

    def ServerLoop(self):
        while self.ShutdownServer != 1:
            data, addr = self.s.recvfrom(1024)
            self.GUI.print(addr,data)
            if self.coada.qsize() > 10:
                header = Header()
                package = Package()
                package.pack = data
                (h, m) = package.getPackageInfo()
                header.setHeaderAttributesFromString(h)
                h.BuilderSetByte1(h.getVersion(), 3, h.getTokenLength())
                h.BuilderBuild()
                package.buildPackage(h.header, str(""))
                self.s.sendto(package.pack, addr)
                self.GUI.print(addr,"Pachet respins deoarece coada serverului este plina")
            else:
                self.GUI.print(addr,"am pus in coada")
                self.coada.put((addr, data))
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
    def QueueExtractAndSolve(self):
        package = Package()
        answer=""
        token=""
        while self.ShutdownServer!=1:
            if self.coada.qsize() > 0:
                (addr, data) = self.coada.get()
                package.pack = data
                (h, m) = package.getPackageInfo()
                header = Header()
                header.setHeaderAttributesFromString(h)
                answer = header.getMessageType()
                token = header.getToken()
                self.addrAnswer[(addr, token)] = answer
                start_new_thread(self.process, (addr, data))

    def process(self, addr, data):
        package = Package()
        header = Header()
        API = GetAPI()
        request = 0
        message = ""
        package.pack = data
        (h, m) = package.getPackageInfo()
        header.setHeaderAttributesFromString(h)
        if header.getVersion() is not self.version:
            self.GUI.print(addr, "Client has wrong version")
        else:
            # initializez datele unui nou client
            if self.locations.get(addr) is None:
                self.locations[addr] = "Iasi"
                self.unit[addr] = "metric"
            # calculez pachetul
            if header.getResponseClass() == 0:
                if header.getResponseCode() == 0:
                    request = self.OK
                    message = ""
                elif header.getResponseCode() == 1:
                    if (m.lower() in ["coords", "humidity", "pressure", "temperature", "visibility", "wind", "zone",
                                      "all"]):
                        data1, response_code_data = API.getWeatherData(self.locations[addr], self.unit[addr])
                        if response_code_data == "200":
                            data = data1
                            if m.lower() == "coords":
                                request = self.OK
                                message = data["coord"]
                            elif m.lower() == "humidity":
                                request = self.OK
                                message = data["main"]["humidity"]
                            elif m.lower() == "pressure":
                                request = self.OK
                                message = data["main"]["pressure"]
                            elif m.lower() == "temperature":
                                request = self.OK
                                message = data["main"]["temp"]
                            elif m.lower() == "visibility":
                                request = self.OK
                                message = data["visibility"]
                            elif m.lower() == "wind":
                                request = self.OK
                                message = data["wind"]
                            elif m.lower() == "zone":
                                request = self.OK
                                message = data["sys"]
                            elif m.lower() == "all":
                                request = self.OK
                                message = data

                        else:
                            request = self.ERROR
                            message = "Server Data could not be accessed or the Location is invalid"
                            self.GUI.print(addr,"Error at getting API data")
                    else:
                        request = self.ERROR
                        message = "Wrong access to resource"
                        self.GUI.print(addr,"Received a wrong GET request")

                elif header.getResponseCode() == 2:
                    if m[:9].lower() == "location:":
                        m = m[9:].lower()
                        self.GUI.print(addr,"The new location is = " + m)
                        self.locations[addr] = m
                        request = self.OK
                        message = ""
                    else:
                        request = self.ERROR
                        self.GUI.print(addr, "Received a wrong POST request")
                        message = "Wrong Location Request"

                elif header.getResponseCode() == 3:
                    if self.unit[addr] == "metric":
                        self.unit[addr] = "imperial"
                        self.GUI.print(addr, "Unit switched to imperial")
                    else:
                        self.unit[addr] = "metric"
                        self.GUI.print(addr,"Unit switched to metric")
                    request = self.OK
                    message = ''
            else:
                request = self.ERROR
                message = data
            header.setRequest(request // 100, request % 100)
            token=header.getToken()
            print(header.getMessageType())
            if header.getMessageType() == 0 and (addr,token) not in self.RST:
                # daca mesajul e confirmable, trimit raspuns ca ACK+mesaj, daca nu pot raspunde acum, trimit ACK,
                # apoi confirmalbe+mesaj pe acelasi token, dar MSG ID schimbat
                if self.DelayFlag == 1:
                    # daca am setat din interfata delay trimit ack gol si astept 1sec
                    header.setMessageID(header.getMessageId() + 1)
                    header.setType(2)
                    package.buildPackage(header.header, str(""))
                    self.GUI.print(addr, "nu pot raspunde, trimit ACK gol")
                    self.s.sendto(package.pack, addr)
                    time.sleep(1)
                    # trimit pack confirmable cu datele cerute initial
                    header.setType(0)
                    header.setMessageID(header.getMessageId() + 2)
                    package.buildPackage(header.header, str(message))
                    self.GUI.print(addr, "am procesat, trimit pachetul confirmable")
                    self.s.sendto(package.pack, addr)

                    #daca nu primesc ack pe parcursul urmatoarei secunde, retransmit, altfel ma dau batut
                    for x in range(3):
                        if (addr,token) in self.RST:
                            del self.RST[(addr,token)]
                            break
                        time.sleep(1)
                        if ((addr,token) in self.addrAnswer.keys()) and self.addrAnswer[(addr,token)] != 2:
                            self.GUI.print(addr, "n-am primit ACK retransmit")
                            self.s.sendto(package.pack, addr)
                        elif ((addr,token) in self.addrAnswer.keys()) and self.addrAnswer[(addr,token)] == 2:
                            self.GUI.print(addr, "am primit ACK")
                            del self.addrAnswer[(addr,token)]
                            break
                else:
                    # trimit ack piggyback
                    header.setMessageID(header.getMessageId() + 1)
                    header.setType(2)
                    package.buildPackage(header.header, str(message))
                    self.s.sendto(package.pack, addr)
                    if (addr, token) in self.addrAnswer.keys():
                        del self.addrAnswer[(addr,token)]

            elif header.getMessageType() == 1 and (addr,token) not in self.RST:
                # daca req e non-confirmable, trimit raspunsul tot ca un mesaj non-confirmable
                header.setMessageID(header.getMessageId() + 1)
                package.buildPackage(header.header, str(message))
                self.s.sendto(package.pack, addr)
                if (addr, token) in self.addrAnswer.keys():
                    del self.addrAnswer[(addr,token)]

            elif header.getMessageType() == 2:
                if (addr, token) in self.addrAnswer.keys():
                    del self.addrAnswer[(addr, token)]
            elif header.getMessageType() == 3:
                self.RST[(addr,token)]=1
            else:
                self.GUI.print(addr,"Wrong message type value " + str(header.getMessageType()))
