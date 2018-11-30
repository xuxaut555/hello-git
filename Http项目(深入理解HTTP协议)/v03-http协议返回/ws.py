import socket



def getHttpHeader(skt):
    '''
    得到传入socket的http请求头
    :param skt: 通信的socket
    :return: 解析后的请求头内容，字典形式
    '''

    # 读取某一行
    # 直到读取的行返回空行为止

    # 用来存放结果，dict类型
    rst = {}

    line = getLine(skt)
    while line:
        '''
        判断得到的行是报头还是首部行，两个操作方法不一样
        算法是：
        1. 利用‘： ’作为分隔符，分割字符串
        2. 如果是首部行，则一定会把字符串分成两个子串
        3. 否则就是一个字符串
        '''
        r = line.split(r': ')

        if len(r) == 2:
            rst[r[0]] = r[1]
        else:
            r = line.split(r' ')
            rst['method'] = r[0]
            rst['uri'] = r[1]
            rst['version'] = r[2]

        line = getLine(skt)

    return rst




def getLine(skt):
    '''
    从socket中读取某一行
    :param skt: ocket
    :return:  返回读取到的一行str格式内容
    '''
    '''
    前提:
    1. http协议传输内容是ascii编码
    2. 真正传输的内容是通过网络流传输
    3. 回车换行： b'\r', b'\n', b表示是一个bytes格式
    '''
    # 每次从socket读取一个byte内容
    b1 = skt.recv(1)
    b2 = 0
    #data用来存放读取的行的内容
    data = b''

    #当确定还没有读到一行最后，也就是回车换行符号的时候，需要循环
    while b2 != b'\r' and b1 != b'\n':
        b2 = b1
        b1 = skt.recv(1)

        data += bytes(b2)

    # decode 需要一个参数，即编码，但是不给的话就采用默认utf-8解码
    return data.strip(b'\r').decode()



def sendRsp(skt, content):
    '''
    发送返回值，利用传入的socket
    :param skt: 通信的socket
    :return:
    '''

    # 构建返回头
    rsp_1 = "HTTP/1.1 200 OK\r\n"
    rsp_2 = "Date: 20180616\r\n"
    # 求返回内容的长度
    len_value= len(content)
    rsp_3 = "Content-Length: {0}\r\n".format(len_value)
    rsp_4 = "\r\n"
    rsp_content = content
    # rsp代表返回的全部数据信息,里面包含http协议本身的内容
    rsp = rsp_1 + rsp_2 + rsp_3 + rsp_4 + rsp_content

    skt.send(rsp.encode())



# 理解两个参数的含义
# 理解创建一个socket的过程
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 注意addr的格式是tuple
# 以及tuple两个元素的含义
sock.bind(("127.0.0.1", 7852))
print("已经绑定端口........")
# 监听
sock.listen()
print("正在监听......")

# 接受一个传进来的socket
print("准备接受socket传入....")
skt, addr = sock.accept()
print("已经接收到传入socket： {0}".format(skt))

# 实际处理请求内容
http_info = getHttpHeader(skt)
print(http_info)




# 给对方一个反馈
msg = "I love only wangxiaojing"
sendRsp(skt, msg)

skt.close()
sock.close()

