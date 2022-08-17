from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import configparser
import logging
import random
import datetime

config = configparser.ConfigParser()
config.read("bot.ini")

updater = Updater(token=config["KEYS"]["BOT_TOKEN"], use_context="true")
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
first_time = datetime.datetime.now()

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
    time = True
    first_time = datetime.datetime.now()
    choice = random.choice(globals()[update.effective_chat.id])
    message = choice + " was selected!"
    context.bot.send_message(chat_id= update.effective_chat.id, text=message)
    context.bot.send_message(chat_id= update.effective_chat.id, text= " To clear the wheel, enter /clear or you can try again.")
    timing(update, context,time)
    
def clear(update,context):
    del globals()[update.effective_chat.id]
    context.bot.send_message(chat_id= update.effective_chat.id, text= "Memory Cleared")
    
def timing(update,context,time):
    while time == True:
        final_time = datetime.datetime.now()
        difference = final_time - first_time
        if difference.total_seconds() >= 120:
             del globals()[update.effective_chat.id]
             context.bot.send_message(chat_id= update.effective_chat.id, text= "Memory Cleared due to inactivity")
             break

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("spin_the_wheel", spin_the_wheel))
dispatcher.add_handler(CommandHandler("spin", spin))
dispatcher.add_handler(CommandHandler("clear", clear))
dispatcher.add_handler(MessageHandler(Filters.text, text))
updater.start_polling()