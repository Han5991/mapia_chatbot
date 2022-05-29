import os
from flask import Flask, render_template, request, jsonify
from google.cloud import dialogflow_v2 as dfw
from google.api_core.exceptions import InvalidArgument

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index_page_landing():
    if request.method == "POST":
        return jsonify({"response": chatbot_request(request.get_json()['input'])})
    else:

        return render_template('chat.html')


def chatbot_request(txt_input):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'newagent-fwew-c432a2379a24.json'

    session_client = dfw.SessionsClient()
    session = session_client.session_path('newagent-fwew', 'mine')
    text_input = dfw.types.TextInput(text=txt_input, language_code='ko')
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
