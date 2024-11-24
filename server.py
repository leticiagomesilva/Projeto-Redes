import socket
import threading

def checksum(data):
    return sum(ord(c) for c in data) & 0xFFFF

class Servidor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print("Servidor iniciado e ouvindo...")

    def handle_client(self, conn, addr):
        print(f"Conexão estabelecida com {addr}")
        while True:
            data = conn.recv(1024).decode('utf-8')
            if data == "DISCONNECT":
                break
            payload, recv_checksum = data.rsplit(':', 1)
            if checksum(payload) == int(recv_checksum):
                conn.sendall("ACK".encode('utf-8'))
                print("Mensagem recebida corretamente.")
            else:
                conn.sendall("NAK".encode('utf-8'))
                print("Erro de checksum detectado.")

        conn.close()
        print(f"Conexão com {addr} encerrada.")

    def start(self):
        while True:
            conn, addr = self.socket.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    server = Servidor('127.0.0.1', 12345)
    server.start()

