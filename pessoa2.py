import socket
import select

class ChatServer:
    def __init__(self, host='127.0.0.1', port=9999):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = {}  # {socket: username}
        print(f"Servidor rodando em {host}:{port}")

    def broadcast(self, message, sender=None):
        print(f"Broadcast: {message}")  # Debug
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
            client.close()
            self.broadcast(f"{username} saiu do chat!")
            print(f"Cliente removido: {username}")  # Debug

    def run(self):
        while True:
            try:
                readable, _, _ = select.select([self.server] + list(self.clients.keys()), [], [], 0.1)
                
                for sock in readable:
                    if sock == self.server:
                        # Nova conexão
                        client, addr = self.server.accept()
                        username = client.recv(1024).decode().strip()
                        self.clients[client] = username
                        print(f"Novo cliente: {username}")  # Debug
                        self.broadcast(f"{username} entrou no chat!")
                        
                    else:
                        # Mensagem de cliente existente
                        try:
                            message = sock.recv(1024).decode()
                            if message:
                                username = self.clients[sock]
                                self.broadcast(f"{username}: {message}", sock)
                            else:
                                self.remove_client(sock)
                        except:
                            self.remove_client(sock)
            except Exception as e:
                print(f"Erro no servidor: {str(e)}")  # Debug

if __name__ == "__main__":
    server = ChatServer()
    server.run()