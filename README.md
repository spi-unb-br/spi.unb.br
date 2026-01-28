# Sistema de Extração de Formulários

Este projeto contém um sistema para extração de dados de formulários de páginas web.

## 📋 Pré-requisitos

- **Python 3.x** instalado
- **Visual Studio Code** (VSCode)
- **Extensão Live Server** instalada no VSCode

## 🚀 Como executar o projeto

### 1. Instalar a extensão Live Server no VSCode

1. Abra o VSCode
2. Vá em **Extensions** (Ctrl+Shift+X)
3. Pesquise por "Live Server"
4. Clique em **Install** na extensão de Ritwick Dey

### 2. Executar o servidor web

1. Abra a pasta `html` no VSCode
2. Clique com o botão direito no arquivo HTML
3. Selecione **"Open with Live Server"**
4. A página será aberta automaticamente no navegador (geralmente em `http://127.0.0.1:5500`)

### 3. Executar o programa principal

No terminal, execute o arquivo `main.py` na raiz do projeto:

```bash
python main.py
```

## 📁 Estrutura do projeto

```
projeto/
├── main.py                 # Arquivo principal de execução
├── html/                   # Pasta com páginas HTML
│   └── index.html   # Página simulando site alvo
├── scrap/                  # Pasta com scripts de teste
│   └── ...                 # Scripts de scraping de teste
└── README.md               # Este arquivo
```

## 📝 Mudanças recentes

### ✅ Adicionado
- Página HTML para simular a página alvo
- Função de extrair formulários

### 🔄 Modificado
- Arquivo `teste_forms.py` renomeado para `main.py`
- Lógica de extração alterada no arquivo main

### 📦 Criado
- Scripts de teste na pasta `scrap/`

## 🛠️ Tecnologias utilizadas

- **Python** - Linguagem de programação principal
- **HTML/CSS** - Interface web
- **Live Server** - Servidor local para desenvolvimento

## 📖 Observações

- Certifique-se de que o Live Server esteja rodando antes de executar o `main.py`
- A URL padrão do Live Server é `http://127.0.0.1:5500`
- Se a porta padrão estiver ocupada, o Live Server usará outra porta automaticamente
