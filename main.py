from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import csv


# Constantes
SELETOR_PAGINA_ATUAL = (By.XPATH, f"//ul[contains(@class, 'pagination')]/li[contains(@class, 'active')]/a")
PAGINA_INICIAL = 1 # Pagina crescente ele ira skipar ate o numero da pagina informaca
NUMERO_TOTAL_PAGINAS = 20 # Alterar para o numero total de paginas
NUMERO_TOTAL_ITENS_POR_PAGINA = 12 # Default 12, Maximo 1000


# Criacao do driver e carregamento da pagina inicial
options = webdriver.ChromeOptions()
# Salva a sessao do usuario na pasta
options.add_argument('user-data-dir=C:\\scrapper-placa-renavam')
driver = webdriver.Chrome('./chromedriver', options=options)
driver.get("https://portalservicos.denatran.serpro.gov.br/#/meusVeiculos")

def getSeletorPaginaAtiva(num_pagina): return (By.XPATH, f"//ul[contains(@class, 'pagination')]/li[contains(@class, 'active')]/a[text() = '{num_pagina}']")

def getSeletorUltimaPaginaAtiva(): return (By.XPATH, f"//ul[contains(@class, 'pagination')]/li[contains(@class, 'active')]/a[text() != '1']")

# Espera o elemento com o seletor aparecer na pagina
def wait_and_find_element(selector, time_in_sec=90):
    return WebDriverWait(driver, time_in_sec).until(EC.visibility_of_element_located(selector))

# Extrai a placa e o renavam do html do span
def extract_placa_and_renavan(html_bruto):
    html_sem_espacos = re.sub(r'\s', '', html_bruto)
    return re.search('</span>(\w+)</div>.+</span>(\w+)</div>', html_sem_espacos, re.IGNORECASE).groups()

# Obtem o numero da pagina atual
def get_pagina_atual():
    return int(driver.find_element(by=SELETOR_PAGINA_ATUAL[0], value=SELETOR_PAGINA_ATUAL[1]).get_attribute('innerHTML'))

def ir_para_pagina(numero_pagina):
    driver.execute_script(f'angular.element("ul.pagination").scope().paginacaoOnClick({numero_pagina});')
    wait_and_find_element(getSeletorPaginaAtiva(numero_pagina))

def definir_tamanho_maximo_pagina():
    driver.execute_script(f'angular.element("ul.pagination").scope().tamanhoPagina={NUMERO_TOTAL_ITENS_POR_PAGINA}')

def scrape_pagina(writer, numero_pagina, qtd_tentativas=0):
    try:
        proxima_pagina = str(numero_pagina+1)
       
        print("Extraindo pagina:", numero_pagina)
        placas_renavam = driver.find_elements_by_css_selector(".veiculo .info")

        for pr in placas_renavam:
            conteudo_pr = pr.get_attribute('innerHTML')
            placa, renavan = extract_placa_and_renavan(conteudo_pr)
            if placa != 'Placa':
                writer.writerow([numero_pagina, placa, renavan])

            # Click na pagina
            ir_para_pagina(proxima_pagina)
    except Exception as error:
        print("Ocorreu um erro. Analise e mude os valores caso queira continuar", error)
        if qtd_tentativas < 5:
            print("Tentando processar novamente")
            scrape_pagina(writer=writer, numero_pagina=numero_pagina, qtd_tentativas=qtd_tentativas + 1)
        else:
            raise error


# MAIN
with open("./placas_renavam.csv", 'a') as f:
    writer = csv.writer(f)
    
    # Configuracao do maximo de itens por pagina
    wait_and_find_element(getSeletorPaginaAtiva(1))
    definir_tamanho_maximo_pagina()
    ir_para_pagina(1)
    
    for num_pagina in range(PAGINA_INICIAL, NUMERO_TOTAL_PAGINAS + 1):
        scrape_pagina(writer=writer, numero_pagina=num_pagina)

