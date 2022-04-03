#importar bibliotecas
import requests
import json
import time
import sqlite3
import pandas as pd

#Funções

# inserção dos dados no bd
def insert_db(requisicao):
    con = sqlite3.connect('ceps.db')
    cur = con.cursor()
    ceps = requisicao['cep']
    ceps = ceps.replace('-', '')
    logradouro = requisicao['logradouro']
    complemento = requisicao['complemento']
    bairro = requisicao['bairro']
    localidade = requisicao['localidade']
    uf = requisicao['uf']
    ibge = requisicao['ibge']
    gia = requisicao['gia']
    ddd = requisicao['ddd']
    siafi = requisicao['siafi']
    cur.execute("INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?)",
                (ceps, logradouro, complemento, bairro, localidade, uf, ibge, ddd, siafi))
    con.commit()
    con.close()

#inserir cep não encontrado no BD
def insert_mistake(i):
    i = int(i)
    con = sqlite3.connect('ceps.db')
    cur = con.cursor()
    cur.execute("INSERT INTO datanull VALUES (?)", ([str(i)]))
    con.commit()
    con.close()

#ajustar numero de digitos cep
def tamanho_cep(i):
    if 8 - len(str(i)) == 7:
        i = str(i)
        cep = f'0000000{i}'
        return cep
    if 8 - len(str(i)) == 6:
        i = str(i)
        cep = f'000000{i}'
        return cep
    if 8 - len(str(i)) == 5:
        i = str(i)
        cep = f'00000{i}'
        return cep
    if 8 - len(str(i)) == 4:
        i = str(i)
        cep = f'0000{i}'
        return cep
    if 8 - len(str(i)) == 3:
        i = str(i)
        cep = f'000{i}'
        return cep
    if 8 - len(str(i)) == 2:
        i = str(i)
        cep = f'00{i}'
        return cep
    if 8 - len(str(i)) == 1:
        i = str(i)
        cep = f'0{i}'
        return cep
    if 8 - len(str(i)) == 0:
        i = str(i)
        cep = f'{i}'
        return str(cep)
#busca dos ceps
faixa_procura = pd.read_excel('progresso.xlsx')
i = faixa_procura['ultimo_cep'][0]
b = faixa_procura['ultimo_cep']
while i < 100000000:
    i = i + 1
    cep = tamanho_cep(i)
    requisicao = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    requisicao = requisicao.json()
    if len(requisicao) == 1:
        insert_mistake(cep)
    else:
        insert_db(requisicao)
    b[0] = i
    b.to_excel('progresso.xlsx', index = False)
    print(i)
    time.sleep(5)