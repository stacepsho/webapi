from flask import Flask, request, jsonify
#from flask_cors import CORS
import os
import json
import requests
#from slack_sdk import WebClient
#from slack_sdk.errors import SlackApiError

app = Flask(__name__)
#CORS(app)

received_data = []
#slack_tk=""
#slack_channel=""

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
                selected_cam = data.get("state", {}).get("values", {}).get("JlDto", {}).get("hv5Cg", {}).get("selected_option", {}).get("value")
                message_ts = data['container']['message_ts']
                print(f"response url is ：{response_url}", flush=True)
                print(f"plateno is ：{plateno}", flush=True)
                print(f"selected_cam is ：{selected_cam}", flush=True)

                #得知訊息了，回應結果
                if plateno=="":
                    #是CAM的回應
                    response_payload = {
                    "replace_original": "false",
                    "response_type": "in_channel",
                    "thread_ts": message_ts,
                    "text": f"收到，{selected_cam} 已經暫停轉向"
                    }
                else:
                    response_payload = {
                    "replace_original": "false",
                    "response_type": "in_channel",
                    "thread_ts": message_ts,
                    "text": f"收到，{plateno} 謝謝你的回報"
                    }

                #開始回應
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
    #SLASH COMMAND 停止巡弋
    if request.content_type == 'application/x-www-form-urlencoded':
        print("---x-www-form-urlencoded---", flush=True)
        data = request.form
        if data:
            # 列出所有的鍵值對
            key_value_pairs = {key: data[key] for key in data}
            print("---Received Key-Value Pairs---", flush=True)
            for key, value in key_value_pairs.items():
                print(f"key is ：{key}", flush=True)
                print(f"value is ：{value}", flush=True)
            
            #回應訊息到群組
            #msg ='[{"type":"section","text":{"type":"mrkdwn","text":":請指定*專案跟攝影機*"}},{"type":"divider"},{"type":"section","text":{"type":"mrkdwn","text":"*<fakeLink.toYourApp.com|專案>*\n專案名稱"},"accessory":{"type":"static_select","placeholder":{"type":"plain_text","emoji":true,"text":"專案"},"options":[{"text":{"type":"plain_text","emoji":true,"text":"台中AI"},"value":"台中AI"},{"text":{"type":"plain_text","emoji":true,"text":"台中4合1"},"value":"台中4合1"},{"text":{"type":"plain_text","emoji":true,"text":"高雄AI"},"value":"高雄AI"}]}},{"type":"section","text":{"type":"mrkdwn","text":"*<fakeLink.toYourApp.com|攝影機>*\n攝影機"},"accessory":{"type":"static_select","placeholder":{"type":"plain_text","emoji":true,"text":"攝影機"},"options":[{"text":{"type":"plain_text","emoji":true,"text":"CAM_01"},"value":"CAM_01"},{"text":{"type":"plain_text","emoji":true,"text":"CAM_02"},"value":"CAM_02"},{"text":{"type":"plain_text","emoji":true,"text":"CAM_03"},"value":"CAM_03"}]}},{"type":"divider"},{"type":"actions","elements":[{"type":"button","text":{"type":"plain_text","emoji":true,"text":"送出"},"value":"送出"}]}]'
            #toSLACK(slack_tk,slack_channel,msg,"","","mybot",9999)

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

def toSLACK(slack_token, channel_id ,msg, img_file_path,video_file_path,bot_name,mid):
    #
    # 透過SLACK送出訊息
    #
    client = WebClient(token=slack_token)
    try:
        #response = client.chat_postMessage(channel=channel_id, text=msg) 
        #blocks 是slack特定的文字區塊，採用json format
        if "[{" in msg:
            response = client.chat_postMessage(channel=channel_id, blocks=msg)
        else:
            response = client.chat_postMessage(channel=channel_id, text=msg) 

        if(img_file_path!=''):
            response = client.files_upload_v2(channel=channel_id,title="照片：",file=img_file_path,username=bot_name)
            permalink = response['files'][0]['permalink']
        if(video_file_path!=''):
            response = client.files_upload_v2(channel=channel_id,title="影片：",file=video_file_path,username=bot_name)
            permalink = response['files'][0]['permalink']

        print(f"ID:{mid} Message post successfully!")
        logging.info(f"ID:{mid} Message post successfully!")
        #The response includes the "timestamp ID" (ts) and the channel-like thing where the message was posted
        return int(response['ok']), ''
        
    except SlackApiError as e:
        print(f"【錯誤】: {e.response['error']}")
        logging.fatal(f"ID:{mid}. ERROR:{e.response['error']}")
        return 0, e.response['error']


if __name__ == '__main__':
    port_nr = int(os.environ.get("PORT", 10000))
    app.run(debug=True,port=port_nr, host='0.0.0.0')
    #app.run(debug=True)
