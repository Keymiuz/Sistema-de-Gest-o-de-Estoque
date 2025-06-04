import sqlite3
from database import DATABASE_PATH
from datetime import datetime

def conectar_bd():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

def adicionar_produto(codigo, nome, descricao, unidade_medida, preco_custo, preco_venda, estoque_inicial=0, estoque_minimo=0):
    conn, cursor = conectar_bd()
    try:
        cursor.execute('''
        INSERT INTO produtos (codigo, nome, descricao, unidade_medida, preco_custo, preco_venda, estoque_atual, estoque_minimo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (codigo, nome, descricao, unidade_medida, preco_custo, preco_venda, estoque_inicial, estoque_minimo))
        conn.commit()
        print(f"Produto '{nome}' adicionado com sucesso! ID: {cursor.lastrowid}")
        return cursor.lastrowid 
    except sqlite3.IntegrityError:
        print(f"Erro: Já existe um produto com o código '{codigo}'.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao adicionar o produto: {e}")
        return None
    finally:
        conn.close()

def listar_produtos():
    conn, cursor = conectar_bd()
    try:
        cursor.execute("SELECT id, codigo, nome, descricao, unidade_medida, preco_custo, preco_venda, estoque_atual, estoque_minimo FROM produtos ORDER BY nome ASC")
        produtos_raw = cursor.fetchall()
        produtos = [dict(produto_row) for produto_row in produtos_raw]
        print(f"DEBUG [estoque.listar_produtos]: Produtos buscados do BD: {produtos}") 
        return produtos
    except Exception as e:
        print(f"Ocorreu um erro ao listar os produtos: {e}")
        return []
    finally:
        conn.close()

def buscar_produto_por_codigo(codigo):
    conn, cursor = conectar_bd()
    try:
        cursor.execute("SELECT * FROM produtos WHERE codigo = ?", (codigo,))
        produto = cursor.fetchone()
        produtos_formatados = [dict(produto_row) for produto_row in produtos]
        return produtos_formatados
    except Exception as e:
        print(f"Ocorreu um erro ao buscar o produto por código: {e}")
        return None
    finally:
        conn.close()

def buscar_produto_por_id(produto_id):
    conn, cursor = conectar_bd()
    try:
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()
        return dict(produto) if produto else None
    except Exception as e:
        print(f"Ocorreu um erro ao buscar o produto por ID: {e}")
        return None
    finally:
        conn.close()

def atualizar_produto(produto_id, codigo, nome, descricao, unidade_medida, preco_custo, preco_venda, estoque_minimo):
    conn, cursor = conectar_bd()
    try:
        cursor.execute('''
        UPDATE produtos
        SET codigo = ?, nome = ?, descricao = ?, unidade_medida = ?,
            preco_custo = ?, preco_venda = ?, estoque_minimo = ?
        WHERE id = ?
        ''', (codigo, nome, descricao, unidade_medida, preco_custo, preco_venda, estoque_minimo, produto_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Produto ID {produto_id} atualizado com sucesso!")
            return True
        else:
            print(f"Nenhum produto encontrado com ID {produto_id} para atualizar.")
            return False
    except sqlite3.IntegrityError:
        print(f"Erro: Já existe outro produto com o código '{codigo}'.")
        return False
    except Exception as e:
        print(f"Ocorreu um erro ao atualizar o produto: {e}")
        return False
    finally:
        conn.close()

def remover_produto(produto_id):
    
    conn, cursor = conectar_bd()
    try:
        cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Produto ID {produto_id} removido com sucesso!")
            return True
        else:
            print(f"Nenhum produto encontrado com ID {produto_id} para remover.")
            return False
    except Exception as e:
        print(f"Ocorreu um erro ao remover o produto: {e}")
        return False
    finally:
        conn.close()

def atualizar_estoque(produto_id, quantidade_movimentada, tipo_movimento="saida"):
  
    conn, cursor = conectar_bd()
    try:
        produto_atual = buscar_produto_por_id(produto_id) # Reutiliza a função
        if not produto_atual:
            print(f"Produto com ID {produto_id} não encontrado para atualizar estoque.")
            return None

        estoque_atual = produto_atual['estoque_atual']

        if tipo_movimento == "saida":
            if estoque_atual < quantidade_movimentada:
                print(f"Erro: Estoque insuficiente para o produto ID {produto_id}. Estoque: {estoque_atual}, Saída: {quantidade_movimentada}")
                return None 
            novo_estoque = estoque_atual - quantidade_movimentada
        elif tipo_movimento == "entrada":
            novo_estoque = estoque_atual + quantidade_movimentada
        else:
            print("Tipo de movimento de estoque inválido.")
            return None

        cursor.execute("UPDATE produtos SET estoque_atual = ? WHERE id = ?", (novo_estoque, produto_id))
        conn.commit()

        print(f"Estoque do produto ID {produto_id} atualizado para {novo_estoque}.")

        if novo_estoque < produto_atual['estoque_minimo']:
            print(f"ALERTA: Produto '{produto_atual['nome']}' (ID: {produto_id}) está com estoque baixo ({novo_estoque} unidades). Mínimo: {produto_atual['estoque_minimo']}.")
        
        return novo_estoque
    except Exception as e:
        print(f"Erro ao atualizar estoque do produto ID {produto_id}: {e}")
        return None
    finally:
        conn.close()

def listar_produtos_para_selecao():
    conn, cursor = conectar_bd()
    try:
        cursor.execute("SELECT id, codigo, nome FROM produtos ORDER BY nome ASC")
        produtos = cursor.fetchall()
        return [{"id": produto["id"], "display_text": f"{produto['codigo']} - {produto['nome']}"} for produto in produtos]
    except Exception as e:
        print(f"Ocorreu um erro ao listar produtos para seleção: {e}")
        return []
    finally:
        conn.close()

def registrar_entrada_estoque(produto_id, quantidade, preco_custo_unitario=None, fornecedor=None, nota_fiscal=None):
    if quantidade <= 0:
        print("Erro: A quantidade de entrada deve ser positiva.")
        return False, "Quantidade deve ser positiva."

    conn, cursor = conectar_bd()
    try:
        conn.execute("BEGIN TRANSACTION")
        produto_atual = buscar_produto_por_id(produto_id) 
        if not produto_atual:
            return False, f"Produto com ID {produto_id} não encontrado."

        if preco_custo_unitario is None:
            preco_custo_compra = produto_atual['preco_custo']
        else:
            preco_custo_compra = preco_custo_unitario
            

        novo_estoque = atualizar_estoque(produto_id, quantidade, tipo_movimento="entrada")
        if novo_estoque is None: 
            conn.execute("ROLLBACK") 
            return False, "Falha ao atualizar o estoque do produto."

        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
        INSERT INTO compras_historico (produto_id, quantidade, preco_custo_unitario, data_compra, fornecedor, nota_fiscal)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (produto_id, quantidade, preco_custo_compra, data_atual, fornecedor, nota_fiscal))

        conn.commit() 
        print(f"Entrada de {quantidade} unidade(s) para o produto ID {produto_id} registrada com sucesso.")
        return True, "Entrada registrada com sucesso."
    except Exception as e:
        conn.execute("ROLLBACK") 
        return False, f"Erro ao registrar entrada: {e}"
    finally:
        conn.close()
    
def buscar_produto_por_id(produto_id, cursor_externo=None):
    conn_local = None
    cursor_usado = cursor_externo
    
    if cursor_usado is None:
        conn_local, cursor_usado = conectar_bd()
    
    produto_dict = None
    try:
        cursor_usado.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        produto_row = cursor_usado.fetchone()
        if produto_row:
            produto_dict = dict(produto_row)
    except Exception as e:
        print(f"Ocorreu um erro ao buscar o produto por ID ({produto_id}): {e}")
    finally:
        if conn_local: 
            conn_local.close()
    return produto_dict

def atualizar_estoque(produto_id, quantidade_movimentada, tipo_movimento="saida", cursor_externo=None):
    conn_local = None
    cursor_usado = cursor_externo

    if cursor_usado is None:
        conn_local, cursor_usado = conectar_bd()

    try:
        produto_atual_dict = buscar_produto_por_id(produto_id, cursor_externo=cursor_usado)
        if not produto_atual_dict:
            print(f"Produto com ID {produto_id} não encontrado para atualizar estoque (dentro de atualizar_estoque).")
            return None

        estoque_atual = produto_atual_dict['estoque_atual']

        if tipo_movimento == "saida":
            if estoque_atual < quantidade_movimentada:
                print(f"Erro (dupla checagem): Estoque insuficiente para o produto ID {produto_id}. Estoque: {estoque_atual}, Saída: {quantidade_movimentada}")
                return None
            novo_estoque = estoque_atual - quantidade_movimentada
        elif tipo_movimento == "entrada":
            novo_estoque = estoque_atual + quantidade_movimentada
        else:
            print("Tipo de movimento de estoque inválido.")
            return None

        cursor_usado.execute("UPDATE produtos SET estoque_atual = ? WHERE id = ?", (novo_estoque, produto_id))
        
        if conn_local: 
            conn_local.commit()

        if novo_estoque < produto_atual_dict['estoque_minimo']:
            print(f"ALERTA: Produto '{produto_atual_dict['nome']}' (ID: {produto_id}) está com estoque baixo ({novo_estoque} unidades). Mínimo: {produto_atual_dict['estoque_minimo']}.")
        
        return novo_estoque
    except Exception as e:
        print(f"Erro DENTRO de atualizar_estoque para o produto ID {produto_id}: {e}")
        return None 
    finally:
        if conn_local:  
            conn_local.close()

if __name__ == '__main__':
    

    print("\n--- Lista de Produtos ---")
    produtos_cadastrados = listar_produtos()
    if produtos_cadastrados:
        for produto in produtos_cadastrados:
            print(f"ID: {produto['id']}, Código: {produto['codigo']}, Nome: {produto['nome']}, Estoque: {produto['estoque_atual']}, Preço Venda: R${produto['preco_venda']:.2f}")
    else:
        print("Nenhum produto cadastrado.")


    print("\n--- Lista de Produtos Atualizada ---")
    produtos_cadastrados = listar_produtos()
    if produtos_cadastrados:
        for produto in produtos_cadastrados:
            print(f"ID: {produto['id']}, Código: {produto['codigo']}, Nome: {produto['nome']}, Estoque: {produto['estoque_atual']}")
    else:
        print("Nenhum produto cadastrado.")