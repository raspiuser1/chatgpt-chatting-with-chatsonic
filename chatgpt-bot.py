#subtitle bot
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import telegram
import os
import sys
#pip install openai
import openai
import requests
import time

#==============================================opties=================================================
#api key voor de openai text generator
openai.api_key = open("ai_key.txt").readline().rstrip()


#chatsonic info
chatsonic_api_key = open("chatsonic_api.txt").readline().rstrip()
urlchatsonic = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"
headerschatsonic = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-API-KEY": chatsonic_api_key
}


#credits @ https://github.com/raspiuser1/
#token that can be generated talking with @BotFather on telegram, put this in key.txt
my_token=open("key.txt").readline().rstrip()

#==============================================================================================================

updater = Updater(my_token,use_context=True)
bot = telegram.Bot(token=my_token)

def help(update: Update, context: CallbackContext):
	update.message.reply_text(""" ======Options YT subtitle Bot======
Credits @ https://github.com/raspiuser1

/go [ question to chatgpt which will be aswered by chatsonic ]

""")

def stop(update: Update, context: CallbackContext):
    global go_flag
    go_flag = False
    update.message.reply_text = "Bot stopped"
    
def chatgpt(x):
    response = openai.Completion.create(model="text-davinci-003", prompt=x, temperature=0.7, max_tokens=1000)
    answer_chatgpt = response["choices"][0]["text"]
    return answer_chatgpt
    
def chatsonic(x):
    responsechatsonic = requests.post(urlchatsonic, json={"enable_memory": False,"enable_google_results": "True","input_text": x}, headers=headerschatsonic)
    response_Json = responsechatsonic.json()
    answer_chatsonic = response_Json["message"]
    return answer_chatsonic

def go(update: Update, context: CallbackContext):
    global answer1,answer2,go_flag
    go_flag = True
    quest = update.message.text[4:]
    print("User: "+ quest)
    answer1 = chatgpt(quest)
    #print(chatsonic(quest))
    print("chatgpt: " + answer1)
    update.message.reply_text("chatgpt: " + answer1)
    time.sleep(1.5)
    while go_flag:
        answer2 = chatsonic(answer1)
        update.message.reply_text("chatsonic: " + answer2)
        print("chatsonic: " + answer2)
        time.sleep(1.5)
        answer1 = chatgpt(answer2)
        update.message.reply_text("chatgpt: " + answer1)
        print("chatgpt: " + answer1)
        time.sleep(1.5)
        


def main():
    #telegram options=================================================================================================
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('go', go))
    updater.dispatcher.add_handler(CommandHandler('stop', stop))
    updater.start_polling(timeout=600)
    #updater.idle()
main()    
