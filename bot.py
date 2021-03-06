import websocket
import json
import requests
import urllib
import os

# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###VARIABLES THAT YOU NEED TO SET MANUALLY IF NOT ON HEROKU#####
BOT_ID = os.environ['BOT_ID']
BOT_NAME = os.environ['BOT_NAME']
TOKEN = os.environ['SLACK_TOKEN']
###############################################################
# print 'BOT_ID=%s\nBOT_NAME=%s\nSLACK_TOKEN=%s' % (BOT_ID, BOT_NAME, TOKEN)
yolo_mode = False

def parse_join(message):
    global yolo_mode
    try:
        """Parses a received message and does actions based on the type of the message."""
        received_message = json.loads(message)
        #print '\033[91m' + str(received_message) + '\033[0m'
        if received_message['type'] == 'channel_joined':
            try:
                print '\033[91m I JOINED A CHANNEL \033[0m'
                chan = received_message['channel']['id']
                params = {
                  'channel' : chan,
                  'token' : TOKEN,
                  'text' : 'Hello to everybody, looks like you need my help in this channel, what can I do for you? type `@' + BOT_NAME + " help`",
                  'parse' : 'full',
                  'as_user' : 'true'
                }
                resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                # print resp.json()
            except Exception as ex:
                print ex
        elif received_message['type'] == 'message' and received_message['user'] != BOT_ID:
            try:
                print '\033[91m MESSAGE RECEIVED \033[0m'
                print '\033[91m %s \033[0m' % str(received_message)
                received_text = received_message['text']
                chan = received_message['channel']
                if '@' + BOT_ID in received_text: #message for me
                    if 'hi' in received_text.lower() or 'hello' in received_text.lower():
                        params = {
                          'channel' : chan,
                          'token' : TOKEN,
                          'text' : 'Greetings, sir. \n ' if not yolo_mode else 'HI THERE',
                          'parse' : 'full',
                          'as_user' : 'true'
                        }
                        resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                        # print resp.json()
                        print '\033[91m HI POSTED \033[0m'
                    if 'turn yolo' in received_text.lower():
                        yolo_mode = True
                        params = {
                          'channel' : chan,
                          'token' : TOKEN,
                          'text' : 'NP \n ',
                          'parse' : 'full',
                          'as_user' : 'true'
                        }
                        resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                        # print resp.json()                        
                        print '\033[91m YOLO MODE ACTIVATED \033[0m'
                    elif 'turn normal' in received_text.lower():
                        yolo_mode = False
                        params = {
                          'channel' : chan,
                          'token' : TOKEN,
                          'text' : 'What did just happen sir.? \n ',
                          'parse' : 'full',
                          'as_user' : 'true'
                        }
                        resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                        # print resp.json()
                        print '\033[91m YOLO MODE DECTIVATED \033[0m'
                    elif 'help' in received_text:
                        params = {
                          'channel' : chan,
                          'token' : TOKEN,
                          'text' : 'You can ask me any graph by using \n '+
                                   '`@' + BOT_NAME + ' graph [COIN1] [COIN2] [TIME]`\n'+
                                   'where `TIME` is 24h, 7d, 30d, 1y. \n' +
                                   'And of course sir. `COIN1` and `COIN2` are coins\n' +
                                   'Example of call may be `@' + BOT_NAME + ' graph ETH BTC 24h` \n' +
                                   '_Sources from : Cryptonator, Cryptohistory (Graphs) and Poloniex_\n' +
                                   #'*Project Repository on Github.com :* https://github.com/AlessandroSanino1994/cryptocharts-slack-bot \n' +
                                   'Support my creator : Pay his pizzas and coffee\n' +
                                   '@thebotguy\n' +
                                   #'*Paypal :* https://paypal.me/AlessandroSanino \n' +
                                   '*Bitcoin :* 1DVgmv6jkUiGrnuEv1swdGRyhQsZjX9MT3' if not yolo_mode else 'FUCK OFF',
                          'parse' : 'full',
                          'as_user' : 'true'
                        }
                        resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                        # print resp.json()
                        print '\033[91m HELP MESSAGE POSTED \033[0m'
                    elif 'graph' in received_text:
                        try:
                            message_args = received_text.split(' ')
                            params = {
                              'channel' : chan,
                              'token' : TOKEN,
                              'text' : None,
                              'attachments' : None,
                              'parse' : 'full',
                              'as_user' : 'true'
                            }
                            if len(message_args) == 5:
                                coin1 = message_args[2].lower()
                                coin2 = message_args[3].lower()
                                timeframe = message_args[4].lower()

                                if not timeframe in ['24h', '7d', '30d', '1y']:
                                    response_text = 'Invalid time frame sir. , the available options are : [24h, 7d, 30d, 1y]\n.' if not yolo_mode else 'DAFUQ?\n'
                                    response_text += 'Please ask me more by typing `@' + BOT_NAME + ' help`' if not yolo_mode else '4 NOOBZ : `@' + BOT_NAME + ' help`'
                                else: #tries to get image
                                  try:
                                    url = 'https://cryptohistory.org/charts/candlestick/'
                                    url += coin1 + '-' + coin2 + '/' + timeframe + '/png'
                                    resp = requests.get(url)
                                    if resp.status_code == requests.codes.ok:
                                        resp = requests.get('https://api.cryptonator.com/api/ticker/' + coin1 + '-' + coin2)
                                        respJson = resp.json()
                                        if resp.status_code == requests.codes.ok:
                                            if respJson['success'] == True:
                                                #print '\033[91m ' + str(resp) + ' \033[0m'
                                                response_text =  '\nThe current price of ' + coin1.upper() + ' is ' + respJson['ticker']['price'] + ' ' + coin2.upper()
                                                response_text += '\nCurrent Volume of the last 24 hours is ' + respJson['ticker']['volume'] + ' ' + coin1.upper()
                                                response_text += ' (which equals to ' + str(float(respJson['ticker']['price']) * float(respJson['ticker']['volume'])) + ' ' + coin2.upper() + ')'
                                            else:
                                                print '\033[91m ' + respJson['error'] + ' \033[0m'
                                                response_text = 'Current Price and Volume are not available, but I have the graph, sir.' if not yolo_mode else "INCOMIIIIINGGGG"
                                        else:
                                            response_text = 'Current Price and Volume are not available, but I have the graph, sir.' if not yolo_mode else "INCOMIIIIINGGGG"
                                        title = coin1.upper() + ' - ' + coin2.upper() + ' '
                                        if timeframe == '24h':
                                            title += '24 Hours'
                                        elif timeframe == '7d':
                                            title += '7 Days'
                                        elif timeframe == '30d':
                                            title += '30 Days'
                                        elif timeframe == '7d':
                                            title += '1 Year'
                                        else:
                                            title += 'Invalid Timeframe [please contact my developer to fix this]' if not yolo_mode else "DAFUQ?"
                                        title += ' graph'
                                        params['attachments'] = json.dumps([
                                            {
                                                'pretext' : response_text,
                                                'fallback': 'Crypto Graph',
                                                'color': '#36a64f',
                                                'title': title,
                                                'image_url': url,
                                                'thumb_url': url
                                            }
                                        ])
                                        #print str(params)
                                    else:
                                        response_text = 'Excuse me sir, but I can\'t find the coin pair you are asking for.\n'
                                        response_text += 'Please have in mind that I get data from Poloniex archives.'
                                        params['text'] = response_text if not yolo_mode else "WTF? PLZ GOOD COINZ"
                                    resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                                    # print resp.json()
                                  except Exception as ex:
                                    print ex
                            else:
                              params['text'] = 'Sorry sir. it seems that you want a graph but you don\'t provide me enough info.\n Check `@' + BOT_NAME + ' help` for info' if not yolo_mode else '4 NOOBZ: `@' + BOT_NAME + ' help`'
                              resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                              # print resp.json()
                        except Exception as ex:
                            print ex
                    elif 'thank you' in received_text or 'thanks' in received_text:
                        try:
                            req = rtm_open_channel(channel=chan)
                            params = {
                              'channel' : chan,
                              'token' : TOKEN,
                              'text' : 'You\'re welcome sir. It\'s a pleasure to me to be helpful. :)' if not yolo_mode else 'GG',
                              'parse' : 'full',
                              'as_user' : 'true'
                            }
                            resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                            # print resp.json()
                            print '\033[91m YOU\'RE WELCOME MESSAGE POSTED \033[0m'
                        except Exception as ex:
                            print ex
                    else:
                        try:
                            req = rtm_open_channel(channel=chan)
                            params = {
                              'channel' : chan,
                              'token' : TOKEN,
                              'text' : 'Excuse me sir., but I don\'t understand what you are saying. May you ask me for help?\n `@' + BOT_NAME + ' help`' if not yolo_mode else '4 NOOBZ: `@' + BOT_NAME + ' help`',
                              'parse' : 'full',
                              'as_user' : 'true'
                            }
                            resp = requests.post('https://slack.com/api/chat.postMessage', params=params)
                            # print resp.json()
                            print '\033[91m I DON\'T UNDERSTAND MESSAGE POSTED \033[0m'
                        except Exception as ex:
                            print ex
            except Exception as ex:
                print ex
        elif received_message['type'] == 'hello':
            print '\033[91m HELLO RECEIVED \033[0m'
        else: pass
    except Exception as ex:
        print ex

def start_rtm():
    """Connects to Slacks and initiates socket handshake, returns a websocket"""
    req = requests.get('https://slack.com/api/rtm.start?token='+TOKEN, verify=False)
    req = req.json()
    websocket_url = req['url']
    return websocket_url

def rtm_open_channel(channel):
    """Connects to Slacks and opens specified channel"""
    params = {
       'token' : TOKEN,
       'channel' : channel,
    }
    req = requests.get('https://slack.com/api/im.open', params=params)
    req = req.json()
    return req

def on_message(ws, message):
    parse_join(message)

def on_error(ws, error):
    print 'SOME ERROR HAS HAPPENED', error

def on_close(ws):
    print '\033[91m'+'Connection Closed'+'\033[0m'

def on_open(ws):
    print 'Connection Started'

if __name__ == '__main__':
    print 'connecting...'
    r = start_rtm()
    ws = websocket.WebSocketApp(r, on_message = on_message, on_error = on_error, on_close = on_close)
    #ws.on_open
    print 'connected'
    ws.run_forever()
