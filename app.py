from flask import Flask, request, jsonify
#from flask_cors import CORS
import os
import json

app = Flask(__name__)
#CORS(app)

received_data = []

@app.route('/postData', methods=['POST'])
def receive_data():
    if request.content_type == 'application/x-www-form-urlencoded':
        print("---x-www-form-urlencoded---")
        data = request.form
        if data:
            # 列出所有的鍵值對
            key_value_pairs = {key: data[key] for key in data}
            print("---Received Key-Value Pairs---")
            for key, value in key_value_pairs.items():
                print(f"{key}: {value}")
            return jsonify({"message": "Data received"}), 201
        else:
            return jsonify({"error": "No data received"}), 400
    elif request.content_type == 'application/json':
        print("---json---")
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400
    else:
        print("---Unsupported Content-Type---")
        return jsonify({"error": "Unsupported Content-Type"}), 415
    
    received_data.append(data)
    #print(f"---Received data---: {data}")
    return jsonify({"message": "Data received"}), 201

@app.route('/getData', methods=['GET'])
def list_data():
    # 在控制台顯示將要列出的資料
    print(f"---Listing all received data---: {received_data}")
    return jsonify(received_data), 200

@app.route('/')
def hello():
    return f'---RUNNING---'

if __name__ == '__main__':
    port_nr = int(os.environ.get("PORT", 10000))
    app.run(debug=True,port=port_nr, host='0.0.0.0')
    #app.run(debug=True)
