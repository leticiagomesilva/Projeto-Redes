import socket
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ACK_MESSAGE = "!ACK"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Defina o tempo limite global para a conexão
CONNECTION_TIMEOUT = 300  # Tempo limite em segundos
start_time = time.time()  # Inicia o temporizador para toda a conexão

def check_connection_timeout():
    """Verifica se o tempo de conexão foi excedido."""
    elapsed_time = time.time() - start_time
    if elapsed_time > CONNECTION_TIMEOUT:
        print(f"[CLIENT] Tempo de conexão expirado. Desconectando...")
        client.send(DISCONNECT_MESSAGE.encode(FORMAT))  # Envia desconexão
        client.close()
        return True
    return False

def generate_checksum(message):
    """Gera um checksum para a mensagem (diferenca entre o numero de bytes da mensagem e ela mesma)."""
    msg_length = len(message)
    checksum = msg_length - msg_length  # Isso sempre dará 0
    return checksum

def send_messages(messages, checksums):
    """Envia um conjunto de mensagens para o servidor com checksums."""
    if check_connection_timeout():  # Verifica timeout de conexão
        return  # Sai se o tempo de conexão expirar
    
    # Junta as mensagens com um delimitador '|' para enviá-las como uma única string
    msg = '|'.join(messages)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    # Envia o comprimento da mensagem
    client.send(send_length)
    # Envia a mensagem
    client.send(message)
    # Envia os checksums como um array
    client.send(str(checksums).encode(FORMAT))
    
    response = client.recv(2048).decode(FORMAT)
    if response == ACK_MESSAGE:
        print("[CLIENT] Todas as mensagens foram confirmadas com sucesso.")
    elif response.startswith("NACK:"):
        # Extrai os índices de mensagens com erro
        error_indices = eval(response.split(":")[1])
        for idx in error_indices:
            print(f"[CLIENT] Mensagem {idx} foi recebida com erro de integridade!")



def send_burst(num_packets, error_packet=None):
    """Envia múltiplas mensagens em rajada com ou sem erro, com checksums."""
    if check_connection_timeout():  # Verifica timeout de conexão
        return  # Sai se o tempo de conexão expirar
    
    messages = []
    checksums = []
    for i in range(num_packets):
        if check_connection_timeout():  # Verifica timeout de conexão
            return  # Sai se o tempo de conexão expirar
        
        msg = input(f"Digite a mensagem para o pacote {i + 1}: ")  # Permite digitar a mensagem para cada pacote
        checksum = generate_checksum(msg)  # Gera o checksum normal (0)
        
        if error_packet is not None and i == error_packet - 1:  # Adiciona erro no pacote especificado
            checksum = 1  # Modifica o checksum para 1, simulando erro
        
        messages.append(msg)
        checksums.append(checksum)
    
    send_messages(messages, checksums)

def main_menu():
    while True:
        if check_connection_timeout():  # Verifica timeout de conexão
            break  # Sai se o tempo de conexão expirar
        
        print("1. Enviar pacote único")
        print("2. Enviar pacotes em rajada")
        print("3. Enviar rajadas com erro")  # Nova opção para enviar rajadas com erro
        print("4. Sair")  # Mover opção de sair para a posição 4
        choice = input("Escolha uma opção: ")

        if choice == '1':
            msg = input("Digite a mensagem para enviar: ")
            send_messages([msg], [generate_checksum(msg)])  # Envia uma lista com uma única mensagem e seu checksum
        elif choice == '2':
            while True:
                try:
                    num_packets = int(input("Digite o número de pacotes para enviar em rajada: "))
                    break  # Sai do loop se a entrada for um número válido
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número.")
            
            send_burst(num_packets)  # Envia pacotes sem erro
        elif choice == '3':
            while True:
                try:
                    num_packets = int(input("Digite o número de pacotes para enviar em rajada (com erro): "))
                    break  # Sai do loop se a entrada for um número válido
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número.")
            
            while True:
                try:
                    error_packet = int(input(f"Digite em qual pacote (1 a {num_packets}) o erro deve ser inserido: "))
                    if 1 <= error_packet <= num_packets:
                        break  # Sai do loop se a entrada for um número válido dentro do intervalo
                    else:
                        print(f"Por favor, digite um número entre 1 e {num_packets}.")
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número válido.")
            
            send_burst(num_packets, error_packet)  # Envia pacotes com erro em um pacote específico
        elif choice == '4':
            send_messages([DISCONNECT_MESSAGE], [generate_checksum(DISCONNECT_MESSAGE)])  # Envia a mensagem de desconexão
            break
        else:
            print("Opção inválida. Tente novamente.")

main_menu()