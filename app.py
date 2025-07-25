from flask import Flask, render_template, request, jsonify
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure setup
api_key = os.environ["GITHUB_TOKEN"]
token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "meta/Llama-4-Scout-17B-16E-Instruct"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

app = Flask(__name__)


def get_answer(question):
    resp = client.complete(
        messages=[
                    SystemMessage("You are Hepmate, a smart, and witty AI assistant designed to help users with informative, and engaging responses. about health and especially hepatitis"),            
                    UserMessage(f"{question}"),
        ],
        temperature=1.0,
        top_p=1.0,
        max_tokens=1000,
        model=model,
        stop=None,
    )

    answer = resp.choices[0].message.content
    return answer



@app.route('/hepmate', methods=['POST'])
def hepmate():
    incoming_question = request.values.get('Body', '').lower()
    print(incoming_question)

    answer = get_answer(incoming_question)
    print(answer)

    hepmate_resp = MessagingResponse()
    msg = hepmate_resp.message()
    msg.body(answer)

    return str(hepmate_resp)


# Web interface: HTML chat page
@app.route('/')
def webchat():
    return render_template('/index.html')


# Web interface: chat API for AJAX
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    bot_reply = get_answer(user_message)
    return jsonify({'response': bot_reply})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
