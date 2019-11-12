import socket
from header import Header
from package import Package

UDP_IP = '127.0.0.1'
UDP_PORT = 80
s = socket.socket(socket.AF_INET)
s.connect((UDP_IP,UDP_PORT))

header=Header()
header.BuilderSetByte1(1,2,4)
header.BuilderSetByteResp(0,1)
header.BuilderSetMessageId(31)
header.BuilderSetToken(63)
header.BuilderBuild()

package = Package()
package.buildPackage(header.header,"Coords")
print("sending")
s.sendall(package.getPackage())
data = s.recv(1024)
print(data.decode())
print(header.header)
s.close()