import socket
import hashlib
import time
import threading

def checksum(data):
    return sum(ord(c) for c in data) & 0xFFFF

class Cliente:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send_with_ack(self, data):
        chk = checksum(data)
        message = f"{data}:{chk}"
        self.socket.sendall(message.encode('utf-8'))
        print(f"Enviado: {message}")
        self.await_ack()

    def await_ack(self):
        while True:
            response = self.socket.recv(1024).decode('utf-8')
            if response == "ACK":
                print("ACK recebido")
                break
            elif response == "NAK":
                print("NAK recebido, reenviando dados")
                self.send_with_ack(data)

    def close(self):
        self.socket.sendall("DISCONNECT".encode('utf-8'))
        self.socket.close()
        print("Conexão encerrada.")


# Utilização
cliente = Cliente('127.0.0.1', 12345)
cliente.send_with_ack("Olá, servidor!")
cliente.close()
