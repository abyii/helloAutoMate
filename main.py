from quart import Quart, request
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import telegram
import os

app = Quart(__name__)

telegram_bot_token="5409399469:AAGRoB-pli3h6hcF42kvjyPbNBirjeUaUdg"
subscribed_ids = set()
  
bot = telegram.Bot(telegram_bot_token)
hook = bot.set_webhook("https://helloautomate.herokuapp.com/")
if not hook:
    print("Webhook setup failed. exiting.");
    exit(0)


@app.route('/', methods=['GET','POST'])
async def getMessages():
    try:
        if request.method=='GET':
            return "Hello"
        elif request.method=='POST':
            req = await request.get_json(force=True)
            update = Update.de_json(req, bot)
            text = update.message.text.lower()
            chat_id = update.message.chat.id
            name = update.message.chat.first_name
            if text in ['start','/start']:
                bot.send_message(chat_id = chat_id, text= f''' Hello 👋, {name}. commands: /spotify (Subscribe to get notified when Abhishek likes a song on Spotify) ''')
                return "201"
            elif text in ['spotify', '/spotify']:
                if chat_id in subscribed_ids:
                    bot.send_message(chat_id = chat_id, text=''' You've already subscribed to Spotify updates. send /ewspotify or /stopspotify to unsubscribe.''' )
                    return "201"
                else:
                    subscribed_ids.add(chat_id)
                    bot.send_message(chat_id = chat_id, text=''' You just subscribed to Spotify updates. send /ewSpotify or /stopSpotify to unsubscribe.''')
                    return "201"
            elif text in ['/ewspotify', '/stopspotify', 'stop spotify', 'ew spotify']:
                subscribed_ids.remove(chat_id)
                bot.send_message(chat_id = chat_id, text=''' You just unsubscribed to Spotify updates. Thankyou ''')
                return "201"
            else:
                bot.send_message(chat_id = chat_id, text="unknown command bro")
                return "201"
    except:
        return "Something went wrong." 

@app.route('/triggerSpotify', methods=['GET','POST'])
async def triggerSpotify():
    try:
        if request.method =='POST':
            data = await request.get_json()
            info = list(data.values())
            for id in subscribed_ids:
                bot.send_message(text=f'Abhishek just liked {info[2]} by {info[0]}. {info[1]}', chat_id=id)
        return "done" 
    except:
        print('An exception occurred')
        return "done"
       
        
