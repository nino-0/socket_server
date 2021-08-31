import socket
import threading

# Connection Data
# socket.gethostbyname(socket.gethostname())  # '127.0.0.1'
host = '127.0.0.1'  # socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
fila = []
# Sending Messages To All Connected Clients


def broadcast(message):

    for client in clients:
        client.send(message)

# envia uma msg para o cliente executar o RPA


def send_exec_cliente():
    while True:
        print("digite 'exec' para inciar um execuçao de robô")
        msg = input('')
        if len(fila) > 0:
            na_vez = fila[0]

            na_vez.send(msg.encode('ascii'))
            fila.pop(0)
        else:
            print("não há ninguem conectado no server")
# Handling Messages From Clients


def handle(client):
    while True:
        try:
            # Broadcasting Messages

            message = client.recv(1024)
            msg_decode = message.decode(FORMAT)
            cliente_nome = msg_decode[msg_decode.find(
                "[")+1:msg_decode.find("]")]
            content = msg_decode[msg_decode.find(":")+1:]
            if content == "done":
                print('tamanho da fila', len(fila))
                print(f"{cliente_nome} Finalizou a execução")
                fila.append(client)
                print('tamanho da fila', len(fila))
                # adiciona o cliente no final da fila

            # broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            # broadcast('{} left!'.format(nickname).encode(FORMAT))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function

# pegando valor entre cochete. y nome da str
# name = y[y.find("[")+1:y.find("]")]


def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        fila.append(client)
        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        # broadcast("{} joined!".format(nickname).encode('ascii'))
        # client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# receive()
write_thread = threading.Thread(target=receive)
write_thread.start()
print("server is runing")
write_thread = threading.Thread(target=send_exec_cliente)
write_thread.start()
