# ui/janela_despesas.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import despesas 


class JanelaDespesas(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registrar Nova Despesa")
        self.geometry("500x350") 
        self.transient(master)
        self.grab_set()

        self.despesas_db = despesas
        self.categorias_sugeridas = [
            "Alimentação", "Transporte", "Aluguel", "Salários", "Impostos",
            "Marketing", "Fornecedores", "Material de Escritório", "Manutenção",
            "Comunicações (Telefone/Internet)", "Outras"
        ]

        self.criar_widgets()

    def criar_widgets(self):
        frame_principal = ttk.Frame(self, padding="10")
        frame_principal.pack(expand=True, fill="both")

        ttk.Label(frame_principal, text="Data:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_data = ttk.Entry(frame_principal, width=15)
        self.entry_data.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d")) # Data atual como padrão
       

        ttk.Label(frame_principal, text="Descrição:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_descricao = ttk.Entry(frame_principal, width=40)
        self.entry_descricao.grid(row=1, column=1, padx=5, pady=5, sticky="ew", columnspan=2)

        ttk.Label(frame_principal, text="Categoria:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.combo_categoria = ttk.Combobox(frame_principal, width=37, values=self.categorias_sugeridas)
        self.combo_categoria.grid(row=2, column=1, padx=5, pady=5, sticky="ew", columnspan=2)
        if self.categorias_sugeridas:
            self.combo_categoria.current(len(self.categorias_sugeridas)-1) # Seleciona "Outras" ou a última

        ttk.Label(frame_principal, text="Valor (R$):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_valor = ttk.Entry(frame_principal, width=15)
        self.entry_valor.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Botões
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.grid(row=4, column=0, columnspan=3, pady=20)

        btn_salvar = ttk.Button(frame_botoes, text="Salvar Despesa", command=self.salvar_despesa)
        btn_salvar.pack(side="left", padx=10)

        btn_limpar = ttk.Button(frame_botoes, text="Limpar Campos", command=self.limpar_campos)
        btn_limpar.pack(side="left", padx=10)
        

    def limpar_campos(self):
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_descricao.delete(0, tk.END)
        self.combo_categoria.set('') # Limpa a seleção/texto
        if self.categorias_sugeridas:
            self.combo_categoria.current(len(self.categorias_sugeridas)-1)
        self.entry_valor.delete(0, tk.END)
        self.entry_descricao.focus()

    def salvar_despesa(self):
        data = self.entry_data.get().strip()
        descricao = self.entry_descricao.get().strip()
        categoria = self.combo_categoria.get().strip() # Pega o texto, mesmo que não seja da lista
        valor_str = self.entry_valor.get().strip().replace(",",".")

        if not data or not descricao or not valor_str:
            messagebox.showerror("Erro de Validação", "Data, Descrição e Valor são obrigatórios.", parent=self)
            return
        
        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro de Validação", "Formato da Data inválido. Use AAAA-MM-DD.", parent=self)
            return

        try:
            valor = float(valor_str)
            if valor <= 0:
                messagebox.showerror("Erro de Validação", "O Valor da despesa deve ser positivo.", parent=self)
                return
        except ValueError:
            messagebox.showerror("Erro de Validação", "Valor da despesa deve ser um número.", parent=self)
            return

        sucesso, mensagem = self.despesas_db.adicionar_despesa(data, descricao, categoria, valor)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem, parent=self)
            self.limpar_campos()
        else:
            messagebox.showerror("Erro ao Salvar", mensagem, parent=self)