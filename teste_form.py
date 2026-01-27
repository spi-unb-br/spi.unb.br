from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ================= CONFIGURAÇÃO =================
BASE_URL = "https://sites.google.com/view/spi-imoveis/com-cadastro-virtual"

# Links de teste dos formulários (simulando os botões)
FORMULARIOS = [
    "https://forms.office.com/Pages/ResponsePage.aspx?id=h7AshbEn8k6d6XnH7IOQsV1sPT3CUK9NovOoG_WqCMtUNDEzTkxDNUozMk5XMlY5S0NTT0RQNERaSS4u",
    "https://forms.office.com/Pages/ResponsePage.aspx?id=h7AshbEn8k6d6XnH7IOQsV1sPT3CUK9NovOoG_WqCMtUMkRNQ0ExNFpMMkJBREFVMzFUSTRLRE5aTS4u",
    "https://forms.office.com/Pages/ResponsePage.aspx?id=h7AshbEn8k6d6XnH7IOQsV1sPT3CUK9NovOoG_WqCMtUMDMxQTlOOFpSUTUxT0JTNVFGOEZFNzdZMS4u",
    "https://forms.office.com/Pages/ResponsePage.aspx?id=h7AshbEn8k6d6XnH7IOQsV1sPT3CUK9NovOoG_WqCMtUN09OSVE0MUFRMkJTMDUyQlFWTEhITklUSC4u"
]

# Dados para preencher
DADOS = [
    "Luciana",
    "Freitas",
    "45994951404",
    "lmfreitas864@gmail.com",
    "991748889",
    "61"
]
# ===============================================

service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)

try:
    print("🟢 Abrindo página base do Google Sites...")
    driver.get(BASE_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)

    # Itera pelos formulários
    for i, form_url in enumerate(FORMULARIOS, start=1):
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
        botao_enviar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button"))
        )
        driver.execute_script("arguments[0].click();", botao_enviar)
        print(f"✅ Formulário {i} enviado")

        # 4️⃣ Voltar para a aba da página base
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)  # Pequena pausa para estabilidade

    print("🟢 Todos os formulários foram processados.")
    print("🔵 O navegador permanecerá aberto para auditoria visual.")

    # Mantém o navegador aberto indefinidamente
    input("Pressione ENTER no terminal para encerrar o robô...")

except Exception as e:
    print("❌ Erro durante execução:", e)
    input("Pressione ENTER para encerrar...")

finally:
    print("🟢 Processo finalizado (navegador mantido aberto)")
