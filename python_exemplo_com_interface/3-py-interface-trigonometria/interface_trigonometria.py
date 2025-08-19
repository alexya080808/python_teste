import tkinter as tk #Importa a biblioteca Tkinter para a criação da interface gráfica
import math # Importa a biblioteca math para realizar operações matemáticas
from PIL import Image, ImageTk # Importa as classes Image e ImageTk da biblioteca PIL para manipulação de imagens
import os # Importa a biblioteca os para operações com o sistema de arquivos
import sys # Importa a biblioteca sys para manupulaçãõ de variáveis e funções do sistema

def resource_path(relative_path):
    """
    Obtém o caminho absoluto do recurso, funciona tanto em ambiente de desenvolvimento quanto após o empacotamento com PyInstaller.
    """
    try:
        # PyInstaller cria um diretório temporário e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se não estiver executando pelo PyInstaller, utiliza o caminho absoluto do diretório atual
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path) # Retorna o caminho completo do arquivo

def calcular():
    """
    Realiza o cáculo dos valores trigonométricos (seno, cosseno e tangente) do ângulo fornecido e atualiza as labels com os resultados.
    """
    try:
        angulo = float(entrada_angulo.get())  # Obtém o valor do ângulo inserido pelo usuário
        radiano = math.radians(angulo)  # Converte o ângulo de graus para radianos

        # Calcula os valores trigonométricos
        seno = math.sin(radiano)
        cosseno = math.cos(radiano)
        tangente = math.tan(radiano)

        # Atualiza as labels com os resultados formatados com 3 casas decimais
        resultado_seno.config(text=f"{seno:.3f}")
        resultado_cosseno.config(text=f"{cosseno:.3f}")
        resultado_tangente.config(text=f"{tangente:.3f}")
    except ValueError:
        # Em caso de erro (por exemplo, entrada inválida), exibe "Erro" nas labels
        resultado_seno.config(text="Erro")
        resultado_cosseno.config(text="Erro")
        resultado_tangente.config(text="Erro")

def limpar():
    """
    Limpa a entrada do usuário e reseta as labels dos resultados.
    """
    entrada_angulo.delete(0, tk.END)  # Limpa o campo de entrada
    resultado_seno.config(text="") # Limpa o resultado do seno
    resultado_cosseno.config(text="") # Limpa o resultado do cosseno
    resultado_tangente.config(text="") # Limpa o resultado da tangente

def validar_entrada(texto):
    """
    Valída a entrada do usuário permitindo apenas números e garantindo que o valor esteja entre 0 e 90.
    """
    if texto.isdigit() or texto == "": # Permite apenas números ou campo vazio
        if texto == "":  # Se o campo estiver vazio, permite a entrrada
            return True
        valor = int(texto) # Converte o texto para inteiro
        return 0 <= valor <= 90  # Verifica se o valor está entre 0 e 90
    return False  # Se não for um número, retorna False
     
# Configuração da janela principal
janela = tk.Tk() # Criar a janela principal
janela.title("Calculadora Trigonométrica") # Define o título da janela
janela.geometry("400x550") # Define o tamanho da janela
janela.configure(bg="#f0f0f0") # Define a cor de fundo da janela

# Carregar e definir o ícone da janela
try:
    icone_path = resource_path("seno.png")  # Caminho do ícone
    icone = Image.open(icone_path)  # Abrir a imagem do ícone
    icone = ImageTk.PhotoImage(icone)  # Converter para PhotoImage
    janela.iconphoto(True, icone)  # Definir o ícone da janela
except FileExistsError:
    print("Imagem 'seno.png' não encontrada para o ícone") # Caso o arquivo não exista, exibe mensagem de erro

# Imagem seno2.png
try:
    imagem_path = resource_path("seno2.png")  # Caminho da imagem
    imagem = Image.open(imagem_path)  # Abrir a imagem
    imagem = imagem.resize((380, 200), Image.LANCZOS)  # Redimensionar a imagem
    foto = ImageTk.PhotoImage(imagem)  # Converter para PhotoImage
    label_imagem = tk.Label(janela, image=foto, bg="#f0f0f0", borderwidth=0)  # Criar um rótulo com a imagem
    label_imagem.image = foto  # Manter uma referência à imagem
    label_imagem.pack(pady=20)  # Adicionar o rótulo à janela
