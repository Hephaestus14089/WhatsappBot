from flask import Flask
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/chat', methods=['POST'])
def chat():
    mssg = "Hello there"
    resp = MessagingResponse()
    resp.message(mssg)
    return str(resp)

if __name__ == '__main__':
    app.run()
