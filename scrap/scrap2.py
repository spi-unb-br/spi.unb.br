def extrair_formularios_xpath(driver, base_url):
    """
    Versão usando XPath mais específico
    """
    driver.get(base_url)
    time.sleep(3)
    
    try:
        # XPath para encontrar links dentro de divs com role="presentation"
        xpath = '//div[@role="presentation"]//a[@href]'
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        
        links = driver.find_elements(By.XPATH, xpath)
        
        formularios = []
        for link in links:
            href = link.get_attribute('href')
            if href and 'forms.' in href:  # Filtrar apenas links de formulários
                formularios.append(href)
                print(f"Formulário encontrado: {href}")
        
        return formularios
        
    except Exception as e:
        print(f"Erro: {e}")
        return []