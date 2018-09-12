# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import mysql.connector
from Extra_produtos import *

def open_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="admin",
        passwd="12345",
        database="test"
    )
    return db

def close_connection():
    db.close()

def open_browser():
    driver = webdriver.Firefox()
    return driver

def close_browser():
    driver.close()

def set_URL(URL, driver):
    winHandleBefore = driver.current_window_handle
    driver.get(URL)
    driver.switch_to_window(winHandleBefore)
    time.sleep(5)

URL_arroz = "https://www.deliveryextra.com.br/busca?c= cat2:alimentos_arrozcomum"
URL_feijao = "https://www.deliveryextra.com.br/busca?c= cat2:alimentos_feijao"
URL_acucar = "https://www.deliveryextra.com.br/busca?c=%20cat2:alimentos_acucar"

prod = [URL_arroz, URL_feijao, URL_acucar]
db = open_connection()
driver = open_browser()
Produtos = ProdutoExtra("https://www.deliveryextra.com.br/", db,driver)

for i in prod:
    set_URL(i, driver)
    dados = Produtos.get_data()
    Produtos.list_prod(dados)

# set_URL("https://www.carrefour.com.br/arroz-e-graos?termo=%3Arelevance-nonfoodzipzone%3Anavegacao%3Aarroz-parboilizado", driver)
#
# Produtos = ProdutoCarrefour("https://www.carrefour.com.br/arroz-e-graos?termo=%3Arelevance-nonfoodzipzone%3Anavegacao%3Aarroz-parboilizado",driver)
# Produtos.get_data()
close_browser()
close_connection()