from header import Header
class Package():
    def __init__(self):
        self.header = ""
        self.message = ""
        self.pack = ""


    def buildPackage(self,header,message):
        self.header = header
        self.message = message
        if self.message is None or self.message is "":
            self.pack=self.header.encode()
        else:
            self.pack = (self.header + self.message).encode()
        return self.pack


    def getPackage(self):
        a = self.pack.decode()
        length = int(str(a[4:8]),2)
        self.header = a[0:32+length*8]
        if self.message is not None:
            self.message = a[32+length*8:]
        else:
            self.message=""
        return self.header,self.message


    def getHeader(self):
        return self.header
    def getMessage(self):
        return self.message