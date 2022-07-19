from quart import Quart, request
from telegram.update import Update
import telegram
import os
from dotenv import load_dotenv
from database import get_database

load_dotenv()

app = Quart(__name__)

db = get_database()
people = db["people"]

subscribed_ids = set()
bot = telegram.Bot(os.environ['TELE_KEY'])
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
            person_id = update.message.from_user.id
            username = update.message.from_user.username
            if text in ['start','/start']:
                bot.send_message(chat_id = chat_id, 
text= 
f''' 
Hello 👋, {name}. 
commands: 
/spotify (Subscribe to get notified when there's a new song on da playlist..) 
/stopSpotify (Unsubscribe from getting spotify updates)
    ''')
                return "201"
            elif text in ['spotify', '/spotify']:
                person = people.find_one({"chat_id":chat_id})
                if person:
                    bot.send_message(chat_id = chat_id, text=''' You've already subscribed to Spotify updates. send /ewspotify or /stopspotify to unsubscribe.''' )
                    return "201"
                else:
                    person = people.find_one({"id":person_id})
                    if person:
                        people.update_one({"id":person_id}, {"$set":{"chat_id":chat_id}})
                    else:
                        people.insert_one({
                            "name":name,
                            "id":person_id,
                            "chat_id":chat_id,
                            "username":username,
                            "preferSpotify":True
                        })
                    bot.send_message(chat_id = chat_id, text=''' You just subscribed to Spotify updates. send /ewSpotify or /stopSpotify to unsubscribe.''')
                    return "201"
            elif text in ['/ewspotify', '/stopspotify', 'stop spotify', 'ew spotify']:
                person = people.find_one({"chat_id":chat_id})
                if person and person['preferSpotify']:
                    people.update_one({"chat_id":chat_id}, {"$set":{"preferSpotify":False}})
                    bot.send_message(chat_id = chat_id, text=''' You just unsubscribed to Spotify updates. Thankyou ''')
                else:
                    bot.send_message(chat_id = chat_id, text='''You haven't subscribed to unsubscibe.''')
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
            track = data['track']
            artist = data['artist']
            link = data['link']
            friends = people.find({"preferSpotify":True})
            for friend in friends:
                bot.send_message(text=f'New song on da playlist! {track} by {artist}. {link}', chat_id=friend["chat_id"])
        return "done" 
    except:
        print('An exception occurred')
        return "done"
       
        
