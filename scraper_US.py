import datetime
import gspread
import openai
import json
import pandas as pd
import prettytable
import requests
from bs4 import BeautifulSoup as bs
from oauth2client.service_account import ServiceAccountCredentials

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['CUSR0000SA0','CUUR0000SA0', 'CUSR0000SA0L1E','CUUR0000SA0L1E','WPSFD4','WPUFD4', 'WPSFD49104','WPUFD49104', 'CES0000000001','LNS14000000','CES0500000003'],"startyear":"2021", "endyear":"2023"})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)
for series in json_data['Results']['series']:
    x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
    seriesId = series['seriesID']
    for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']
        footnotes=""
        for footnote in item['footnotes']:
            if footnote:
                footnotes = footnotes + footnote['text'] + ','
        if 'M01' <= period <= 'M12':
            x.add_row([seriesId,year,period,value,footnotes[0:-1]])
    output = open(seriesId + '.txt','w')
    output.write (x.get_string())
    output.close()
    
  ### Montando a estrutura para formação de texto, de acordo com os dados dos EUA
dados = p.json()
def CPI_PPI(n,p,s,q):
  ###### Leituras recentes
  if n == 0:
    indice = "CPI"
  else:
    indice = "PPI"
  CPI_atual = dados['Results']['series'][n]['data'][0]['value'] ### dado ajustado
  CPI_anterior = dados['Results']['series'][n]['data'][1]['value']
  CPI_atual_una = dados['Results']['series'][p]['data'][0]['value'] ### dado não ajustado
  CPI_mes_atual_12 = dados['Results']['series'][p]['data'][12]['value']
  CPI_mensal = (float(CPI_atual) - float(CPI_anterior))*100/float(CPI_anterior)
  CPI_anual = (float(CPI_atual_una) - float(CPI_mes_atual_12))*100/float(CPI_mes_atual_12)
  CPI_mensal_ajustado ='%.1f' % CPI_mensal
  CPI_anual_ajustado ='%.1f' % CPI_anual

  ### Núcleo do CPI (sem energia e alimentos):
  NCPI_atual = dados['Results']['series'][s]['data'][0]['value']
  NCPI_anterior = dados['Results']['series'][s]['data'][1]['value']
  NCPI_atual_una = dados['Results']['series'][q]['data'][0]['value']
  NCPI_mes_atual_12 = dados['Results']['series'][q]['data'][12]['value']
  NCPI_mensal = (float(NCPI_atual) - float(NCPI_anterior))*100/float(NCPI_anterior)
  NCPI_anual = (float(NCPI_atual_una) - float(NCPI_mes_atual_12))*100/float(NCPI_mes_atual_12)
  NCPI_mensal_ajustado ='%.1f' % NCPI_mensal
  NCPI_anual_ajustado ='%.1f' % NCPI_anual

  ####### Leituras anteriores do CPI
  CPI_anterior = dados['Results']['series'][n]['data'][1]['value']
  CPI_anterior_una = dados['Results']['series'][p]['data'][1]['value']
  CPI_anterior_2 = dados['Results']['series'][n]['data'][2]['value']
  CPI_mes_anterior_12 = dados['Results']['series'][p]['data'][13]['value']
  CPI_mensal_anterior = (float(CPI_anterior) - float(CPI_anterior_2))*100/float(CPI_anterior_2)
  CPI_anual_anterior = (float(CPI_anterior_una) - float(CPI_mes_anterior_12))*100/float(CPI_mes_anterior_12)
  CPI_mensal_anterior_ajustado ='%.1f' % CPI_mensal_anterior
  CPI_anual_anterior_ajustado ='%.1f' % CPI_anual_anterior

  ####### Leituras anteriores do núcleo do CPI
  NCPI_anterior = dados['Results']['series'][s]['data'][1]['value']
  NCPI_anterior_una = dados['Results']['series'][q]['data'][1]['value']
  NCPI_anterior_2 = dados['Results']['series'][s]['data'][2]['value']
  NCPI_mes_anterior_12 = dados['Results']['series'][q]['data'][13]['value']
  NCPI_mensal_anterior = (float(NCPI_anterior) - float(NCPI_anterior_2))*100/float(NCPI_anterior_2)
  NCPI_anual_anterior = (float(NCPI_anterior_una) - float(NCPI_mes_anterior_12))*100/float(NCPI_mes_anterior_12)
  NCPI_mensal_anterior_ajustado ='%.1f' % NCPI_mensal_anterior
  NCPI_anual_anterior_ajustado ='%.1f' % NCPI_anual_anterior

  lista_dados = [indice, CPI_atual, CPI_anterior, CPI_atual_una, CPI_mes_atual_12, CPI_mensal_ajustado, CPI_anual_ajustado, NCPI_atual, NCPI_anterior, NCPI_atual_una, NCPI_mes_atual_12, NCPI_mensal_ajustado, NCPI_anual_ajustado, CPI_mensal_anterior_ajustado, CPI_anual_anterior_ajustado, NCPI_mensal_anterior_ajustado, NCPI_anual_anterior_ajustado]

  return lista_dados
    
def lista_vagas():
### Primeiro, começando pela definição do número total de vagas geradas:
    dados = p.json()
    mes_atual_mt = dados['Results']['series'][8]['data'][0]['value']
    mes_anterior_mt = dados['Results']['series'][8]['data'][1]['value']
    mes_antes_anterior_mt = dados['Results']['series'][8]['data'][2]['value']
    total_de_vagas = '%.0f' %((float(mes_atual_mt) - float(mes_anterior_mt)))
    total_de_vagas_antes = '%.0f' %((float(mes_anterior_mt) - float(mes_antes_anterior_mt))) 

      ### Segundo, descobrindo a taxa de desemprego do mês:
    taxa_desemprego_atual = dados['Results']['series'][9]['data'][0]['value']
    taxa_desemprego_anterior = dados['Results']['series'][9]['data'][1]['value']
    lista_vagas = ["", mes_atual_mt, mes_anterior_mt, mes_antes_anterior_mt, total_de_vagas, total_de_vagas_antes, taxa_desemprego_atual, taxa_desemprego_anterior]
    return lista_vagas

