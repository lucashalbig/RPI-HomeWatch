from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext.filters import Filters
from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from os import popen, stat
import logging
import re
import sys
from os import popen
import requests
from requests.auth import HTTPBasicAuth

logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.DEBUG)

updater = Updater('750271675:AAEkV_kRGIVD6cC9wMrwndNctDxNKjw2Ru8'); dispatcher = updater.dispatcher

def voice_message_handeling(bot, update):
	msg = update.message
	voice = msg.voice
	voice = msg.voice
	file = voice.get_file()
	x = file.download_as_bytearray()
	auth = HTTPBasicAuth('apikey', '6ZQckyY_kEgJPG8Jr7bNeH52HXXKbYPbSkxjp9QDF4sd')
	print('Requesting recognition...')
	r = requests.post('https://gateway-syd.watsonplatform.net/speech-to-text/api/v1/recognize?model=de-DE_BroadbandModel', 
		data = x, headers = {'Accept':'application/json','Content-Type': 'audio/ogg'}, auth = auth)
	r.raise_for_status()
	jso = r.json()
	result = jso['results'][0]
	alt = result['alternatives'][0]
	text = alt['transcript'].strip()
	msg.reply_text(f'*Analysed text*\n{text}', parse_mode = 'Markdown')
	if text in ['start','beenden','foto','video']:
		msg.reply_text('Befehl erkant')
	else:
		msg.reply_text('Befehl nicht erkant')
	

			

dispatcher.add_handler(MessageHandler(Filters.voice, voice_message_handeling))

updater.start_polling()
updater.idle()
