import socket
import threading

class SocketHandler:

    def __init__(self, sock):
        self.sock = sock
        # 放置Http请求的头部信息
        self.headInfo = set()

    def startHandler(self):
        '''
        处理传入请求做两件事情
        1. 解析http协议
        2. 返回n内容
        :return:
        '''
        self.headHandler()
        self.sendRsp()
        return None

    def headHandler(self):
        # 两个下划线开头的变量是啥意思捏？
        self.headInfo = self.__getAllLine()
        print(self.headInfo)
        return None

    def sendRsp(self):
        data = "HELLO WORLD"
        self.__sendRspAll(data)
        return None

#####################################

    def __getLine(self):

        b1 = self.sock.recv(1)
        b2 = 0
        data = b''

        while  b2 != b'\r' and b1 != b'\n' :
            b2 = b1
            b1 = self.sock.recv(1)

            data += bytes(b2)

        return data.strip(b'\r')


    def __getAllLine(self):

        data = b''
        dataList = list()
        data = b''

        while True:
            data = self.__getLine()
            if data:
                dataList.append(data)
            else:
                return dataList

        return None

    def __sendRspLine(self,data):

        data += "\r\n"
        self.sock.send(data.encode("ASCII"))
        return None


    def __sendRspAll(self, data):

        self.__sendRspLine("HTTP/1.1 200 OK")

        strRsp = "Content-Length: "
        strRsp += str(len(data))
        self.__sendRspLine( strRsp )

        self.__sendRspLine("Content-Type: text/html")

        self.__sendRspLine("")
        self.__sendRspLine(data)


class WebServer():


    def __init__(self, ip='127.0.0.1', port=7853):
        self.ip = ip
        self.port = port

        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)
        print("WebServer is started............................")

    def start(self):
        '''
        服务器程序一共永久性不间断提供服务
        :return:
        '''
        while True:
            skt, addr = self.sock.accept()

            if skt:
                print("Received a socket {0} from {1} ................. ".format(skt.getpeername(), addr))
                # sockHandler负责具体通信
                sockHandler = SocketHandler(skt)
                thr = threading.Thread(target=sockHandler.startHandler , args=( ) )
                thr.setDaemon(True)
                thr.start()
                thr.join()

                skt.close()
                print("Socket {0} handling is done............".format(addr))



if __name__ == '__main__':
    ws = WebServer()
    ws.start()