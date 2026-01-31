import customtkinter as ctk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class BotSimples(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Bot Teste - Debug")
        self.geometry("700x600")
        
        self.bot_ativo = False
        self.driver = None
        
        self.criar_interface()
        
    def criar_interface(self):
        # Título
        ctk.CTkLabel(
            self,
            text="🤖 Bot de Teste - Debug",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        # URL
        frame_url = ctk.CTkFrame(self)
        frame_url.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(frame_url, text="URL:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=10)
        
        self.entry_url = ctk.CTkEntry(frame_url, width=400, height=35)
        self.entry_url.pack(side="left", padx=10)
        self.entry_url.insert(0, "https://www.google.com")
        
        # Botões
        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(pady=20)
        
        self.btn_iniciar = ctk.CTkButton(
            frame_botoes,
            text="▶️ INICIAR TESTE",
            command=self.iniciar_teste,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#22c55e",
            hover_color="#16a34a"
        )
        self.btn_iniciar.pack(side="left", padx=10)
        
        self.btn_parar = ctk.CTkButton(
            frame_botoes,
            text="⏹️ PARAR",
            command=self.parar_teste,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            state="disabled"
        )
        self.btn_parar.pack(side="left", padx=10)
        
        # Status
        self.label_status = ctk.CTkLabel(
            self,
            text="⏸️ Aguardando",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#94a3b8"
        )
        self.label_status.pack(pady=10)
        
        # Log
        ctk.CTkLabel(
            self,
            text="📝 Log de Atividades",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=5)
        
        self.text_log = ctk.CTkTextbox(
            self,
            height=300,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.text_log.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def log(self, mensagem, cor="#ffffff"):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.text_log.insert("end", f"[{timestamp}] {mensagem}\n")
        self.text_log.see("end")
        self.update()
    
    def status(self, texto, cor="#ffffff"):
        """Atualiza status"""
        self.label_status.configure(text=texto, text_color=cor)
        self.update()
    
    def iniciar_teste(self):
        """Inicia o teste"""
        self.log("="*50)
        self.log("🚀 INICIANDO TESTE DO BOT", "#3b82f6")
        self.log("="*50)
        
        url = self.entry_url.get().strip()
        if not url:
            self.log("❌ URL vazia!", "#ef4444")
            return
        
        self.bot_ativo = True
        self.btn_iniciar.configure(state="disabled")
        self.btn_parar.configure(state="normal")
        
        # Executar em thread
        self.log("🧵 Criando thread...", "#64748b")
        thread = threading.Thread(target=self.executar_teste, args=(url,), daemon=True)
        self.log("🧵 Iniciando thread...", "#64748b")
        thread.start()
        self.log("✅ Thread iniciada!", "#22c55e")
    
    def parar_teste(self):
        """Para o teste"""
        self.log("⏹️ Parando bot...", "#f59e0b")
        self.bot_ativo = False
        self.btn_iniciar.configure(state="normal")
        self.btn_parar.configure(state="disabled")
        self.status("⏸️ Parado", "#f59e0b")
        
        if self.driver:
            try:
                self.log("🔴 Fechando navegador...", "#64748b")
                self.driver.quit()
                self.log("✅ Navegador fechado", "#22c55e")
            except Exception as e:
                self.log(f"⚠️ Erro ao fechar: {e}", "#f59e0b")
    
    def executar_teste(self, url):
        """Executa o teste completo"""
        try:
            self.log("📍 PASSO 1: Configurando Chrome", "#3b82f6")
            self.status("⚙️ Configurando...", "#3b82f6")
            
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            self.log("✅ Opções configuradas")
            
            self.log("📍 PASSO 2: Baixando ChromeDriver", "#3b82f6")
            self.log("⏳ Isso pode demorar na primeira vez...")
            
            driver_path = ChromeDriverManager().install()
            self.log(f"✅ Driver baixado: {driver_path}")
            
            self.log("📍 PASSO 3: Inicializando Chrome", "#3b82f6")
            self.status("🌐 Abrindo navegador...", "#3b82f6")
            
            self.driver = webdriver.Chrome(
                service=Service(driver_path),
                options=options
            )
            self.log("✅ Navegador aberto!", "#22c55e")
            
            self.log("📍 PASSO 4: Acessando URL", "#3b82f6")
            self.log(f"🔗 URL: {url}")
            self.status("🌐 Carregando página...", "#3b82f6")
            
            self.driver.get(url)
            self.log("✅ Navegação iniciada")
            
            self.log("📍 PASSO 5: Aguardando carregar", "#3b82f6")
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            self.log("✅ Página carregada!", "#22c55e")
            
            self.status("✅ Teste concluído!", "#22c55e")
            
            # Loop de monitoramento
            self.log("\n📍 PASSO 6: Iniciando monitoramento", "#3b82f6")
            self.status("👀 Monitorando...", "#22c55e")
            
            contador = 0
            while self.bot_ativo:
                contador += 1
                self.log(f"🔄 Ciclo #{contador}")
                
                try:
                    # Aqui você pode adicionar sua lógica
                    titulo = self.driver.title
                    self.log(f"   📄 Título da página: {titulo}", "#64748b")
                    
                    # Exemplo: contar links
                    links = self.driver.find_elements(By.TAG_NAME, "a")
                    self.log(f"   🔗 Links encontrados: {len(links)}", "#64748b")
                    
                except Exception as e:
                    self.log(f"   ⚠️ Erro no ciclo: {e}", "#f59e0b")
                
                if self.bot_ativo:
                    self.log(f"   ⏸️ Aguardando 3 segundos...", "#64748b")
                    time.sleep(3)
            
            self.log("\n🏁 Monitoramento encerrado", "#94a3b8")
            
        except Exception as e:
            import traceback
            erro = traceback.format_exc()
            self.log(f"\n❌ ERRO CRÍTICO!", "#ef4444")
            self.log(f"Mensagem: {str(e)}", "#ef4444")
            self.log(f"\nStack trace completo:", "#64748b")
            self.log(erro, "#64748b")
            self.status("❌ Erro!", "#ef4444")
            
        finally:
            self.btn_iniciar.configure(state="normal")
            self.btn_parar.configure(state="disabled")
            self.log("\n🏁 Teste finalizado")


if __name__ == "__main__":
    app = BotSimples()
    app.mainloop()
