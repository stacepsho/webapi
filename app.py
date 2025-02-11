from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

received_data = []

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    received_data.append(data)
    # 在控制台顯示收到的資料
    print(f"---Received data---: {data}")
    return jsonify({"message": "Data received"}), 201

@app.route('/data', methods=['GET'])
def list_data():
    # 在控制台顯示將要列出的資料
    print(f"---Listing all received data---: {received_data}")
    return jsonify(received_data), 200

@app.route('/')
def hello():
    return f'---RUNNING---'

if __name__ == '__main__':
    port_nr = int(os.environ.get("PORT", 8888))
    app.run(debug=True,port=port_nr, host='0.0.0.0')
    #app.run(debug=True)
