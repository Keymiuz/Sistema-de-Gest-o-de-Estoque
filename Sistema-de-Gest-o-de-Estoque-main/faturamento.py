import sqlite3
from database import DATABASE_PATH
from datetime import datetime
import estoque 

def conectar_bd(): 
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

def registrar_venda(data_venda, itens_venda, valor_total_venda, cliente=None, metodo_pagamento=None):
    conn = None 
    try:
        conn, cursor = conectar_bd() 
        cursor.execute("BEGIN TRANSACTION") 

        for item in itens_venda:
            produto_id = item['produto_id']
            quantidade_vendida = item['quantidade']
            produto_atual = estoque.buscar_produto_por_id(produto_id, cursor_externo=cursor) 

            if not produto_atual:
                cursor.execute("ROLLBACK")
                conn.close() 
                return False, f"Produto com ID {produto_id} não encontrado no catálogo."
            
            if produto_atual['estoque_atual'] < quantidade_vendida:
                cursor.execute("ROLLBACK")
                conn.close() 
                return False, f"Estoque insuficiente para o produto '{produto_atual['nome']}' (ID: {produto_id}). Disponível: {produto_atual['estoque_atual']}, Pedido: {quantidade_vendida}."

        cursor.execute('''
        INSERT INTO faturamento (data, cliente, valor_total, metodo_pagamento)
        VALUES (?, ?, ?, ?)
        ''', (data_venda, cliente, valor_total_venda, metodo_pagamento))
        
        faturamento_id = cursor.lastrowid
        if not faturamento_id:
            cursor.execute("ROLLBACK")
            conn.close()
            return False, "Falha ao obter ID do faturamento."

        for item in itens_venda:
            cursor.execute('''
            INSERT INTO itens_faturamento (faturamento_id, produto_id, quantidade, preco_unitario_venda, subtotal)
            VALUES (?, ?, ?, ?, ?)
            ''', (faturamento_id, item['produto_id'], item['quantidade'], item['preco_venda_unitario'], item['subtotal']))

            novo_estoque_registrado = estoque.atualizar_estoque(
                item['produto_id'], 
                item['quantidade'], 
                tipo_movimento="saida", 
                cursor_externo=cursor
            )
            if novo_estoque_registrado is None: 
                cursor.execute("ROLLBACK")
                conn.close()
                return False, f"Falha crítica ao atualizar estoque para o produto ID {item['produto_id']} durante a venda."


        cursor.execute("COMMIT") 
        print(f"Venda ID {faturamento_id} registrada com sucesso.")
        return True, faturamento_id

    except sqlite3.Error as e:
        if conn: 
            try:
                cursor.execute("ROLLBACK")
            except: 
                pass
        print(f"Erro SQLite ao registrar venda: {e}")
        return False, f"Erro no banco de dados ao registrar venda: {e}"
    except Exception as e:
        if conn:
            try:
                cursor.execute("ROLLBACK")
            except:
                pass
        print(f"Ocorreu um erro geral ao registrar a venda: {e}")
        return False, f"Ocorreu um erro geral ao registrar a venda: {e}"
    finally:
        if conn:
            conn.close() 

def listar_vendas(data_inicio=None, data_fim=None):
    conn, cursor = conectar_bd()
    try:
        query = "SELECT id, data, cliente, valor_total, metodo_pagamento FROM faturamento"
        params = []
        query += " ORDER BY data DESC"
        cursor.execute(query, params)
        vendas = cursor.fetchall()
        return [dict(venda) for venda in vendas]
    except Exception as e:
        print(f"Ocorreu um erro ao listar as vendas: {e}")
        return []
    finally:
        conn.close()

def buscar_itens_por_faturamento_id(faturamento_id):
    conn, cursor = conectar_bd()
    try:
        cursor.execute('''
            SELECT p.codigo, p.nome, iff.quantidade, iff.preco_unitario_venda, iff.subtotal
            FROM itens_faturamento iff
            JOIN produtos p ON iff.produto_id = p.id
            WHERE iff.faturamento_id = ?
        ''', (faturamento_id,))
        itens = cursor.fetchall()
        return [dict(item) for item in itens]
    except Exception as e:
        print(f"Erro ao buscar itens da venda {faturamento_id}: {e}")
        return []
    finally:
        conn.close()


if __name__ == '__main__':
    print("\n--- Lista de Vendas ---")
    vendas_cadastradas = listar_vendas()
    if vendas_cadastradas:
        for venda in vendas_cadastradas:
            print(f"ID: {venda['id']}, Data: {venda['data']}, Cliente: {venda['cliente']}, Total: R${venda['valor_total']:.2f}, Pag: {venda['metodo_pagamento']}")
    else:
        print("Nenhuma venda registrada.")