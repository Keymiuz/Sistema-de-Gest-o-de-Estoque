import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date 
import reports 
import os

try:
    from tkcalendar import DateEntry
    TKCALENDAR_AVAILABLE = True
except ImportError:
    TKCALENDAR_AVAILABLE = False

class JanelaRelatorioFinanceiro(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Relatório Financeiro Consolidado")
        self.geometry("650x500")  
        self.transient(master)
        self.grab_set()

        self.reports_db = reports
        self.data_inicio = None
        self.data_fim = None

        self.criar_widgets_filtros()
        self.criar_widgets_resultados()
        self.btn_gerar.focus()

    def criar_widgets_filtros(self):
        frame_filtros = ttk.LabelFrame(self, text="Filtrar por Período (Opcional)", padding="10")
        frame_filtros.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame_filtros, text="Data Início:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        if TKCALENDAR_AVAILABLE:
            self.date_inicio = DateEntry(frame_filtros, width=12, date_pattern='yyyy-mm-dd',
                                     borderwidth=2, state="readonly") 
        else:
            self.date_inicio = ttk.Entry(frame_filtros, width=15)
            self.date_inicio.insert(0, "AAAA-MM-DD")
        self.date_inicio.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_filtros, text="Data Fim:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        if TKCALENDAR_AVAILABLE:
            self.date_fim = DateEntry(frame_filtros, width=12, date_pattern='yyyy-mm-dd',
                                  borderwidth=2, state="readonly")
        else:
            self.date_fim = ttk.Entry(frame_filtros, width=15)
            self.date_fim.insert(0, "AAAA-MM-DD")
        self.date_fim.grid(row=0, column=3, padx=5, pady=5)

        self.var_usar_filtro = tk.BooleanVar(value=False)
        chk_usar_filtro = ttk.Checkbutton(frame_filtros, text="Usar filtro de data", variable=self.var_usar_filtro, command=self.toggle_date_entries)
        chk_usar_filtro.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.toggle_date_entries()

        frame_botoes = ttk.Frame(frame_filtros)
        frame_botoes.grid(row=0, column=4, rowspan=2, padx=10, pady=5, sticky="nsew")

        self.btn_gerar = ttk.Button(frame_botoes, text="Gerar Relatório", command=self.gerar_e_exibir_relatorio, style="Accent.TButton")
        self.btn_gerar.pack(fill="x", pady=2)
        
        self.btn_exportar = ttk.Button(frame_botoes, text="Exportar para Excel", command=self.exportar_para_excel, style="Accent.TButton")
        self.btn_exportar.pack(fill="x", pady=2)
        self.btn_exportar.state(['disabled'])  

    def toggle_date_entries(self):
        estado = tk.NORMAL if self.var_usar_filtro.get() else tk.DISABLED
        if TKCALENDAR_AVAILABLE:
            self.date_inicio.config(state=estado if estado == tk.NORMAL else "readonly")
            self.date_fim.config(state=estado if estado == tk.NORMAL else "readonly")
        else:
            self.date_inicio.config(state=estado)
            self.date_fim.config(state=estado)

    def criar_widgets_resultados(self):
        frame_resultados = ttk.LabelFrame(self, text="Resultados", padding="15")
        frame_resultados.pack(padx=10, pady=10, fill="both", expand=True)

        label_font = ("Arial", 12)
        value_font = ("Arial", 12, "bold")

        ttk.Label(frame_resultados, text="Total de Vendas (Receita):", font=label_font).grid(row=0, column=0, sticky="w", pady=8)
        self.lbl_total_vendas = ttk.Label(frame_resultados, text="R$ 0.00", font=value_font, foreground="green")
        self.lbl_total_vendas.grid(row=0, column=1, sticky="e", pady=8, padx=10)

        ttk.Label(frame_resultados, text="Total Gasto em Compras:", font=label_font).grid(row=1, column=0, sticky="w", pady=8)
        self.lbl_total_compras = ttk.Label(frame_resultados, text="R$ 0.00", font=value_font, foreground="orange")
        self.lbl_total_compras.grid(row=1, column=1, sticky="e", pady=8, padx=10)

        ttk.Label(frame_resultados, text="Total de Despesas:", font=label_font).grid(row=2, column=0, sticky="w", pady=8)
        self.lbl_total_despesas = ttk.Label(frame_resultados, text="R$ 0.00", font=value_font, foreground="red")
        self.lbl_total_despesas.grid(row=2, column=1, sticky="e", pady=8, padx=10)
        
        ttk.Separator(frame_resultados, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=15)

        ttk.Label(frame_resultados, text="SALDO EMPRESARIAL:", font=("Arial", 14, "bold")).grid(row=4, column=0, sticky="w", pady=10)
        self.lbl_saldo_empresarial = ttk.Label(frame_resultados, text="R$ 0.00", font=("Arial", 14, "bold"))
        self.lbl_saldo_empresarial.grid(row=4, column=1, sticky="e", pady=10, padx=10)

        frame_resultados.columnconfigure(1, weight=1) 

    def gerar_e_exibir_relatorio(self):
        self.data_inicio = None
        self.data_fim = None

        if self.var_usar_filtro.get():
            try:
                if TKCALENDAR_AVAILABLE:
                    data_i_obj = self.date_inicio.get_date()
                    data_f_obj = self.date_fim.get_date()
                    self.data_inicio = data_i_obj.strftime("%Y-%m-%d")
                    self.data_fim = data_f_obj.strftime("%Y-%m-%d")
                else: 
                    data_i_str = self.date_inicio.get()
                    data_f_str = self.date_fim.get()
                    if data_i_str == "AAAA-MM-DD" or data_f_str == "AAAA-MM-DD": 
                         messagebox.showerror("Erro de Data", "Por favor, insira as datas ou desmarque o filtro.", parent=self)
                         return
                    date.fromisoformat(data_i_str) 
                    date.fromisoformat(data_f_str)
                    self.data_inicio = data_i_str
                    self.data_fim = data_f_str

                if self.data_inicio > self.data_fim:
                    messagebox.showerror("Erro de Data", "A Data Início não pode ser posterior à Data Fim.", parent=self)
                    return
            except ValueError:
                messagebox.showerror("Erro de Data", "Formato de data inválido. Use AAAA-MM-DD.", parent=self)
                return
        
        relatorio = self.reports_db.gerar_relatorio_financeiro_consolidado(self.data_inicio, self.data_fim)
        
        self.lbl_total_vendas.config(text=f"R$ {relatorio['total_vendas']:.2f}")
        self.lbl_total_compras.config(text=f"R$ {relatorio['total_compras_custo']:.2f}")
        self.lbl_total_despesas.config(text=f"R$ {relatorio['total_despesas']:.2f}")
        
        saldo = relatorio['saldo_empresarial']
        self.lbl_saldo_empresarial.config(text=f"R$ {saldo:.2f}")
        
        cor_saldo = "green" if saldo >= 0 else "red"
        self.lbl_saldo_empresarial.config(foreground=cor_saldo)
        
        self.btn_exportar.state(['!disabled'])

    def exportar_para_excel(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Arquivos Excel", "*.xlsx"), ("Todos os arquivos", "*.*")],
            initialfile=f"relatorio_financeiro_{date.today().strftime('%Y%m%d')}.xlsx",
            title="Salvar relatório como..."
        )
        
        if not filepath:  
            return
            
        diretorio = os.path.dirname(filepath)
        
        try:
            caminho_arquivo = self.reports_db.exportar_para_excel(
                self.data_inicio, 
                self.data_fim, 
                diretorio
            )
            
            if caminho_arquivo:
                messagebox.showinfo(
                    "Exportação Concluída",
                    f"Relatório exportado com sucesso para:\n{filepath}",
                    parent=self
                )
                if messagebox.askyesno("Abrir Arquivo", "Deseja abrir o arquivo agora?", parent=self):
                    os.startfile(filepath)
            else:
                messagebox.showerror(
                    "Erro na Exportação",
                    "Não foi possível exportar o relatório. Verifique os dados e tente novamente.",
                    parent=self
                )
                
        except Exception as e:
            messagebox.showerror(
                "Erro na Exportação",
                f"Ocorreu um erro ao exportar o relatório:\n{str(e)}",
                parent=self
            )