from flask import Flask
from tchan import ChannelScraper
import requests
import os

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]


app = Flask(__name__)

menu = """
<br><a href="/">Página Inicial</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a><br> | <a href="/promocoes">Promoções</a>"""

indice = """<br><img src="https://cdn-dejpn.nitrocdn.com/uxismCAJKdZklcCeScRYXbxxVTZIsrib/assets/static/optimized/rev-58a7024/wp-content/uploads/2021/08/FANI-slider-02.png"><br>"""
imagem = """<br><img src="https://media.tenor.com/QPDDG_qlvKkAAAAC/tata-werneck-trolala.gif"><br>"""


@app.route("/")
def index():
  return indice + menu + "Olá, mundo! Esse é meu site. (Arthur Cagliari)"

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página Sobre"

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página Contato" + imagem

@app.route("/promocoes")
def promocoes():
  conteudo = menu + """
  Encontrei as seguintes promoções no <a href="https://t.me/promocoeseachadinhos">@promocoeseachadinhos</a>:
  <br>
  <ul>
  """
  for promocao in ultimas_promocoes():
    conteudo += f"<li>{promocao}</li>"
  return conteudo + "</ul>"

@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  request.post(f'https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage', data=mensagem)
  return "Mensagem enviada!"
