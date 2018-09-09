# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import mysql.connector
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  passwd="12345",
  database="test"
)

mycursor = mydb.cursor()

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
#c = csv.writer(open("produtos.csv", "w"))
#c.writerow(['Nome', 'Subcategoria', 'Peso', 'Fabricante', 'Preco'])
for rice in rice_list:
    name = rice['produto-nome']
    preco = rice['produto-preco']
    fabricante = rice['produto-fabricante']
    p_qtd = rice['produto-qtd']
    p_sku = rice['produto-sku']
    p_ruptura = rice['ruptura']
    subcategoria = rice['subcategoria']
    if name and preco and p_ruptura=="Falso":
        #CategorizarPorTipo
        if str(name).find("Parboilizado") != -1:
            subcategoria = "Arroz Parboilizado"
        elif str(name).find("Agulhinha") != -1:
            subcategoria = "Arroz Agulhinha"
        elif str(name).find("Integral") != -1:
            subcategoria = "Arroz Integral"
        elif str(name).find("Risoto") != -1:
            subcategoria = "Risoto"
        elif str(name).find("Orgânico") != -1:
            subcategoria = "Orgânico"
        else:
            subcategoria = "Outros"
        #CategorizarPorPeso
        peso_text = str(name)[::-1]
        peso_text = peso_text.split()
        peso = peso_text[0]
        peso = peso[::-1]
        #CategorizarPorFabricante
        print("======================================")
        if str(name).find("URBANO") != -1:
            fabricante = "URBANO"
        elif str(name).find("TIO JOÃO") != -1:
            fabricante = "TIO JOÃO"
        elif str(name).find("PASTAROTTI") != -1:
            fabricante = "PASTAROTTI"
        elif str(name).find("BIJU") != -1:
            fabricante = "BIJU"
        elif str(name).find("PANTERA") != -1:
            fabricante = "PANTERA"
        elif str(name).find("PILECO NOBRE") != -1:
            fabricante = "PILECO NOBRE"
        elif str(name).find("CAMIL") != -1:
            fabricante = "CAMIL"
        elif str(name).find("LA PASTINA") != -1:
            fabricante = "LA PASTINA"
        elif str(name).find("RÁRIS") != -1:
            fabricante = "RÁRIS"
        elif str(name).find("CASINO") != -1:
            fabricante = "CASINO"
        elif str(name).find("BLUE VILLE") != -1:
            fabricante = "BLUE VILLE"
        elif str(name).find("QUALITÁ") != -1:
            fabricante = "QUALITÁ"
        elif str(name).find("PRATO FINO") != -1:
            fabricante = "PRATO FINO"
        elif str(name).find("Organic") != -1:
            fabricante = "Organic"
        print('Name: %s' % (name))
        print('Price: %s' % (preco))
        print('Qtd: %s' % (p_qtd))
        print('Subcategoria: %s' % (subcategoria))
        print('Peso: %s' % (peso))
        print('Fabricante: %s' % (fabricante))
        #c.writerow([name,subcategoria,peso,fabricante,preco])
        mycursor.execute("SELECT * from Produtos where Nome ='" + name + "' and IdMercado = 4")

        if mycursor.fetchone() != None:
            mycursor.execute(
                "UPDATE Produtos set preco = '"+preco+"' where IdMercado = 4 and Nome = '"+name+"'")
        else:
            mycursor.execute("INSERT INTO Produtos (Nome, Categoria, Subcategoria, Fabricante, Preco, Peso, Quantidade, IdMercado)"
                         " VALUES ('" + str(name) + "', 'Alimentos', '"+ str(subcategoria) +"', '"+ str(fabricante) +"', '"+ str(preco) +"','"+str(peso)+"','"+str(p_qtd)+"', 4)")

        mydb.commit()

mydb.close()
driver.close()
