from telegram.ext import Updater, CommandHandler
from terminator import handlepg, getpid
from os import popen
import logging

# Den Ordner mit dem Kamera-Modul importieren
from sys import path
path.append('/usr/lib/python3/dist-packages')

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

updater = Updater('750271675:AAEkV_kRGIVD6cC9wMrwndNctDxNKjw2Ru8'); dispatcher = updater.dispatcher
#~ print(updater.bot.get_me())

def isRunning():
    motion_pid, err = getpid()
    if motion_pid:
        return True
    else:
        return False

def start(bot, update):
    update.message.reply_text('Willkommen beim Motion-Überwachungs-Kontrollzentrum.\n\
Hier können Sie Ihr Überwachungssystem aus der Ferne steuern.\n\
Um das System zu starten senden Sie /startMotion und um das System zu beenden senden Sie /termMotion')
dispatcher.add_handler(CommandHandler('start', start))


def startMotion(bot, update):
    motion_started = isRunning()
    if not motion_started:
        popen('sudo motion')
        update.message.reply_text('Motion Start-Befehl wurde ausgeführt.')
        motion_started = True
    else:
        update.message.reply_text('Motion wird bereits ausgeführt.')
dispatcher.add_handler(CommandHandler('startMotion', startMotion))


def termMotion(bot, update):
    motion_started = isRunning()
    if motion_started:
        x = handlepg()
        update.message.reply_text(x)
        motion_started = False
    else:
        update.message.reply_text('Motion wurde bereits beendet.')
dispatcher.add_handler(CommandHandler('termMotion', termMotion))
        
def sendImage(bot, update):
    motion_started = isRunning()
    #~ Falls motion läuft: Beenden
    if motion_started:
        x = handlepg()
        if x != 'Erfolgreich beendet':
            update.message.reply_text('Fehler! Unerwartete Antwort vom Programm.')
    #~ Die Kamera-Bibliothek importieren
    from picamera import PiCamera
    # Die Kamera initialisieren (die Kamera wird nicht mehr von anderen Programmen zugänglich sein.)
    camera = PiCamera()
    # Ein Bild machen und speichern
    camera.capture('shot.jpg')
    #~ Das Bild an den User senden
    update.message.reply_photo(open('shot.jpg', 'rb'))
    #~ Die Kamera wieder für andere Programme freigeben
    camera.close()
    #~ Hinweis an den User senden
    if motion_started:
        update.message.reply_text('Nicht vergessen... motion lief vor dieser Bildaufnahme und nun nicht mehr, wieder starten mit /startMotion')
dispatcher.add_handler(CommandHandler('sendImage', sendImage)) 

updater.start_polling()
updater.idle()







