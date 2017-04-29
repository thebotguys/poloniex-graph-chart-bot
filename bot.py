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
BOT_NAME = os.environ['BOT-NAME']
TOKEN = os.environ['SLACK-TOKEN']
###############################################################

def parse_join(message):
    try:
        receivedMessage = json.loads(message)
        #print '\033[91m' + str(m) + '\033[0m'
        if (receivedMessage['type'] == 'channel_joined'):
            print '\033[91m I JOINED A CHANNEL \033[0m'
            chan = receivedMessage['channel']['id']
            req = rtm_open_channel()
            params = {
              'channel' : chan,
              'token' : TOKEN,
              'text' : 'Hello to everybody, looks like you need my help in this channel, what can I do for you?',
              'parse' : 'full',
              'as_user' : 'true'
            }
            resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
        elif (receivedMessage['type'] == 'message') and receivedMessage['user'] != BOT_ID:
            print '\033[91m MESSAGE RECEIVED \033[0m'
            receivedText = receivedMessage['text']
            chan = receivedMessage['channel']
            if '@' + BOT_ID in receivedText: #message for me
                #TODO parse message
                if 'help' in receivedText:
                    req = rtm_open_channel(channel=chan)
                    params = {
                      'channel' : chan,
                      'token' : TOKEN,
                      'text' : '[TODO]You can ask me any graph by using \n '+
                               '`@' + BOT_NAME + ' graph [COIN1] [COIN2] [TIME]`\n'+
                               'where `TIME` is 24h, 7d, 30d, 1y. \n' +
                               'And of course sir. `COIN1` and `COIN2` are coins\n' +
                               'Example of call may be `@' + BOT_NAME + ' graph ARK USD 24h`',
                      'parse' : 'full',
                      'as_user' : 'true'
                    }
                    resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                    print '\033[91m HELP MESSAGE POSTED \033[0m'
        elif(receivedMessage['type'] == 'hello'):
            print '\033[91m HELLO RECEIVED \033[0m'
        else:pass
    except Exception as ex:
        print '\033[91m Exception : Message => ' + str(receivedMessage) + '\n \
               Error :' + ex + ' \033[0m'
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

def rtm_open_channel(channel):
    params = {
       'token' : TOKEN,
       'channel' : channel,
    }
    req = requests.get('https://slack.com/api/im.open', params=params)
    req = req.json()
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
