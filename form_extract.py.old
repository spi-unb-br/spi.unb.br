import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


    
# Extrai os links dos formulários da página
    
    
def form_extract(driver, base_url):

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
                    print(f"Formulário encontrado: {href}\n")
            except:
                continue
        
        return forms
        
    except Exception as e:
        print(f"Erro ao extrair formulários: {e}")
        return []
