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
    webbrowser.open("https://servicosonline.cpfl.com.br/agencia-webapp/#/taxas-tarifas/localizar-distribuidora")
    loadImage('captcha.png')
    pyautogui.press('f12')
    sleep(5)
    loadImage('network.png')
    pyautogui.click()
    loadImage('captcha.png')
    pyautogui.click()
    loadImage('provingSuccess.png')
    loadImage('filter_network.png', locationY=25)
    pyautogui.click(clicks=3, interval=0.25)
    pyautogui.write('token')
    loadImage('token_network.png')
    pyautogui.click()
    loadImage('response_network.png')
    pyautogui.click()
    loadImage('response_network.png', locationY=30)
    pyautogui.click(clicks=3, interval=0.25)
    pyautogui.hotkey(('ctrl', 'c'))
    token = pyperclip.paste()
    token = token[1:len(token) - 1]
    pyautogui.hotkey(('ctrl', 'w'))

    try:
        # Token is valid by 15 minutes
        header = {'Clientid': 'agencia-virtual-cpfl-web', 'Captcha-Token': token}
        states = requests.get('https://servicosonline.cpfl.com.br/agencia-webapi/api/estado?apenasConcessao=true', headers=header).json()
        # Connection with database
        conn = sqlite3.connect('EnergyPrice\\EnergyBD.db')
        stmt = conn.cursor()
        # Verify if exists table state
        res = stmt.execute("SELECT name FROM sqlite_master WHERE name='state'")
        compare = res.fetchone()
        if compare is None:
            stmt.execute("CREATE TABLE state(id, name)")
            stmt.executemany("INSERT INTO state VALUES(:Codigo, :Nome)", states['Estados'])
            conn.commit()
        for state in states['Estados']:
            cities = requests.get(f"https://servicosonline.cpfl.com.br/agencia-webapi/api/estado/{state['Codigo']}/municipio?apenasConcessao=true", headers=header).json()
            # Verify if exists table city
            res = stmt.execute("SELECT name FROM sqlite_master WHERE name='city'")
            compare = res.fetchone()
            if compare is None:
                stmt.execute("CREATE TABLE city(id, name, flag, company, validityperiod, state)")
            for city in cities['Municipios']:
                # Verify if the info of the city already exist in database
                name = 'FeeList' + city['Codigo'] + state['Codigo']
                sql = "SELECT name FROM sqlite_master WHERE name='{}'".format(name)
                res = stmt.execute(sql)
                compare = res.fetchone()
                if compare is None:
                    # Collect data about the city
                    dataPost = {'CodMunicipio': city['Codigo']}
                    dataCity = requests.post(f'https://servicosonline.cpfl.com.br/agencia-webapi/api/taxas-tarifas/validar-situacao', json=dataPost, headers=header).json()
                    # Join data about the city for SQL command
                    city['State'] = state['Codigo']
                    city['ValidityPeriod'] = dataCity['PeriodoVigencia']
                    city['Flag'] = dataCity['Bandeira']
                    city['Company'] = dataCity['Empresa']
                    # Join data about the fee of the city
                    FeeList = dataCity['ListTarifas']
                    for Fee in FeeList:
                        Fee['City'] = city['Codigo']
                    sql = "CREATE TABLE {}(Description, TUSD, TE_Verde, TE_Amarela, TE_Vermelha, Discount)".format(name)
                    stmt.execute(sql)
                    sql = "INSERT INTO {} VALUES(:Descricao, :TUSD_MWH, :TE_Verde, :TE_Amarela, :TE_Vermelha, :Desconto)".format(name)
                    stmt.executemany(sql, FeeList)
                    conn.commit()
                print("Next " + state['Codigo'] + "-" + city['Nome'])
            # Verify if the info is already in the table
            res = stmt.execute("SELECT id FROM state WHERE id=?", [state['Codigo']])
            compare = res.fetchone()
            if compare is None:
                stmt.executemany("INSERT INTO city VALUES(:Codigo, :Nome, :Flag, :Company, :ValidityPeriod, :State)", cities['Municipios'])
                conn.commit()
    except Exception as e:
        pass
    finally:
        if (stmt):
            stmt.close()
        if (conn):
            conn.close()

main()