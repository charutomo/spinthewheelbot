from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import configparser
import logging
import random
import datetime

config = configparser.ConfigParser()
config.read("bot.ini")
data = {}

updater = Updater(token=config["KEYS"]["BOT_TOKEN"], use_context="true")
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id= update.effective_chat.id, 
    text="""
    spin_the_wheel - starts a wheel
spin - spin the wheel
add - add an option to the wheel
remove - remove an option from the wheel
flip - flip a coin""")
    print(update.effective_user.id)

def spin_the_wheel(update, context):
    #instantiate an empty array with the chat id
    data[update.effective_chat.id]= [[], 0]
    context.bot.send_message(chat_id= update.effective_chat.id, text="Wheel started! Please type in the choices.")

def add(update, context):
    # if the array exists, add to it and inform the user
    if (update.effective_chat.id in data) and (context.args != []):
        sentence = ""
        for i in range(len(context.args)):
            sentence += context.args[i] +" "
        data[update.effective_chat.id][0].append(sentence)
        message = sentence + " added!"
    elif (context.args == []):
        message = "Please add a choice after the command!"
    context.bot.send_message(chat_id= update.effective_chat.id, text=message)

def remove(update, context):
    # if the array exists, remove from it and inform the user
    if (update.effective_chat.id in data) and (context.args != []):
        try:
            sentence = ""
            for i in range(len(context.args)):
                sentence += context.args[i] +" "
            data[update.effective_chat.id][0].remove(sentence)
            message = sentence + " removed!"
        except:
            message = sentence + " does not exist!"
    elif (context.args == []):
        message = "Please add a choice after the command!"
    context.bot.send_message(chat_id= update.effective_chat.id, text=message)

def spin(update, context):
    if (update.effective_chat.id in data) and (data[update.effective_chat.id][1] != []):
        # returns a random choice from the list and delete the list
        choice = random.choice(data[update.effective_chat.id][0])
        data[update.effective_chat.id][1] = datetime.datetime.now()
        message = choice + " was selected!"
        context.bot.send_message(chat_id= update.effective_chat.id, text=message)
        for user in data:
            if ((datetime.datetime.now() - data[user][1]).seconds) >= 120:
                del data[user]
    else:
        context.bot.send_message(chat_id= update.effective_chat.id, text="Please run the /spin_the_wheel command to start a wheel!")

def flip(update, context):
    context.bot.send_message(chat_id= update.effective_chat.id, text=random.choice(["Heads", "Tails"]))


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("spin_the_wheel", spin_the_wheel))
dispatcher.add_handler(CommandHandler("spin", spin))
dispatcher.add_handler(CommandHandler("add", add))
dispatcher.add_handler(CommandHandler("remove", remove))
dispatcher.add_handler(CommandHandler("flip", flip))
updater.start_polling()