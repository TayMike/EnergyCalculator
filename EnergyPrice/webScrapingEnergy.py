from bs4 import BeautifulSoup
import requests

html = requests.get("https://servicosonline.cpfl.com.br/agencia-webapp/#/taxas-tarifas/localizar-distribuidora").content

soup = BeautifulSoup(html, 'html.parser')

print(soup.prettify())

GREEN_FLAG = 0
YELLOW_FLAG = 0.01874
RED_FLAG = 0.03971
WATER_SCARCITY_FLAG = 0.09492