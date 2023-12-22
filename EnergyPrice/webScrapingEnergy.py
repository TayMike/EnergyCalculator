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

# Delay for time out if the script do not find the image on the screen
DELAY = 60

# Flags for extra fee in energy prices in Brazil
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
    """Web scraping data from CPFL
    To get the token authenticator is necessary check the captcha manually
    After that the code is going to run fine, maybe you need run the script twice because the timer of the token
    """

    # Take captcha token for Rest API
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
                # Verify if the info of the city already exist in database, this is the best place for that code because speed up the script in case of the token expires
                name = 'FeeList' + city['Codigo'] + state['Codigo']
                # There is no risk of SQL injection here, so it is possible make this to create tables dinamycally
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
            # Verify if the info of states is already in the table. This will prevent the duplication of the code 
            res = stmt.execute("SELECT id FROM state WHERE id=?", [state['Codigo']])
            compare = res.fetchone()
            if compare is None:
                stmt.executemany("INSERT INTO city VALUES(:Codigo, :Nome, :Flag, :Company, :ValidityPeriod, :State)", cities['Municipios'])
                conn.commit()
    except Exception as e:
        e.with_traceback()
    finally:
        if (stmt):
            stmt.close()
        if (conn):
            conn.close()

main()