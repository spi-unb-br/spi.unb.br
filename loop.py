import json
import os
import time
from datetime import datetime

from form_extract import form_extract

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
    dados = ler_dados()
    link_atual = form_extract(driver, BASE_URL)[0]  # Supondo que o primeiro link seja o relevante
    
    if link_atual != dados['ultimo_link']:
        print(f"Novo link encontrado em {datetime.now()}")
        executar_funcao_principal()
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
        
        time.sleep(1)  # Aguarda 1 segundo antes da próxima verificação

# Executar
monitorar_continuamente()