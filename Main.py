from GUI import MainApp
from GetApiData import  GetAPI
from socket import *




if __name__=="__main__":
    API=GetAPI()
    a=MainApp(API)
    API.getWeatherData("Iasi")
    a.startMainProgramLoop()


