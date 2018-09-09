from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

driver = webdriver.Firefox()
driver.get("https://www.deliveryextra.com.br/secoes/C312/alimentos?qt=12&p=0&gt=list")
time.sleep(10)
teste = driver.find_element_by_partial_link_text("Entrega")
teste.click()
driver.find_element_by_name("cep").send_keys("60843260")
driver.find_element_by_class_name("mt-10").click()
time.sleep(10)
driver.close()
