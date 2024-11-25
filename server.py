import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ACK_MESSAGE = "!ACK"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            try:
                msg_length = int(msg_length)
            except ValueError:
                msg = msg_length  # Caso a mensagem não seja numérica, ela já é uma mensagem completa
                print(f"[{addr}] Mensagem de desconexão recebida: {msg}")
                if msg == DISCONNECT_MESSAGE:
                    connected = False  # Encerra a conexão caso a mensagem de desconexão seja recebida
            else:
                msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            # Aqui, as mensagens são divididas por um delimitador e processadas
            messages = msg.split("|")  # As mensagens serão separadas por '|'
            checksums = conn.recv(2048).decode(FORMAT)  # Recebe os checksums
            checksums = eval(checksums)  # Converte a string de volta para lista
            
            print(f"[{addr}] Mensagens recebidas:")
            error_indices = []  # Lista para armazenar índices de mensagens com erro

            for i, message in enumerate(messages):
                print(f"Mensagem {i+1}: {message}")
                print(f"Checksum {i+1}: {checksums[i]}")

                # Verifica se o checksum é 0
                if checksums[i] == 0:
                    print(f"[{addr}] Mensagem {i+1} chegou íntegra!")
                else:
                    print(f"[{addr}] Mensagem {i+1} corrompida! (Checksum errado)")
                    messages[i] = "ERRO"  # Substitui a mensagem corrompida por "ERRO"
                    error_indices.append(i + 1)  # Armazena o índice da mensagem com erro (começando do 1)

            # Mostra as mensagens com "ERRO" para pacotes corrompidos
            print(f"[{addr}] Mensagens após verificação:")
            for i, message in enumerate(messages):
                print(f"Mensagem {i+1}: {message}")

            # Envia resposta de acordo com a verificação de erros
            if error_indices:
                nack_message = f"NACK:{error_indices}"  # Monta o NACK com os índices dos erros
                conn.send(nack_message.encode(FORMAT))  # Envia NACK com os índices dos erros
            else:
                conn.send(ACK_MESSAGE.encode(FORMAT))  # Envia ACK se tudo estiver íntegro

    conn.close()



def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()