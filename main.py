import tkinter as tk
from tkinter import ttk
from tkinter import messagebox 
import database
from ui.janela_produtos import JanelaProdutos 
from ui.janela_compra_estoque import JanelaCompraEstoque 
from ui.janela_despesas import JanelaDespesas 
from ui.janela_faturamento import JanelaFaturamento
from ui.janela_relatorio_financeiro import JanelaRelatorioFinanceiro 

class AppGestao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão Financeira e de Estoque")
        self.geometry("800x600")
        database.criar_tabelas() 
        style = ttk.Style(self) 
        style.configure("Accent.TButton", font = ('calibri', 10, 'bold'), foreground='black', background='green')
        self.criar_widgets_principais()

    def criar_widgets_principais(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Sair", command=self.quit)

        menu_cadastros = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)
        menu_cadastros.add_command(label="Produtos", command=self.abrir_janela_produtos)
        
        menu_movimentacoes = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Movimentações", menu=menu_movimentacoes)
        menu_movimentacoes.add_command(label="Registrar Venda (Faturamento)", command=self.abrir_janela_faturamento)
        menu_movimentacoes.add_command(label="Registrar Compra (Entrada Estoque)", command=self.abrir_janela_compra_estoque)
        menu_movimentacoes.add_command(label="Registrar Despesa", command=self.abrir_janela_despesas)
        
        menu_relatorios = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Relatórios", menu=menu_relatorios)
        menu_relatorios.add_command(label="Financeiro Consolidado", command=self.abrir_janela_relatorio_financeiro)

        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        label_inicial = ttk.Label(self.main_frame, text="Bem-vindo ao Sistema de Gestão!", font=("Arial", 16))
        label_inicial.pack(pady=20)

        frame_botoes_rapidos = ttk.Frame(self.main_frame)
        frame_botoes_rapidos.pack(pady=20)

        btn_produtos_rapido = ttk.Button(frame_botoes_rapidos, text="Gerenciar Produtos", command=self.abrir_janela_produtos, width=30)
        btn_produtos_rapido.grid(row=0, column=0, padx=10, pady=5)

        btn_venda_rapido = ttk.Button(frame_botoes_rapidos, text="Registrar Nova Venda", command=self.abrir_janela_faturamento, width=30)
        btn_venda_rapido.grid(row=0, column=1, padx=10, pady=5)
        
        btn_despesa_rapido = ttk.Button(frame_botoes_rapidos, text="Registrar Nova Despesa", command=self.abrir_janela_despesas, width=30)
        btn_despesa_rapido.grid(row=1, column=0, padx=10, pady=5)

        btn_compra_rapido = ttk.Button(frame_botoes_rapidos, text="Registrar Compra/Entrada", command=self.abrir_janela_compra_estoque, width=30)
        btn_compra_rapido.grid(row=1, column=1, padx=10, pady=5)

        btn_relatorio_rapido = ttk.Button(frame_botoes_rapidos, text="Relatório Financeiro", command=self.abrir_janela_relatorio_financeiro, width=30, style="Accent.TButton")
        btn_relatorio_rapido.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def abrir_janela_produtos(self):
        if not hasattr(self, 'janela_produtos_ativa') or not self.janela_produtos_ativa.winfo_exists():
            self.janela_produtos_ativa = JanelaProdutos(self)
            self.janela_produtos_ativa.focus_set() 
        else:
            self.janela_produtos_ativa.focus_set()

    def abrir_janela_compra_estoque(self):
        if not hasattr(self, 'janela_compra_ativa') or \
           not self.janela_compra_ativa.winfo_exists():
            self.janela_compra_ativa = JanelaCompraEstoque(self)
            self.janela_compra_ativa.focus_set()
        else:
            self.janela_compra_ativa.focus_set()

    def abrir_janela_despesas(self):
        if not hasattr(self, 'janela_despesas_ativa') or \
           not self.janela_despesas_ativa.winfo_exists():
            self.janela_despesas_ativa = JanelaDespesas(self)
            self.janela_despesas_ativa.focus_set()
        else:
            self.janela_despesas_ativa.focus_set()

    def abrir_janela_faturamento(self):
        if not hasattr(self, 'janela_faturamento_ativa') or \
           not self.janela_faturamento_ativa.winfo_exists():
            self.janela_faturamento_ativa = JanelaFaturamento(self)
            self.janela_faturamento_ativa.focus_set()
        else:
            self.janela_faturamento_ativa.focus_set()

    def abrir_janela_relatorio_financeiro(self):
        if not hasattr(self, 'janela_relatorio_ativa') or \
           not self.janela_relatorio_ativa.winfo_exists():
            self.janela_relatorio_ativa = JanelaRelatorioFinanceiro(self)
            self.janela_relatorio_ativa.focus_set()
        else:
            self.janela_relatorio_ativa.focus_set()

if __name__ == "__main__":
    app = AppGestao()
    app.mainloop()