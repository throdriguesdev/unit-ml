from flask import Flask
from routes import prediction_routes
from logging_config import setup_logging
from routes import prediction_routes
app = Flask(__name__)
app.register_blueprint(prediction_routes)
setup_logging(app)
if __name__ == '__main__':
    app.run(debug=False)
