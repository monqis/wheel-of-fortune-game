from flask import Flask, request, jsonify
import random

app = Flask(__name__)

data = {
    "message": "hi"
}


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/data', methods=['GET'])
def data():
    # name = request.args.get('name')
    return jsonify({
        "message": random.randint(0, 10)
    })

