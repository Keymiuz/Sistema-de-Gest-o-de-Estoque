# Sistema de Gestão Financeira e de Estoque

Sistema completo para gerenciamento de estoque, vendas, compras e despesas, desenvolvido em Python com interface gráfica Tkinter.

## 📋 Requisitos do Sistema

- Python 3.6 ou superior
- Windows 7/8/10/11
- 500MB de espaço em disco
- 2GB de RAM (mínimo)

## 🚀 Instalação 

1. **Baixe o projeto**
   - Faça o download do arquivo ZIP do projeto
   - Extraia o conteúdo para uma pasta de sua preferência

2. **Instale as dependências**
   - Navegue até a pasta do projeto
   - Execute o arquivo `install.bat` como administrador
   - Siga as instruções na tela

## 🖥️ Instalação Manual

1. **Instale o Python**
   - Acesse [python.org](https://www.python.org/downloads/)
   - Baixe e instale a versão mais recente do Python 3.x
   - Marque a opção "Add Python to PATH" durante a instalação

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o sistema**
   ```bash
   python main.py
   ```

## 📦 Empacotamento (opcional)

Para criar um executável .exe:

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Crie o executável:
   ```bash
   pyinstaller --onefile --windowed --icon=app.ico main.py
   ```

3. O executável estará em `dist/main.exe`

## 📂 Estrutura de Arquivos (A estrutura já está aprensentada aqui no Github, mas se você quiser visualizar ela em forma de gráfico)

```
sistema-gestao/
├── data/                   # Pasta do banco de dados
│   └── gestao.db          
├── ui/                    # Interfaces gráficas
│   ├── janela_produtos.py
│   ├── janela_faturamento.py
│   └── Outras windows gráficas...
├── database.py            # Configuração do banco
├── main.py                # Aplicação principal
├── requirements.txt       # Dependências
└── install.bat           # Script de instalação
```

## 📝 Primeiros Passos

1. **Cadastre seus produtos**
   - Acesse o menu "Cadastros > Produtos"
   - Preencha as informações do produto
   - Clique em "Salvar"

2. **Registre uma venda**
   - Acesse "Movimentações > Registrar Venda"
   - Selecione os produtos vendidos
   - Informe a quantidade e o método de pagamento

3. **Acompanhe seu estoque**
   - O estoque é atualizado automaticamente
   - Receba alertas quando os itens estiverem abaixo do mínimo

## ❓ Suporte

Para suporte, entre em contato:
- Email: jpcicolo@gmail.comgit init
- Celular: (11) 97646-8942

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para obter o texto completo da licença.

---

Desenvolvido por [João Pedro Cicolo](mailto:jpcicolo@gmail.com)
