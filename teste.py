from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://sites.google.com/view/spi-imoveis/com-cadastro-virtual")

wait = WebDriverWait(driver, 30)

# Aguarda a página carregar
wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))

# Captura TODOS os links da página
links = driver.find_elements(By.TAG_NAME, "a")

formularios = []

for link in links:
    href = link.get_attribute("href")
    texto = link.text.lower()

    if href and "form" in href.lower():
        formularios.append(href)

print(f"Total de formulários encontrados: {len(formularios)}")

# Remove duplicados
formularios = list(set(formularios))

# Abre cada formulário
for i, url in enumerate(formularios, start=1):
    print(f"Abrindo formulário {i}: {url}")
    driver.execute_script("window.open(arguments[0]);", url)
    time.sleep(3)

input("Pressione ENTER para finalizar")
driver.quit()
