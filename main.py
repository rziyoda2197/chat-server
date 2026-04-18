import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast(f'{nickname} left the chat!'.encode('ascii'))
                break

    def receive(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast(f'{nickname} left the chat!'.encode('ascii'))
                break

    def register(self, client):
        while True:
            try:
                nickname = client.recv(1024).decode('ascii')
                if nickname not in self.nicknames:
                    self.nicknames.append(nickname)
                    self.clients.append(client)
                    client.send('Nickname accepted!'.encode('ascii'))
                    self.broadcast(f'{nickname} joined the chat!'.encode('ascii'))
                    break
                else:
                    client.send('Nickname already taken!'.encode('ascii'))
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast(f'{nickname} left the chat!'.encode('ascii'))
                break

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        print(f'Chat server is listening on {self.host}:{self.port}')

        while True:
            client, address = server.accept()
            print(f'Connected with {str(address)}')

            client_handler = threading.Thread(target=self.register, args=(client,))
            client_handler.start()

            client_handler = threading.Thread(target=self.receive, args=(client,))
            client_handler.start()

def main():
    server = ChatServer()
    server.run()

if __name__ == "__main__":
    main()
