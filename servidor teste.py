import socket
import select

class ChatServer:
    def __init__(self, host='127.0.0.1', port=219):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = {}  # {socket: username}
        print(f"Servidor rodando em {host}:{port}")

    def broadcast(self, message, sender=None):
        for client in self.clients:
            if client != sender:
                try:
                    client.send(message.encode())
                except:
                    self.remove_client(client)

    def remove_client(self, client):
        if client in self.clients:
            username = self.clients[client]
            del self.clients[client]
            self.broadcast(f"{username} saiu do chat!")
            client.close()

    def run(self):
        while True:
            readable, _, _ = select.select([self.server] + list(self.clients.keys()), [], [])
            for sock in readable:
                if sock == self.server:
                    # Nova conexão
                    client, _ = self.server.accept()
                    username = client.recv(1024).decode()
                    self.clients[client] = username
                    self.broadcast(f"{username} entrou no chat!")
                else:
                    # Mensagem de cliente existente
                    try:
                        message = sock.recv(1024).decode()
                        if message:
                            self.broadcast(f"{self.clients[sock]}: {message}", sock)
                    except:
                        self.remove_client(sock)

if __name__ == "__main__":
    server = ChatServer()
    server.run()