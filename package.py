class Package():
    def __init__(self):
        self.header = ""
        self.message = ""
        self.pack = ""
    def buildPackage(self,header,message):
        self.header = header
        self.message = message
        self.pack = (self.header + self.message).encode()
        return self.pack
    def getPackage(self):
        a = self.pack.decode()
        length = int(str(a[4:8]),2)
        self.header = a[0:32+length*8]
        self.message = a[32+length*8:]
        print(self.header)
        print(self.message)
    def getHeader(self):
        return self.header
    def getMessage(self):
        return self.message