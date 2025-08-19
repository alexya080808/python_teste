import sqlite3
from datetime import datetime

# Classe para gerenciar a conexão com o banco de dados SQLite
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    # Cria a tabela 'transacoes' se ela não existir
    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            tipo TEXT NOT NULL,
            data TEXT DEFAULT CURRENT_DATE
        )
        ''')
        self.conn.commit()

    # Insere uma nova transação no banco de dados
    def insert_transaction(self, descricao, valor, tipo):
        data = datetime.now().strftime("%d/%m/%Y")
        self.cursor.execute("INSERT INTO transacoes (descricao, valor, tipo, data) VALUES (?, ?, ?, ?)",
                           (descricao, valor, tipo, data))
        self.conn.commit()

    # Retorna todas as transações do banco de dados ordenadas por ID decrescente
    def get_all_transactions(self):
        self.cursor.execute("SELECT * FROM transacoes ORDER BY id DESC")
        return self.cursor.fetchall()

    # Calcula o saldo atual (receitas - despesas)
    def get_balance(self):
        self.cursor.execute("SELECT SUM(CASE WHEN tipo='receita' THEN valor ELSE -valor END) FROM transacoes")
        result = self.cursor.fetchone()[0]
        return result if result else 0

    # Exclui uma transação do banco de dados
    def delete_transaction(self, id):
        self.cursor.execute("DELETE FROM transacoes WHERE id=?", (id,))
        self.conn.commit()

    # Atualiza uma transação existente
    def update_transaction(self, id, descricao, valor, tipo):
        self.cursor.execute("UPDATE transacoes SET descricao=?, valor=?, tipo=? WHERE id=?", 
                           (descricao, valor, tipo, id))
        self.conn.commit()

    # Fecha a conexão com o banco de dados
    def close(self):
        self.conn.close()