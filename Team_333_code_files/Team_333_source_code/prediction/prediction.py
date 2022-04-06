from prometheus_api_client import PrometheusConnect
from oauth2client.service_account import ServiceAccountCredentials
from torch.autograd import Variable
import torch
import gspread
import random
import numpy as np
import pandas as pd
import torch.nn as nn
from df2gspread import df2gspread as d2g
import datetime
from twilio.rest import Client

num_epochs = 2000
learning_rate = 0.01
input_size = 1
hidden_size = 2
num_layers = 1
num_classes = 1
seq_length = 12
account_sid = "AC57d6a864abf05463d052680e60e3577a"
auth_token = "2b0dd9f07f0c0007c56d7ec684a9c5f4"
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
spreadsheet_key = '1Bp0UY4R4MQK5NfBCcUMumBearNc_9UqppaqCy7Ei5qk'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'secrets.json', scope)


class LSTM(nn.Module):  # Model

    def __init__(self, num_classes, input_size, hidden_size, num_layers):
        super(LSTM, self).__init__()

        self.num_classes = num_classes
        self.num_layers = num_layers
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.seq_length = seq_length

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                            num_layers=num_layers, batch_first=True)

        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        h_0 = Variable(torch.zeros(
            self.num_layers, x.size(0), self.hidden_size))

        c_0 = Variable(torch.zeros(
            self.num_layers, x.size(0), self.hidden_size))

        # Propagate input through LSTM
        ula, (h_out, _) = self.lstm(x, (h_0, c_0))

        h_out = h_out.view(-1, self.hidden_size)

        out = self.fc(h_out)

        return out


# Get the Prometheus data by using the python API
# And get the data from the sheets to update it
def getDataPrometheus():
    prom = PrometheusConnect('http://localhost:7000/')

    val = prom.custom_query_range(
        'rate(process_cpu_seconds_total{mode!="idle"}[30s])*100', start_time=start_time, end_time=end_time, step='10s')

    val = np.expand_dims(val, axis=0)
    val_t = Variable(torch.Tensor(val))

    gc = gspread.authorize(credentials)
    spreadsheet_key = '1Bp0UY4R4MQK5NfBCcUMumBearNc_9UqppaqCy7Ei5qk'

    df = pd.read_csv(
        f"https://docs.google.com/spreadsheets/d/{spreadsheet_key}/export?format=csv", index_col=0)

    return val_t, df


# Adjust time zone
def genColumn(df):
    time = datetime.datetime.now()
    times = []
    for i in range(1, len(df)+1):
        updTime = time - datetime.timedelta(hours=len(df)-i)
        times.append(updTime.strftime("%Y-%m-%d %H:%M:%S"))
    df['Time'] = times
    df.set_index('Time')
    return df


# generate predictions by loading model
def getPredict(val_t):
    model = LSTM(num_classes, input_size, hidden_size, num_layers)
    model.load_state_dict(torch.load("model"))
    model.eval()
    pred = model(val_t).item()
    return pred

# Get the data and generate predictions for the next
# hour. Send message if required. Update the Google Sheet
# that Grafana gets data from
def run():
    val_t, df = getDataPrometheus()  # Get Data From Promethues

    pred = getPredict(val_t)  # Predict Using DL Model

    # Send Message to user if predicted utilisation is high
    if(pred > 80):
        sendMessage()

    df = genColumn(df)   # Adjust Time Zone
    time = datetime.datetime.now()+datetime.timedelta(hours=1)
    # add row
    row = {'Time': [time.strftime("%Y-%m-%d %H:%M:%S")],
           'CPU Utilisation': [pred]}
    row = pd.DataFrame.from_dict(row)
    row['CPU Utilisation'] = pd.to_numeric(row['CPU Utilisation'])
    df = df.append(row, ignore_index=True)

    df = df.set_index('Time')
    # upload to Sheets
    d2g.upload(df, spreadsheet_key, "cpu utilization",
               credentials=credentials, row_names=True)


# Send Alert message to user
def sendMessage():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="More than 80% CPU utilisation predicted for the next hour. Have a look at the server. ",
        from_='+12076871194',
        to='+9195611177'
    )


if __name__ == "main":
    run()
