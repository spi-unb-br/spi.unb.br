def extrair_formularios_robusto(driver, base_url):
    """
    Versão mais robusta com múltiplas estratégias
    """
    driver.get(base_url)
    
    # Aguardar carregamento
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    time.sleep(2)
    
    formularios = []
    
    # Estratégia 1: Buscar por role="presentation"
    try:
        elementos = driver.find_elements(By.CSS_SELECTOR, 'div[role="presentation"] a[href*="forms"]')
        formularios.extend([el.get_attribute('href') for el in elementos if el.get_attribute('href')])
    except:
        pass
    
    # Estratégia 2: Buscar diretamente por links de formulários
    if not formularios:
        try:
            elementos = driver.find_elements(By.CSS_SELECTOR, 'a[href*="forms.office.com"], a[href*="forms.google.com"]')
            formularios.extend([el.get_attribute('href') for el in elementos if el.get_attribute('href')])
        except:
            pass
    
    # Remover duplicatas mantendo a ordem
    formularios = list(dict.fromkeys(formularios))
    
    return formularios