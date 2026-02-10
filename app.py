import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os
from datetime import datetime
import threading

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class BotFormulariosApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração da janela
        self.title("Bot de Formulários - Automação")
        self.iconbitmap("icon.ico")
        self.geometry("900x700")
        
        # Variáveis
        self.dados_padrao = ["Luciana", "Freitas", "45994951404", "lmfreitas864@gmail.com"]
        self.dados_usuario = self.carregar_dados_usuario()
        self.driver = None
        self.wait = None
        self.bot_ativo = False
        self.BASE_URL = "http://127.0.0.1:5500/html/index.html"  # Altere para sua URL
        
        # Criar interface
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal com scroll
        main_container = ctk.CTkScrollableFrame(self, corner_radius=0)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # ========== SEÇÃO: TÍTULO ==========
        titulo = ctk.CTkLabel(
            main_container,
            text="🤖 Bot de Preenchimento de Formulários",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(pady=(10, 20))
        
        # ========== SEÇÃO: DADOS SALVOS ==========
        frame_dados = ctk.CTkFrame(main_container, corner_radius=15)
        frame_dados.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            frame_dados,
            text="📋 Dados Cadastrados",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(15, 10))
        
        # Criar labels para mostrar dados
        self.labels_dados = {}
        campos = ["Nome", "Sobrenome", "CPF", "Email", "Telefone", "DDD"]


        
        for i, campo in enumerate(campos):
            frame_linha = ctk.CTkFrame(frame_dados, fg_color="transparent")
            frame_linha.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(
                frame_linha,
                text=f"{campo}:",
                font=ctk.CTkFont(size=14, weight="bold"),
                width=120,
                anchor="w"
            ).pack(side="left")
            
            label_valor = ctk.CTkLabel(
                frame_linha,
                text=self.dados_usuario[i] if i < 6 else "---",
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            label_valor.pack(side="left", fill="x", expand=True)
            self.labels_dados[campo] = label_valor

        
        # Botão atualizar dados
        self.btn_atualizar_dados = ctk.CTkButton(
            frame_dados,
            text="✏️ Atualizar Dados",
            command=self.abrir_janela_edicao,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#f59e0b",
            hover_color="#d97706"
        )
        self.btn_atualizar_dados.pack(pady=15)
        
        # ========== SEÇÃO: CONTROLES ==========
        frame_controles = ctk.CTkFrame(main_container, corner_radius=15)
        frame_controles.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            frame_controles,
            text="⚙️ Controles do Bot",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(15, 10))
        
        # URL Base
        frame_url = ctk.CTkFrame(frame_controles, fg_color="transparent")
        frame_url.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            frame_url,
            text="URL Base:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=(0, 10))
        
        self.entry_url = ctk.CTkLabel(
            frame_url,
            height=35,
            font=ctk.CTkFont(size=14),
            anchor="w",
            text=self.BASE_URL
        )
        self.entry_url.pack(side="left", fill="x", expand=True)
        
        # Botões de controle
        frame_botoes = ctk.CTkFrame(frame_controles, fg_color="transparent")
        frame_botoes.pack(pady=15)
        
        self.btn_iniciar = ctk.CTkButton(
            frame_botoes,
            text="▶️ Iniciar Monitoramento",
            command=self.iniciar_bot,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#22c55e",
            hover_color="#16a34a"
        )
        self.btn_iniciar.pack(side="left", padx=10)
        
        self.btn_parar = ctk.CTkButton(
            frame_botoes,
            text="⏹️ Parar Bot",
            command=self.parar_bot,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            state="disabled"
        )
        self.btn_parar.pack(side="left", padx=10)
        
        # ========== SEÇÃO: STATUS E LOG ==========
        frame_status = ctk.CTkFrame(main_container, corner_radius=15)
        frame_status.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Status atual
        frame_status_header = ctk.CTkFrame(frame_status, fg_color="transparent")
        frame_status_header.pack(fill="x", padx=15, pady=(15, 5))
        
        ctk.CTkLabel(
            frame_status_header,
            text="📊 Status:",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        
        self.label_status = ctk.CTkLabel(
            frame_status_header,
            text="Aguardando início",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#94a3b8"
        )
        self.label_status.pack(side="left", padx=10)
        
        # Log de atividades
        ctk.CTkLabel(
            frame_status,
            text="📝 Log de Atividades",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 5))
        
        self.text_log = ctk.CTkTextbox(
            frame_status,
            height=250,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.text_log.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Botão limpar log
        btn_limpar_log = ctk.CTkButton(
            frame_status,
            text="🗑️ Limpar Log",
            command=self.limpar_log,
            width=150,
            height=30,
            font=ctk.CTkFont(size=12)
        )
        btn_limpar_log.pack(pady=(0, 15))
        
    def abrir_janela_edicao(self):
        """Abre janela para editar dados do usuário"""
        janela = ctk.CTkToplevel(self)
        janela.title("Editar Dados")
        janela.geometry("500x550")
        janela.grab_set()  # Torna a janela modal
        
        ctk.CTkLabel(
            janela,
            text="✏️ Editar Dados Cadastrados",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=20)
        
        # Campos de entrada
        campos = ["Telefone", "DDD"]
        entries = []
        
        for i, campo in enumerate(campos):
            frame = ctk.CTkFrame(janela, fg_color="transparent")
            frame.pack(fill="x", padx=30, pady=8)
            
            ctk.CTkLabel(
                frame,
                text=f"{campo}:",
                font=ctk.CTkFont(size=14, weight="bold"),
                width=100,
                anchor="w"
            ).pack(side="left")
            
            entry = ctk.CTkEntry(
                frame,
                height=35,
                font=ctk.CTkFont(size=13)
            )
            entry.pack(side="left", fill="x", expand=True)

            
            if i < len(self.dados_usuario):
                count = len(self.dados_usuario) - len(campos) + i
                entry.insert(0, self.dados_usuario[count])
                self.adicionar_log(f"Carregado {campos[i]}: {self.dados_usuario[count]}")
                
            
            entries.append(entry)
        
        def salvar():
            novos_dados = [entry.get().strip() for entry in entries]
            self.dados_usuario = novos_dados
            self.salvar_dados_usuario()
            self.atualizar_exibicao_dados()
            self.adicionar_log("✅ Dados atualizados com sucesso!", "#22c55e")
            janela.destroy()
        
        # Botões
        frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
        frame_botoes.pack(pady=30)
        
        ctk.CTkButton(
            frame_botoes,
            text="💾 Salvar",
            command=salvar,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#22c55e",
            hover_color="#16a34a"
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            frame_botoes,
            text="❌ Cancelar",
            command=janela.destroy,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#ef4444",
            hover_color="#dc2626"
        ).pack(side="left", padx=10)
    
    def atualizar_exibicao_dados(self):
        """Atualiza a exibição dos dados na interface"""
        campos = ["Telefone", "DDD"]
        for i, campo in enumerate(campos):
            valor = self.dados_usuario[i] if i < len(self.dados_usuario) else "---"
            self.labels_dados[campo].configure(text=valor)
    
    def carregar_dados_usuario(self):
        """Carrega dados do usuário do arquivo"""
        dir_form_data = os.path.join(os.path.expanduser('~'), 'form_data')
        if not os.path.exists(dir_form_data):
            os.makedirs(dir_form_data, exist_ok=True)
        arquivo_path = os.path.join(dir_form_data, 'dados_usuario.json')
        # Ensure the directory exists
        os.makedirs(os.path.dirname(arquivo_path), exist_ok=True)
        if os.path.exists(arquivo_path):
            with open(arquivo_path, 'r') as f:
                dados_arquivo = json.load(f)
                self.dados_padrao.extend(dados_arquivo)
                return self.dados_padrao
        # Dados padrão
        return ["Luciana", "Freitas", "45994951404", "lmfreitas864@gmail.com", "991748889", "61"]
    
    def salvar_dados_usuario(self):
        """Salva dados do usuário em arquivo"""
        dir_form_data = os.path.join(os.path.expanduser('~'), 'form_data')
        if not os.path.exists(dir_form_data):
            os.makedirs(dir_form_data, exist_ok=True)
        arquivo_path = os.path.join(dir_form_data, 'dados_usuario.json')
        with open(arquivo_path, 'w') as f:
            json.dump(self.dados_usuario, f, indent=2)
    
    def adicionar_log(self, mensagem, cor="#ffffff"):
        """Adiciona mensagem ao log com timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.text_log.insert("end", f"[{timestamp}] {mensagem}\n")
        self.text_log.see("end")
        self.update()
    
    def limpar_log(self):
        """Limpa o log de atividades"""
        self.text_log.delete("1.0", "end")
    
    def atualizar_status(self, texto, cor="#ffffff"):
        """Atualiza o status atual"""
        self.label_status.configure(text=texto, text_color=cor)
    
    def iniciar_bot(self):
        """Inicia o bot em uma thread separada"""
        
        if not self.BASE_URL:
            self.adicionar_log("❌ Por favor, insira a URL base!", "#ef4444")
            return
        
        if not any(self.dados_usuario):
            self.adicionar_log("❌ Por favor, cadastre seus dados primeiro!", "#ef4444")
            return
        
        self.bot_ativo = True
        self.btn_iniciar.configure(state="disabled")
        self.btn_atualizar_dados.configure(state="disabled")
        self.btn_parar.configure(state="normal")
        
        # Inicia bot em thread separada
        thread = threading.Thread(target=self.executar_bot, daemon=True)
        thread.start()
    
    def parar_bot(self):
        """Para a execução do bot"""
        self.bot_ativo = False
        self.btn_iniciar.configure(state="normal")
        self.btn_atualizar_dados.configure(state="normal")
        self.btn_parar.configure(state="disabled")
        self.atualizar_status("⏸️ Bot pausado", "#f59e0b")
        self.adicionar_log("⏹️ Bot parado pelo usuário", "#f59e0b")
        
        if self.driver:
            try:
                self.driver.quit()
                self.adicionar_log("🔴 Navegador fechado", "#64748b")
            except:
                pass
    
    def executar_bot(self):
        """Execução principal do bot"""
        try:
            self.adicionar_log("🟢 Iniciando bot de formulários...")
            self.atualizar_status("🚀 Iniciando navegador...", "#3b82f6")
            
            # Forçar atualização da interface
            self.update_idletasks()
            
            # Configurar Selenium
            self.adicionar_log("⚙️ Configurando Chrome...")
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            
            self.adicionar_log("📥 Baixando ChromeDriver...")
            self.update_idletasks()
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            self.wait = WebDriverWait(self.driver, 30)
            
            self.adicionar_log("✅ Navegador iniciado com sucesso!")
            self.atualizar_status("🌐 Acessando página...", "#3b82f6")
            self.update_idletasks()
            
            self.adicionar_log(f"🔗 Acessando: {self.BASE_URL}")
            self.driver.get(self.BASE_URL)
            time.sleep(1)
            
            self.adicionar_log("⏳ Aguardando página carregar...")
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(1)
            
            self.adicionar_log(f"✅ Página carregada com sucesso!")
            self.atualizar_status("👀 Monitorando...", "#22c55e")
            self.update_idletasks()
            
            # Loop de monitoramento
            contador_ciclos = 0
            while self.bot_ativo:
                try:
                    contador_ciclos += 1
                    self.adicionar_log(f"🔄 Ciclo #{contador_ciclos} - Verificando...")
                    self.update_idletasks()
                    
                    self.verificar_e_executar()
                    
                except Exception as e:
                    import traceback
                    erro_completo = traceback.format_exc()
                    self.adicionar_log(f"⚠️ Erro no ciclo: {str(e)}", "#f59e0b")
                    self.adicionar_log(f"Detalhes: {erro_completo}", "#64748b")
                
                if self.bot_ativo:
                    self.adicionar_log("⏸️ Aguardando 2 segundos...", "#64748b")
                    time.sleep(2)
            
            self.adicionar_log("🛑 Loop de monitoramento encerrado")
            
        except Exception as e:
            import traceback
            erro_completo = traceback.format_exc()
            self.adicionar_log(f"❌ Erro crítico: {str(e)}", "#ef4444")
            self.adicionar_log(f"Stack trace completo:\n{erro_completo}", "#64748b")
            self.atualizar_status("❌ Erro", "#ef4444")
            self.btn_iniciar.configure(state="normal")
            self.btn_parar.configure(state="disabled")
            self.bot_ativo = False
    
    def form_extract(self, driver, base_url):
        # Acessar a página base
        driver.get(base_url)
        
        # Aguardar a página carregar completamente
        time.sleep(3)
        
        # Buscar os links dos formulários
        try:
            # Aguardar os elementos estarem presentes
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="presentation"]'))
            )
            
            forms = []
            
            # Buscar pela div com role="presentation"
            divs_presentation = driver.find_elements(By.CSS_SELECTOR, 'div[role="presentation"]')
            
            for div in divs_presentation:
                try:
                    # Procurar por links dentro da div
                    link = div.find_element(By.TAG_NAME, 'a')
                    href = link.get_attribute('href')
                    
                    # Verificar se é um link de formulário do Google/Office Forms
                    if href and ('forms.office.com' in href or 'forms.google.com' in href):
                        forms.append(href)
                        self.adicionar_log(f"Formulário encontrado: {href}\n")
                except:
                    continue
            
            return forms
            
        except Exception as e:
            self.atualizar_status("❌ Erro ao extrair formulários", "#ef4444")
            return []
    
    def verificar_e_executar(self):
        """Verifica novos formulários e executa preenchimento"""
        self.driver.refresh()
        self.adicionar_log("🔄 Verificando novos formulários...")
        
        FORMS = self.form_extract(self.driver, self.BASE_URL)
        
        if FORMS:
            self.adicionar_log(f"📋 {len(FORMS)} formulário(s) encontrado(s):")
            for idx, form in enumerate(FORMS, 1):
                self.adicionar_log(f"   {idx}. {form}")
        else:
            self.adicionar_log("📋 Nenhum formulário encontrado")
        
        # Ler dados salvos
        dados_anteriores = self.ler_dados()
        link_atual = FORMS[0] if FORMS else None
        
        if link_atual and link_atual != dados_anteriores.get('ultimo_link'):
            self.adicionar_log("🆕 Novo formulário detectado!", "#22c55e")
            self.atualizar_status("📝 Preenchendo formulários...", "#3b82f6")
            
            # Processar formulários
            for i, form_url in enumerate(FORMS, start=1):
                if not self.bot_ativo:
                    break
                
                self.adicionar_log(f"📝 Processando formulário {i}/{len(FORMS)}")
                
                try:
                    # Abrir nova aba
                    self.driver.execute_script("window.open(arguments[0], '_blank');", form_url)
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    
                    # Preencher campos
                    inputs = self.wait.until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
                    )
                    
                    for campo, valor in zip(inputs, self.dados_padrao):
                        campo.send_keys(valor)
                        time.sleep(0.1)
                    
                    self.adicionar_log(f"✏️ Campos preenchidos no formulário {i}")
                    
                    # Enviar formulário
                    send_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button"))
                    )
                    self.driver.execute_script("arguments[0].click();", send_button)
                    
                    self.adicionar_log(f"✅ Formulário {i} enviado com sucesso!", "#22c55e")
                    
                    # Voltar para aba principal
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    time.sleep(1)
                    
                except Exception as e:
                    self.adicionar_log(f"❌ Erro no formulário {i}: {str(e)}", "#ef4444")
            
            # Salvar último link processado
            self.salvar_dados(link_atual)
            self.adicionar_log("💾 Dados salvos com sucesso!")
            self.atualizar_status("👀 Monitorando...", "#22c55e")
            
        else:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.adicionar_log(f"⏳ Nenhuma atualização ({timestamp})")
    
    def ler_dados(self, arquivo='dados.json'):
        """Lê dados do arquivo de controle"""
        dir_form_data = os.path.join(os.path.expanduser('~'), 'form_data')
        arquivo_path = os.path.join(dir_form_data, arquivo)
        if os.path.exists(arquivo_path):
            with open(arquivo_path, 'r') as f:
                return json.load(f)
        return {'ultimo_link': None, 'ultima_atualizacao': None}
    
    def salvar_dados(self, link, arquivo='dados.json'):
        """Salva dados de controle"""
        dados = {
            'ultimo_link': link,
            'ultima_atualizacao': datetime.now().isoformat()
        }
        
        dir_form_data = os.path.join(os.path.expanduser('~'), 'form_data')
        if not os.path.exists(dir_form_data):
            os.makedirs(dir_form_data, exist_ok=True)
        
        arquivo_path = os.path.join(dir_form_data, arquivo)
        with open(arquivo_path, 'w') as f:
            json.dump(dados, f, indent=2)


if __name__ == "__main__":
    app = BotFormulariosApp()
    app.mainloop()