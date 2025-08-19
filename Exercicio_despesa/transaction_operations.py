from tkinter import messagebox

# Classe responsável pelas operações de transações financeiras
class TransactionOperations:
    def __init__(self, db, ui):
        self.db = db
        self.ui = ui

    # Adiciona uma nova transação
    def adicionar_transacao(self):
        descricao = self.ui.entry_descricao.get().strip()
        valor_str = self.ui.entry_valor.get().strip().replace(",", ".")
        tipo = self.ui.combo_tipo.get().lower()
        
        # Validações
        if not all([descricao, valor_str, tipo]):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        try:
            valor = float(valor_str)
            if valor <= 0:
                raise ValueError("Valor deve ser positivo")
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido! Use apenas números positivos.")
            return
        
        # Insere no banco de dados
        self.db.insert_transaction(descricao, valor, tipo)
        
        # Limpa campos e atualiza interface
        self.limpar_campos()
        self.ui.atualizar_dados()
        messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")

    # Exclui a transação selecionada
    def excluir_transacao(self):
        selecionado = self.ui.tree.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione uma transação para excluir!")
            return
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta transação?"):
            item = self.ui.tree.item(selecionado[0])
            transacao_id = item['values'][0]  # Pega o ID da primeira coluna
            
            self.db.delete_transaction(transacao_id)
            self.ui.atualizar_dados()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Transação excluída com sucesso!")

    # Atualiza uma transação existente
    def atualizar_transacao(self):
        if self.ui.selected_transaction:
            descricao = self.ui.entry_descricao.get().strip()
            valor_str = self.ui.entry_valor.get().strip().replace(",", ".")
            tipo = self.ui.combo_tipo.get().lower()
            
            # Validações
            if not all([descricao, valor_str, tipo]):
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return
            
            try:
                valor = float(valor_str)
                if valor <= 0:
                    raise ValueError("Valor deve ser positivo")
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido! Use apenas números positivos.")
                return
            
            # Atualiza no banco de dados
            self.db.update_transaction(self.ui.selected_transaction[0], descricao, valor, tipo)
            
            # Limpa campos e atualiza interface
            self.limpar_campos()
            self.ui.atualizar_dados()
            self.ui.selected_transaction = None
            messagebox.showinfo("Sucesso", "Transação atualizada com sucesso!")
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma transação para atualizar.")

    # Limpa todos os campos do formulário
    def limpar_campos(self):
        self.ui.entry_descricao.delete(0, 'end')
        self.ui.entry_valor.delete(0, 'end')
        self.ui.combo_tipo.set("")
        self.ui.selected_transaction = None