import socket
import time

from header import Header
from package import Package

UDP_IP = '127.0.0.1'
UDP_PORT = 100
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect((UDP_IP,UDP_PORT))

header=Header()


header.BuilderSetByte1(1,0,4)
header.BuilderSetByteResp(0,1)
header.BuilderSetMessageId(31)
header.BuilderSetToken(63)
header.BuilderBuild()

package = Package()
package.buildPackage(header.header,"Temperature")
print("sending")
s.sendto(package.getPackage(),(UDP_IP,UDP_PORT))
data = s.recvfrom(1024)
package.pack=data[0]
package.getPackageInfo()
print(package.getMessage())
data = s.recvfrom(1024)
package.pack=data[0]
package.getPackageInfo()
print(package.getMessage())

data = s.recvfrom(1024)
package.pack=data[0]
package.getPackageInfo()
print(package.getMessage())
data = s.recvfrom(1024)
package.pack=data[0]
package.getPackageInfo()
print(package.getMessage())
data = s.recvfrom(1024)
package.pack=data[0]
package.getPackageInfo()
print(package.getMessage())


# time.sleep(1)
# header.BuilderSetByte1(1,3,4)
# header.BuilderSetByteResp(0,0)
# header.BuilderSetMessageId(33)
# header.BuilderSetToken(63)
# header.BuilderBuild()
#
# package = Package()
# package.buildPackage(header.header,"")
# s.sendto(package.getPackage(),(UDP_IP,UDP_PORT))

s.close()