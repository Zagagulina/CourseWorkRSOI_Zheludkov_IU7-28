from flask import Flask, render_template, session, request
from datetime import datetime, timedelta
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

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'jojr034859435-80c,vunasfxitmqp,4jr9x.neasoir.x0-r-a94.qx3jx.moka'

app.permanent_session_lifetime = timedelta(days=31)

def register_blueprints(app):
    from serviceAgregation import serviceAgregation
    from serviceAgregationPublisher import serviceAgregationPublisher
    from serviceAgregationTemplate import serviceAgregationTemplate
    from serviceAgregationUser import serviceAgregationUser
    from serviceAgregationController import serviceAgregationController
    from serviceInterface import serviceInterface
    app.register_blueprint(serviceAgregation)
    app.register_blueprint(serviceAgregationPublisher)
    app.register_blueprint(serviceAgregationUser)
    app.register_blueprint(serviceAgregationTemplate)
    app.register_blueprint(serviceInterface)
    app.register_blueprint(serviceAgregationController)

register_blueprints(app)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True, threaded = True)