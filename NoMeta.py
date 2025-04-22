import tkinter as tk
from PIL import Image
import piexif
from tkinter import filedialog
import os
import json
from tkinter import messagebox

# Função para selecionar a imagem
def selecionar_imagem():
    imagem = filedialog.askopenfile(title="Select a Image", filetypes=[("Imagens", "*.jpg;*.jpeg;*.png;*.gif")])
    if imagem:
        label_caminho.config(text=f"Imagem selecionada: {imagem.name}")
        # Ativa o botão "Limpar Metadados"
        botao_limpar.config(state=tk.NORMAL, command=lambda: limpar_metadados(imagem.name))
        botao_rastreia.config(state=tk.NORMAL, command=lambda: rastreia_metadados(imagem.name))
        

# Função para limpar os metadados e salvar a nova imagem
def limpar_metadados(caminho_imagem):
    try:
        # Abrir a imagem com Pillow
        imagem = Image.open(caminho_imagem)

        # Remover metadados EXIF usando piexif
        piexif.remove(caminho_imagem)

        # Salvar a imagem sem metadados
        novo_caminho = caminho_imagem.replace(".jpg", "_sem_metadados.jpg").replace(".jpeg", "_sem_metadados.jpeg")
        imagem.save(novo_caminho)

        label_caminho.config(text=f"Imagem salva sem metadados como: {novo_caminho}")
    except Exception as e:
        label_caminho.config(text=f"Erro: {e}")

def rastreia_metadados(caminho_imagem):
    try:
        imagem = Image.open(caminho_imagem)
        meta = piexif.load(caminho_imagem)

        meta_convertido = converter_bytes_para_string(meta)
        meta_json = json.dumps(meta_convertido, indent=4)

        if not os.path.exists("metadados"):
            os.makedirs("metadados")

        with open("metadados/metadados.json", "w") as file:
            file.write(meta_json)

        messagebox.showinfo("Sucesso", "Metadados rastreados em: metadados/metadados.json")
    except Exception as e:
        messagebox.showerror("Erro", f"{e}")

def converter_bytes_para_string(dado):
    if isinstance(dado, dict):
        return {k: converter_bytes_para_string(v) for k, v in dado.items()}
    elif isinstance(dado, list):
        return [converter_bytes_para_string(i) for i in dado]
    elif isinstance(dado, bytes):
        try:
            return dado.decode('utf-8', errors='replace')
        except:
            return str(dado)  # fallback se não for UTF-8
    else:
        return dado


# Criar a janela principal
janela = tk.Tk()
janela.title("NoMoreMeta!")

# Label de título
label_titulo = tk.Label(janela, text="NoMoreMeta! >:(")
label_titulo.pack(pady=10)

# Criar o botão para selecionar a imagem
botao_selecionar = tk.Button(janela, text="Selecionar Imagem", command=selecionar_imagem)
botao_selecionar.pack(pady=10)

# Criar um label para mostrar o caminho da imagem
label_caminho = tk.Label(janela, text="Nenhuma imagem selecionada")
label_caminho.pack(pady=10)

# Criar um botão para limpar os metadados (inicialmente desativado)
botao_limpar = tk.Button(janela, text="Limpar Metadados", state=tk.DISABLED)
botao_limpar.pack(pady=10)

botao_rastreia = tk.Button(janela, text="Rastrar Metadados", state=tk.DISABLED)
botao_rastreia.pack(pady=10)

# Iniciar a interface gráfica
janela.mainloop()
