from quart import Quart
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import os

telegram_bot_token="5409399469:AAGRoB-pli3h6hcF42kvjyPbNBirjeUaUdg"
  
updater = Updater("5409399469:AAGRoB-pli3h6hcF42kvjyPbNBirjeUaUdg",
                  use_context=True)
  
  
def start(update: Update, context: CallbackContext):
    update.message.reply_text("""
    HelloAutoMateBot.                          
    """)
  
def help(update: Update, context: CallbackContext):
    update.message.reply_text("""""")
    
def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("""unknown command bro""")
    
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

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
