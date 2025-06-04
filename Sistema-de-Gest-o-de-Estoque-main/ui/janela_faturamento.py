# ui/janela_faturamento.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import estoque 
import faturamento 

class JanelaFaturamento(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registrar Nova Venda")
        self.geometry("950x700") 
        self.transient(master)
        self.grab_set()

        self.estoque_db = estoque
        self.faturamento_db = faturamento
        
        self.produtos_disponiveis_para_venda = [] 
        self.itens_na_venda_atual = [] 

        self.metodos_pagamento = ["Dinheiro", "Cartão de Débito", "Cartão de Crédito", "PIX", "Boleto", "Outro"]

        self.criar_widgets_cabecalho_venda()
        self.criar_widgets_adicionar_item()
        self.criar_widgets_itens_venda() 
        self.criar_widgets_totalizadores_e_acoes()

        self.carregar_produtos_para_combobox()

    def criar_widgets_cabecalho_venda(self):
        frame_cabecalho = ttk.LabelFrame(self, text="Dados da Venda", padding="10")
        frame_cabecalho.pack(padx=10, pady=5, fill="x")

        ttk.Label(frame_cabecalho, text="Data:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_data_venda = ttk.Entry(frame_cabecalho, width=20)
        self.entry_data_venda.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.entry_data_venda.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        ttk.Label(frame_cabecalho, text="Cliente:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_cliente = ttk.Entry(frame_cabecalho, width=30)
        self.entry_cliente.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_cabecalho, text="Método Pag.:").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.combo_metodo_pagamento = ttk.Combobox(frame_cabecalho, values=self.metodos_pagamento, width=20, state="readonly")
        self.combo_metodo_pagamento.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        if self.metodos_pagamento:
            self.combo_metodo_pagamento.current(0)


    def carregar_produtos_para_combobox(self):
        produtos_raw = self.estoque_db.listar_produtos() 
        self.produtos_disponiveis_para_venda = []
        combo_values = []
        for p in produtos_raw:
            if p['estoque_atual'] > 0 : 
                display_text = f"{p['codigo']} - {p['nome']} (Est: {p['estoque_atual']})"
                self.produtos_disponiveis_para_venda.append({
                    'id': p['id'], 
                    'display_text': display_text, 
                    'preco_venda': p['preco_venda'],
                    'nome': p['nome'], 
                    'estoque_atual': p['estoque_atual']
                })
                combo_values.append(display_text)
        self.combo_produtos_venda['values'] = combo_values


    def criar_widgets_adicionar_item(self):
        frame_add_item = ttk.LabelFrame(self, text="Adicionar Produto à Venda", padding="10")
        frame_add_item.pack(padx=10, pady=5, fill="x")

        ttk.Label(frame_add_item, text="Produto:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.combo_produtos_venda = ttk.Combobox(frame_add_item, width=50, state="readonly")
        self.combo_produtos_venda.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.combo_produtos_venda.bind("<<ComboboxSelected>>", self.ao_selecionar_produto_para_venda)

        ttk.Label(frame_add_item, text="Preço Unit. R$:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.label_preco_venda_item = ttk.Label(frame_add_item, text="0.00", width=10, anchor="e")
        self.label_preco_venda_item.grid(row=0, column=3, padx=5, pady=2, sticky="w")
        
        ttk.Label(frame_add_item, text="Estoque Disp:").grid(row=0, column=4, padx=5, pady=2, sticky="w")
        self.label_estoque_disp_item = ttk.Label(frame_add_item, text="0", width=7, anchor="e")
        self.label_estoque_disp_item.grid(row=0, column=5, padx=5, pady=2, sticky="w")


        ttk.Label(frame_add_item, text="Quantidade:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.entry_quantidade_item = ttk.Entry(frame_add_item, width=10)
        self.entry_quantidade_item.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        self.entry_quantidade_item.insert(0, "1")

        self.btn_adicionar_item_venda = ttk.Button(frame_add_item, text="Adicionar Item", command=self.adicionar_item_a_venda_atual, state="disabled")
        self.btn_adicionar_item_venda.grid(row=1, column=2, padx=10, pady=5, columnspan=2)

    def ao_selecionar_produto_para_venda(self, event=None):
        selected_idx = self.combo_produtos_venda.current()
        if selected_idx >= 0:
            produto_selecionado = self.produtos_disponiveis_para_venda[selected_idx]
            self.label_preco_venda_item.config(text=f"{produto_selecionado['preco_venda']:.2f}")
            self.label_estoque_disp_item.config(text=f"{produto_selecionado['estoque_atual']}")
            self.entry_quantidade_item.delete(0, tk.END)
            self.entry_quantidade_item.insert(0, "1")
            self.btn_adicionar_item_venda.config(state="normal")
        else:
            self.label_preco_venda_item.config(text="0.00")
            self.label_estoque_disp_item.config(text="0")
            self.btn_adicionar_item_venda.config(state="disabled")
            
    def criar_widgets_itens_venda(self):
        frame_itens = ttk.LabelFrame(self, text="Itens da Venda", padding="10")
        frame_itens.pack(padx=10, pady=5, fill="both", expand=True)

        colunas = ("nome_produto", "quantidade", "preco_unitario", "subtotal")
        self.tree_itens_venda = ttk.Treeview(frame_itens, columns=colunas, show="headings", height=10)

        self.tree_itens_venda.heading("nome_produto", text="Produto")
        self.tree_itens_venda.heading("quantidade", text="Qtd.")
        self.tree_itens_venda.heading("preco_unitario", text="Preço Unit. R$")
        self.tree_itens_venda.heading("subtotal", text="Subtotal R$")

        self.tree_itens_venda.column("nome_produto", width=350)
        self.tree_itens_venda.column("quantidade", width=80, anchor="center")
        self.tree_itens_venda.column("preco_unitario", width=150, anchor="e")
        self.tree_itens_venda.column("subtotal", width=150, anchor="e")

        scrollbar = ttk.Scrollbar(frame_itens, orient="vertical", command=self.tree_itens_venda.yview)
        self.tree_itens_venda.configure(yscrollcommand=scrollbar.set)
        
        self.tree_itens_venda.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.btn_remover_item_venda = ttk.Button(self, text="Remover Item Selecionado da Venda", command=self.remover_item_da_venda_atual, state="disabled")
        self.btn_remover_item_venda.pack(pady=5)
        self.tree_itens_venda.bind("<<TreeviewSelect>>", lambda e: self.btn_remover_item_venda.config(state="normal" if self.tree_itens_venda.selection() else "disabled"))


    def criar_widgets_totalizadores_e_acoes(self):
        frame_total = ttk.Frame(self, padding="10")
        frame_total.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame_total, text="TOTAL DA VENDA: R$", font=("Arial", 14, "bold")).pack(side="left", padx=10)
        self.label_valor_total_venda = ttk.Label(frame_total, text="0.00", font=("Arial", 14, "bold"))
        self.label_valor_total_venda.pack(side="left")

        self.btn_finalizar_venda = ttk.Button(frame_total, text="Finalizar Venda", command=self.finalizar_venda, state="disabled", style="Accent.TButton") 
        self.btn_finalizar_venda.pack(side="right", padx=20)

        self.btn_cancelar_venda = ttk.Button(frame_total, text="Cancelar Venda", command=self.cancelar_venda)
        self.btn_cancelar_venda.pack(side="right", padx=5)
        
        style = ttk.Style(self)
        style.configure("Accent.TButton", font = ('calibri', 12, 'bold'), foreground='green')


    def adicionar_item_a_venda_atual(self):
        selected_idx_combo = self.combo_produtos_venda.current()
        if selected_idx_combo < 0:
            messagebox.showerror("Erro", "Selecione um produto.", parent=self)
            return

        try:
            quantidade = int(self.entry_quantidade_item.get())
            if quantidade <= 0:
                messagebox.showerror("Erro", "Quantidade deve ser positiva.", parent=self)
                return
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.", parent=self)
            return

        produto_info_combo = self.produtos_disponiveis_para_venda[selected_idx_combo]
        produto_id = produto_info_combo['id']
        nome_produto = produto_info_combo['nome']
        preco_venda_unitario = produto_info_combo['preco_venda']
        estoque_disponivel = produto_info_combo['estoque_atual']

        if quantidade > estoque_disponivel:
            messagebox.showwarning("Estoque Insuficiente", 
                                   f"Estoque disponível para '{nome_produto}': {estoque_disponivel} unidades.\nNão é possível adicionar {quantidade} unidades.",
                                   parent=self)
            return

        item_existente = None
        for item in self.itens_na_venda_atual:
            if item['produto_id'] == produto_id:
                item_existente = item
                break
        
        if item_existente:
            nova_quantidade_total = item_existente['quantidade'] + quantidade
            if nova_quantidade_total > estoque_disponivel:
                 messagebox.showwarning("Estoque Insuficiente", 
                                   f"Você já tem {item_existente['quantidade']} de '{nome_produto}' na venda.\nAdicionar mais {quantidade} excederia o estoque de {estoque_disponivel} unidades.",
                                   parent=self)
                 return
            item_existente['quantidade'] = nova_quantidade_total
            item_existente['subtotal'] = item_existente['quantidade'] * item_existente['preco_venda_unitario']
        else:
            subtotal = quantidade * preco_venda_unitario
            self.itens_na_venda_atual.append({
                'produto_id': produto_id,
                'nome_produto': nome_produto, 
                'quantidade': quantidade,
                'preco_venda_unitario': preco_venda_unitario,
                'subtotal': subtotal
            })
        
        self.atualizar_tabela_itens_venda()
        self.atualizar_total_venda()
        self.limpar_campos_item()


    def remover_item_da_venda_atual(self):
        selecionados = self.tree_itens_venda.selection()
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione um item da venda para remover.", parent=self)
            return

        indices_para_remover = []
        for iid_selecionado in selecionados:
            valores_linha = self.tree_itens_venda.item(iid_selecionado, "values")
            nome_produto_tree = valores_linha[0]
            subtotal_tree = float(valores_linha[3])

            for i, item_lista in enumerate(self.itens_na_venda_atual):
                if item_lista['nome_produto'] == nome_produto_tree and abs(item_lista['subtotal'] - subtotal_tree) < 0.001 : 
                    indices_para_remover.append(i)
                    break

        for index in sorted(indices_para_remover, reverse=True):
            del self.itens_na_venda_atual[index]

        self.atualizar_tabela_itens_venda()
        self.atualizar_total_venda()
        self.btn_remover_item_venda.config(state="disabled")


    def atualizar_tabela_itens_venda(self):
        # Limpar tabela
        for i in self.tree_itens_venda.get_children():
            self.tree_itens_venda.delete(i)
        
        # Preencher com itens atuais
        for item in self.itens_na_venda_atual:
            self.tree_itens_venda.insert("", "end", values=(
                item['nome_produto'],
                item['quantidade'],
                f"{item['preco_venda_unitario']:.2f}",
                f"{item['subtotal']:.2f}"
            ))
        
        self.btn_finalizar_venda.config(state="normal" if self.itens_na_venda_atual else "disabled")


    def atualizar_total_venda(self):
        total = sum(item['subtotal'] for item in self.itens_na_venda_atual)
        self.label_valor_total_venda.config(text=f"{total:.2f}")
        return total

    def limpar_campos_item(self):
        self.combo_produtos_venda.set('') 
        self.label_preco_venda_item.config(text="0.00")
        self.label_estoque_disp_item.config(text="0")
        self.entry_quantidade_item.delete(0, tk.END)
        self.entry_quantidade_item.insert(0, "1")
        self.btn_adicionar_item_venda.config(state="disabled")
        self.combo_produtos_venda.focus()


    def cancelar_venda(self):
        if self.itens_na_venda_atual:
            if not messagebox.askyesno("Cancelar Venda", "Tem certeza que deseja cancelar esta venda e limpar todos os itens?", parent=self):
                return
        self.itens_na_venda_atual = []
        self.atualizar_tabela_itens_venda()
        self.atualizar_total_venda()
        self.limpar_campos_item()
        self.entry_data_venda.delete(0, tk.END)
        self.entry_data_venda.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.entry_cliente.delete(0, tk.END)
        self.combo_metodo_pagamento.current(0)
        messagebox.showinfo("Cancelado", "Venda cancelada.", parent=self)


    def finalizar_venda(self):
        if not self.itens_na_venda_atual:
            messagebox.showerror("Erro", "Nenhum item na venda para finalizar.", parent=self)
            return

        data_venda = self.entry_data_venda.get().strip()
        cliente = self.entry_cliente.get().strip()
        metodo_pagamento = self.combo_metodo_pagamento.get()
        valor_total = self.atualizar_total_venda() 

        if not data_venda:
            messagebox.showerror("Erro", "Data da venda é obrigatória.", parent=self)
            return
        
        if not messagebox.askyesno("Finalizar Venda", f"Confirmar venda no valor total de R$ {valor_total:.2f}?", parent=self):
            return

        itens_para_registrar = []
        for item_ui in self.itens_na_venda_atual:
            itens_para_registrar.append({
                'produto_id': item_ui['produto_id'],
                'quantidade': item_ui['quantidade'],
                'preco_venda_unitario': item_ui['preco_venda_unitario'],
                'subtotal': item_ui['subtotal']
            })
        
        sucesso, resultado = self.faturamento_db.registrar_venda(
            data_venda, itens_para_registrar, valor_total, 
            cliente if cliente else None, 
            metodo_pagamento
        )

        if sucesso:
            faturamento_id = resultado
            messagebox.showinfo("Sucesso", f"Venda ID {faturamento_id} registrada com sucesso!", parent=self)
            
            if hasattr(self.master, 'janela_produtos_ativa') and \
               self.master.janela_produtos_ativa and \
               self.master.janela_produtos_ativa.winfo_exists():
                self.master.janela_produtos_ativa.carregar_produtos_na_tabela()
            
            self.carregar_produtos_para_combobox()

            self.itens_na_venda_atual = []
            self.atualizar_tabela_itens_venda()
            self.atualizar_total_venda()
            self.limpar_campos_item()
            self.entry_data_venda.delete(0, tk.END)
            self.entry_data_venda.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.entry_cliente.delete(0, tk.END)
            self.combo_metodo_pagamento.current(0)

        else: 
            messagebox.showerror("Falha ao Registrar Venda", resultado, parent=self)