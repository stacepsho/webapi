from flask import Flask, request, jsonify
#from flask_cors import CORS
import os
import json
import requests

app = Flask(__name__)
#CORS(app)

received_data = []

@app.route('/postData', methods=['POST'])
def receive_data():
    if request.content_type == 'application/x-www-form-urlencoded':
        print("---x-www-form-urlencoded---", flush=True)
        data = request.form
        if data:
            # 列出所有的鍵值對
            key_value_pairs = {key: data[key] for key in data}
            #print("---Received Key-Value Pairs---", flush=True)
            for key, value in key_value_pairs.items():
                print(f"key is ：{key}", flush=True)
                print(f"value is ：{value}", flush=True)
            #return jsonify({"message": "Data received"}), 200
            response_url = data.get("response_url")
            print(f"respons url is ：{response_url}", flush=True)
            return jsonify({"text": "Success!","response_type":"in_channel"}), 200
            
            #取出response_url
            #response_url = payload.get("response_url")

        else:
            return jsonify({"error": "No data received"}), 400
    elif request.content_type == 'application/json':
        print("---json---", flush=True)
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400
    else:
        print("---Unsupported Content-Type---", flush=True)
        return jsonify({"error": "Unsupported Content-Type"}), 415
    
    received_data.append(data)
    print(f"---Received data---: {data}", flush=True)
    return jsonify({"message": "Data received"}), 200

@app.route('/getData', methods=['GET'])
def list_data():
    # 在控制台顯示將要列出的資料
    print(f"---Listing all received data---: {received_data}", flush=True)
    return jsonify(received_data), 200

@app.route('/')
def hello():
    return f'---RUNNING---'

def replySlack(url):
    payload = {
        "text": "SUCCESS"
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)

if __name__ == '__main__':
    port_nr = int(os.environ.get("PORT", 10000))
    app.run(debug=True,port=port_nr, host='0.0.0.0')
    #app.run(debug=True)
