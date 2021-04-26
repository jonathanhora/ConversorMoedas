import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency


url = "https://www.iban.com/currency-codes"
paises_moeda = []

request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")

table = soup.find("table")
rows = table.find_all("tr")[1:]

for row in rows:
  items = row.find_all("td")
  pais = items[0].text
  codigo =items[2].text
  if pais and codigo: 
    if pais != "No universal currency":
      moeda_do_pais = {
        'pais':pais.capitalize(),
        'codigo': codigo
      }
      paises_moeda.append(moeda_do_pais)

def seleciona_origem():
  try:
    origem = int(input("Informe pelo número o país de origem da Moeda.\n"))
    if origem > len(paises_moeda):
      print("Escolha um país da lista:")
      seleciona_origem()
    else:
      moeda_do_pais_origem = paises_moeda[origem]
      print(f"(X) {moeda_do_pais_origem['pais']}")
      selecionar_destino(moeda_do_pais_origem) 
  except ValueError:
    print("Isso não é um número!")
    seleciona_origem()

def selecionar_destino(moeda_do_pais_origem):
  try:
    destino = int(input("Quer negociar com qual outro pais?\n"))
    if destino > len(paises_moeda):
      print("Escolha um país da lista:")
      selecionar_destino()
    else:
      moeda_do_pais_destino = paises_moeda[destino]
      verificar_quantidade(moeda_do_pais_origem,moeda_do_pais_destino)
  except:
    print("Isso não é um número!")
    selecionar_destino(moeda_do_pais_origem)

def verificar_quantidade (moeda_do_pais_origem,moeda_do_pais_destino):
  try:
    quantidade_moeda = int(input(f"Quantos {moeda_do_pais_origem['codigo']} quer converter para {moeda_do_pais_destino['codigo']}\n"))

    url_converter = "https://transferwise.com/gb/currency-converter/"
    r_url_converter = requests.get(f"{url_converter}{moeda_do_pais_origem['codigo'].lower()}-to-{moeda_do_pais_destino['codigo'].lower()}-rate?amount={quantidade_moeda}")

    html_url_conerter = r_url_converter.text
    soup = BeautifulSoup(html_url_conerter, 'html.parser')
    valor_para_converter = float(soup.find('h3', class_='cc__source-to-target').find('span', class_='text-success').string)

    quantidade_formatada = format_currency(quantidade_moeda,moeda_do_pais_origem['codigo'] )

    valor_convertido = quantidade_moeda*valor_para_converter

    convertido_formatado = format_currency(valor_convertido,moeda_do_pais_destino['codigo'] )

    print( f"{quantidade_formatada} é igual a {convertido_formatado}")


  except:
    print("Informe o valor em números\n")
    verificar_quantidade (moeda_do_pais_origem,moeda_do_pais_destino)



print("Bem-vindo ao Negociador de Moedas!\nEscolha pelo número da lista o país que desja consultar o código da moeda.\n")

for index, moeda_do_pais in enumerate(paises_moeda):
  print(f"#{index} {moeda_do_pais['pais']}")
  
seleciona_origem()
