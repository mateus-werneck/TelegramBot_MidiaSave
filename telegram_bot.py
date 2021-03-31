
import logging, time, re, shutil
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
from decoding import getMedia

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

source=''
button = 0
twitter = ''

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Olá, me manda um link do Instagram ou Twitter que eu irei procurar para você!')
    update.message.reply_text('Se você mandar um link e não receber seu arquivo em até 10 segundos. Por favor tente mandar mais uma vez!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

################################## Send Media to User  ##################################
def getLink(update, context):
    global twitter, youtube
    bot = telegram.Bot(token="TOKEN")
    url =''
    url = update.message.text
    smile = u' \U0001F604'
    
    if(re.search('twitter', url) != None):
        bot.send_message(chat_id=update.message.chat_id, text='Isso pode demorar um pouco')
        if (getSource(url) == True):
            if (twitter != ''):
                bot.send_document(chat_id=update.message.chat_id, document = open(twitter, 'rb'))
                bot.send_message(chat_id=update.message.chat_id, text='Pronto ' + smile)
                print("Salvo com Sucesso. Twitter")
                print(update.message.chat_id)  
            else:
                bot.send_message(chat_id=update.message.chat_id, text='Parece que você mandou um link inválido')   
    
    elif (re.search('instagram', url) != None):
        if(getSource(url) == True):
            bot.send_video(chat_id=update.message.chat_id, video = source)
            bot.send_message(chat_id=update.message.chat_id, text='Pronto ' + smile)
            print("Salvo com Sucesso. Instagram")
            print(update.message.chat_id) 
    
    
############################### Get Media From User Input(URL) ##################################           
def getSource(url):
    global source, button, twitter, youtube
    if (re.search('instagram', url) != None):
        source=getMedia(url, button)
        button += 1
        if (source != ''):
            return True
        else:
            return False
    elif (re.search('twitter', url)):
        twitter = getMedia(url, button)
        return True            

############################ Bot Main Function #########################################    
def main():
    """Start the bot."""
    updater = Updater("TOKEN", use_context=True, request_kwargs={'read_timeout': 1000, 'connect_timeout': 1000})

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, getLink))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()