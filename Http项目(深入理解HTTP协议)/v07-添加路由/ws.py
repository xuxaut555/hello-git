class ServerContent:
    ip = '127.0.0.1'
    port = 9999

    head_protocal = "HTTP/1.1 "
    head_code_200 = "200 "
    head_status_OK = "OK"

    head_content_length = "Content-Length: "
    head_content_type = "Content-Type: "
    content_type_html = "text/html"

    blank_line = ""



import socket
import threading

class SocketHandler:

    def __init__(self, sock):
        self.sock = sock
        # 放置Http请求的头部信息
        self.headInfo = dict()

    def startHandler(self):
        '''
        处理传入请求做两件事情
        1. 解析http协议
        2. 返回n内容
        :return:
        '''
        self.headHandler()
        self.reqRoute()
        return None

    def reqRoute(self):

        uri = self.headInfo.get("uri")
        if uri == b"/":
            self.sendRsp(r"./webapp/hello.html")
            return None
        if uri == b"/favicon.ico":
            self.sendStaticIco(r"./static/fav.jfif")
            return None

        self.sendRsp(r"./webapp/404.html")

    def sendStaticIco(self, fp):
        with open(fp, mode='rb') as f:
            ico = f.read()
            self.__sendRspAll(ico)

    def headHandler(self):
        self.headInfo = dict()
        tmpHead = self.__getAllLine()
        for line in tmpHead:
            if b":" in line:
                # split的具体含义
                infos = line.split(b": ")
                self.headInfo[infos[0]] = infos[1]
            else:
                infos = line.split(b" ")
                self.headInfo["protocal"] = infos[2]
                self.headInfo["method"] = infos[0]
                self.headInfo["uri"] = infos[1]


    def sendRsp(self, fp):
        data = "HELLO WORLD"
        '''
        想返回一个静态页面，可以考虑把静态页面文件读入，作为str类型
        然后作为一共长字符串返回
        '''

        #r'.\webapp\hello.html'

        with  open(fp, mode='r', encoding='utf-8') as f:
            data = f.read()
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

        if type(data) == bytes:
            self.sock.send(data)
        else:
            data += "\r\n"
            self.sock.send(data.encode())
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


    def __init__(self, ip=ServerContent.ip, port=ServerContent.port):
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
