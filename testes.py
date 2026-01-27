from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)

try:
    # 1️⃣ Abre o site principal
    driver.get("https://sites.google.com/view/spi-imoveis/com-cadastro-virtual")

    # 2️⃣ Aguarda a página carregar
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3)

    # 3️⃣ Busca links
    links = driver.find_elements(By.TAG_NAME, "a")
    formularios = []

    for link in links:
        if "Formulário para o Cadastro Virtual" in link.text:
            formularios.append(link)

    if not formularios:
        raise Exception("❌ Nenhum botão de formulário encontrado.")

    print(f"✅ {len(formularios)} formulário(s) encontrado(s)")

    # 4️⃣ Clica no primeiro formulário
    driver.execute_script("arguments[0].scrollIntoView(true);", formularios[0])
    time.sleep(1)
    driver.execute_script("arguments[0].click();", formularios[0])

    # 5️⃣ Abre formulário de teste
    driver.get(
        "https://forms.office.com/pages/responsepage.aspx?"
        "id=h7AshbEn8k6d6XnH7IOQsV1sPT3CUK9NovOoG_WqCMtUNDEzTkxDNUozMk5XMlY5S0NTT0RQNERaSS4u"
    )

    # 6️⃣ Aguarda campos
    inputs = wait.until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "input"))
    )

    dados = [
        "Luciana",
        "Freitas",
        "45994951404",
        "lmfreitas864@gmail.com",
        "lmfreitas864@gmail.com",
        "991748889",
        "61"
    ]

    for campo, valor in zip(inputs, dados):
        campo.send_keys(valor)
        time.sleep(0.3)

    # 7️⃣ Enviar formulário
    botao_enviar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button"))
    )
    driver.execute_script("arguments[0].click();", botao_enviar)

    print("✅ Formulário enviado com sucesso")

    # 🔒 Mantém aberto indefinidamente
    print("🟢 Processo concluído.")
    print("🔵 Navegador permanecerá aberto. Feche manualmente para encerrar.")
    input("Pressione ENTER no terminal para finalizar o robô...")

except Exception as e:
    print("❌ Erro durante execução:", e)
    input("Erro detectado. Pressione ENTER para encerrar...")

finally:
    print("🟢 Processo finalizado (navegador mantido aberto)")
