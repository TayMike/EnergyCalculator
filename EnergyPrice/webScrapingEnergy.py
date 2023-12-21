"""Web Scraping from CPFL - Brazil
Official site:
https://servicosonline.cpfl.com.br/agencia-webapp/#/taxas-tarifas/localizar-distribuidora"""

import requests
import pyautogui
import webbrowser
import pyperclip
import datetime
import os
from time import sleep

import sqlite3
from sqlite3 import Error

DELAY = 10
GREEN_FLAG = 0
YELLOW_FLAG = 0.01874
RED_FLAG = 0.03971
WATER_SCARCITY_FLAG = 0.09492

def findImage(file: str, locationX: int, locationY: int) -> None:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    location = pyautogui.locateCenterOnScreen(f'{dir_path}\\img\\{file}', grayscale=True, confidence=0.8)
    pyautogui.moveTo(location[0] + locationX, location[1] + locationY)

def loadImage(file: str, locationX: int = 0, locationY: int = 0) -> bool:
    now = datetime.datetime.now()
    while True:
        try:
            findImage(file, locationX, locationY)
            return True
        except:
            if datetime.datetime.now() - now >= datetime.timedelta(seconds=DELAY):
                return False
            else:
                continue

def main():
    """TODO Explain the core"""

    """Take captcha token"""
    # webbrowser.open("https://servicosonline.cpfl.com.br/agencia-webapp/#/taxas-tarifas/localizar-distribuidora")
    # loadImage('captcha.png')
    # pyautogui.press('f12')
    # sleep(5)
    # loadImage('network.png')
    # pyautogui.click()
    # loadImage('captcha.png')
    # pyautogui.click()
    # sleep(60)
    # loadImage('filter_network.png', locationY=25)
    # pyautogui.click(clicks=3, interval=0.25)
    # pyautogui.write('token')
    # loadImage('token_network.png')
    # pyautogui.click()
    # loadImage('response_network.png')
    # pyautogui.click()
    # loadImage('response_network.png', locationY=30)
    # pyautogui.click(clicks=3, interval=0.25)
    # pyautogui.hotkey(('ctrl', 'c'))
    # token = pyperclip.paste()
    # token = token[1:len(token) - 1]
    # pyautogui.hotkey(('ctrl', 'w'))

    try:
        # Token is valid by 15 minutes
        header = {'Clientid': 'agencia-virtual-cpfl-web', 'Captcha-Token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJDYXB0Y2hhVmFsaWRvIjoiUyIsImNsaWVudElkIjoiYWdlbmNpYS12aXJ0dWFsLWNwZmwtd2ViIiwiQ2FwdGNoYUhvc3ROYW1lIjoic2Vydmljb3NvbmxpbmUuY3BmbC5jb20uYnIiLCJpc3MiOiJodHRwczovL3NlcnZpY29zb25saW5lLmNwZmwuY29tLmJyLyIsImF1ZCI6ImFnZW5jaWEtdmlydHVhbC1jcGZsLXdlYiIsImV4cCI6MTcwMzE5MzA3MSwibmJmIjoxNzAzMTkyNDcxfQ.UxNXe8k9z-LVwJz9VkqCMBe6DNu6Bq_ZjVQsZdA0_X0"}

        states = requests.get('https://servicosonline.cpfl.com.br/agencia-webapi/api/estado?apenasConcessao=true', headers=header).json()
        conn = sqlite3.connect('EnergyPrice\\EnergyBD.db')
        stmt = conn.cursor()
        res = stmt.execute("SELECT name FROM sqlite_master WHERE name='state'")
        if res.fetchone() is None:
            stmt.execute("CREATE TABLE state(id, name)")
        stmt.executemany("INSERT INTO state VALUES(:Codigo, :Nome)", states['Estados'])
        conn.commit()
        for state in states['Estados']:
            cities = requests.get(f"https://servicosonline.cpfl.com.br/agencia-webapi/api/estado/{state['Codigo']}/municipio?apenasConcessao=true", headers=header).json()
            res = stmt.execute("SELECT name FROM sqlite_master WHERE name='city'")
            if res.fetchone() is None:
                stmt.execute("CREATE TABLE city(id, name, flag, company, validityperiod, state)")
            for city in cities['Municipios']:
                city['UF'] = state['Codigo']
                dataPost = {'CodMunicipio': city['Codigo']}
                table = requests.post(f'https://servicosonline.cpfl.com.br/agencia-webapi/api/taxas-tarifas/validar-situacao', json=dataPost, headers=header).json()
            stmt.executemany("INSERT INTO city VALUES(:Codigo, :Nome, :UF)", cities['Municipios'])
            conn.commit()
    except ConnectionError as e:
        e.with_traceback()
    finally:
        if (stmt):
            stmt.close()
        if (conn):
            conn.close()

main()