def lista_ganho():
  ### Terceiro, calculando o ganho por hora na relação mensal e relação anual
    ganho_atual = dados['Results']['series'][10]['data'][0]['value']
    ganho_anterior = dados['Results']['series'][10]['data'][1]['value']
    ganho_antes_ant = dados['Results']['series'][10]['data'][2]['value']
    ganho_12anterior = dados['Results']['series'][10]['data'][12]['value']
    ganho_13anterior = dados['Results']['series'][10]['data'][12]['value']
    ganho_perc_mes = '%.1f' % ((float(ganho_atual) - float(ganho_anterior))*100/float(ganho_anterior))
    ganho_perc_mes_ant = '%.1f' % ((float(ganho_anterior) - float(ganho_antes_ant))*100/float(ganho_antes_ant))
    ganho_perc_ano = '%.1f' % ((float(ganho_atual) - float(ganho_12anterior))*100/float(ganho_12anterior))
    ganho_perc_ano_ant = '%.1f' % ((float(ganho_anterior) - float(ganho_13anterior))*100/float(ganho_13anterior))
    lista_ganho = ["", ganho_atual, ganho_anterior, ganho_antes_ant, ganho_12anterior, ganho_13anterior, ganho_perc_mes, ganho_perc_mes_ant, ganho_perc_ano, ganho_perc_ano_ant]
    return lista_ganho

def mes(p,n):
    if dados['Results']['series'][p]['data'][n]['period'] == 'M01':
      mes_1 = 'janeiro'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M02':
      mes_1 = 'fevereiro'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M03':
      mes_1 = 'março'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M04':
      mes_1 = 'abril'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M05':
      mes_1 = 'maio'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M06':
      mes_1 = 'junho'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M07':
      mes_1 = 'julho'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M08':
      mes_1 = 'agosto'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M09':
      mes_1 = 'setembro'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M10':
      mes_1 = 'outubro'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M11':
      mes_1= 'novembro'
    else:
      mes_1 = 'dezembro'
    return mes_1

  mes0CPI = mes(0,0)
  mes1CPI = mes(0,1)
  mes2CPI = mes(0,2)

  mes0PPI = mes(4,0)
  mes1PPI = mes(4,1)
  mes2PPI = mes(4,2)

  mes0Pay = mes(8,0)
  mes1Pay = mes(8,1)
  mes2Pay = mes(8,2)
    
  lista_ganho = lista_ganho()
  lista_vagas = lista_vagas()
  
  #### O código abaixo limpa e preenche a minha planilha
def publicado():
  start_row = 3
  end_row = 25
  start_col = 'A'
  end_col = 'Q'
  range_string = f'{start_col}{start_row}:{end_col}{end_row}'
  cell_list = sheet.range(range_string)
  for cell in cell_list:
      cell.value = ''
  sheet.update_cells(cell_list)
  
  lista_titulos = ["","dado bruto atual", "dado bruto anterior", "dado bruto não ajustado", "dado bruto há 12 meses","mensal (%)","anual (%)", "núcleo bruto", "núcleo bruto anterior", "núcleo bruto não ajustado", "núcleo bruto há 12 meses","núcleo/mensal (%)", "núcleo/anual (%)", "último mensal (%)", "último anual (%)", "último mensal núcleo (%)", "último anual núcleo (%)"]
  lista_meses_CPI = ["mês referência", mes0CPI, mes1CPI, mes0CPI, mes0CPI, mes0CPI, mes0CPI, mes0CPI, mes1CPI, mes0CPI, mes0CPI, mes0CPI, mes0CPI, mes1CPI, mes1CPI, mes1CPI, mes1CPI]
  lista_meses_PPI = ["mês referência", mes0PPI, mes1PPI, mes0PPI, mes0PPI, mes0PPI, mes0PPI, mes0PPI, mes1PPI, mes0PPI, mes0PPI, mes0PPI, mes0PPI, mes1PPI, mes1PPI, mes1PPI, mes1PPI]
  lista_vazia = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
  lista_payroll = ["payroll (merc. de trabalho)", "dado burto atual", "dado br. mês anterior", "dado br. dois meses antes", "total de vagas, em milhares", "total de vagas mês anterior, em milhares", "taxa de desemprego atual", "taxa de desemprego anterior"]
  lista_meses_pay = ["mês referência", mes0Pay, mes1Pay, mes2Pay, mes0Pay, mes1Pay, mes0Pay, mes1Pay, mes0Pay, mes1Pay]
  lista_payroll2 = ["ganho salarial", "ganho atual bruto", "ganho anterior bruto", "ganho há dois meses bruto", "ganho bruto 12 meses", "ganho bruto 13 meses", "ganho perc. atual", "ganho perc. anterior", "ganho acu. 12", "ganho acu. 12 anterior"]

  return sheet.append_rows([lista_titulos, lista_meses_CPI, CPI_PPI(0,1,2,3), lista_vazia, lista_meses_PPI, CPI_PPI(4,5,6,7), lista_vazia, lista_meses_pay, lista_payroll, lista_vagas, lista_vazia, lista_meses_pay, lista_payroll2, lista_ganho])
