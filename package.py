from header import Header
class Package():
    def __init__(self):
        self.header = ""
        self.message = ""
        self.pack = ""


    def buildPackage(self,header,message):
        self.header = header+str('11111111')
        self.message = message
        if self.message == None or self.message == "":
            a = bytearray()
            aux = 0
            cnt = 0
            for x in self.header:
                if cnt < 8:
                    cnt = cnt + 1
                    aux = (aux << 1) | (ord(x) - ord('0'))
                else:
                    cnt = 1
                    a.append(aux)
                    aux = (ord(x) - ord('0'))
            a.append(aux)
            self.pack = a
        else:
            a = bytearray()
            aux = 0
            cnt = 0
            for x in self.header:
                if cnt < 8:
                    cnt = cnt + 1
                    aux = (aux << 1) | (ord(x) - ord('0'))
                else:
                    cnt = 1
                    a.append(aux)
                    aux = (ord(x) - ord('0'))
            a.append(aux)

            self.pack = a + self.message.encode()
        return self.pack


    def getPackageInfo(self):
        #TODO REMOVE DECODE AND GET DATA
        a = self.pack
        print("De Decodat "+ str(a))
        headerbyte=bytearray()
        messagebyte=bytearray()
        endHd=0
        for x in a:
            if x == 255:
                endHd=1
                continue
            if endHd == 0:
                headerbyte.append(x)
            else:
                messagebyte.append(x)

        bytes_as_bits = ''.join(format(byte, '08b') for byte in headerbyte)
        self.header = str(bytes_as_bits)
        self.message = messagebyte.decode()
        print("Dupa decodare Header: "+str(self.header))
        print("Dupa decodare Data: " + str(self.message))
        return (self.header,self.message)

    def getPackage(self):
        return self.pack

    def getHeader(self):
        return self.header
    def getMessage(self):
        return self.message