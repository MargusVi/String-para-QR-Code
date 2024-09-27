import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import io
import os

def generate_qr_code():
    # Obtém o texto inserido pelo usuário
    data = entry.get()
    if not data:
        messagebox.showwarning("Entrada Vazia", "Por favor, digite um texto para gerar o QR Code.")
        return
    # Cria o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    # Gera a imagem do QR Code
    img = qr.make_image(fill='black', back_color='white')
    # Salva a imagem em um objeto BytesIO
    byte_arr = io.BytesIO()
    img.save(byte_arr, format='PNG')
    # Exibe a imagem na interface gráfica
    byte_arr.seek(0)
    qr_img = Image.open(byte_arr)
    qr_img_tk = ImageTk.PhotoImage(qr_img)
    qr_label.config(image=qr_img_tk)
    qr_label.image = qr_img_tk

    # Copia a imagem para a área de transferência (somente Windows)
    if os.name == 'nt':
        try:
            import win32clipboard
            from io import BytesIO

            output = BytesIO()
            qr_img.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            messagebox.showinfo("QR Code", "QR Code gerado e copiado para a área de transferência.")
        except ImportError:
            messagebox.showwarning("Erro", "pywin32 não está instalado. Não foi possível copiar a imagem para a área de transferência.")
    else:
        messagebox.showinfo("QR Code", "QR Code gerado. Copiar para a área de transferência não é suportado neste sistema operacional.")

# Configura a janela principal
root = tk.Tk()
root.title("Gerador de QR Code")

# Configura os widgets
entry_label = tk.Label(root, text="Digite o texto para gerar o QR Code:")
entry_label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

generate_button = tk.Button(root, text="Gerar QR Code", command=generate_qr_code)
generate_button.pack(pady=10)

qr_label = tk.Label(root)
qr_label.pack(pady=10)

# Executa o loop principal da interface gráfica
root.mainloop()