import socket
import tkinter as tk
from tkinter import messagebox

class ChatClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat")
        self.root.geometry("400x500")
        self.setup_login()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def setup_login(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)
        tk.Label(self.frame, text="Nome:").pack()
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack()
        tk.Button(self.frame, text="Conectar", command=self.connect).pack()
        
    def setup_chat(self):
        self.frame.destroy()
        self.chat_text = tk.Text(self.root, height=20, state='disabled')
        self.chat_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(padx=5, pady=5, fill=tk.X)
        
        self.msg_entry = tk.Entry(bottom_frame)
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.msg_entry.bind('<Return>', lambda e: self.send_message())
        
        tk.Button(bottom_frame, text="Enviar", command=self.send_message).pack(side=tk.RIGHT)
        
        self.root.after(100, self.check_messages)
        
    def connect(self):
        try:
            self.client.connect(('127.0.0.1', 200))
            self.client.send(self.name_entry.get().encode())
            self.setup_chat()
        except:
            messagebox.showerror("Erro", "Não foi possível conectar ao servidor")
            
    def send_message(self):
        msg = self.msg_entry.get().strip()
        if msg:
            try:
                self.client.send(msg.encode())
                self.msg_entry.delete(0, tk.END)
            except:
                messagebox.showerror("Erro", "Falha ao enviar mensagem")
                
    def check_messages(self):
        try:
            self.client.settimeout(0.1)
            message = self.client.recv(1024).decode()
            self.chat_text.config(state='normal')
            self.chat_text.insert(tk.END, message + '\n')
            self.chat_text.see(tk.END)
            self.chat_text.config(state='disabled')
        except socket.timeout:
            pass
        except:
            messagebox.showerror("Erro", "Conexão perdida")
            self.root.quit()
            return
        self.root.after(100, self.check_messages)
        
    def run(self):
        self.root.mainloop()
        self.client.close()

if __name__ == "__main__":
    ChatClient().run()
