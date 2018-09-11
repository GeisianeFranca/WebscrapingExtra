# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import mysql.connector
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

class Produto(object):

    def __init__(self,URL):
        self.URL = URL
        self.produc_list = []
        self.db = mysql.connector.connect(
            host="localhost",
            user="admin",
            passwd="12345",
            database="test"
        )
        self.list_tipo = ["Parboilizado", "Agulhinha", "Integral", "Risoto", "Orgânico", "Basmati", "Carioca", "Preto",
                          "Branco", "Vermelho", "Fradinho"]
        self.list_fabricante = ["URBANO", "TIO JOÃO", "PASTAROTTI", "BIJU", "PANTERA", "CAMIL", "LA PASTINA", "RÁRIS", "BLUE VILLE",
                                "CASINO", "QUALITÁ", "PRATO FINO", "PILECCO NOBRE", "PILECO NOBRE", "Organic", "KI CALDO",
                                "SUPER MÁXIMO", "SUPER MAXIMO", "YOKI", "VAPZA"]
        self.list_subcategoria = ["arroz", "feijao"]
        self.cursor = self.db.cursor(buffered=True)

    def set_URL(self, URL):
        self.URL = URL
        winHandleBefore = self.driver.current_window_handle
        self.driver.get(URL)
        self.driver.switch_to_window(winHandleBefore)
        time.sleep(5)

    def open_browser(self):
        self.driver = webdriver.Firefox()
        self.driver.get(self.URL)

    def get_data(self):
        filter_text = str(self.driver.find_element_by_class_name("filter").text)
        filter_list = filter_text.split()
        while filter_list[1] != filter_list[3]:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            filter_text = str(self.driver.find_element_by_class_name("filter").text)
            filter_list = filter_text.split()
        data = self.driver.find_element_by_class_name("product-list-wrapper")
        html = data.get_attribute("innerHTML")
        soup = BeautifulSoup(html, "html.parser")
        product_list = soup.findAll('div', class_='panel-product')
        return product_list

    def def_subcategoria(self):
        self.subcategoria = "Outro"
        for i in self.list_subcategoria:
            if str(self.URL).find(i) != -1:
                self.subcategoria = i
        return self.subcategoria

    def def_peso(self):
        peso_text = str(self.nome)[::-1]
        peso_text = peso_text.split()
        self.peso = peso_text[0]
        self.peso = self.peso[::-1]
        return self.peso

    def def_tipo(self):
        self.tipo = "Outro"
        for i in self.list_tipo:
            if str(self.nome).find(i) != -1:
                self.tipo = i
        return self.tipo

    def def_fabricante(self):
        self.fabricante = "Outro"
        for i in self.list_fabricante:
            if str(self.nome).find(i) != -1:
                self.fabricante = i
        return self.fabricante

    def list_prod(self, product_list):
        for product in product_list:
            self.nome = product['produto-nome']
            self.preco = product['produto-preco']
            self.fabricante = self.def_fabricante()
            self.p_qtd = product['produto-qtd']
            p_sku = product['produto-sku']
            self.p_ruptura = product['ruptura']
            self.subcategoria = self.def_subcategoria()
            if self.nome and self.preco and self.p_ruptura=="Falso":
                print("=========================")
                print("Nome: %s" %(self.nome))
                print("Preco: %s" %(self.preco))
                print("Fabricante: %s" % (self.def_fabricante()))
                print("Quantidade: %s" % (self.p_qtd))
                print("Subcategoria: %s" % (self.def_subcategoria()))
                print("Tipo: %s" % (self.def_tipo()))
                print("Peso: %s" % (self.def_peso()))
                self.cursor.execute("SELECT * from Produtos where Nome ='" + self.nome + "' and IdMercado = 4")
                if self.cursor.fetchone() != None:
                    self.cursor.execute(
                        "UPDATE Produtos set preco = '" + self.preco + "' where IdMercado = 4 and Nome = '" + self.nome + "'")
                else:
                    self.cursor.execute(
                        "INSERT INTO Produtos (Nome, Categoria, Subcategoria, Fabricante, Preco, Peso, Quantidade, IdMercado, tipo)"
                        " VALUES ('" + str(self.nome) + "', 'Alimentos', '" + str(self.def_subcategoria()) + "', '" + str(
                            self.def_fabricante()) + "', '" + str(self.preco) + "','" + str(self.def_peso()) + "','" + str(
                            self.p_qtd) + "', 4, '" + str(self.def_tipo()) + "')")

                self.db.commit()

    def close_browser(self):
        self.driver.close()




URL_arroz = "https://www.deliveryextra.com.br/busca?c= cat2:alimentos_arrozcomum"
URL_feijao = "https://www.deliveryextra.com.br/busca?c= cat2:alimentos_feijao"

prod = [URL_arroz, URL_feijao]

Produtos = Produto("https://www.deliveryextra.com.br/")
Produtos.open_browser()

for i in prod:
    Produtos.set_URL(i)
    dados = Produtos.get_data()
    Produtos.list_prod(dados)

Produtos.close_browser()