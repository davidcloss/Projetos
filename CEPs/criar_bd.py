import sqlite3
#criando bd
con = sqlite3.connect('ceps.db')
cur = con.cursor()
# criando tabela
cur.execute('''CREATE TABLE data
               (cep TEXT, logradouro TEXT, complemento TEXT, bairro TEXT, localidade TEXT, uf TEXT, ibge INTEGER, ddd INTEGER, siafi INTEGER)''')

# CRIEI UMA TABELA PARA ARMAZENAR OS NUMEROS QUE NÃO PUXAREM CEP TER CONTROLE SE FUNCIONOU
cur.execute('''CREATE TABLE datanull
               (cep TEXT)''')

con.close()