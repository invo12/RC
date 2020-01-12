

class Header():
    def __init__(self):
        self.header=""

        #Version + message type + token length
        self.byte1=""
        #Response code
        self.byteResp=""
        #Message id
        self.byteMesg=""

        #Token
        self.token=0
        self.tokenLength = 0

        self.version = 0
        self.messageType = 0
        self.tokenLength = 0
        self.responseClass = 0
        self.responseCode = 0
        self.messageId = 0


    def BuilderSetByte1(self,version,messageType,tokenLength):
        self.tokenLength = format(tokenLength,'04b')
        self.version=format(version,'02b')
        self.messageType = format(messageType, '02b')
        self.byte1=(version<<6) + (messageType<<4)+tokenLength
        self.byte1=format(self.byte1,'08b')



    def BuilderSetByteResp(self,codeClass,responseCode):
        self.byteResp=(codeClass<<5)+responseCode
        self.byteResp=format(self.byteResp,'08b')
        self.responseClass=format(codeClass,'03b')
        self.responseCode=format(responseCode,'05b')


    def BuilderSetMessageId(self,messageID):
        self.messageId=format(messageID,'016b')


    def BuilderSetToken(self,token):
        if self.getTokenLength()>0 and self.getTokenLength()<=8:
            self.token=format(token,'0'+str(self.getTokenLength()*8)+'b')


    def BuilderBuild(self):
        if self.getTokenLength() > 0:
            self.header=""+str(self.byte1)+str(self.byteResp)+str(self.messageId)+str(self.token)
        else:
            self.header =""+str(self.byte1)+str(self.byteResp)+str(self.messageId)

        return self.header


    def setHeaderAttributesFromString(self,header):
        self.header=header
        self.byte1=header[0:8]
        self.byteResp=header[8:16]
        self.byteMesg=header[16:32]
        self.version = self.header[0:2]
        self.messageType=self.header[2:4]
        self.tokenLength = self.header[4:8]
        self.responseClass=self.header[8:11]
        self.responseCode=self.header[11:16]
        self.messageId=self.header[16:32]
        if self.getTokenLength() > 0:
            self.token=self.header[32:32+self.getTokenLength()*8]
        else:
            self.token = ""

    def getVersion(self):
        return int(str(self.version),2)

    def getMessageType(self):
        return int(str(self.messageType),2)

    def getTokenLength(self):
        return int(str(self.tokenLength),2)

    def getResponseClass(self):
        return int(str(self.responseClass),2)

    def getResponseCode(self):
        return int(str(self.responseCode),2)

    def getMessageId(self):
        return int(str(self.messageId),2)

    def getToken(self):
        return int(str(self.token),2)

    def getHeader(self):
        return self.header

    def BuilderPrint(self):
        print("\n\nBuilder-> ")
        print("Vers+Type+Token Length=" + str(self.byte1))
        print("ReqCode= " + str(self.byteResp))
        print("MessageId=" + str(self.messageId))
        print("Token=", str(self.token))
        print("Header-> " + str(self.header))
        print("Header size->" + str(len(self.header)))

    def Print(self):
        print("\n\nAttr-> ")
        print("Vers= " + str(self.getVersion()))
        print("Message Type= " + str(self.getMessageType()))
        print("Token Length="  + str(self.getTokenLength()))
        print("Response Class= " + str(self.getResponseClass()))
        print("Response Code= " + str(self.getResponseCode()))
        print("MessageId=" + str(self.getMessageId()))
        print("Token=", str(self.getToken()))
        print("Header-> " + str(self.header))
        print("Header size->" + str(len(self.header)))

    def setMessageID(self, param):
        self.header=self.header[0:16]+format(param,'016b')+self.header[32:]

    def setType(self, param):
        self.header=self.header[0:2]+format(param,'02b')+self.header[4:]

    def setRequest(self,requestClass,requestCode):
        self.header = self.header[0:8] + format(requestClass,'03b') + format(requestCode,'05b') + self.header[16:]
