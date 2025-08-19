import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
from transaction_operations import TransactionOperations
import os
import sys

# Função para lidar com caminhos de recursos (mesma do main.py)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TelaFinancas(ctk.CTk):
    def __init__(self, db):
        super().__init__()  # Inicializa a classe pai (CTk)
        self.db = db  # Armazena a instância do banco de dados
        self.transaction_operations = TransactionOperations(db, self)  # Cria instância de operações de transação
        self.setup_ui()  # Configura a interface do usuário
        self.selected_transaction = None  # Armazena a transação selecionada na lista
        self.set_icon()  # Define o ícone da janela

    def set_icon(self):
        # Define o ícone da janela
        icon_path = resource_path("assets/money.ico")
        try:
            self.iconbitmap(icon_path)
        except:
            print(f"Não foi possível carregar o ícone: {icon_path}")

    def setup_ui(self):
        # Configura a interface do usuário
        self.title("💰 Gerenciador de Despesas")
        self.geometry("800x600")

        # Tenta carregar o ícone padrão
        try:
            icon_image = Image.open(resource_path("assets/money.png"))
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.iconphoto(False, icon_photo)
        except Exception as e:
            print(f"Não foi possível carregar o ícone padrão: {e}")

        # Cria o frame principal
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Dashboard - Saldo
        self.label_saldo = ctk.CTkLabel(self.frame, text="Saldo: R$ 0,00", 
                                       font=("Arial", 24, "bold"))
        self.label_saldo.pack(pady=10)

        # Seção do formulário
        ctk.CTkLabel(self.frame, text="Nova Transação", 
                    font=("Arial", 16, "bold")).pack(pady=(20, 5))

        # Frame do formulário
        self.form_frame = ctk.CTkFrame(self.frame)
        self.form_frame.pack(pady=10)

        # Campos de entrada
        self.entry_descricao = ctk.CTkEntry(self.form_frame, 
                                           placeholder_text="Ex: Almoço, Salário, Combustível", 
                                           width=250)
        self.entry_descricao.pack(side="left", padx=5)

        self.entry_valor = ctk.CTkEntry(self.form_frame, 
                                       placeholder_text="Ex: 150.50 ou 1500,00", 
                                       width=150)
        self.entry_valor.pack(side="left", padx=5)

        self.combo_tipo = ctk.CTkComboBox(self.form_frame, 
                                         values=["Receita", "Despesa"], 
                                         width=120)
        self.combo_tipo.pack(side="left", padx=5)

        # Frame dos botões
        self.btn_frame = ctk.CTkFrame(self.frame)
        self.btn_frame.pack(pady=10)

        # Botões de ação
        self.adicionar_btn = ctk.CTkButton(self.btn_frame, text="Adicionar",
                                          fg_color="#4CAF50", hover_color="#45a049",
                                          width=100, 
                                          command=self.transaction_operations.adicionar_transacao)
        self.adicionar_btn.pack(side="left", padx=5)

        self.atualizar_btn = ctk.CTkButton(self.btn_frame, text="Atualizar",
                                          fg_color="#2196F3", hover_color="#1976D2",
                                          width=100,
                                          command=self.transaction_operations.atualizar_transacao)
        self.atualizar_btn.pack(side="left", padx=5)

        self.excluir_btn = ctk.CTkButton(self.btn_frame, text="Excluir",
                                        fg_color="#F44336", hover_color="#d32f2f",
                                        width=100,
                                        command=self.transaction_operations.excluir_transacao)
        self.excluir_btn.pack(side="left", padx=5)

        self.limpar_btn = ctk.CTkButton(self.btn_frame, text="Limpar",
                                       fg_color="#FF9800", hover_color="#F57C00",
                                       width=100,
                                       command=self.transaction_operations.limpar_campos)
        self.limpar_btn.pack(side="left", padx=5)

        # Seção da lista
        ctk.CTkLabel(self.frame, text="Histórico de Transações", 
                    font=("Arial", 16, "bold")).pack(pady=(20, 5))

        # Configura o estilo da Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

        # Cria a Treeview para exibir as transações
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Data", "Descrição", "Tipo", "Valor"), 
                                show="headings", height=10)

        # Configura as colunas
        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Data", text="Data", anchor="center")
        self.tree.heading("Descrição", text="Descrição", anchor="w")
        self.tree.heading("Tipo", text="Tipo", anchor="center")
        self.tree.heading("Valor", text="Valor", anchor="e")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Data", width=100, anchor="center")
        self.tree.column("Descrição", width=300, anchor="w")
        self.tree.column("Tipo", width=100, anchor="center")
        self.tree.column("Valor", width=120, anchor="e")

        self.tree.pack(padx=20, pady=20, fill="both", expand=True)

        # Associa a seleção na Treeview ao método on_transaction_select
        self.tree.bind("<<TreeviewSelect>>", self.on_transaction_select)

        # Carrega os dados iniciais
        self.atualizar_dados()

    def atualizar_dados(self):
        # Limpa todos os itens existentes na Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insere todas as transações do banco de dados na Treeview
        for row in self.db.get_all_transactions():
            id_trans, descricao, valor, tipo, data = row
            valor_fmt = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            
            # Define as tags para colorir as linhas
            if tipo == "receita":
                tags = ("receita",)
            else:
                tags = ("despesa",)
            
            self.tree.insert("", "end", values=(id_trans, data, descricao, tipo.title(), valor_fmt), tags=tags)

        # Configura as cores das tags
        self.tree.tag_configure("receita", foreground="#4CAF50")
        self.tree.tag_configure("despesa", foreground="#F44336")

        # Atualiza o saldo
        self.atualizar_saldo()

    def atualizar_saldo(self):
        # Calcula e exibe o saldo atual
        saldo = self.db.get_balance()
        saldo_fmt = f"R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        self.label_saldo.configure(text=f"Saldo: {saldo_fmt}")
        
        # Define a cor baseada no saldo
        cor = "#4CAF50" if saldo >= 0 else "#F44336"
        self.label_saldo.configure(text_color=cor)

    def on_transaction_select(self, event):
        # Manipula o evento de seleção de uma transação na Treeview
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item, "values")
            self.selected_transaction = values
            
            # Preenche os campos com os dados da transação selecionada
            self.entry_descricao.delete(0, 'end')
            self.entry_descricao.insert(0, values[2])  # Descrição
            
            # Remove formatação do valor
            valor_str = values[4].replace("R$ ", "").replace(".", "").replace(",", ".")
            self.entry_valor.delete(0, 'end')
            self.entry_valor.insert(0, valor_str)
            
            self.combo_tipo.set(values[3])  # Tipo