import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'gestao.db')

def conectar_bd():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

def criar_tabelas():
    conn, cursor = conectar_bd()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE NOT NULL,
        nome TEXT NOT NULL,
        descricao TEXT,
        unidade_medida TEXT,
        preco_custo REAL,
        preco_venda REAL NOT NULL,
        estoque_atual INTEGER DEFAULT 0,
        estoque_minimo INTEGER DEFAULT 0
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS faturamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        cliente TEXT, 
        valor_total REAL NOT NULL,
        metodo_pagamento TEXT 
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS itens_faturamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faturamento_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_unitario_venda REAL NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (faturamento_id) REFERENCES faturamento (id) ON DELETE CASCADE,
        FOREIGN KEY (produto_id) REFERENCES produtos (id) ON DELETE RESTRICT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS despesas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        descricao TEXT NOT NULL,
        categoria TEXT,
        valor REAL NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS compras_historico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_custo_unitario REAL,
        data_compra TEXT NOT NULL,
        fornecedor TEXT,
        nota_fiscal TEXT,
        FOREIGN KEY (produto_id) REFERENCES produtos (id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_tabelas()
    print("Banco de dados e tabelas verificados/criados com sucesso!")