import tkinter as tk
from tkinter import ttk, messagebox
import estoque 

class JanelaCompraEstoque(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Registrar Compra/Entrada de Estoque")
        self.geometry("550x400")
        self.transient(master)
        self.grab_set()

        self.estoque_db = estoque
        self.produtos_disponiveis = [] 

        self.criar_widgets()
        self.carregar_produtos()

    def criar_widgets(self):
        frame_principal = ttk.Frame(self, padding="10")
        frame_principal.pack(expand=True, fill="both")

        ttk.Label(frame_principal, text="Produto:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_produtos = ttk.Combobox(frame_principal, state="readonly", width=40)
        self.combo_produtos.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.combo_produtos.bind("<<ComboboxSelected>>", self.ao_selecionar_produto)

        ttk.Label(frame_principal, text="Preço de Custo Atual (R$):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.label_preco_custo_atual = ttk.Label(frame_principal, text="N/A")
        self.label_preco_custo_atual.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_principal, text="Quantidade Comprada:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_quantidade = ttk.Entry(frame_principal, width=15)
        self.entry_quantidade.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_principal, text="Novo Preço Custo Unit. (R$):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_novo_preco_custo = ttk.Entry(frame_principal, width=15)
        self.entry_novo_preco_custo.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(frame_principal, text="(Opcional, se diferente do atual)").grid(row=3, column=2, padx=5, pady=2, sticky="w")


        ttk.Label(frame_principal, text="Fornecedor:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_fornecedor = ttk.Entry(frame_principal, width=43)
        self.entry_fornecedor.grid(row=4, column=1, padx=5, pady=5, columnspan=2, sticky="ew")

        ttk.Label(frame_principal, text="Nota Fiscal:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_nota_fiscal = ttk.Entry(frame_principal, width=43)
        self.entry_nota_fiscal.grid(row=5, column=1, padx=5, pady=5, columnspan=2, sticky="ew")


        btn_registrar = ttk.Button(frame_principal, text="Registrar Entrada", command=self.registrar_entrada)
        btn_registrar.grid(row=6, column=0, columnspan=3, pady=20)

    def carregar_produtos(self):
        self.produtos_disponiveis = self.estoque_db.listar_produtos_para_selecao()
        if self.produtos_disponiveis:
            self.combo_produtos['values'] = [p['display_text'] for p in self.produtos_disponiveis]
        else:
            self.combo_produtos['values'] = []
            messagebox.showwarning("Aviso", "Nenhum produto cadastrado. Cadastre produtos antes de registrar entradas.", parent=self)
            self.destroy() 

    def ao_selecionar_produto(self, event=None):
        selecionado_idx = self.combo_produtos.current()
        if selecionado_idx >= 0:
            produto_id_selecionado = self.produtos_disponiveis[selecionado_idx]['id']
            produto_info = self.estoque_db.buscar_produto_por_id(produto_id_selecionado)
            if produto_info and produto_info.get('preco_custo') is not None:
                self.label_preco_custo_atual.config(text=f"{produto_info['preco_custo']:.2f}")
                self.entry_novo_preco_custo.delete(0, tk.END) 
                self.entry_novo_preco_custo.insert(0, f"{produto_info['preco_custo']:.2f}") 
            else:
                self.label_preco_custo_atual.config(text="N/A")
                self.entry_novo_preco_custo.delete(0, tk.END)


    def registrar_entrada(self):
        try:
            selecionado_idx = self.combo_produtos.current()
            if selecionado_idx < 0:
                messagebox.showerror("Erro", "Selecione um produto.", parent=self)
                return

            produto_id = self.produtos_disponiveis[selecionado_idx]['id']
            
            quantidade_str = self.entry_quantidade.get().strip()
            if not quantidade_str:
                 messagebox.showerror("Erro de Validação", "A Quantidade Comprada é obrigatória.", parent=self)
                 return
            quantidade = int(quantidade_str)
            if quantidade <= 0:
                messagebox.showerror("Erro", "A quantidade deve ser um número positivo.", parent=self)
                return

            novo_preco_custo_str = self.entry_novo_preco_custo.get().strip().replace(",",".")
            novo_preco_custo = None
            if novo_preco_custo_str: 
                novo_preco_custo = float(novo_preco_custo_str)
                if novo_preco_custo < 0:
                    messagebox.showerror("Erro", "O novo preço de custo não pode ser negativo.", parent=self)
                    return
            
            fornecedor = self.entry_fornecedor.get().strip()
            nota_fiscal = self.entry_nota_fiscal.get().strip()

        except ValueError:
            messagebox.showerror("Erro", "Quantidade ou Novo Preço de Custo inválidos. Verifique os números.", parent=self)
            return
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}", parent=self)
            return

        sucesso, mensagem = self.estoque_db.registrar_entrada_estoque(
            produto_id,
            quantidade,
            preco_custo_unitario=novo_preco_custo,
            fornecedor=fornecedor if fornecedor else None,
            nota_fiscal=nota_fiscal if nota_fiscal else None
        )

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem, parent=self)
            if hasattr(self.master, 'janela_produtos_ativa') and \
               self.master.janela_produtos_ativa and \
               self.master.janela_produtos_ativa.winfo_exists():
                self.master.janela_produtos_ativa.carregar_produtos_na_tabela()
            self.destroy() 
        else:
            messagebox.showerror("Erro", mensagem, parent=self)