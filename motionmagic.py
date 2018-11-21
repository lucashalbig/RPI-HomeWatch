""" © Lucas Halbig@ALBBW 2018
Alle Rechte vorbehalten
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext.filters import Filters
from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from terminator import handlepg, getpid
from os import popen, stat
import logging
import re
from get_ipaddress import getIPs
import sys
from os import popen
import requests
from requests.auth import HTTPBasicAuth
import itertools


IPs = getIPs()
if len(IPs) == 0:
    print('FEHLER: Sie müssen mit einem Netzwerk verbunden, um diesen Bot verwenden zu können...') 
    sys.exit(1)

# Den Ordner mit dem Kamera-Modul importieren (für neue python Versionen)
from sys import path
path.append('/usr/lib/python3/dist-packages')


# FEHLER im Ablauf in die Konsole übergeben
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

#~ Den Bot-Updater initi
updater = Updater('750271675:AAEkV_kRGIVD6cC9wMrwndNctDxNKjw2Ru8'); dispatcher = updater.dispatcher
#~ print(updater.bot.get_me())

#~ Prüfen, ob das Programm motion läuft
def isRunning(name = 'motion'):
    motion_pid, err = getpid(name = name)
    if motion_pid:
        return True
    else:
        return False

#~ Beim Botbefehl /start eine Willkommensnachricht
def start(bot, update):
    update.message.reply_text('Willkommen beim Motion-Überwachungs-Kontrollzentrum.\n\
Hier können Sie Ihr Überwachungssystem aus der Ferne steuern.\n\
Um das System zu starten senden Sie /startMotion\n\
und um das System zu beenden senden Sie /termMotion\n\n\
Wollen Sie ein aktuelles Bild auf ihr Handy gesendet haben, schicken Sie /sendImage\n\
und wenn Sie ein Video aufzeichnen möchten, dann fangen Sie mit /sendVideo an und folgen den Anweisungen.\n\
(Es ist anzumerken, dass bei diesen Befehlen das Programm motion unterbrochen wird und somit jegliche Überwachung bis zum manuellen Neustart (via /startMotion) unterbrochen ist...)')
dispatcher.add_handler(CommandHandler('start', start))

#~ Beim Botbefehl /startMotion started das Programm, wenn es nicht bereits ausgeführt wird
def startMotion(bot, update):
    motion_started = isRunning()
    if not motion_started:
        popen('sudo motion')
        update.message.reply_text('Motion Start-Befehl wurde ausgeführt.')
        motion_started = True
    else:
        update.message.reply_text('Motion wird bereits ausgeführt.')
dispatcher.add_handler(CommandHandler('startMotion', startMotion))

#~ Beim Botbefehl /termMotion beendet das Programm, wenn es noch nicht beendet ist...
def termMotion(bot, update):
    bot.send_chat_action(update.message.from_user.id, 'typing')
    motion_started = isRunning()
    if motion_started:
        x = handlepg()
        update.message.reply_text(x)
    else:
        update.message.reply_text('Motion wurde bereits beendet.')
dispatcher.add_handler(CommandHandler('termMotion', termMotion))

def termImgView(bot, update):
    bot.send_chat_action(update.message.from_user.id, 'typing')
    feh_started = isRunning(name = 'feh')
    if feh_started:
        x = handlepg(name = 'feh')
        update.message.reply_text(x)
    else:
        update.message.reply_text('Der Bildbetrachter wird derzeit nicht ausgeführt.')
dispatcher.add_handler(CommandHandler('termImgView', termImgView))

def termMotion(bot, update):
    motion_started = isRunning()
    if motion_started:
        x = handlepg()
        update.message.reply_text(x)
    else:
        update.message.reply_text('Motion wurde bereits beendet.')
dispatcher.add_handler(CommandHandler('termMotion', termMotion))

#~ Die Kamera-Bibliothek importieren
from picamera import PiCamera

#~ Aufnahme-Prozedur
def capture(mode = 'image', length = None, filename = 'shot.jpg'):
    # Die Kamera initialisieren (die Kamera wird nicht mehr von anderen Programmen zugänglich sein.)
    camera = PiCamera()
    if mode == 'image':
        # Ein Bild machen und speichern
        camera.capture(filename)
        return True
    elif mode == 'video':
        # Ein Video aufzeichnen
        camera.start_recording('/home/pi/video.h264')
        sleep(length)
        camera.stop_recording()
        x = call(['MP4Box', '-fps', '30', '-add', '/home/pi/video.h264', filename])
        if x != 0:
            return False
        else:
            return True
    #~ Die Kamera wieder für andere Programme freigeben
    camera.close()

#~ Der Botbefehl /sendImage hält bei Bedarf das Programm motion an (erforderlich um die Kamera zu verwenden) und sendet ein aktuelles Bild an denjenigen der es angefragt hat
#~ War motion ausgeführt, so wird ein Hinweis darüber gegeben, dass es womöglich neu gestartet werden muss...
def sendImage(bot, update):
    motion_started = isRunning()
    #~ Falls motion läuft: Beenden
    if motion_started:
        x = handlepg()
        if x != 'Erfolgreich beendet':
            update.message.reply_text('Fehler! Unerwartete Antwort vom Programm.')
    #~ BILDAUFNAHME
    x = capture()
    if x:
        #~ Das Bild an den User senden
        update.message.reply_photo(open('shot.jpg', 'rb'))
    else:
        print('Es ist ein Fehler aufgetreten')
    #~ Hinweis an den User senden, damit er sofort motion wieder aktivieren kann
    if motion_started:
        update.message.reply_text('Nicht vergessen... motion lief vor dieser Bildaufnahme und nun nicht mehr, wieder starten mit /startMotion')
dispatcher.add_handler(CommandHandler('sendImage', sendImage)) 

#~ Der Botbefehl /sendVideo hält bei Bedarf das Programm motion an (erforderlich um die Kamera zu verwenden) und sendet ein aktuelles Video an denjenigen der es angefragt hat
#~ War motion ausgeführt, so wird ein Hinweis darüber gegeben, dass es womöglich neu gestartet werden muss...
def sendVideo(bot, update):
    update.message.reply_text('*Antworten Sie auf diese Nachricht mit der Zeit, die sie aufnehmen wollen!*\n\
(Beachten Sie, dass die größe auf 50 MB beschränkt ist)', 
    parse_mode = 'Markdown', reply_markup = ForceReply())
dispatcher.add_handler(CommandHandler('sendVideo', sendVideo))

def message_handeling(bot, update):
    msg = update.message
    replied_msg = msg.reply_to_message
    if replied_msg:
        msg_reply_text = replied_msg.text
        if msg_reply_text.startswith('Antworten Sie auf diese Nachricht mit '):
            x = re.search('Antworten Sie auf diese Nachricht mit ([^\n]+)', msg_reply_text)
            response_requested = x.group(1)
            if response_requested == 'der Zeit, die sie aufnehmen wollen!':
                x = re.fullmatch('(\d+h)?(\d+m)?(\d+s)?', msg.text)
                SUM_seconds = 0
                if x:
                    hours = x.group(1)
                    minutes = x.group(2)
                    seconds = x.group(3)
                    print(hours, minutes, seconds)
                    if hours:
                        addition = (int(hours[:-1])*3600)
                        SUM_seconds += addition
                        #~ print(f'Adding {addition} seconds to the sum')
                    if minutes:
                        addition = int(minutes[:-1])*60
                        SUM_seconds += addition
                        #~ print(f'Adding {addition} seconds to the sum')
                    if seconds:
                        addition = int(seconds[:-1])
                        SUM_seconds += addition
                        #~ print(f'Adding {addition} seconds to the sum')
                    keyboard = [[InlineKeyboardButton('Bestätigen', callback_data = f'CONFIRMvid_{SUM_seconds}')]]
                    msg.reply_text(f'Bestätgen Sie die folgende Zeitangabe *{msg.text}* ({SUM_seconds} Sekunden)', 
                        parse_mode = 'Markdown', reply_markup = InlineKeyboardMarkup(keyboard))
            

dispatcher.add_handler(MessageHandler(Filters.text, message_handeling))

def handlePhoto(bot, update):
    update.message.reply_text('Bild empfangen.')
    file = update.message.photo[-1].get_file()
    file.download(custom_path = 'image.jpg')
    popen('feh -F -Z image.jpg')
    update.message.reply_text('Bild wird angezeigt, beenden via /termImgView.') 
dispatcher.add_handler(MessageHandler(Filters.photo, handlePhoto))



def CBQ(bot, update):
    query = update.callback_query
    if query:
        data = query.data
        x = data.split('_')
        if x[0] == 'CONFIRMvid':
            seconds = x[1]
            motion_started = isRunning()
            #~ Falls motion läuft: Beenden
            if motion_started:
                x = handlepg()
                if x != 'Erfolgreich beendet':
                    update.message.reply_text('Fehler! Unerwartete Antwort vom Programm.')
            #~ VIDEOAUFNAHME
            x = capture(mode = 'video', length = seconds, filename = '/var/www/html/video.mp4')
            if x:
                #~ Das Video an den User senden
                #~ Das Telegram-Dateilimit berägt 50 MB pro Datei also müssen wir das Video bei Ǜberschreitung dieser Größe stattdessen auf den Webserver des PIs speichern bzw. z.b. auf 
                fstats = os.stat('/var/www/html/video.mp4')
                BYTES_SIZE = int(str(fstats.st_size))
                MiBsize = BYTES_SIZE/1024/1024
                if MiBsize <= 50:
                    update.message.reply_video(open('/var/www/html/video.mp4', 'rb'))
                else:
                    update.message.reply_text(f'http://{IPs[0]}/video.mp4')
            else:
                print('Es ist ein Fehler aufgetreten')
            #~ Hinweis an den User senden, damit er sofort motion wieder aktivieren kann
            if motion_started:
                update.message.reply_text('Nicht vergessen... motion lief vor dieser Bildaufnahme und nun nicht mehr, wieder starten mit /startMotion')
        
        
    
dispatcher.add_handler(CallbackQueryHandler(CBQ))


def voice_message_handeling(bot, update):
	commands = ['starten','beenden','foto','video','magie beenden']
	msg = update.message
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
	
	word_alts = result['word_alternatives']
	Aalternatives = []
	for word_alt in word_alts:
		alternatives = word_alt['alternatives']
		real_word_alts = []
		for alternative in alternatives:
			real_word_alts.append(alternative['word'])
		Aalternatives.append(real_word_alts)
	it_prod = itertools.product(*Aalternatives)
	x = list(it_prod)
	
	theories = []
	for a in x:
		b = ' '.join(a)
		theories.append(b)

	for theory in theories:
		if theory in commands:
			msg.reply_text(f'*Analysed command text*\n{text}', parse_mode = 'Markdown', quote = True)
			if theory == 'starten':
				startMotion(bot, update)
			elif theory == 'beenden':
				termMotion(bot, update)
			elif theory == 'foto':
				sendImage(bot, update)
			elif theory == 'video':
				sendVideo(bot, update)
			elif theory == 'magie beenden':
				updater.idle()
			break
		else:
			msg.reply_text('Befehl nicht erkant')
	

			

dispatcher.add_handler(MessageHandler(Filters.voice, voice_message_handeling))


updater.start_polling()
updater.idle()







