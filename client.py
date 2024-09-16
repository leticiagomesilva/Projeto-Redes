import socket
HOST = '127.0.0.1'
PORT = 5000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
destinatario = (HOST, PORT)
tcp.connect(destinatario)
print('Para sair use CTRL+X\n')

mensagem = input()
while mensagem != '\x18':
    tcp.send(mensagem)
    mensagem = input()

tcp.close()