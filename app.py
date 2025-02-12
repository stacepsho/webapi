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
            #key_value_pairs = {key: data[key] for key in data}
            #print("---Received Key-Value Pairs---", flush=True)
            #for key, value in key_value_pairs.items():
            #    print(f"key is ：{key}", flush=True)
            #    print(f"value is ：{value}", flush=True)

            data = request.form['payload'] 
            if data:
                #SLACK來的資料，取得，response_url 是回應的url
                data = json.loads(data)  # 解析JSON
                print(f"{data}", flush=True)
                response_url = data.get("response_url")
                plateno = data.get("state", {}).get("values", {}).get("csBjQ", {}).get("plain_text_input-action", {}).get("value")
                message_ts = data['container']['message_ts']
                print(f"response url is ：{response_url}", flush=True)
                print(f"plateno is ：{plateno}", flush=True)
                print(f"message_ts is ：{message_ts}", flush=True)

                #得知訊息了，回應結果
                response_payload = {
                    "replace_original": "false",
                    "response_type": "in_channel",
                    "thread_ts": message_ts,
                    "text": f"收到，{plateno} 謝謝你的回報"
                }
                response_headers = {
                    "Content-Type": "application/json"
                }
                response = requests.post(response_url, data=json.dumps(response_payload), headers=response_headers)
                print(f'After POST Body: {data}', flush=True)
                print(f'After POST Status Code: {response.status_code}', flush=True)
                print(f'After POST Headers: {response.headers}', flush=True)
                print(f'After POST Response Body: {response.text}', flush=True)
                #return jsonify({"text": "Data received"}), 200

            else:
                key_value_pairs = {key: data[key] for key in data}
                print("---Received Key-Value Pairs---", flush=True)
                for key, value in key_value_pairs.items():
                    print(f"key is ：{key}", flush=True)
                    print(f"value is ：{value}", flush=True)
                    return jsonify({"text": "Data received"}), 200
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
    #print(f"---Received data---: {data}", flush=True)
    return jsonify({"text": "Data received"}), 200

@app.route('/stopPTZ', methods=['POST'])
def command_stopptz():
    #SLASH COMMAND
    if request.content_type == 'application/x-www-form-urlencoded':
        print("---x-www-form-urlencoded---", flush=True)
        data = json.loads(request.form)
    elif request.content_type == 'application/json':
        print("---json---", flush=True)
        data = request.get_json()
    else:
        print("---Unsupported Content-Type---", flush=True)
        return jsonify({"error": "Unsupported Content-Type"}), 415

    print(f"{data}", flush=True)
    return jsonify({"text": "Data received"}), 200

@app.route('/getData', methods=['GET'])
def list_data():
    # 在控制台顯示將要列出的資料
    print(f"---Listing all received data---: {received_data}", flush=True)
    return jsonify(received_data), 200

@app.route('/')
def hello():
    return f'---RUNNING---'

if __name__ == '__main__':
    port_nr = int(os.environ.get("PORT", 10000))
    app.run(debug=True,port=port_nr, host='0.0.0.0')
    #app.run(debug=True)
