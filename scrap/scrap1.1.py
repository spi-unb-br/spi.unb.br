from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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


def preencher_formulario(driver, form_url):
    """
    Função para preencher um formulário específico
    Adicione aqui sua lógica de preenchimento
    """
    print(f"\n>>> Acessando formulário: {form_url}")
    driver.get(form_url)
    time.sleep(3)
    
    # AQUI VAI SEU CÓDIGO DE PREENCHIMENTO
    # Exemplo:
    # campo_nome = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    # campo_nome.send_keys("Meu Nome")
    # etc...
    
    print(">>> Formulário preenchido!")


def main():
    # Configurar o driver do Chrome
    options = webdriver.ChromeOptions()
    
    # Instala automaticamente o chromedriver correto
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
      )
    # options.add_argument('--headless=new')  # Descomente para rodar sem abrir janela
    
    # Se você já tem o chromedriver instalado no PATH, apenas:
    
    # OU se você baixou o chromedriver manualmente:
    # service = Service('caminho/completo/para/chromedriver')
    # driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # URL base onde estão os links dos formulários
        base_url = "https://sites.google.com/view/spi-imoveis/com-cadastro-virtual"  # Coloque a URL correta aqui
        
        print("=" * 60)
        print("INICIANDO EXTRAÇÃO DE FORMULÁRIOS")
        print("=" * 60)
        
        # Extrair os formulários dinamicamente
        FORMULARIOS = extrair_formularios(driver, base_url)
        
        print(FORMULARIOS)
        
        if not FORMULARIOS:
            print("\n⚠️  ATENÇÃO: Nenhum formulário encontrado!")
            print("Verifique se a URL está correta e se os elementos existem na página.")
            return
        
        print(f"\n✅ {len(FORMULARIOS)} formulário(s) encontrado(s):")
        print("-" * 60)
        for i, form in enumerate(FORMULARIOS, 1):
            print(f"{i}. {form}")
        print("-" * 60)
        
        # Processar cada formulário
        for idx, form_url in enumerate(FORMULARIOS, 1):
            print(f"\n{'=' * 60}")
            print(f"PROCESSANDO FORMULÁRIO {idx}/{len(FORMULARIOS)}")
            print(f"{'=' * 60}")
            
            preencher_formulario(driver, form_url)
            
            # Pequena pausa entre formulários
            time.sleep(2)
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS FORMULÁRIOS FORAM PROCESSADOS!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Aguardar antes de fechar (para você ver o resultado)
        print("\nFechando navegador em 5 segundos...")
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    main()
    