import socket
import threading
import time

host = socket.gethostbyname(socket.gethostname())
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} Left The Chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, adress = server.accept()
        print(f'Connected With {str(adress)}')

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f'Client Username: {nickname}')
        broadcast(f'{nickname} Connected To The Server!\n'.encode('utf-8'))
        client.send('Connected To The Server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('-------------------------------------------------')
print(f'Connecting To {host} On Port {port}...')
time.sleep(2)
print('Server Is Running!')
print('-------------------------------------------------')
receive()
