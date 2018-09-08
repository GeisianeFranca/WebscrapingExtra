from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

driver = webdriver.Firefox()
driver.get("https://www.deliveryextra.com.br/busca?c= cat2:alimentos_arrozcomum")
time.sleep(10)

filter_text = str(driver.find_element_by_class_name("filter").text)
filter_list = filter_text.split()

while filter_list[1] != filter_list[3]:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)
    filter_text = str(driver.find_element_by_class_name("filter").text)
    filter_list = filter_text.split()

data = driver.find_element_by_class_name("product-list-wrapper")
html = data.get_attribute("innerHTML")
soup = BeautifulSoup(html, "html.parser")
rice_list = soup.findAll('div', class_='panel-product')
c = csv.writer(open("produtos.csv", "w"))
c.writerow(['Nome', 'Preco'])
for rice in rice_list:
    name = rice['produto-nome']
    preco = rice['produto-preco']
    fabricante = rice['produto-fabricante']
    p_qtd = rice['produto-qtd']
    p_sku = rice['produto-sku']
    p_ruptura = rice['ruptura']
    subcategoria = rice['subcategoria']
    if name and preco and p_ruptura=="Falso":
        print('Name: %s' % (name))
        print('Price: %s' % (preco))
        print('Qtd: %s' % (p_qtd))
        print('Sku: %s' % (p_sku))
        print('Ruptura: %s' % (p_ruptura))
        print('subcategoria: %s' % (subcategoria))
        print('Fab: %s\n' %(fabricante))
        c.writerow([name,preco])
print(len(rice_list))
driver.close()
