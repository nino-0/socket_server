import socket
import threading
import time

FORMAT = "utf-8"
# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# '192.168.100.102'
# Listening to Server and Sending Nickname


def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024)
            msg_decode = message.decode('ascii')

            if msg_decode == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(msg_decode)
                if msg_decode == 'exec':

                    print(f" o cliente {nickname} esta executando....")
                    # executar o script RPA
                    time.sleep(10)
                    client.send(f"[{nickname}]:done".encode('utf-8'))
                    print("execução finalizada")

        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break
# Sending Messages To Server


def write():
    while True:
        print("digite algo: ", end='')
        message = '[{}]:{}'.format(nickname, input(''))
        client.send(message.encode('ascii'))


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# write_thread = threading.Thread(target=write)
# write_thread.start()
