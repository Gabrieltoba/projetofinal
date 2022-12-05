# Ao abrir o GitPod, execute:
# pip install -r material.txt

#Trabalho Final da Disciplina Linguagem de Programação:
#Importando as bibliotecas.
from flask import Flask, render_template, request
import pandas as pd
from uuid import uuid4
import csv


app = Flask(__name__)


#A função abaixo é ler o arquivo compras.csv e joga para o index.html.
@app.route('/')
def index():
    with open('compras.csv', 'rt') as file_in:
        compras = csv.DictReader(file_in)
        return render_template('index.html', compras=compras)


#função que está abaixo é responsável por enviar uma rota ao navegador.
@app.route('/create')
def create():
    return render_template('material.html')


#SalvaR as variaveis do forms em uma nova row no arquivo compras.csv.
@app.route('/save', methods=['POST'])
def save():

    material = request.form['Material']         
    quantidade = request.form['Quantidade'] 
    preco = request.form['Preco']

    entrada= []
    entrada.append([uuid4(), material, quantidade,preco]) 

    #Adiciona append uma nova row no compras.csv
    with open('compras.csv', 'a') as file_out:
        escritor = csv.writer(file_out)
        escritor.writerows(entrada)
   
    #Lendo o arquivo"compras.csv" 
    with open('compras.csv', 'rt') as file_in:
        compras = csv.DictReader(file_in)
        return render_template('index.html', compras=compras)



#Função para deletar rows de acordo com o Id.
@app.route('/delete/<id>')
def delete(id):

    #Caregamento do arquivo compras.csv pelo pandas.
    data = pd.read_csv("compras.csv") 

    #Redirecionando para a coluna 'Id'.
    data = data.set_index("Id") 

    #Todas fileiras que tiver a mesma variavel "id" na coluna index.
    data.drop(id, axis='index', inplace=True) 
    
    #Salvamento do novo dataset.
    data.to_csv('compras.csv')  

    #função que le o arquivo e envia a variavel para o html.
    with open('compras.csv', 'rt') as file_in:
        compras = csv.DictReader(file_in)
        return render_template('index.html', compras=compras)
    

#As variaveis da fileiras que o usuario quer modificar e colocar dentro da tabela.
@app.route('/update/<id>/<material>/<quantidade>/<preco>')
def update(id,material,quantidade,preco):
    lista = [id,material,quantidade,preco]
    return render_template('update.html', lista=lista)


#Função para salvar as modificação feita na tabela.
@app.route('/saveup', methods=['POST'])
def saveup():

    #Obtem as novas variaveis.
    #O id esta ocultado na pagina.
    id = request.form['id'] 
    material = request.form['material']         
    quantidade = request.form['quantidade'] 
    preco = request.form['preco']

    #Abre o dataframe do compras.csv
    data = pd.read_csv("compras.csv")

    #Cria um novo dataframe apartir das novas variaveis abaixo.
    novo_dataframe = pd.DataFrame({'Id': [id],'Material': [material],'Quantidade': [quantidade],'Preco': [preco]})

    
    #Usamos o DataFrame para uma combinação de uma nova lista e a coluna existente. 
    data = data.set_index("Id")
    novo_dataframe =  novo_dataframe.set_index("Id")

    #Atualiza o data frame antigo com os novos dados.
    data.update(novo_dataframe)

    #Salvamento do arquivo.
    data.to_csv('compras.csv')

    #Redireciona para "index.html"
    with open('compras.csv', 'rt') as file_in:
        compras = csv.DictReader(file_in)
        return render_template('index.html', compras=compras)

app.run(debug=True)






