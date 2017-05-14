from flask import Flask
from datetime import datetime
import logging
import logging.handlers

def get_str_date_tyme():
    return datetime.now().strftime("%d.%m.%Y_%Hh.%Mm.%Ss")

path_log = 'log' + get_str_date_tyme() + '.txt'

logger = logging.getLogger("")
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(path_log, maxBytes=10000, backupCount=1)
formatter = logging.Formatter(
    '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logging.getLogger().addHandler(logging.StreamHandler())

app = Flask(__name__)
app.secret_key = 'fjoasfj0 r0-4-3 ufjaosp 9f-ujsaklfjlwdaf-j0=9ufjaw[fj,;dsfaj;slkfj'

def register_blueprints(app):
    from serviceTemplate import serviceTemplate
    app.register_blueprint(serviceTemplate)

register_blueprints(app)

@app.route('/')
def hello_world():
    return 'serviceTemplate!'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 2000, debug = True)
