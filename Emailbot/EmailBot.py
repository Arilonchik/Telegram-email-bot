from telegram import Bot
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from Emailbot.config import TG_Token
from Emailbot.config import TG_API_URL
from threading import Thread
from Emailbot.EmailChecker import take_mess
import time

password = 'your_password'   # Bot entry password.
chatKeys = {}
lastMes = 0


def check_send(bot: Bot):
    """
    Check email by EmailChecker every 300 sec and send new mails to every chat, that connected to bot every.
    :param bot: Bot

    """
    global lastMes
    global chatKeys
    time.sleep(300)
    while True:
        text, lastMes = take_mess(lastMes)
        if text != "NO":
            for key in chatKeys:
                if chatKeys[key] == 1:
                    bot.send_message(
                        chat_id=key,
                        text=text
                    )
        time.sleep(300)


def do_start(bot: Bot, update: Update):
    """
    Start new chat, checking password.
    :param bot: Bot
    :param update: Update

    """
    chat_id = update.message.chat_id
    if chat_id in chatKeys.keys():
        text = 'U have already started'
    else:
        text = 'Started, enter password'
        chatKeys[chat_id] = 0
    bot.send_message(
        chat_id=chat_id,
        text=text
    )


def do_answer(bot: Bot, update: Update):
    """
    Answer to another messages.
    :param bot: Bot
    :param update: Update

    """
    chat_id = update.message.chat_id
    answer = update.message.text
    text = ''
    if chat_id in chatKeys.keys():
        if chatKeys.get(chat_id) == 1:
            check = False
        else:
            check = True
            if answer == password:
                chatKeys[chat_id] = 1
                text = 'Right password, working'
            else:
                text = 'Wrong password'
    else:
        text = 'Problems'
        check = True
    if check:
        bot.send_message(
            chat_id=chat_id,
            text=text
        )


def main():
    """ Bot starts. """
    bot = Bot(
        token=TG_Token,
        base_url=TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_answer)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()

    checker = Thread(target=check_send, args=(bot,))
    checker.start()
    updater.idle()


if __name__ == '__main__':
    main()
