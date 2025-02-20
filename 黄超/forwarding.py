import socket
import threading
import time
def tcp_mapping_worker(conn_receiver, conn_sender):
    while True:
        try:
            data = conn_receiver.recv(2048)
        except Exception:
            print('Event: Connection closed.')
            break
    
        if not data:
            print('Info: No more data is received.')
            break
    
        try:
            conn_sender.sendall(data)
        except Exception:
            print('Error: Failed sending data.')
            break
    
        print('Info: Mapping > %s -> %s > %d bytes.' % (conn_receiver.getpeername(), conn_sender.getpeername(), len(data)))
    
    conn_receiver.close()
    conn_sender.close()
    
    return

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#本机ip地址和端口
local_host = '192.168.79.128'
local_port = 9922
#远端ip地址和端口
remote_host = '127.0.0.1'
remote_port = 9921

s.bind((local_host,local_port))
print('本机ip地址和端口'+local_host+':'+str(local_port))
print('远端ip地址和端口'+remote_host+':'+str(remote_port))
s.listen(5)

print('Starting mapping service on ' + local_host+ ':' + str(local_port) + ' ...')
c,addr = s.accept()
s2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
active1 = True
i=0
while active1:  #请求连接，每五秒发送一次请求，若超过一分钟则终止程序
	try:
		s2.connect((remote_host,remote_port))     #建立连接
		active1 = False
	except Exception as error:
		time.sleep(5)
		i=i+1
		if i==12:
			print('连接超时')
			active1=False
		else:
			continue

threading.Thread(target=tcp_mapping_worker,args=(c,s2)).start() 
threading.Thread(target=tcp_mapping_worker,args=(s2,c)).start()
