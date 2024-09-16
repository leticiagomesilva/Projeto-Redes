import socket
HOST = '127.0.0.1'
PORT = 5000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (HOST, PORT)
tcp.bind(origem)
tcp.listen(1)

while True:
    con, client = tcp.accept()
    print('Conectado por: ', client)
    while True:
        mensagem = con.recv(1024)
        if not mensagem: break
        print(client, mensagem)
    print('Finalizando conexão do cliente: ', client)
    con.close()