# despesas.py
import sqlite3
from database import DATABASE_NAME 
from datetime import datetime

def conectar_bd():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

def adicionar_despesa(data, descricao, categoria, valor):
    conn, cursor = conectar_bd()
    try:
        if not all([data, descricao, valor]):
            print("Erro: Data, Descrição e Valor são obrigatórios.")
            return False, "Data, Descrição e Valor são obrigatórios."
        if not isinstance(valor, (int, float)) or valor <= 0:
            print("Erro: Valor da despesa deve ser um número positivo.")
            return False, "Valor da despesa deve ser um número positivo."

        cursor.execute('''
        INSERT INTO despesas (data, descricao, categoria, valor)
        VALUES (?, ?, ?, ?)
        ''', (data, descricao, categoria, valor))
        conn.commit()
        print(f"Despesa '{descricao}' no valor de {valor} adicionada com sucesso! ID: {cursor.lastrowid}")
        return True, f"Despesa adicionada com sucesso! ID: {cursor.lastrowid}"
    except Exception as e:
        print(f"Ocorreu um erro ao adicionar a despesa: {e}")
        return False, f"Ocorreu um erro ao adicionar a despesa: {e}"
    finally:
        conn.close()

def listar_despesas(data_inicio=None, data_fim=None):
    conn, cursor = conectar_bd()
    try:
        query = "SELECT id, data, descricao, categoria, valor FROM despesas"
        params = []
        if data_inicio and data_fim:
            query += " WHERE data BETWEEN ? AND ?"
            params.extend([data_inicio, data_fim])
        elif data_inicio:
            query += " WHERE data >= ?"
            params.append(data_inicio)
        elif data_fim:
            query += " WHERE data <= ?"
            params.append(data_fim)
        
        query += " ORDER BY data DESC"

        cursor.execute(query, params)
        despesas_raw = cursor.fetchall()
        return [dict(despesa) for despesa in despesas_raw]
    except Exception as e:
        print(f"Ocorreu um erro ao listar as despesas: {e}")
        return []
    finally:
        conn.close()

if __name__ == '__main__':
    print("\n--- Lista de Despesas ---")
    despesas_cadastradas = listar_despesas()
    if despesas_cadastradas:
        for despesa in despesas_cadastradas:
            print(f"ID: {despesa['id']}, Data: {despesa['data']}, Desc: {despesa['descricao']}, Cat: {despesa['categoria']}, Valor: R${despesa['valor']:.2f}")
    else:
        print("Nenhuma despesa cadastrada.")