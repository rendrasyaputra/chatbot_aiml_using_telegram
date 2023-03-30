import aiml
import random
import mysql.connector
from library.preprocessing import preprocess
from telegram.ext import Updater, MessageHandler, Filters

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chatbotaiml"
)

kernel = aiml.Kernel()
kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml")

DEFAULT_RESPONSES = [
    "Maaf, kami tidak mengerti maksud pertanyaan anda",
    "Maaf, kami tidak dapat mengerti pertanyaan anda, silakan ketikkan ulang pertanyaan anda",
    "Pertanyaan yang anda inputkan tidak ada pada database kami, mohon masukkan pertanyaan lain"]

def get_bot_response(update, context):
    query = update.message.text
    print ("Inputan User : ", query )
    sentence = query
    preprocessed_text = preprocess(sentence)
    response = kernel.respond(preprocessed_text)
    x = response.replace("((", "<").replace("))", ">")
    if x is None or x == "":
        cursor = mydb.cursor()
        cursor.execute("SELECT bot_response FROM conversation WHERE user_input LIKE %s", (preprocessed_text,))
        result = cursor.fetchone()
        if result is not None:
            update.message.reply_text(result[0].replace("<br>", "\n"))
        else:
            update.message.reply_text(random.choice(DEFAULT_RESPONSES))
    else:
        update.message.reply_text(x)

updater = Updater('6286336431:AAH-MoisrmkXIZDpSv4UjY_B0dvOfgFgyk8', use_context=True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text, get_bot_response))

updater.start_polling()
updater.idle()