import tkinter as tk
from tkinter import ttk, messagebox
import estoque 

class JanelaProdutos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gerenciar Produtos")
        self.geometry("900x600") 
        self.transient(master) 
        self.grab_set() 
        
        self.estoque_db = estoque
        self.produtos_disponiveis = [] 

        self.criar_widgets_formulario()
        self.criar_widgets_tabela()
        
        print("DEBUG [JanelaProdutos.__init__]: Chamando carregar_produtos_na_tabela()")
        self.carregar_produtos_na_tabela() 

    def criar_widgets_formulario(self):
        frame_formulario = ttk.LabelFrame(self, text="Cadastrar/Editar Produto", padding="10")
        frame_formulario.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame_formulario, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_codigo = ttk.Entry(frame_formulario, width=15)
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Nome:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_nome = ttk.Entry(frame_formulario, width=40)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5, columnspan=3, sticky="ew")

        ttk.Label(frame_formulario, text="Descrição:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_descricao = ttk.Entry(frame_formulario, width=40)
        self.entry_descricao.grid(row=2, column=1, padx=5, pady=5, columnspan=3, sticky="ew")

        ttk.Label(frame_formulario, text="Unidade:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_unidade = ttk.Entry(frame_formulario, width=10)
        self.entry_unidade.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.entry_unidade.insert(0, "UN")

        ttk.Label(frame_formulario, text="Preço Custo R$:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_preco_custo = ttk.Entry(frame_formulario, width=15)
        self.entry_preco_custo.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_formulario, text="Preço Venda R$:").grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.entry_preco_venda = ttk.Entry(frame_formulario, width=15)
        self.entry_preco_venda.grid(row=3, column=3, padx=5, pady=5, sticky="ew")
        
        ttk.Label(frame_formulario, text="Estoque Inicial:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_estoque_inicial = ttk.Entry(frame_formulario, width=15)
        self.entry_estoque_inicial.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        self.entry_estoque_inicial.insert(0, "0")

        ttk.Label(frame_formulario, text="Estoque Mínimo:").grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.entry_estoque_minimo = ttk.Entry(frame_formulario, width=15)
        self.entry_estoque_minimo.grid(row=4, column=3, padx=5, pady=5, sticky="ew")
        self.entry_estoque_minimo.insert(0, "0")

        frame_botoes_form = ttk.Frame(frame_formulario)
        frame_botoes_form.grid(row=5, column=0, columnspan=4, pady=10)

        self.btn_salvar = ttk.Button(frame_botoes_form, text="Salvar Novo", command=self.salvar_novo_produto)
        self.btn_salvar.pack(side="left", padx=5)
        
        self.btn_atualizar_selecionado = ttk.Button(frame_botoes_form, text="Atualizar Selecionado", command=self.atualizar_produto_selecionado, state="disabled")
        self.btn_atualizar_selecionado.pack(side="left", padx=5)

        self.btn_limpar = ttk.Button(frame_botoes_form, text="Limpar Campos", command=self.limpar_campos_formulario)
        self.btn_limpar.pack(side="left", padx=5)

        self.produto_id_selecionado = None

    def criar_widgets_tabela(self):
        frame_tabela = ttk.LabelFrame(self, text="Produtos Cadastrados", padding="10")
        frame_tabela.pack(padx=10, pady=10, fill="both", expand=True)

        colunas = ("id", "codigo", "nome", "unidade", "preco_venda", "estoque_atual", "estoque_minimo")
        self.tree_produtos = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

        self.tree_produtos.heading("id", text="ID")
        self.tree_produtos.heading("codigo", text="Código")
        self.tree_produtos.heading("nome", text="Nome")
        self.tree_produtos.heading("unidade", text="Un.")
        self.tree_produtos.heading("preco_venda", text="P. Venda R$")
        self.tree_produtos.heading("estoque_atual", text="Est. Atual")
        self.tree_produtos.heading("estoque_minimo", text="Est. Mínimo")

        self.tree_produtos.column("id", width=40, anchor="center")
        self.tree_produtos.column("codigo", width=80)
        self.tree_produtos.column("nome", width=250)
        self.tree_produtos.column("unidade", width=50, anchor="center")
        self.tree_produtos.column("preco_venda", width=100, anchor="e")
        self.tree_produtos.column("estoque_atual", width=80, anchor="center")
        self.tree_produtos.column("estoque_minimo", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree_produtos.yview)
        self.tree_produtos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_produtos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree_produtos.bind("<<TreeviewSelect>>", self.ao_selecionar_produto_na_tabela)

        frame_botoes_tabela = ttk.Frame(self) 
        frame_botoes_tabela.pack(pady=5)

        self.btn_remover = ttk.Button(frame_botoes_tabela, text="Remover Selecionado", command=self.remover_produto_selecionado, state="disabled")
        self.btn_remover.pack(side="left", padx=5)

        self.btn_editar = ttk.Button(frame_botoes_tabela, text="Editar Selecionado", command=self.carregar_produto_para_edicao, state="disabled")
        self.btn_editar.pack(side="left", padx=5)

    def carregar_produtos_na_tabela(self):
        print("DEBUG [carregar_produtos_na_tabela]: Iniciando carregamento de produtos.")
        for i in self.tree_produtos.get_children():
            self.tree_produtos.delete(i)
        
        produtos = self.estoque_db.listar_produtos()
        self.produtos_disponiveis = produtos 
        print(f"DEBUG [carregar_produtos_na_tabela]: Produtos recebidos de estoque_db.listar_produtos(): {produtos}") 
        
        if not produtos:
            print("DEBUG [carregar_produtos_na_tabela]: Nenhum produto recebido para listar.")

        for produto in produtos:
            preco_venda_formatado = f"{produto['preco_venda']:.2f}"
            valores_para_inserir = (
                produto['id'],
                produto['codigo'],
                produto['nome'],
                produto['unidade_medida'],
                preco_venda_formatado,
                produto['estoque_atual'],
                produto['estoque_minimo']
            )
            print(f"DEBUG [carregar_produtos_na_tabela]: Inserindo na Treeview: {valores_para_inserir}")
            self.tree_produtos.insert("", "end", values=valores_para_inserir)
            
        self.desabilitar_botoes_edicao_remocao() 
        print("DEBUG [carregar_produtos_na_tabela]: Carregamento finalizado.")

    def validar_campos(self, eh_novo_produto=True):
        codigo = self.entry_codigo.get().strip()
        nome = self.entry_nome.get().strip()
        try:
            preco_custo_str = self.entry_preco_custo.get().strip().replace(",",".")
            preco_venda_str = self.entry_preco_venda.get().strip().replace(",",".")
            estoque_inicial_str = self.entry_estoque_inicial.get().strip()
            estoque_minimo_str = self.entry_estoque_minimo.get().strip()

            preco_custo = float(preco_custo_str) if preco_custo_str else 0.0
            preco_venda = float(preco_venda_str)
            estoque_inicial = int(estoque_inicial_str) if eh_novo_produto and estoque_inicial_str else 0
            estoque_minimo = int(estoque_minimo_str) if estoque_minimo_str else 0

        except ValueError:
            messagebox.showerror("Erro de Validação", "Preço(s), Estoque Inicial ou Estoque Mínimo devem ser números válidos.", parent=self)
            return None

        if not codigo or not nome:
            messagebox.showerror("Erro de Validação", "Código e Nome são obrigatórios.", parent=self)
            return None
        if preco_venda <= 0:
            messagebox.showerror("Erro de Validação", "Preço de Venda deve ser maior que zero.", parent=self)
            return None
        if preco_custo < 0 or estoque_inicial < 0 or estoque_minimo < 0 :
            messagebox.showerror("Erro de Validação", "Valores numéricos não podem ser negativos.", parent=self)
            return None

        return {
            "codigo": codigo, "nome": nome, "descricao": self.entry_descricao.get().strip(),
            "unidade_medida": self.entry_unidade.get().strip() or "UN",
            "preco_custo": preco_custo, "preco_venda": preco_venda,
            "estoque_inicial": estoque_inicial, "estoque_minimo": estoque_minimo
        }

    def salvar_novo_produto(self):
        dados_produto = self.validar_campos(eh_novo_produto=True)
        if not dados_produto:
            return

        resultado = self.estoque_db.adicionar_produto(
            codigo=dados_produto['codigo'], nome=dados_produto['nome'], descricao=dados_produto['descricao'],
            unidade_medida=dados_produto['unidade_medida'], preco_custo=dados_produto['preco_custo'],
            preco_venda=dados_produto['preco_venda'], estoque_inicial=dados_produto['estoque_inicial'],
            estoque_minimo=dados_produto['estoque_minimo']
        )

        if resultado: 
            messagebox.showinfo("Sucesso", f"Produto '{dados_produto['nome']}' adicionado com sucesso!", parent=self)
            self.limpar_campos_formulario()
            self.carregar_produtos_na_tabela()
        else:
            messagebox.showerror("Erro", "Não foi possível adicionar o produto. Verifique o console para detalhes.", parent=self)

    def limpar_campos_formulario(self):
        self.entry_codigo.delete(0, "end")
        self.entry_nome.delete(0, "end")
        self.entry_descricao.delete(0, "end")
        self.entry_unidade.delete(0, "end")
        self.entry_unidade.insert(0, "UN")
        self.entry_preco_custo.delete(0, "end")
        self.entry_preco_venda.delete(0, "end")
        self.entry_estoque_inicial.delete(0, "end")
        self.entry_estoque_inicial.insert(0, "0")
        self.entry_estoque_minimo.delete(0, "end")
        self.entry_estoque_minimo.insert(0, "0")
        
        self.produto_id_selecionado = None 
        self.btn_salvar.config(text="Salvar Novo", command=self.salvar_novo_produto) 
        self.entry_codigo.config(state="normal") 
        self.entry_estoque_inicial.config(state="normal") 

        if hasattr(self, 'btn_atualizar_selecionado'):
            self.btn_atualizar_selecionado.config(state="disabled")
        if hasattr(self, 'btn_editar'):
            self.btn_editar.config(state="disabled")
        if hasattr(self, 'btn_remover'):
            self.btn_remover.config(state="disabled")
        
        if hasattr(self, 'tree_produtos') and self.tree_produtos.winfo_exists():
            if self.tree_produtos.selection():
                 self.tree_produtos.selection_remove(self.tree_produtos.selection())

    def ao_selecionar_produto_na_tabela(self, event=None):
        selecionado = self.tree_produtos.focus() 
        if selecionado:
            self.btn_editar.config(state="normal")
            self.btn_remover.config(state="normal")
        else:
            self.desabilitar_botoes_edicao_remocao()

    def desabilitar_botoes_edicao_remocao(self):
        if hasattr(self, 'btn_editar'):
            self.btn_editar.config(state="disabled")
        if hasattr(self, 'btn_remover'):
            self.btn_remover.config(state="disabled")
        if hasattr(self, 'btn_atualizar_selecionado'):
            self.btn_atualizar_selecionado.config(state="disabled")
    
    def atualizar_produto_selecionado(self):
        if self.produto_id_selecionado is None:
            messagebox.showerror("Erro", "Nenhum produto selecionado para atualizar.", parent=self)
            return

        dados_produto = self.validar_campos(eh_novo_produto=False)
        if not dados_produto:
            return

        resultado = self.estoque_db.atualizar_produto(
            produto_id=self.produto_id_selecionado,
            codigo=dados_produto['codigo'], 
            nome=dados_produto['nome'], 
            descricao=dados_produto['descricao'],
            unidade_medida=dados_produto['unidade_medida'], 
            preco_custo=dados_produto['preco_custo'],
            preco_venda=dados_produto['preco_venda'], 
            estoque_minimo=dados_produto['estoque_minimo']
        )

        if resultado: 
            messagebox.showinfo("Sucesso", f"Produto '{dados_produto['nome']}' atualizado com sucesso!", parent=self)
            self.limpar_campos_formulario()
            self.carregar_produtos_na_tabela()
        else:
            messagebox.showerror("Erro", "Não foi possível atualizar o produto. Verifique o console para detalhes.", parent=self)

    def carregar_produto_para_edicao(self):
        item_selecionado = self.tree_produtos.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto na tabela para editar.", parent=self)
            return
        
        valores_linha = self.tree_produtos.item(item_selecionado[0], "values")
        produto_id = int(valores_linha[0])

        produto = self.estoque_db.buscar_produto_por_id(produto_id)

        if produto:
            self.limpar_campos_formulario() 
            self.produto_id_selecionado = produto_id

            self.entry_codigo.insert(0, produto['codigo'])
            self.entry_nome.insert(0, produto['nome'])
            self.entry_descricao.insert(0, produto['descricao'] if produto['descricao'] else "")
            self.entry_unidade.delete(0, "end")
            self.entry_unidade.insert(0, produto['unidade_medida'])
            self.entry_preco_custo.insert(0, f"{produto['preco_custo']:.2f}" if produto['preco_custo'] is not None else "")
            self.entry_preco_venda.insert(0, f"{produto['preco_venda']:.2f}")
            
            self.entry_estoque_inicial.delete(0, tk.END)
            self.entry_estoque_inicial.insert(0, str(produto['estoque_atual']))
            self.entry_estoque_inicial.config(state="disabled") 

            self.entry_estoque_minimo.delete(0, tk.END)
            self.entry_estoque_minimo.insert(0, str(produto['estoque_minimo']))

            self.btn_salvar.config(text="Salvar Novo", state="normal", command=self.salvar_novo_produto)
            self.btn_atualizar_selecionado.config(state="normal") 
        else:
            messagebox.showerror("Erro", f"Produto com ID {produto_id} não encontrado no banco de dados.", parent=self)

    def remover_produto_selecionado(self):
        item_selecionado = self.tree_produtos.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto na tabela para remover.", parent=self)
            return
        
        valores_linha = self.tree_produtos.item(item_selecionado[0], "values")
        produto_id = int(valores_linha[0])
        nome_produto = valores_linha[2]

        confirmar = messagebox.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover o produto '{nome_produto}' (ID: {produto_id})?", parent=self)

        if confirmar:
            resultado = self.estoque_db.remover_produto(produto_id)
            if resultado:
                messagebox.showinfo("Sucesso", f"Produto '{nome_produto}' removido com sucesso!", parent=self)
                self.carregar_produtos_na_tabela()
                self.limpar_campos_formulario() 
            else:
                messagebox.showerror("Erro", f"Não foi possível remover o produto '{nome_produto}'. Pode estar associado a vendas ou outras movimentações.", parent=self)
    
    def listar_produtos_para_selecao(self):
        produtos = self.estoque_db.listar_produtos()
        produtos_disponiveis = []
        for produto in produtos:
            display_text = f"{produto['codigo']} - {produto['nome']}"
            produtos_disponiveis.append({
                'id': produto['id'],
                'display_text': display_text,
                'codigo': produto['codigo'],
                'nome': produto['nome']
            })
        return produtos_disponiveis

    def fechar_janela(self):
        self.destroy()