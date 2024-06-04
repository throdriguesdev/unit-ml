import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    log_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=5)
    log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    log_handler.setLevel(logging.DEBUG)
    
    app.logger.addHandler(log_handler)