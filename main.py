from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

import csv
from watson_developer_cloud import ConversationV1
termdict ={}

with open("samples1.csv") as f:
    spamreader = csv.reader(f)
    for row in spamreader:
        print row
        termdict[row[0].lower()] = row[1]

def initContext():
    return {
        'term': None,
        'description': None
    }

conversation = ConversationV1(
    username='3fdbba02-a471-4aaf-be76-189b8f698236',
    password='hlGIoMc5RqXp',
    version='2016-09-20')

# replace with your own workspace_id
workspace_id = '5da1c0c6-432f-43e1-9134-7e0b8a77a68c'


@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():
    message = str(request.form['messageText'])
    # kernel now ready for use
    while True:
        response = {}
        # if there is no context in a
        #if 'context' not in response:
        response['context'] = initContext();


        # When you send multiple requests for the same conversation, include the
        # context object from the previous response.
        response = conversation.message(workspace_id=workspace_id, message_input={'text': message},
                                        context=response['context'])
        print(json.dumps(response, indent=2))
        #print(json.dumps(response['context'], indent=2))
        bot_response = ""
        if 'term'  in response['context'] and response['context']['term'] != None:
            print response['context']['term'].lower()
            response['context']['description'] = termdict.get(response['context']['term'].lower())
            print response['context']
            response = conversation.message(workspace_id=workspace_id,message_input={'text': message},
                                        context=response['context'])
            print response
        bot_response = "".join(response["output"]["text"])
        print bot_response
        return jsonify({'status':'OK','answer':bot_response})

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port,debug=True)