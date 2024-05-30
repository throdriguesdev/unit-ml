from flask import Blueprint, render_template, request, jsonify
from utils import home, predict
prediction_routes = Blueprint('prediction_routes', __name__)
@prediction_routes.route('/ping')
def ping():
    return jsonify({'status': 'up'})
@prediction_routes.route('/')
def index():
    return home()
@prediction_routes.route('/predict', methods=['POST'])
def prediction():
    return predict(request)
