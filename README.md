# 🤖 Sistema de Automação de Formulários com Interface Gráfica

Sistema completo para monitoramento, extração e preenchimento automático de formulários web com interface gráfica moderna.

---

## 📋 Pré-requisitos

### Software Necessário

- **Python 3.8+** instalado
- **Google Chrome** instalado
- **Visual Studio Code** (VSCode)
- **Extensão Live Server** instalada no VSCode

### Bibliotecas Python

```bash
pip install customtkinter selenium webdriver-manager
```

---

## 🚀 Como executar o projeto

### 1️⃣ Instalar a extensão Live Server no VSCode

1. Abra o VSCode
2. Vá em **Extensions** (Ctrl+Shift+X ou Cmd+Shift+X)
3. Pesquise por "Live Server"
4. Clique em **Install** na extensão de **Ritwick Dey**

### 2️⃣ Executar o servidor web (ambiente de desenvolvimento)

1. Abra a pasta `html` no VSCode
2. Clique com o botão direito no arquivo HTML
3. Selecione **"Open with Live Server"**
4. A página será aberta automaticamente no navegador
5. Anote a URL (geralmente `http://127.0.0.1:5500`)

### 3️⃣ Executar a interface gráfica

No terminal, na raiz do projeto, execute:

```bash
python bot_formularios_interface.py
```

### 4️⃣ Configurar a aplicação

1. **Cadastrar seus dados**
   - Clique em "✏️ Atualizar Dados"
   - Preencha: Nome, Sobrenome, CPF, Email, Telefone, DDD
   - Clique em "💾 Salvar"

2. **Configurar URL**
   - Insira a URL do site no campo "URL Base"
   - Exemplo: `http://127.0.0.1:5500` (se estiver testando localmente)

3. **Iniciar monitoramento**
   - Clique em "▶️ Iniciar Monitoramento"
   - Acompanhe o progresso no log em tempo real

---

## 📁 Estrutura do projeto

```
projeto/
├── bot_formularios_interface.py  # 🎨 Interface gráfica principal
├── bot_teste_debug.py            # 🔧 Versão simplificada para debug
├── main.py                       # 📜 Script original (linha de comando)
├── html/                         # 🌐 Páginas HTML para teste
│   └── index.html                # Página simulando site alvo
├── scrap/                        # 🧪 Scripts de teste
│   └── ...                       # Experimentos e testes
├── dados_usuario.json            # 💾 Dados cadastrados (auto-gerado)
├── dados.json                    # 📊 Controle de formulários (auto-gerado)
└── README.md                     # 📖 Este arquivo
```

---

## 🎨 Funcionalidades da Interface

### ✨ Principais Recursos

#### 📋 Gerenciamento de Dados

- ✅ Visualização clara dos dados cadastrados
- ✅ Edição através de janela modal
- ✅ Salvamento automático em JSON
- ✅ Validação visual dos campos

#### ⚙️ Controle do Bot

- ✅ Iniciar/Parar monitoramento com um clique
- ✅ URL configurável na interface
- ✅ Execução em thread separada (não trava a UI)
- ✅ Feedback visual do status atual

#### 📊 Monitoramento em Tempo Real

- ✅ Log detalhado com timestamps
- ✅ Códigos de cores por tipo de mensagem
- ✅ Scroll automático
- ✅ Função limpar log
- ✅ Contador de ciclos de verificação

#### 🎯 Sistema de Cores do Log

