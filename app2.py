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
import sys
import ctypes
import unicodedata
from datetime import datetime
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


# ─────────────────────────────────────────────
#  Dados fixos que nunca são editados pelo usuário
# ─────────────────────────────────────────────
DADOS_FIXOS = {
    "nome":      "Luciana",
    "sobrenome": "Freitas",
    "cpf":       "45994951404",
    "email":     "lmfreitas864@gmail.com",
}

# Campos que o usuário pode editar na interface
CAMPOS_EDITAVEIS = ["Telefone", "DDD"]

# Mapeamento: título normalizado → chave interna
# A busca é feita por IGUALDADE EXATA primeiro, depois por "começa com".
# Isso evita que "sobrenome" case com "nome".
MAPA_TITULO_CAMPO = {
    # nome  (apenas títulos que NÃO contenham "sobrenome")
    "nome":              "nome",
    "primeiro nome":     "nome",
    "first name":        "nome",
    "given name":        "nome",
    # sobrenome
    "sobrenome":         "sobrenome",
    "ultimo nome":       "sobrenome",
    "last name":         "sobrenome",
    "family name":       "sobrenome",
    # cpf
    "cpf":               "cpf",
    "CPF":               "cpf",
    "documento":         "cpf",
    # email
    "email":             "email",
    "e-mail":            "email",
    "correio":           "email",
    # telefone
    "telefone":          "telefone",
    "celular":           "telefone",
    "phone":             "telefone",
    "whatsapp":          "telefone",
    # ddd
    "ddd":           "ddd",
    "codigo de area": "ddd",
    "area":          "ddd",
}


def normalizar(texto: str) -> str:
    """Remove acentos, espaços extras e converte para minúsculo."""
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.strip().lower()


class BotFormulariosApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        if os.name == "nt":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("spi.pluto.app")

        self.title("Bot de Formulários - Automação")
        try:
            self.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass
        self.geometry("900x700")

        # dados_editaveis[0] = Telefone, dados_editaveis[1] = DDD
        self.dados_editaveis = self.carregar_dados_editaveis()
        self.driver = None
        self.wait = None
        self.bot_ativo = False
        self.BASE_URL = "https://sites.google.com/view/spi-imoveis/com-cadastro-virtual"

        self.criar_interface()

    # ──────────────────────────────────────────
    #  Persistência
    # ──────────────────────────────────────────

    def _dir_form_data(self):
        d = os.path.join(os.path.expanduser("~"), "form_data")
        os.makedirs(d, exist_ok=True)
        return d

    def carregar_dados_editaveis(self):
        path = os.path.join(self._dir_form_data(), "dados_usuario.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                dados = json.load(f)
                # Suporte ao formato antigo (lista) e novo (dict)
                if isinstance(dados, list):
                    return dados[:2] if len(dados) >= 2 else ["", ""]
                return [dados.get("telefone", ""), dados.get("ddd", "")]
        return ["991748889", "61"]

    def salvar_dados_editaveis(self):
        path = os.path.join(self._dir_form_data(), "dados_usuario.json")
        with open(path, "w") as f:
            json.dump({"telefone": self.dados_editaveis[0],
                       "ddd":      self.dados_editaveis[1]}, f, indent=2)

    def obter_todos_dados(self) -> dict:
        """Retorna dicionário completo chave→valor para preenchimento."""
        return {
            **DADOS_FIXOS,
            "telefone": self.dados_editaveis[0],
            "ddd":      self.dados_editaveis[1],
        }

    def ler_dados_controle(self, arquivo="dados.json"):
        path = os.path.join(self._dir_form_data(), arquivo)
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return {"ultimo_link": None, "ultima_atualizacao": None}

    def salvar_dados_controle(self, link, arquivo="dados.json"):
        path = os.path.join(self._dir_form_data(), arquivo)
        with open(path, "w") as f:
            json.dump({"ultimo_link": link,
                       "ultima_atualizacao": datetime.now().isoformat()}, f, indent=2)

    # ──────────────────────────────────────────
    #  Interface
    # ──────────────────────────────────────────

    def criar_interface(self):
        main_container = ctk.CTkScrollableFrame(self, corner_radius=0)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            main_container,
            text="🤖 Bot de Preenchimento de Formulários",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).pack(pady=(10, 20))

        # ── Dados cadastrados ──
        frame_dados = ctk.CTkFrame(main_container, corner_radius=15)
        frame_dados.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            frame_dados,
            text="📋 Dados Cadastrados",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(15, 10))

        self.labels_dados = {}

        # Exibe dados fixos (somente leitura)
        for campo, valor in DADOS_FIXOS.items():
            self._linha_dado(frame_dados, campo.capitalize(), valor, editavel=False)

        # Exibe dados editáveis
        for i, campo in enumerate(CAMPOS_EDITAVEIS):
            valor = self.dados_editaveis[i] if i < len(self.dados_editaveis) else "---"
            self._linha_dado(frame_dados, campo, valor, editavel=True)

        self.btn_atualizar_dados = ctk.CTkButton(
            frame_dados,
            text="✏️ Atualizar Dados",
            command=self.abrir_janela_edicao,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#f59e0b",
            hover_color="#d97706",
        )
        self.btn_atualizar_dados.pack(pady=15)

        # ── Controles ──
        frame_controles = ctk.CTkFrame(main_container, corner_radius=15)
        frame_controles.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            frame_controles,
            text="⚙️ Controles do Bot",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=(15, 10))

        frame_url = ctk.CTkFrame(frame_controles, fg_color="transparent")
        frame_url.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_url, text="URL Base:",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(frame_url, text=self.BASE_URL,
                     font=ctk.CTkFont(size=14), anchor="w").pack(side="left", fill="x", expand=True)

        frame_botoes = ctk.CTkFrame(frame_controles, fg_color="transparent")
        frame_botoes.pack(pady=15)

        self.btn_iniciar = ctk.CTkButton(
            frame_botoes, text="▶️ Iniciar Monitoramento",
            command=self.iniciar_bot, width=200, height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#22c55e", hover_color="#16a34a",
        )
        self.btn_iniciar.pack(side="left", padx=10)

        self.btn_parar = ctk.CTkButton(
            frame_botoes, text="⏹️ Parar Bot",
            command=self.parar_bot, width=200, height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#ef4444", hover_color="#dc2626", state="disabled",
        )
        self.btn_parar.pack(side="left", padx=10)

        # ── Status e log ──
        frame_status = ctk.CTkFrame(main_container, corner_radius=15)
        frame_status.pack(fill="both", expand=True, padx=20, pady=10)

        frame_status_header = ctk.CTkFrame(frame_status, fg_color="transparent")
        frame_status_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(frame_status_header, text="📊 Status:",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        self.label_status = ctk.CTkLabel(
            frame_status_header, text="Aguardando início",
            font=ctk.CTkFont(size=18, weight="bold"), text_color="#94a3b8",
        )
        self.label_status.pack(side="left", padx=10)

        ctk.CTkLabel(frame_status, text="📝 Log de Atividades",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))

        self.text_log = ctk.CTkTextbox(frame_status, height=250,
                                       font=ctk.CTkFont(size=12), wrap="word")
        self.text_log.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        ctk.CTkButton(frame_status, text="🗑️ Limpar Log", command=self.limpar_log,
                      width=150, height=30, font=ctk.CTkFont(size=12)).pack(pady=(0, 15))

    def _linha_dado(self, parent, campo, valor, editavel=True):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(frame, text=f"{campo}:",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     width=120, anchor="w").pack(side="left")
        cor = "#ffffff" if editavel else "#94a3b8"
        lbl = ctk.CTkLabel(frame, text=valor,
                           font=ctk.CTkFont(size=14), anchor="w", text_color=cor)
        lbl.pack(side="left", fill="x", expand=True)
        self.labels_dados[campo] = lbl

    # ──────────────────────────────────────────
    #  Janela de edição
    # ──────────────────────────────────────────

    def abrir_janela_edicao(self):
        janela = ctk.CTkToplevel(self)
        janela.title("Editar Dados")
        janela.geometry("500x300")
        janela.grab_set()

        ctk.CTkLabel(janela, text="✏️ Editar Dados Editáveis",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        entries = []
        for i, campo in enumerate(CAMPOS_EDITAVEIS):
            frame = ctk.CTkFrame(janela, fg_color="transparent")
            frame.pack(fill="x", padx=30, pady=8)
            ctk.CTkLabel(frame, text=f"{campo}:",
                         font=ctk.CTkFont(size=14, weight="bold"),
                         width=100, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(frame, height=35, font=ctk.CTkFont(size=13))
            entry.pack(side="left", fill="x", expand=True)
            if i < len(self.dados_editaveis):
                entry.insert(0, self.dados_editaveis[i])
            entries.append(entry)

        def salvar():
            self.dados_editaveis = [e.get().strip() for e in entries]
            self.salvar_dados_editaveis()
            self.atualizar_exibicao_dados()
            self.adicionar_log("✅ Dados atualizados com sucesso!", "#22c55e")
            janela.destroy()

        frame_b = ctk.CTkFrame(janela, fg_color="transparent")
        frame_b.pack(pady=20)
        ctk.CTkButton(frame_b, text="💾 Salvar", command=salvar,
                      width=150, height=40, font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color="#22c55e", hover_color="#16a34a").pack(side="left", padx=10)
        ctk.CTkButton(frame_b, text="❌ Cancelar", command=janela.destroy,
                      width=150, height=40, font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color="#ef4444", hover_color="#dc2626").pack(side="left", padx=10)

    def atualizar_exibicao_dados(self):
        for i, campo in enumerate(CAMPOS_EDITAVEIS):
            valor = self.dados_editaveis[i] if i < len(self.dados_editaveis) else "---"
            if campo in self.labels_dados:
                self.labels_dados[campo].configure(text=valor)

    # ──────────────────────────────────────────
    #  Log / status helpers
    # ──────────────────────────────────────────

    def adicionar_log(self, mensagem, cor="#ffffff"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.text_log.insert("end", f"[{ts}] {mensagem}\n")
        self.text_log.see("end")
        self.update()

    def limpar_log(self):
        self.text_log.delete("1.0", "end")

    def atualizar_status(self, texto, cor="#ffffff"):
        self.label_status.configure(text=texto, text_color=cor)

    # ──────────────────────────────────────────
    #  Controle do bot
    # ──────────────────────────────────────────

    def iniciar_bot(self):
        if not self.BASE_URL:
            self.adicionar_log("❌ URL base não configurada!", "#ef4444")
            return
        self.bot_ativo = True
        self.btn_iniciar.configure(state="disabled")
        self.btn_atualizar_dados.configure(state="disabled")
        self.btn_parar.configure(state="normal")
        threading.Thread(target=self.executar_bot, daemon=True).start()

    def parar_bot(self):
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
            except Exception:
                pass

    def executar_bot(self):
        try:
            self.adicionar_log("🟢 Iniciando bot de formulários...")
            self.atualizar_status("🚀 Iniciando navegador...", "#3b82f6")
            self.update_idletasks()

            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")

            self.adicionar_log("📥 Baixando ChromeDriver...")
            self.update_idletasks()

            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options,
            )
            self.wait = WebDriverWait(self.driver, 30)

            self.adicionar_log("✅ Navegador iniciado!")
            self.atualizar_status("🌐 Acessando página...", "#3b82f6")
            self.driver.get(self.BASE_URL)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(1)
            self.adicionar_log("✅ Página carregada!")
            self.atualizar_status("👀 Monitorando...", "#22c55e")
            self.update_idletasks()

            contador = 0
            while self.bot_ativo:
                contador += 1
                self.adicionar_log(f"🔄 Ciclo #{contador}")
                try:
                    self.verificar_e_executar()
                except Exception as e:
                    import traceback
                    self.adicionar_log(f"⚠️ Erro no ciclo: {e}", "#f59e0b")
                    self.adicionar_log(traceback.format_exc(), "#64748b")
                if self.bot_ativo:
                    time.sleep(1)

        except Exception as e:
            import traceback
            self.adicionar_log(f"❌ Erro crítico: {e}", "#ef4444")
            self.adicionar_log(traceback.format_exc(), "#64748b")
            self.atualizar_status("❌ Erro", "#ef4444")
            self.btn_iniciar.configure(state="normal")
            self.btn_parar.configure(state="disabled")
            self.bot_ativo = False

    # ──────────────────────────────────────────
    #  Extração de formulários
    # ──────────────────────────────────────────

    def form_extract(self, driver, base_url):
        driver.get(base_url)
        time.sleep(1)
        forms = []
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'div[role="presentation"]')
                )
            )
            for div in driver.find_elements(By.CSS_SELECTOR, 'div[role="presentation"]'):
                try:
                    href = div.find_element(By.TAG_NAME, "a").get_attribute("href")
                    if href and ("forms.office.com" in href or "forms.google.com" in href):
                        forms.append(href)
                        self.adicionar_log(f"📎 Formulário encontrado: {href}")
                except Exception:
                    continue
        except Exception as e:
            self.atualizar_status("❌ Erro ao extrair formulários", "#ef4444")
            self.adicionar_log(f"Erro form_extract: {e}", "#ef4444")
        return forms

    # ──────────────────────────────────────────
    #  Preenchimento dinâmico — Google Forms
    # ──────────────────────────────────────────

    def preencher_google_form(self, form_url: str, indice: int):
        """
        Abre o formulário em nova aba, mapeia cada pergunta pelo título
        e preenche dinamicamente, independente da ordem dos campos.
        """
        todos_dados = self.obter_todos_dados()

        self.driver.execute_script("window.open(arguments[0], '_blank');", form_url)
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # Aguarda os itens do formulário
        question_items = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "[data-automation-id='questionItem']")
            )
        )

        preenchidos = 0
        nao_mapeados = []

        for item in question_items:
            try:
                # ── Lê o título da pergunta ──
                try:
                    titulo_el = item.find_element(
                        By.CSS_SELECTOR,
                        "[data-automation-id='questionTitle'] .text-format-content",
                    )
                    titulo_raw = titulo_el.text
                except Exception:
                    continue  # item sem título visível, ignora

                titulo_norm = normalizar(titulo_raw)

                # ── Encontra a chave interna pelo mapa ──
                # Pass 1: igualdade exata (evita "nome" casar com "sobrenome")
                chave_interna = MAPA_TITULO_CAMPO.get(titulo_norm)

                # Pass 2: titulo comeca com a chave
                if chave_interna is None:
                    for palavra_chave, chave in MAPA_TITULO_CAMPO.items():
                        if titulo_norm.startswith(palavra_chave):
                            chave_interna = chave
                            break

                # Pass 3: substring, apenas para chaves longas (> 4 chars)
                if chave_interna is None:
                    for palavra_chave, chave in MAPA_TITULO_CAMPO.items():
                        if len(palavra_chave) > 4 and palavra_chave in titulo_norm:
                            chave_interna = chave
                            break

                if chave_interna is None:
                    nao_mapeados.append(titulo_raw)
                    continue

                valor = todos_dados.get(chave_interna, "")
                if not valor:
                    continue

                # ── Tenta preencher: textInput → textarea ──
                campo_preenchido = False

                for seletor in (
                    "[data-automation-id='textInput']",
                    "textarea",
                    "input[type='text']",
                    "input:not([type='hidden'])",
                ):
                    try:
                        campo = item.find_element(By.CSS_SELECTOR, seletor)
                        campo.clear()
                        campo.send_keys(valor)
                        self.adicionar_log(f"   ✏️  '{titulo_raw}' → '{valor}'")
                        preenchidos += 1
                        campo_preenchido = True
                        time.sleep(0.1)
                        break
                    except Exception:
                        continue

                if not campo_preenchido:
                    nao_mapeados.append(f"{titulo_raw} (sem input encontrado)")

            except Exception as e:
                self.adicionar_log(f"   ⚠️  Erro em item: {e}", "#f59e0b")

        # Feedback de campos não mapeados
        for nm in nao_mapeados:
            self.adicionar_log(f"   ❓ Não mapeado: '{nm}'", "#94a3b8")

        self.adicionar_log(
            f"✏️  {preenchidos} campo(s) preenchido(s) no formulário {indice}"
        )

        # Volta para aba principal
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(1)

    # ──────────────────────────────────────────
    #  Loop de verificação
    # ──────────────────────────────────────────

    def verificar_e_executar(self):
        self.driver.refresh()
        self.adicionar_log("🔄 Verificando novos formulários...")

        FORMS = self.form_extract(self.driver, self.BASE_URL)

        if FORMS:
            self.adicionar_log(f"📋 {len(FORMS)} formulário(s) encontrado(s):")
            for idx, f in enumerate(FORMS, 1):
                self.adicionar_log(f"   {idx}. {f}")
        else:
            self.adicionar_log("📋 Nenhum formulário encontrado")
            return

        dados_controle = self.ler_dados_controle()
        link_atual = FORMS[0]

        if link_atual != dados_controle.get("ultimo_link"):
            self.adicionar_log("🆕 Novo formulário detectado!", "#22c55e")
            self.atualizar_status("📝 Preenchendo formulários...", "#3b82f6")

            for i, form_url in enumerate(FORMS, start=1):
                if not self.bot_ativo:
                    break
                self.adicionar_log(f"📝 Processando formulário {i}/{len(FORMS)}")
                try:
                    self.preencher_google_form(form_url, i)
                except Exception as e:
                    import traceback
                    self.adicionar_log(f"❌ Erro no formulário {i}: {e}", "#ef4444")
                    self.adicionar_log(traceback.format_exc(), "#64748b")
                    # Garante que voltamos para a aba principal em caso de erro
                    try:
                        self.driver.switch_to.window(self.driver.window_handles[0])
                    except Exception:
                        pass

            self.salvar_dados_controle(link_atual)
            self.adicionar_log("💾 Controle salvo!")
            self.atualizar_status("👀 Monitorando...", "#22c55e")
        else:
            ts = datetime.now().strftime("%H:%M:%S")
            self.adicionar_log(f"⏳ Sem atualização ({ts})")


if __name__ == "__main__":
    app = BotFormulariosApp()
    app.mainloop()