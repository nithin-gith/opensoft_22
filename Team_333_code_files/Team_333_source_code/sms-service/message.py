# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['POST'])
def Home():
    message = client.messages \
        .create(
            body="Grafana Alert.",
            from_='+12076871194',
            to='+91XXXXXXXXX'
        )
    return message.sid


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "AC57d6a864abf05463d052680e60e3577a"
auth_token = "2b0dd9f07f0c0007c56d7ec684a9c5f4"
client = Client(account_sid, auth_token)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True , port=3123)