- 🟢 **Verde** (#22c55e) - Sucesso
- 🔴 **Vermelho** (#ef4444) - Erro crítico
- 🟠 **Laranja** (#f59e0b) - Aviso
- 🔵 **Azul** (#3b82f6) - Informação/Processo
- ⚫ **Cinza** (#64748b) - Detalhes técnicos
- ⚪ **Branco** (#ffffff) - Mensagem padrão

---

## 🔧 Versões Disponíveis

### 1. `bot_formularios_interface.py` - Interface Completa

**Use quando:** Quiser usar o sistema completo com interface gráfica

**Recursos:**

- Interface gráfica moderna
- Gerenciamento visual de dados
- Log em tempo real
- Controles intuitivos

### 2. `bot_teste_debug.py` - Versão Debug

**Use quando:** Precisar testar ou debugar problemas

**Recursos:**

- Interface simplificada
- Log ultra-detalhado
- Passo a passo de cada operação
- Ideal para identificar erros

### 3. `main.py` - Script Original

**Use quando:** Preferir executar via terminal

**Recursos:**

- Execução direta no terminal
- Configuração via código
- Sem dependência de interface gráfica

---

## 🛠️ Tecnologias utilizadas

### Backend

- **Python 3.8+** - Linguagem principal
- **Selenium** - Automação do navegador
- **WebDriver Manager** - Gerenciamento automático do ChromeDriver

### Interface

- **CustomTkinter** - Framework moderno para GUI
- **Threading** - Execução assíncrona

### Desenvolvimento

- **HTML/CSS** - Páginas de teste
- **Live Server** - Servidor local para desenvolvimento

---

## 📖 Fluxo de Funcionamento

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Usuário inicia o bot pela interface                         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. Sistema abre o Chrome automaticamente                        │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. Acessa a URL configurada                                     │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. Loop de Monitoramento:                                       │
│     ├─ Extrai links de formulários da página                    │
│     ├─ Compara com último processado                            │
│     ├─ Se houver novos:                                          │
│     │   ├─ Abre formulário em nova aba                          │
│     │   ├─ Preenche campos com dados salvos                     │
│     │   ├─ Envia formulário                                     │
│     │   ├─ Fecha aba                                            │
│     │   └─ Salva registro do processamento                      │
│     └─ Aguarda 2 segundos e repete                              │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. Usuário pode parar a qualquer momento                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🐛 Solução de Problemas

### ❌ "ChromeDriver não encontrado"

**Solução:** O sistema baixa automaticamente. Verifique sua conexão com internet.

### ❌ "Erro ao iniciar Chrome"

**Solução:** Certifique-se de que o Google Chrome está instalado no sistema.

### ❌ Interface não atualiza durante execução

**Solução:** Isso é normal! O bot roda em thread separada. Acompanhe pelo log.

### ❌ "Formulário não encontrado"

**Solução:** Ajuste a função `form_extract()` conforme a estrutura do seu site.

### ❌ Campos não preenchem corretamente

**Solução:** Verifique se a ordem dos dados corresponde aos campos do formulário.

### 🔍 Como debugar:

1. Execute `bot_teste_debug.py` primeiro
2. Observe cada passo no log detalhado
3. Identifique onde o erro ocorre
4. Ajuste o código conforme necessário

---

## 💡 Dicas de Uso

### 🎯 Boas Práticas

1. **Teste localmente primeiro** - Use o Live Server antes de ir para produção
2. **Mantenha backups** - Salve `dados_usuario.json` regularmente
3. **Acompanhe os logs** - Eles mostram exatamente o que está acontecendo
4. **Use o modo debug** - Para identificar problemas rapidamente

### ⚡ Otimizações

- Ajuste o `time.sleep(2)` no loop para verificações mais/menos frequentes
- Modifique os timeouts do `WebDriverWait` conforme a velocidade do site
- Adicione mais logs personalizados se necessário

### 🔒 Segurança

- **NUNCA** compartilhe `dados_usuario.json` (contém dados pessoais)
- Use apenas em sites onde você tem permissão
- Respeite robots.txt e termos de uso dos sites

---

## 📝 Customização

### Adicionar novos campos

Edite as seguintes linhas:

```python
# Linha ~64 e ~186
campos = ["Nome", "Sobrenome", "CPF", "Email", "Telefone", "DDD", "SEU_NOVO_CAMPO"]
```

### Alterar cores da interface

```python
# No início do arquivo
ctk.set_default_color_theme("blue")  # Opções: "blue", "green", "dark-blue"
```

### Modificar intervalo de verificação

```python
# Na função verificar_e_executar
time.sleep(2)  # Altere para o tempo desejado em segundos
```

---

## 📦 Arquivos Gerados

### `dados_usuario.json`

```json
["João", "Silva", "12345678900", "joao@email.com", "999999999", "11"]
```

### `dados.json`

```json
{
  "ultimo_link": "https://exemplo.com/formulario",
  "ultima_atualizacao": "2025-01-31T14:30:00.000000"
}
```

criação do exe: pyinstaller bot_formularios.spec

---

## 🔄 Atualizações Recentes

### ✅ v2.0 - Interface Gráfica

- ➕ Interface CustomTkinter completa
- ➕ Gerenciamento visual de dados
- ➕ Log em tempo real com cores
- ➕ Versão debug para testes
- 🔄 Threading para não travar UI
- 🔄 Melhor tratamento de erros

### ✅ v1.0 - Versão Original

- ➕ Script de linha de comando
- ➕ Extração de formulários
- ➕ Preenchimento automático
- ➕ Monitoramento contínuo

---

### Problemas conhecidos?

1. Verifique os logs na interface
2. Execute a versão debug
3. Consulte a seção "Solução de Problemas"

### Quer contribuir?

- Relate bugs encontrados
- Sugira melhorias
- Compartilhe casos de uso

---

## 📄 Licença

Este projeto é de uso educacional e deve ser utilizado de forma ética e responsável.

---

## 🎓 Aprendizados

Este projeto demonstra:

- ✅ Automação web com Selenium
- ✅ Interfaces gráficas modernas com CustomTkinter
- ✅ Threading em Python
- ✅ Manipulação de arquivos JSON
- ✅ Boas práticas de logging
- ✅ Tratamento de erros robusto

---

**Desenvolvido com Python + CustomTkinter + Selenium**
