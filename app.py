from flask import Flask, render_template, request
# pip install flask-ngrok
# from flask_ngrok import run_with_ngrok  # <-------1

import os

# pip install dialogflow
from google.cloud import dialogflow_v2 as dfw
# from google.cloud import dialogflow as dfw
from google.api_core.exceptions import InvalidArgument

from collections import OrderedDict

app = Flask(__name__)


# run_with_ngrok(app)  # <---- 2


@app.route('/', methods=['GET', 'POST'])
def index_page_landing():
    if request.method == "POST":
        pass
    else:
        return render_template('renewal_index.html', context=conversation_chatbot())


# terminal에서 대화형 챗봇 흉내내기
def conversation_chatbot():
    keys = []
    values = []

    request_text = input("request text : ")

    while request_text != 'exit':
        resp_text = chatbot_request(request_text)
        keys.append(request_text)
        values.append(resp_text)

        request_text = input("request text : ")

    return OrderedDict({key: val for key, val in zip(keys, values)})


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
    # 실행 시
    # PermissionError: [Errno 13] Permission denied: '/var/folders/4w/7mc0wn_x6hg10_bw1777w_qc0000gn/T/ngrok/ngrok'
    # 해당 폴더로 가서 chmod -R 775 ngrok
    '''
    이것도 안될 시,
    run_with_ngrok(app) 주석처리
    '''
    app.run(debug=True, port=8081)
