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

def verifyTableExist(stmt: object, name: str) -> list:
    res = stmt.execute("SELECT name FROM sqlite_master WHERE name=?", [name])
    return res.fetchone()

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
        verifyState = verifyTableExist(stmt, 'state')
        if verifyState is None:
            stmt.execute("CREATE TABLE state(id, name)")
            stmt.executemany("INSERT INTO state VALUES(:Codigo, :Nome)", states['Estados'])
            conn.commit()
        for state in states['Estados']:
            cities = requests.get(f"https://servicosonline.cpfl.com.br/agencia-webapi/api/estado/{state['Codigo']}/municipio?apenasConcessao=true", headers=header).json()
            verifyCity = verifyTableExist(stmt, 'city')
            if verifyCity is None:
                stmt.execute("CREATE TABLE city(id, name, flag, company, validityperiod, state)")
            for city in cities['Municipios']:
                verifyFeeList = verifyTableExist(stmt, 'FeeList')
                if verifyFeeList is None:
                    stmt.execute("CREATE TABLE FeeList(Description, TUSD, TE_Verde, TE_Amarela, TE_Vermelha, Discount, CodeCity)")
                # Verify if the info of the city already exist in database, this is the best place for that code because speed up the script in case of the token expires
                res = stmt.execute("SELECT CodeCity FROM FeeList WHERE CodeCity=?", [city['Codigo']])
                verifyFeeListInsert = res.fetchone()
                if verifyFeeListInsert is None:
                    # Collect data about the city
                    dataPost = {'CodMunicipio': city['Codigo']}
                    dataCity = requests.post(f'https://servicosonline.cpfl.com.br/agencia-webapi/api/taxas-tarifas/validar-situacao', json=dataPost, headers=header).json()
                    # Join data about the city for SQL command
                    city['State'] = state['Codigo']
                    city['ValidityPeriod'] = dataCity['PeriodoVigencia']
                    city['Flag'] = dataCity['Bandeira']
                    city['Company'] = dataCity['Empresa']
                    # The commit of this INSERT is made in the final of this conditional part. It's necessary for do not duplicate the code in case of restart
                    stmt.execute("INSERT INTO city VALUES(:Codigo, :Nome, :Flag, :Company, :ValidityPeriod, :State)", city)
                    # Join data about the fee of the city
                    FeeList = dataCity['ListTarifas']
                    for Fee in FeeList:
                        Fee['CodeCity'] = city['Codigo']
                    stmt.executemany("INSERT INTO FeeList VALUES(:Descricao, :TUSD_MWH, :TE_Verde, :TE_Amarela, :TE_Vermelha, :Desconto, :CodeCity)", FeeList)
                    conn.commit()
                print("Next " + state['Codigo'] + "-" + city['Nome'])
    except TimeoutError as e:
        raise e.with_traceback()
    finally:
        if (stmt):
            stmt.close()
        if (conn):
            conn.close()

main()