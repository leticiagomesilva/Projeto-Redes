# import socket
# import threading

# HOST = '127.0.0.1'
# PORT = 5000

# tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# origem = (HOST, PORT)
# tcp.bind(origem)
# tcp.listen(1)

# while True:
#     con, client = tcp.accept()
#     print('Conectado por: ', client)
#     while True:
#         mensagem = con.recv(1024)
#         if not mensagem: break
#         print(client, mensagem)
#     print('Finalizando conexão do cliente: ', client)
#     con.close()

# ---------
import socket 
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
    
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
server.bind(ADDR)

def handle_client (conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
              
    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print ("[STARTING] Server is starting...")
start()