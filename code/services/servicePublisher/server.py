from flask import Flask
from datetime import datetime
import logging
import logging.handlers

def get_str_date_tyme():
    return datetime.now().strftime("%d.%m.%Y_%Hh.%Mm.%Ss")

path_log = 'C:/bmstu/maga/sem2/CW_RSOI/code/cw_rsoi/services/servicePublisher/log/log' + get_str_date_tyme() + '.txt'

logger = logging.getLogger("")
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(path_log, maxBytes=10000, backupCount=1)
formatter = logging.Formatter(
    '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logging.getLogger().addHandler(logging.StreamHandler())

app = Flask(__name__)
app.secret_key = 'llldsfjii f990-x,jf.9,48ru,js.430ri.-4irsiiowpurkengfdl;sk'

def register_blueprints(app):
    from servicePublisher import servicePublisher
    app.register_blueprint(servicePublisher)

register_blueprints(app)

@app.route('/')
def hello_world():
    return 'servicePublisher!'

if __name__ == '__main__':
    app.run(port = 1000)
