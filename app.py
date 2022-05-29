from flask import Flask, render_template, request, jsonify
import os
from google.cloud import dialogflow_v2 as dfw
from google.api_core.exceptions import InvalidArgument
from collections import OrderedDict

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index_page_landing():
    if request.method == "POST":
        return chat_input()
    else:
        return render_template('chat.html')


def chat_input():
    response = chatbot_request(request.get_json()['input'])
    return jsonify({"response": response})


# def conversation_chatbot():
#     keys = []
#     values = []
#
#     request_text = input("request text : ")
#
#     while request_text != 'exit':
#         resp_text = chatbot_request(request_text)
#         keys.append(request_text)
#         values.append(resp_text)
#
#         request_text = input("request text : ")
#
#     return OrderedDict({key: val for key, val in zip(keys, values)})


def chatbot_request(txt_input):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'newagent-fwew-c432a2379a24.json'

    DIALOGFLOW_PROJECT_ID = 'newagent-fwew'
    DIALOGFLOW_LANGUAGE_CODE = 'ko'
    SESSION_ID = 'mine'

    text_to_be_analyzed = txt_input

    session_client = dfw.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dfw.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dfw.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    print("Query Text : ", response.query_result.query_text)
    print("Detected intent : ", response.query_result.intent.display_name)
    print("Detected intent confidence : ", response.query_result.intent_detection_confidence)
    print("Fulfillment text : ", response.query_result.fulfillment_text)

    return response.query_result.fulfillment_text


if __name__ == "__main__":
    app.run(host='0.0.0.0')
