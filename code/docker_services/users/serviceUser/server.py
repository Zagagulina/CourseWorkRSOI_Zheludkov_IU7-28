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
app.secret_key = 'ttefdwuieygmxfiwusafb,siijf.mz.fnvw trbkjnsvmox.kdfmlfknoiawfmvajvnkl'

def register_blueprints(app):
    from serviceUser import serviceUser
    app.register_blueprint(serviceUser)

register_blueprints(app)

@app.route('/')
def hello_world():
    return 'ServiceUser!'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 4000, debug = True)
