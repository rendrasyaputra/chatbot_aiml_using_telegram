import aiml
import random
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters, Updater, CommandHandler
from library.preprocessing import preprocess

kernel = aiml.Kernel()
kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml")

bot = telegram.Bot(token='6286336431:AAH-MoisrmkXIZDpSv4UjY_B0dvOfgFgyk8')


DEFAULT_RESPONSES = [
    "Maaf, kami tidak mengerti maksud pertanyaan anda",
    "Maaf, kami tidak dapat mengerti pertanyaan anda, silakan ketikkan ulang pertanyaan anda",
    "Pertanyaan yang anda inputkan tidak ada pada database kami, mohon masukkan pertanyaan lain"]

def get_bot_response(text):
    preprocessed_text = preprocess(text)
    response = kernel.respond(preprocessed_text)
    print("Inputan User : ", text)
    x = response.replace("((", "<").replace("))", ">")
    x = x.replace("<br>", "\n")
    print("Respon Bot : ", x)
    if x is None or x == "":
        print(random.choice(DEFAULT_RESPONSES))
        return random.choice(DEFAULT_RESPONSES)
    return x

def telegram_handler(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    response = get_bot_response(text)
    context.bot.send_message(chat_id=chat_id, text=response, parse_mode='HTML')

updater = Updater(token='6286336431:AAH-MoisrmkXIZDpSv4UjY_B0dvOfgFgyk8')
dispatcher = updater.dispatcher


def start_handler(update, context):
    chat_id = update.message.chat_id
    response = "Hai! Saya PMB BOT, Silakan perkenalkan diri sebelum memulai percakapan dengan PMB BOT"
    context.bot.send_message(chat_id=chat_id, text=response)

def end_handler(update, context):
    chat_id = update.message.chat_id
    response = "Terima Kasih telah menggunakan layanan PMB BOT"
    context.bot.send_message(chat_id=chat_id, text=response)

start_handler = CommandHandler('start', start_handler)
dispatcher.add_handler(start_handler)

telegram_handler = MessageHandler(Filters.text, telegram_handler)
dispatcher.add_handler(telegram_handler)

end_handler = CommandHandler('end', end_handler)
dispatcher.add_handler(end_handler)

if __name__ == "__main__":
    updater.start_polling()