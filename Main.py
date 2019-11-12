from GUI import MainApp
from GetApiData import  GetAPI
from socket import *
from header import Header
from package import Package

if __name__=="__main__":
    API=GetAPI()
    a=MainApp(API)
    API.getWeatherData("Iasi","metric")


    # header=Header()
    # header.BuilderSetByte1(1,2,4)
    # header.BuilderSetByteResp(0,1)
    # header.BuilderSetMessageId(31)
    # header.BuilderSetToken(63)
    # header.BuilderBuild()
    # header.BuilderPrint()
    #
    # header.Print()
    #
    # package = Package()
    # package.buildPackage(header.header,"da")
    # package.getPackage()
    #
    # server = Server()
    # client = Client()
    # client.sendPackage(package)
    # server.listenClients()
    #
    # print("here")

    #a=MainApp(API)
    API.getWeatherData("Iasi","metric")


    header=Header()
    header.BuilderSetByte1(1,2,4)
    header.BuilderSetByteResp(0,1)
    header.BuilderSetMessageId(31)
    header.BuilderSetToken(63)
    header.BuilderBuild()
    header.BuilderPrint()

    header.Print()

    package = Package()
    package.buildPackage(header.header,"da")

    print("\n\n\n Package")
    a,b = package.getPackage()
    print(a+" "+b)

    #a.startMainProgramLoop()


