"""
Main file
Connects all blueprint
Add Cors policy
"""

from flask import Flask, send_file
from flask_cors import CORS
from utils import (
  register_blueprints_login,
  register_blueprints_main_page
)



host = "/getimg/"
path = 'G:\back\vose'

app = Flask(__name__)

# Спрятать ключ в продакшне
app.secret_key = 'LPOI(U*((IU*&T^YHJKOL:>:<LjidnkjiuwefjiTFRDES).<mjhuio'
CORS(app)

# импортируют приложения из папки blueprints
register_blueprints_login(app)
register_blueprints_main_page(app)

@app.route('/getimg/<name>')

def GetImg(name):
	return send_file('images/'+name)
