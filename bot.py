from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import configparser
import logging
import random


config = configparser.ConfigParser()
config.read("bot2.ini")

updater = Updater(token=config["KEYS"]["BOT_TOKEN"], use_context="true")
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id= update.effective_chat.id, text="I'm a bot, please talk to me!")
    print(update.effective_user.id)

def spin_the_wheel(update, context):
    #instantiate an empty array with the chat id
    globals()[update.effective_chat.id]= []
    context.bot.send_message(chat_id= update.effective_chat.id, text="Wheel started! Please type in the choices.")

def text(update, context):
    # if the array exists, add to it and inform the user
    if update.effective_chat.id in globals():
        globals()[update.effective_chat.id].append(update.message.text)
        message = update.message.text + " added!"
        context.bot.send_message(chat_id= update.effective_chat.id, text=message)

def spin(update, context):
    # returns a random choice from the list and delete the list
    choice = random.choice(globals()[update.effective_chat.id])
    message = choice + " was selected!"
    del globals()[update.effective_chat.id]
    context.bot.send_message(chat_id= update.effective_chat.id, text=message)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("spin_the_wheel", spin_the_wheel))
dispatcher.add_handler(CommandHandler("spin", spin))
dispatcher.add_handler(MessageHandler(Filters.text, text))
updater.start_polling()