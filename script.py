from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook
import pandas

def raspagem(itemBusca, nomeArquivo):

    site = 'https://www.mercadolivre.com.br/'

    busca = itemBusca
    
    pastaTrabalho = Workbook()

    planilha = pastaTrabalho.active

    opc = webdriver.ChromeOptions()
    opc.add_argument('--headless')

    chorm = webdriver.Chrome(executable_path='chromedriver',chrome_options=opc)
    chorm.implicitly_wait(3)
    chorm.get(site)

    chorm.find_element(By.XPATH,'//*[@id="cb1-edit"]').send_keys(busca)
    chorm.find_element(By.XPATH,'/html/body/header/div/div[2]/form/button').click()

    Produtos = chorm.find_elements(By.CLASS_NAME,'ui-search-layout__item.shops__layout-item')

    planilha['A1'] =  "Nome do Produto"
    planilha['B1'] =  "Preço do Produto"
    planilha['C1'] =  "Link do Produto"

    for i in range(len(Produtos)):
        linha = i + 2
    
        try:
            planilha[f'A{linha}'] = chorm.find_element(By.XPATH,f'//*[@id="root-app"]/div/div[2]/section/ol/li[{linha}]/div/div/div[2]/div[1]/a[1]/h2').get_attribute('innerText')
            planilha[f'B{linha}'] = chorm.find_element(By.XPATH,f'//*[@id="root-app"]/div/div[2]/section/ol/li[{linha}]/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div/span[1]/span[2]/span[2]').get_attribute('innerText')
            planilha[f'C{linha}'] = chorm.find_element(By.XPATH,f'//*[@id="root-app"]/div/div[2]/section/ol/li[{linha}]/div/div/div[2]/div[1]/a[1]').get_attribute('href')
        except:
            continue
        finally:
            print(f'Loading... {round((i+1)/(len(Produtos)+1)*100,2)}%\n')
            
    chorm.quit()
    
    pastaTrabalho.save(f'{nomeArquivo}.xlsx')

    arquivo = pandas.read_excel(f'{nomeArquivo}.xlsx')
    print(arquivo)
