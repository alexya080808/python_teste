import tkinter as tk 

def mostrar_mensagem():
    #obter o texto da caixa de texto
    texto = caixa_texto.get()
    #atualizar o texto 
    label_resultado.config(text=texto)

    #criar janela principal
    janela = tk.Tk()
    janela.title("Exemplo de interface")
    janela.geometry("400x150")

    #criar uma caixa de entrada 
    caixa_texto = tk.Entry(janela, width=60)
    caixa_texto.pack(pady=10)

    #criar um botão 
    botao = tk.Button(janela, text="Mostrar Texto", command=mostrar_mensagem)
    botao.pack(pady=5)

    #criar um rótulo para exibir o resultado
    label_resultado = tk.Label(janela, text="")
    label_resultado.pack(pady=10)

    #executar a tela principal
    janela.mainloop()

    #test

