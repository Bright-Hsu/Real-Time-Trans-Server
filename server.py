import socket
import struct
import threading
import time
import cv2
import numpy


def recvByCount(sock, count):  # 读取count长度的数据
    buf = b''
    while count:
        newbuf = sock.recv(count)  # s.recv()接收. 因为client是通过 sk.recv()来进行接受数据，而count表示，最多每次接受count字节
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def receiveVideo(sock, addr):
    # 接受图片及大小的信息
    print('connect from:' + str(addr))
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')  # avi格式
    videoWriter = cv2.VideoWriter(
        './receive_video/%s.avi' % time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time())), fourcc, 30,
        (640, 480))
    while True:
        start = time.time()
        # 接收图片大小
        recvSize = struct.calcsize('i')
        size_bytes = recvByCount(sock, recvSize)
        if size_bytes is None:
            break
        size = int.from_bytes(size_bytes, byteorder='big')
        print('the image size = ', size, 'bytes，   size_bytes = ', "".join([hex(int(i)) for i in size_bytes]),
              ',     len(size_bytes) = ', len(size_bytes))
        info = struct.unpack('>i', size_bytes)
        print('the image size = ', size, 'bytes，   size_bytes = ', size_bytes, ',     info[0] = ', info[0])
        if len(size_bytes) == 0 or size == 0:
            continue
        # 接收图片
        stringData = recvByCount(sock, size)

        # 将获取到的字符流数据转换成1维数组 data = numpy.fromstring()
        data = numpy.frombuffer(stringData, numpy.uint8)
        # data = numpy.fromstring(stringData, numpy.uint8)
        # data = numpy.asarray(stringData, dtype='uint8')
        decodeImage = cv2.imdecode(data, cv2.IMREAD_COLOR)  # 将数组解码成图像
        # 保存图像
        # cv2.imwrite('receive_video/%s.jpg' 6 % time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time())), decodeImage)
        # 显示图像
        # cv2.imshow('SERVER', decodeImage)

        # =================================================================================================================================
        videoWriter.write(decodeImage)
        end = time.time()
        eachtime = end - start
        print('process time = ', eachtime)
        # ================================================================================================================================
        if cv2.waitKey(10) & 0xff == ord('q'):
            break
    cv2.destroyAllWindows()
    videoWriter.release()


if __name__ == '__main__':
    address = ('192.168.1.102', 8888)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    print(f"[*]Listening:  {address}")
    while True:
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=receiveVideo, args=(sock, addr))
        t.start()
        t.join()
