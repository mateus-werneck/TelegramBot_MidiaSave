
import logging, time, re, shutil, os
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
    global twitter
    bot = telegram.Bot(token="TOKEN")
    url =''
    url = update.message.text
    smile = u' \U0001F604'
    chat_id = update.message.chat_id
    if re.search('twitter', url) != None or re.search('t.co', url) != None:
        bot.send_message(chat_id=update.message.chat_id, text='Isso pode demorar um pouco')
        if (getSource(url, chat_id) == True):
            if (twitter != 'inválido' and twitter != ''):
                bot.send_document(chat_id=update.message.chat_id, document = open(twitter, 'rb'))
                bot.send_message(chat_id=update.message.chat_id, text='Pronto ' + smile)
                print("Salvo com Sucesso. Twitter")
                print(update.message.chat_id, update.message.chat.first_name, update.message.chat.last_name, "@" + update.message.chat.username)
                os.remove('/home/mateus/Documents/Python/telegram_bot/twitter.mp4')
            else:
                bot.send_message(chat_id=update.message.chat_id, text='Parece que você mandou um link inválido. No caso de uma Imagem ou GIF você pode salvar a partir do link que você mandou logo acima')
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Parece que você mandou um link inválido. No caso de uma Imagem ou GIF você pode salvar a partir do link que você mandou logo acima')

    elif (re.search('instagram', url) != None):
        if(getSource(url, chat_id) == True):
            if(type(source) is str):
                if (re.search('instagram', source) != None):
                    bot.send_video(chat_id=update.message.chat_id, video = source, timeout=3600)
                    bot.send_message(chat_id=update.message.chat_id, text='Pronto ' + smile)
                    print("Salvo com Sucesso. Instagram")
                    print(update.message.chat_id, update.message.chat.first_name, update.message.chat.last_name, "@" + update.message.chat.username)
                elif (re.search('.mp4', source) != None):
                    bot.send_video(chat_id=update.message.chat_id, video = open(source, 'rb'), timeout=3600)
                    bot.send_message(chat_id=update.message.chat_id, text='Pronto ' + smile)
                    print("Salvo com Sucesso. Instagram")
                    print(update.message.chat_id, update.message.chat.first_name, update.message.chat.last_name, "@" + update.message.chat.username)
                    shutil.rmtree('/home/mateus/Documents/Python/telegram_bot/IGTV')
            elif type(source) is list:
                for path in source:
                    bot.send_video(chat_id=update.message.chat_id, video = open (path, 'rb'), timeout=3600)
                bot.send_message(chat_id=update.message.chat_id, text='Pronto ' + smile)
                print("Salvo com Sucesso. Instagram")
                print(update.message.chat_id, update.message.chat.first_name, update.message.chat.last_name, "@" + update.message.chat.username)
                shutil.rmtree('/home/mateus/Documents/Python/telegram_bot/IGTV')
                source.clear()
            elif(getSource(url) == -1):
                bot.send_message(chat_id=update.message.chat_id, text='Infelizmente IGTVs não sao suportados por serem muito grandes.')
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Não deu certo. Verifique se a conta do Instagram é privada/fechada')

    elif re.search('youtube', url) != None or re.search('youtu.be', url) != None:
        bot.send_message(chat_id=update.message.chat_id, text='Isso pode levar um tempo. Aguarde...')
        bot.send_message(chat_id=update.message.chat_id, text='Se o video for muito grande ele será dividido em partes.')
        if(getSource(url, chat_id) == True):
            if type(source) is str:
                bot.send_video(chat_id=update.message.chat_id, video = open(source, 'rb'), timeout=3600)
                bot.send_message(chat_id=update.message.chat_id, text='Pronto ' + smile)
                print("Salvo com Sucesso. Youtube")
                print(update.message.chat_id, update.message.chat.first_name, update.message.chat.last_name, "@" + update.message.chat.username)
                shutil.rmtree('/home/mateus/Documents/Python/telegram_bot/youtube')

            elif type(source) is list:
                for path in source:
                    bot.send_video(chat_id=update.message.chat_id, video = open(path, 'rb'), timeout=3600)
                bot.send_message(chat_id=update.message.chat_id, text='Pronto ' + smile)
                print("Salvo com Sucesso. Youtube")
                print(update.message.chat_id, update.message.chat.first_name, update.message.chat.last_name, "@" + update.message.chat.username)
                shutil.rmtree('/home/mateus/Documents/Python/telegram_bot/youtube')
                source.clear()

            '''
            if (re.search('mp3', source) != None):
                bot.send_audio(chat_id=update.message.chat_id, audio = open(source, 'rb'))'''

############################### Get Media From User Input(URL) ##################################

def getSource(url, chat_id):
    bot = telegram.Bot(token="TOKEN")
    global source, button, twitter
######################################### Instagram Check #######################################
    if (re.search('instagram', url) != None):
        source=getMedia(url, button, bot, chat_id)
        button += 1
        if type(source) is str:
            if (re.search('instagram', source) != None or re.search('.mp4', source) != None):
                return True
            else:
                return False

        elif type(source) is list:
            for i in source:
                if re.search('.mp4', i) != None:
                    return True
                else:
                    return False
########################################### Twitter Check #######################################
    elif re.search('twitter', url) != None or re.search('t.co', url) != None:
        twitter = getMedia(url, button, bot, chat_id)
        if twitter == 'inválido':
            return False
        elif (twitter != '' and twitter != 'inválido'):
            return True
######################################### Youtube Check #########################################

    elif re.search('youtube', url) != None or re.search('youtu.be', url) != None:
        source=getMedia(url, button, bot, chat_id)
        return True
############################ Bot Main Function #########################################
def main():
    """Start the bot."""
    updater = Updater("TOKEN", use_context=True)

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
