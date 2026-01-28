from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def extrair_formularios(driver, base_url):
    """
    Extrai os links dos formulários da página
    """
    # Acessar a página base
    driver.get(base_url)
    
    # Aguardar a página carregar completamente
    time.sleep(3)  # Ajuste conforme necessário
    
    # Encontrar todas as divs com role="presentation" que contêm os links
    try:
        # Aguardar os elementos estarem presentes
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="presentation"]'))
        )
        
        # Extrair todos os links dentro dessas divs
        formularios = []
        
        # Buscar pela div com role="presentation" e depois o link dentro dela
        divs_presentation = driver.find_elements(By.CSS_SELECTOR, 'div[role="presentation"]')
        
        for div in divs_presentation:
            try:
                # Procurar por links dentro da div
                link = div.find_element(By.TAG_NAME, 'a')
                href = link.get_attribute('href')
                
                # Verificar se é um link de formulário do Google/Office Forms
                if href and ('forms.office.com' in href or 'forms.google.com' in href):
                    formularios.append(href)
                    print(f"Formulário encontrado: {href}")
            except:
                continue
        
        return formularios
        
    except Exception as e:
        print(f"Erro ao extrair formulários: {e}")
        return []

# Uso no seu código principal
def main():
    # Configurar o driver
    service = Service('caminho/para/chromedriver')  # Ajuste o caminho
    driver = webdriver.Chrome(service=service)
    
    try:
        base_url = "https://sites.google.com/view/spi-imoveis/com-cadastro-virtual"  # Sua URL base
        
        # Extrair os formulários dinamicamente
        FORMULARIOS = extrair_formularios(driver, base_url)
        
        if not FORMULARIOS:
            print("Nenhum formulário encontrado!")
            return
        
        print(f"\n{len(FORMULARIOS)} formulários encontrados:")
        for i, form in enumerate(FORMULARIOS, 1):
            print(f"{i}. {form}")
        
        # Agora processar cada formulário
        for idx, form_url in enumerate(FORMULARIOS, 1):
            print(f"\nProcessando formulário {idx}/{len(FORMULARIOS)}")
            driver.get(form_url)
            time.sleep(2)
            
            # Seu código de preenchimento aqui
            # ...
            
    finally:
        driver.quit()

if __name__ == "__main__":
    main()