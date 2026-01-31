from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import json
import os
import time
from datetime import datetime

from form_extract import form_extract

# ================= CONFIGURAÇÃO =================
# BASE_URL = "https://sites.google.com/view/spi-imoveis/com-cadastro-virtual"
BASE_URL = "http://127.0.0.1:5500/html/index.html"


# Dados para preencher
DADOS = [
    "Luciana",
    "Freitas",
    "45994951404",
    "lmfreitas864@gmail.com",
    "991748889",
    "61"
]


options = webdriver.ChromeOptions()
    
# Instala automaticamente o chromedriver correto
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
    )

options.add_argument("--start-maximized")

# driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)

try:
    print("🟢 Abrindo página base do Google Sites...")
    driver.get(BASE_URL)
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)
    
    # FORMS = form_extract(driver, BASE_URL) 
    # print(f"🟢 {len(FORMS)} formulários extraídos.")
    
    
    ### Comparar os dados 
    
    def ler_dados(arquivo='dados.json'):
        if os.path.exists(arquivo):
            with open(arquivo, 'r') as f:
                return json.load(f)
        return {'ultimo_link': None, 'ultima_atualizacao': None}
    
    def salvar_dados(link, arquivo='dados.json'):
        dados = {
            'ultimo_link': link,
            'ultima_atualizacao': datetime.now().isoformat()
        }
        with open(arquivo, 'w') as f:
            json.dump(dados, f, indent=2)
            
            
    def verificar_e_executar():
        driver.refresh()
        
        FORMS = form_extract(driver, BASE_URL) 
        print(f"🟢 {len(FORMS)} formulários extraídos.")
        
        dados = ler_dados()
        link_atual = FORMS[0]  # Supondo que o primeiro link seja o relevante
        
        print(f"Dados lidos: {dados} \n\n")
        print(f"Link atual: {link_atual}")
        
        if link_atual != dados['ultimo_link']:
            
            print(f"Novo link encontrado em {datetime.now()}")
            # Itera pelos formulários
            for i, form_url in enumerate(FORMS, start=1):
                print(f"🟢 Processando formulário {i}")

                # 1️⃣ Abrir nova aba com o formulário
                driver.execute_script("window.open(arguments[0], '_blank');", form_url)
                driver.switch_to.window(driver.window_handles[-1])

                # 2️⃣ Preencher o formulário
                inputs = wait.until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
                )

                for campo, valor in zip(inputs, DADOS):
                    campo.send_keys(valor)
                    time.sleep(0.1)

                # 3️⃣ Clicar no botão enviar
                send_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button"))
                )
                driver.execute_script("arguments[0].click();", send_button)
                print(f"✅ Formulário {i} enviado")

                # 4️⃣ Voltar para a aba da página base
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)  # Pequena pausa para estabilidade

            print("🟢 Todos os formulários foram processados.")
            print("🔵 O navegador permanecerá aberto para auditoria visual.")

            # Mantém o navegador aberto indefinidamente
            input("Pressione ENTER no terminal para encerrar o robô...")
            
            
            salvar_dados(link_atual)
            return True
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Nenhuma atualização")
            return False

    def monitorar_continuamente():
        print("Iniciando monitoramento...")
        while True:
            try:
                verificar_e_executar()
            except Exception as e:
                print(f"Erro: {e}")
            
            time.sleep(2)  # Aguarda 2 segundos antes da próxima verificação

    # Executar
    monitorar_continuamente()

    

except Exception as e:
    print("❌ Erro durante execução:", e)
    input("Pressione ENTER para encerrar...")

finally:
    print("🟢 Processo finalizado (navegador mantido aberto)")
