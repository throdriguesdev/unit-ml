from flask import Flask
from routes import prediction_routes

app = Flask(__name__)
app.register_blueprint(prediction_routes)

if __name__ == '__main__':
    app.run(debug=False)
