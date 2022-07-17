from tokenize import String
from turtle import up
from matplotlib.font_manager import json_dump
from quart import Quart, request
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import telegram
import os

telegram_bot_token="5409399469:AAGRoB-pli3h6hcF42kvjyPbNBirjeUaUdg"
chat_ids = set()
  
bot = telegram.Bot(telegram_bot_token)
updater = Updater("5409399469:AAGRoB-pli3h6hcF42kvjyPbNBirjeUaUdg",
                  use_context=True)
  
  
def start(update: Update, context: CallbackContext):
    if(update.message.chat.id in chat_ids):
        update.message.reply_text(f'''
        Hey {update.message.chat.first_name}. You've already subscribed to see Abhishek's playlist                         
        ''')
    else:
        chat_ids.add(update.message.chat.id)
        update.message.reply_text(f'''
        Hey {update.message.chat.first_name}. You've just subscribed to see Abhishek's playlist                         
        ''')
  
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, start))

updater.start_polling()
  
# updater.start_webhook(listen="0.0.0.0",
#                       port=int(os.environ.get('PORT', 5000)),
#                       url_path=telegram_bot_token,
#                       webhook_url= "https://helloautomate.herokuapp.com/" + telegram_bot_token
#                       )

app = Quart(__name__)

@app.route('/')
async def hello():
    return 'hello'

@app.route('/triggerSpotify', methods=['GET','POST'])
async def triggerSpotify():
    if request.method =='POST':
        message = str(await request.get_json())
        for id in chat_ids:
            bot.send_message(text=f'Abhishek just liked {message}', chat_id=id)
        return "done"    
        