except FileNotFoundError:
    # Caso a imagem não seja encontrada, exibe uma mensagem de texto no lugar da imagem
    label_imagem = tk.Label(janela, text="Imagem 'seno2.png' não encontrada", bg="#f0f0f0")
    label_imagem.pack(pady=20)  # Adicionar o rótulo à janela

#Entrada do ângulo
frame_entrada = tk.Frame(janela, bg="#f0f0f0")  # Criar um frame para organizar a entrada
frame_entrada.pack(pady=10)  # Adicionar o frame à janela

label_angulo = tk.Label(frame_entrada, text="Ângulo (0 à 90):", font=('Arial', 14), bg="#f0f0f0")  # Label para o campo de entrada
label_angulo.pack(pady=(0, 5))  # Posiciona o label com um pequeno espaçamento inferior

validacao = janela.register(validar_entrada)  # Registrar a função de validação
entrada_angulo = tk.Entry(frame_entrada, width=3, justify='center', font=('Arial', 16), bd=0, highlightthickness=0, relief='flat', bg="#F0f0f0", fg="red", validate="key", validatecommand=(validacao, '%P'))  # Cria o campo de entrada do ângulo
entrada_angulo.pack()  # Posiciona o campo de entrada

# Linha abaixo do campo de entrada
linha = tk.Frame(frame_entrada, bg="black", height=1, width=entrada_angulo.winfo_reqheight())  # Cria uma linha decorativa abaixo do campo de entrada
linha.pack(pady=(0, 5))  # Posiciona o frame na janela com um espaçamento vertical

# Botões 
frame_botoes = tk.Frame(janela, bg="#f0f0f0") # Criar um frame para os botões
frame_botoes.pack(pady=20)  # Adicionar o frame à janela

botao_calcular = tk.Button(frame_botoes, text="Calcular", command=calcular, font=("Arial", 12), bg="#d9d9d9", relief='flat', bd=0, highlightthickness=0)  # Botão para calcular
botao_calcular.pack(side=tk.LEFT, padx=10)  # Adicionar o botão ao frame

botao_limpar = tk.Button(frame_botoes, text="Limpar", command=limpar, font=("Arial", 12), bg="#d9d9d9", relief='flat', bd=0, highlightthickness=0)  # Botão para limpar a entrada e os resultados
botao_limpar.pack(side=tk.RIGHT, padx=10)  # Adicionar o botão ao frame

# Resultados
frame_resultados = tk.Frame(janela, bg="#f0f0f0")  # Criar um frame para os resultados
frame_resultados.pack(pady=10)  # Adicionar o frame à janela

# label e resultado do seno
label_seno = tk.Label(frame_resultados, text="Seno:", font=('Arial', 14), bg="#f0f0f0")  # Rótulo para o seno
label_seno.grid(row=0, column=0, sticky="e", padx=10) 
resultado_seno = tk.Label(frame_resultados, text="", font=('Arial', 12), bg="#f0f0f0")  # Rótulo para o resultado do seno
resultado_seno.grid(row=0, column=1, sticky="w", padx=10, pady=5)

# Label e resultado para o Cosseno
label_cosseno = tk.Label(frame_resultados, text="Cosseno:", font=('Arial', 12), bg="#f0f0f0") 
label_cosseno.grid(row=1, column=0, padx=10, pady=5, sticky='e')  # Label para o cosseno, alinhado à direita
resultado_cosseno = tk.Label(frame_resultados, text="", font=('Arial', 12, 'bold'), fg='red', bg="#f0f0f0")
resultado_cosseno.grid(row=1, column=1, padx=10, pady=5, sticky='w')  # Label que exibe o resultado do cosseno alinhado à esquerda

# Label e resultado para a Tangente
label_tangente = tk.Label(frame_resultados, text="Tangente:", font=('Arial', 12), bg="#f0f0f0") 
label_tangente.grid(row=2, column=0, padx=10, pady=5, sticky='e')  # Label para a tangente, alinhado à direita
resultado_tangente = tk.Label(frame_resultados, text="", font=('Arial', 12, 'bold'), fg='red', bg="#f0f0f0")
resultado_tangente.grid(row=2, column=1, padx=10, pady=5, sticky='w')  # Label que exibe o resultado da tangente alinhado à esquerda

# Iniciar a janela
janela.mainloop()  # Iniciar o loop principal da aplicação, matendo a janela aberta

