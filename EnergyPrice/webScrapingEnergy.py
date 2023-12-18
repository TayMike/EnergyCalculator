import requests

GREEN_FLAG = 0
YELLOW_FLAG = 0.01874
RED_FLAG = 0.03971
WATER_SCARCITY_FLAG = 0.09492

requests.get('https://servicosonline.cpfl.com.br/agencia-webapp/#/taxas-tarifas/localizar-distribuidora').content
header = headers={'Clientid': 'agencia-virtual-cpfl-web', 'Captcha-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJDYXB0Y2hhVmFsaWRvIjoiUyIsImNsaWVudElkIjoiYWdlbmNpYS12aXJ0dWFsLWNwZmwtd2ViIiwiQ2FwdGNoYUhvc3ROYW1lIjoic2Vydmljb3NvbmxpbmUuY3BmbC5jb20uYnIiLCJpc3MiOiJodHRwczovL3NlcnZpY29zb25saW5lLmNwZmwuY29tLmJyLyIsImF1ZCI6ImFnZW5jaWEtdmlydHVhbC1jcGZsLXdlYiIsImV4cCI6MTcwMjkzODk3OCwibmJmIjoxNzAyOTM4Mzc4fQ.thJEfN784axGBQQJwDrA_I_ozE0JzPotpmTg228Zaog'}

state = 'Sao Paulo'
city = 'VOTORANTIM'
states = requests.get('https://servicosonline.cpfl.com.br/agencia-webapi/api/estado?apenasConcessao=true', headers=header).json()
for key in states['Estados']:
    if (key['Nome'] == state):
        codeState = key['Codigo']

cities = requests.get(f'https://servicosonline.cpfl.com.br/agencia-webapi/api/estado/{codeState}/municipio?apenasConcessao=true', headers=header).json()

for key in cities['Municipios']:
    if (key['Nome'] == city):
        codeCity = key['Codigo']

dataPost = {'CodMunicipio': codeCity}
table = requests.post(f'https://servicosonline.cpfl.com.br/agencia-webapi/api/taxas-tarifas/validar-situacao', json=dataPost, headers=header).json()

flag = table['Bandeira']