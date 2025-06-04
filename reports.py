import sqlite3
from database import DATABASE_NAME

def conectar_bd():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

def calcular_total_vendas(data_inicio=None, data_fim=None):
    conn, cursor = conectar_bd()
    total = 0.0
    try:
        query = "SELECT SUM(valor_total) as total_vendas FROM faturamento"
        params = []
        if data_inicio and data_fim:
            query += " WHERE date(data) BETWEEN date(?) AND date(?)" 
            params.extend([data_inicio, data_fim])
        
        cursor.execute(query, params)
        resultado = cursor.fetchone()
        if resultado and resultado['total_vendas'] is not None:
            total = resultado['total_vendas']
    except Exception as e:
        print(f"Erro ao calcular total de vendas: {e}")
    finally:
        conn.close()
    return total

def calcular_total_compras(data_inicio=None, data_fim=None): 
    conn, cursor = conectar_bd()
    total = 0.0
    try:
        query = "SELECT SUM(quantidade * preco_custo_unitario) as total_compras FROM compras_historico"
        params = []
        if data_inicio and data_fim:
            query += " WHERE date(data_compra) BETWEEN date(?) AND date(?)"
            params.extend([data_inicio, data_fim])

        cursor.execute(query, params)
        resultado = cursor.fetchone()
        if resultado and resultado['total_compras'] is not None:
            total = resultado['total_compras']
    except Exception as e:
        print(f"Erro ao calcular total de compras: {e}")
    finally:
        conn.close()
    return total

def calcular_total_despesas(data_inicio=None, data_fim=None):
    conn, cursor = conectar_bd()
    total = 0.0
    try:
        query = "SELECT SUM(valor) as total_despesas FROM despesas"
        params = []
        if data_inicio and data_fim:
            query += " WHERE date(data) BETWEEN date(?) AND date(?)"
            params.extend([data_inicio, data_fim])

        cursor.execute(query, params)
        resultado = cursor.fetchone()
        if resultado and resultado['total_despesas'] is not None:
            total = resultado['total_despesas']
    except Exception as e:
        print(f"Erro ao calcular total de despesas: {e}")
    finally:
        conn.close()
    return total

def gerar_relatorio_financeiro_consolidado(data_inicio=None, data_fim=None):
    vendas = calcular_total_vendas(data_inicio, data_fim)
    compras = calcular_total_compras(data_inicio, data_fim)
    despesas = calcular_total_despesas(data_inicio, data_fim)
    
    saldo = vendas - compras - despesas
    
    return {
        "total_vendas": vendas,
        "total_compras_custo": compras,
        "total_despesas": despesas,
        "saldo_empresarial": saldo
    }

if __name__ == '__main__':
    relatorio = gerar_relatorio_financeiro_consolidado() 
    print("--- Relatório Financeiro Consolidado (Teste) ---")
    print(f"Total de Vendas: R$ {relatorio['total_vendas']:.2f}")
    print(f"Total Gasto em Compras: R$ {relatorio['total_compras_custo']:.2f}")
    print(f"Total de Despesas: R$ {relatorio['total_despesas']:.2f}")
    print(f"Saldo Empresarial: R$ {relatorio['saldo_empresarial']:.2f}")