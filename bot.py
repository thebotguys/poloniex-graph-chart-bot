import websocket
import json
import requests
import urllib
import os

# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###VARIABLES THAT YOU NEED TO SET MANUALLY IF NOT ON HEROKU#####
BOT_ID = os.environ['BOT-ID']
TOKEN = os.environ['SLACK-TOKEN']
###############################################################

def parse_join(message):
    m = json.loads(message)
    print '\033[91m' + str(m) + '\033[0m'
    if (m['type'] == 'channel_joined'):
        req = requests.get('https://slack.com/api/im.open?token='+TOKEN+'&channel='+m['channel']['id'])
        req = req.json()
        chan = m['channel']['id']
        message = 'Hello to everybody, looks like you need my help in this channel, what can I do for you?'
        resp = requests.post('https://slack.com/api/chat.postMessage?token='+TOKEN+'&channel='+chan+'&text='+urllib.quote(message)+'&parse=full&as_user=true')
    elif (m['type'] == 'message'):
        messageText = m['text']
        if '@' + BOT_ID in messageText: #message for me
            if 'help' in messageText:
                req = requests.get('https://slack.com/api/im.open?token='+TOKEN+'&channel='+m['channel']['id'])
                req = req.json()
                chan = m['channel']['id']
                message = '[TODO]You can ask me any graph by using @' + BOT_NAME + ' graph [COIN1] [COIN2] [TIME], where TIME is 24h, 7d, 30d, 1y. And of course sir. COIN1 and COIN2 are coins'
                resp = requests.post('https://slack.com/api/chat.postMessage?token='+TOKEN+'&channel='+chan+'&text='+urllib.quote(message)+'&parse=full&as_user=true')
    elif (m['type'] == 'hello'):
        print '\033[91m HELLO RECEIVED \033[0m'

    else:pass
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
