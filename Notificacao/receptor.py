import socket
import time
import threading
import sys
import os
import winreg
from winotify import Notification
import pystray
from PIL import Image, ImageDraw

HOST = "172.16.1.242"  # <-- IP do seu PC (host) aqui
PORT = 5000

def adicionar_inicializacao():
    exe_path = sys.executable if not getattr(sys, 'frozen', False) else sys.argv[0]
    chave = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    )
    winreg.SetValueEx(chave, "ReceptorNotificacoes", 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(chave)

def criar_icone():
    img = Image.new("RGB", (64, 64), color=(0, 120, 215))
    draw = ImageDraw.Draw(img)
    draw.ellipse((16, 16, 48, 48), fill=(255, 255, 255))
    return img

def escutar():
    while True:
        try:
            client = socket.socket()
            client.connect((HOST, PORT))
            while True:
                data = client.recv(1024).decode()
                if data:
                    titulo, mensagem = data.split("||")
                    Notification(
                        app_id="Notificações",
                        title=titulo,
                        msg=mensagem
                    ).show()
        except:
            time.sleep(5)
 
def main():
    adicionar_inicializacao()
    threading.Thread(target=escutar, daemon=True).start()
    icone = pystray.Icon(
        "Notificações",
        criar_icone(),
        "Receptor de Notificações",
        menu=pystray.Menu(
            pystray.MenuItem("Fechar", lambda icon, item: icon.stop())
        )
    )
    icone.run()

if __name__ == "__main__":
    main()