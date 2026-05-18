import socket
import threading

clients = []

def handle_client(conn):
    clients.append(conn)
    try:
        while True:
            conn.recv(1024)  # mantém conexão viva
    except:
        clients.remove(conn)
        conn.close()

def aceitar_conexoes(server):
    while True:
        conn, addr = server.accept()
        print(f"[+] Receptor conectado: {addr}")
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

def enviar_notificacao(titulo, mensagem):
    for conn in clients[:]:
        try:
            payload = f"{titulo}||{mensagem}"
            conn.send(payload.encode())
        except:
            clients.remove(conn)

# Inicia servidor
server = socket.socket()
server.bind(("0.0.0.0", 5000))
server.listen(10)
print("Servidor rodando. Receptores podem se conectar agora.")
threading.Thread(target=aceitar_conexoes, args=(server,), daemon=True).start()

# Loop para enviar notificações pelo terminal
while True:
    titulo = input("Título: ")
    msg = input("Mensagem: ")
    enviar_notificacao(titulo, msg)
    print(f"Notificação enviada para {len(clients)} receptor(es).\n")