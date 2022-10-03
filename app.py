from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from create import create_event
from get import get_events

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/chat', methods=['POST'])
def chat_reply():
    mssg = request.form.get('Body')
    phone_no = request.form.get('From')

    if mssg.startswith('create'):
        start_date, start_time, end_date, end_time = mssg.split(' ')[1:5]

        event_name = ""
        for word in mssg.split(' ')[5:]:
            event_name += word + " "
        event_name = event_name[0:len(event_name) - 1]

        reply = create_event(event_name, start_date, start_time, end_date, end_time)

    elif mssg.startswith('list'):
        if len(mssg.split(' ')) > 1:
            count = mssg.split(' ')[1]

            reply = get_events(int(count))
        else:
            reply = get_events()

    else:
        reply = """
        Please enter a valid command.
        Help:
        1. create 16-Oct-22 10:30AM 16-Oct-22 05:00PM Blood Donation
        2. list 5
        """

    resp = MessagingResponse()
    resp.message(reply)

    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)
