import websocket
import json
import requests
import urllib
import os

# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###VARIABLES THAT YOU NEED TO SET MANUALLY IF NOT ON HEROKU#####
try:
    BOT_NAME = os.environ['BOT_NAME']
    TOKEN = os.environ['SLACK-TOKEN']
except:
	TOKEN = 'Manually set the API Token if you\'re not running through heroku or have not set vars in ENV'
    BOT_NAME = 'Manually set bot name here if you\'re not running through heroku or have not set vars in ENV'
###############################################################

def parse_join(message):
    m = json.loads(message)
    if (m['type'] == 'channel_joined'):
        req = requests.get('https://slack.com/api/im.open?token='+TOKEN+'&channel='+m['channel']['id'])
        req = req.json()
        chan = req['channel']['id']
        message = 'Hello to everybody, looks like you need my help in this channel, what can I do for you?'
        resp = requests.post('https://slack.com/api/chat.postMessage?token='+TOKEN+'&channel='+chan+'&text='+urllib.quote(message)+'&parse=full&as_user=true')
    elif (m['type'] == 'message'):
        messageText = m['text']
        if '@' + BOT_NAME in messageText: #message for me
            if 'help' in messageText:
                req = requests.get('https://slack.com/api/im.open?token='+TOKEN+'&channel='+m['channel']['id'])
                req = req.json()
                chan = req['channel']['id']
                message = 'You can ask me any graph by using @' + BOT_NAME + ' graph [COIN1] [COIN2] [TIME], where TIME is 24h, 7d, 30d, 1y. And of course sir. COIN1 and COIN2 are coins'
                resp = requests.post('https://slack.com/api/chat.postMessage?token='+TOKEN+'&channel='+chan+'&text='+urllib.quote(message)+'&parse=full&as_user=true')

#    {
#'text' : 'Here's your graph, sir.',
#    'attachments': [
#        {
#            'fallback': '',
#            'color': '#36a64f',
#            'title': 'DASH-USDT Chart - 7 Days',
#            'image_url': 'https://cryptohistory.org/charts/candlestick/dash-usdt/7d/png'
#        }
#    ]
#}
        #DEBUG
        #print '\033[91m' + 'HELLO SENT' + m['user']['id'] + '\033[0m'
        #

#Connects to Slacks and initiates socket handshake
def start_rtm():
    r = requests.get('https://slack.com/api/rtm.start?token='+TOKEN, verify=False)
    r = r.json()
    r = r['url']
    return r

def on_message(ws, message):
    parse_join(message)

def on_error(ws, error):
    print 'SOME ERROR HAS HAPPENED', error

def on_close(ws):
    print '\033[91m'+'Connection Closed'+'\033[0m'

def on_open(ws):
    print 'Connection Started'

if __name__ == '__main__':
    r = start_rtm()
    ws = websocket.WebSocketApp(r, on_message = on_message, on_error = on_error, on_close = on_close)
    #ws.on_open
    ws.run_forever()
