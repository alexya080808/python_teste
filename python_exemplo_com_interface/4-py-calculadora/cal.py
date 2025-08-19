import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from functools import partial
import os
import sys

def resource_path(relative_path):
    """Obtém o caminho absoluto do recurso, funcionando com PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Calculadora:
    def __init__(self):
        # Inicializa a janela principal
        self.janela = ttk.Window(title="Calculadora SENAI", themename="darkly")
        self.janela.geometry('400x750')

        # Cores e fontes
        self.cor_fundo = 'black'
        self.cor_botao = 'secondary'
        self.cor_texto = 'white'
        self.cor_operacao = 'warning'
        self.font_botao = ('Roboto', 18)
        self.font_display = ('Roboto', 36)

        # Ícone da janela
        icon_path = resource_path('calc.ico')
        if os.path.exists(icon_path):
            self.janela.iconbitmap(icon_path)

        # Frame para display
        self.display_frame = ttk.Frame(self.janela)
        self.display_frame.pack(fill='both', expand=True)

        self.display = ttk.Label(
            self.display_frame,
            text='',
            font=self.font_display,
            anchor='e',
            padding=(20, 10)
        )
        self.display.pack(fill='both', expand=True)

        # Frame para botões
        self.buttons_frame = ttk.Frame(self.janela)
        self.buttons_frame.pack(fill='both', expand=True)

        self.botoes = [
            ['C', '<⊠', '^', '/'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '+'],
            ['1', '2', '3', '-'],
            ['.', '0', '()', '=']
        ]

        # Criação dos botões
        for i, linha in enumerate(self.botoes):
            for j, texto in enumerate(linha):
                estilo = 'warning.TButton' if texto in ['C', '<⊠', '^', '/', 'x', '+', '-', '='] else 'secondary.TButton'
                botao = ttk.Button(
                    self.buttons_frame,
                    text=texto,
                    style=estilo,
                    width=10,
                    command=partial(self.interpretar_botao, texto)
                )
                botao.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')

        # Configuração do grid para botões
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.buttons_frame.grid_columnconfigure(j, weight=1)

        # Frame para imagem SENAI
        self.frame_imagem = ttk.Frame(self.janela)
        self.frame_imagem.pack(fill='both', expand=True)

        imagem_path = resource_path('Senai.png')
        if os.path.exists(imagem_path):
            imagem = Image.open(imagem_path)
            imagem = imagem.resize((300, 100), Image.LANCZOS)
            imagem_tk = ImageTk.PhotoImage(imagem)
            label_imagem = ttk.Label(self.frame_imagem, image=imagem_tk, text="")
            label_imagem.image = imagem_tk
            label_imagem.pack()

        # Frame para seletor de temas
        self.frame_tema = ttk.Frame(self.janela)
        self.frame_tema.pack(fill='x', padx=10, pady=10)

        self.label_tema = ttk.Label(self.frame_tema, text="Escolher tema:", font=('Roboto', 12))
        self.label_tema.pack(side='top', pady=(0, 5))

        self.temas = ['darkly', 'cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 'pulse',
                      'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerulean']
        self.selector_tema = ttk.Combobox(self.frame_tema, values=self.temas, state='readonly')
        self.selector_tema.set('darkly')
        self.selector_tema.pack(side='top', fill='x')
        self.selector_tema.bind("<<ComboboxSelected>>", self.mudar_tema)

        # Inicia a janela
        self.janela.mainloop()

    def mudar_tema(self, evento):
        novo_tema = self.selector_tema.get()
        self.janela.style.theme_use(novo_tema)

    def interpretar_botao(self, valor):
        texto_atual = self.display.cget("text")

        if valor == 'C':
            self.display.configure(text='')
        elif valor == '<⊠':
            self.display.configure(text=texto_atual[:-1])
        elif valor == '=':
            self.calcular()
        elif valor == '()':
            if not texto_atual or texto_atual[-1] in '+-/*':
                self.display.configure(text=texto_atual + '(')
            elif texto_atual[-1].isdigit():
                self.display.configure(text=texto_atual + ')')
        else:
            self.display.configure(text=texto_atual + valor)

    def calcular(self):
        #Avalia a expressão matemática
        expressao = self.display.cget("text").replace('x', '*').replace('^', '**')
        try:
            resultado = eval(expressao)
            self.display.configure(text=str(resultado))
        except:
            # Exibe uma mensagem de erro se a expressão for inválida
            self.display.configure(text='Erro')

# Inicia a aplicação
if __name__ == "__main__":
    Calculadora()
   
    