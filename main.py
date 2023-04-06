import socket
import threading
import time
import os


def receiveVideo(conn, addr):
    print('[*]connect from:' + str(addr))
    start = time.time()
    videoname = "%s.mp4" % (time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time())))
    global size
    size = 0
    videopath = "D:/receive_video/" + videoname
    while True:  # 一次接收1024字节 持续发送
        stringData = conn.recv(1024)
        if not stringData:
            break
        size += len(stringData)
        with open(videopath, 'ab') as f:
            f.write(stringData)

    end = time.time()
    print('[*]process time (sec): ', end - start)
    # video_size = os.path.getsize(videopath)  # #单位是B(字节)
    # print(f"[*]This File is {round(video_size / 1024 / 1024, 2)} MB")
    print('size: ', size)
    print('[*]This path send over')


if __name__ == '__main__':
    address = ('0.0.0.0', 8888)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    print(f"[*]Listening:  {address}")
    while True:
        conn, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=receiveVideo, args=(conn, addr))
        t.start()
    s.close()
