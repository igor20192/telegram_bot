#!/usr/bin/env python


import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


kategoria, city = range(2)


def start(update: Update, context: CallbackContext) -> int:

    reply_keyboard = [
        ["NEWS📰", "ФУТБОЛЛ⚽️", "SAT NEWS📡", "SAT ТАБЛИЦА ЧАСТОТ\n🛰", "Погода☔️"]
    ]
    update.message.reply_text(
        "Выберите раздел 👇",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return kategoria


def kategor(update: Update, context: CallbackContext) -> int:
    if update.message.text == "ФУТБОЛЛ⚽️":
        try:
            url = "https://satsis.info/forum/sputnikovye-novosti-chast-2_07-08-2015_page_2"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            quotes = soup.find_all(
                "div", {"class": "shb-body st-sidebar-block-bg-football"}
            )

            for q in quotes:
                p = q.text
            update.message.reply_text("⚽️" + p)
            return kategoria
        except ConnectionError:
            update.message.reply_text("Ошибка соеденения")
        except ConnectionResetError:
            update.message.reply_text(
                "Удаленный хост принудительно разорвал существующее подключение"
            )
            return kategoria
    elif update.message.text == "SAT NEWS📡":
        try:
            url1 = "http://www.uzsat.net/forum/12-%D1%82%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D0%BD%D0%B4%D0%B5%D1%80%D0%BD%D1%8B%D0%B5-%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F/"
            responce1 = requests.get(url1)
            soup1 = BeautifulSoup(responce1.text, "lxml")
            qs = soup1.find_all("span", {"class": "ipsPagination_last"})

            for i in qs[:1]:
                h = i.find("a").get("href")

            url = h
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            quotes = soup.find_all("p")

            x = 0
            for q in quotes[2:-2]:
                ps = q.text
                if len(ps) > 4095:
                    update.message.reply_text("📡" + ps[x:4095])
                    x = 4095
                    while True:
                        if len(ps[x:]) > 4095:
                            update.message.reply_text("📡" + ps[x : x + 4095])
                            x += 4095
                        else:
                            update.message.reply_text("📡" + ps[x:])
                            break
                else:
                    update.message.reply_text("📡" + ps)
            return kategoria
        except ConnectionError:
            update.message.reply_text("Ошибка соеденения")
            return kategoria
    elif update.message.text == "SAT ТАБЛИЦА ЧАСТОТ\n🛰":
        data = {
            "orbitpoz": ["177w_74e", "72e_1.9e", "0.8e_61w"],
            "Перейти": [
                "https://www.lyngsat.com/asia.html",
                "https://www.lyngsat.com/europe.html",
                "https://www.lyngsat.com/atlantic.html",
            ],
        }
        df = pd.DataFrame(data, index=["Asia", "Europe", "Atlantik"])

        update.message.reply_text(
            "          orbitpoz                                Перейти\nAsia      177w_74e      https://www.lyngsat.com/asia.html\nEurope    72e_1.9e    https://www.lyngsat.com/europe.html\nAtlantik  0.8e_61w  https://www.lyngsat.com/atlantic.html"
        )
        return kategoria
    elif update.message.text == "NEWS📰":
        try:
            url = "https://news.google.com/topstories?hl=ru&gl=UA&ceid=UA:ru"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            quotes = soup.find_all("a", {"class": "VDXfz"})
            for p in quotes:
                x = p.get("href")
                update.message.reply_text("https://news.google.com" + x[1:])

            return kategoria

        except ConnectionError:
            update.message.reply_text("Ошибка соеденения")
            return kategoria

    elif update.message.text == "Погода☔️":
        update.message.reply_text("☔️Введите название города")
        return city


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    from config import Token, sity

    # Create the Updater and pass it your bot's token.
    updater = Updater(Token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states KATEGOPIA
    conv_handler = ConversationHandler(
        allow_reentry=True,
        run_async=True,
        entry_points=[CommandHandler("start", start)],
        states={
            kategoria: [
                MessageHandler(
                    Filters.regex(
                        "^(NEWS📰|ФУТБОЛЛ⚽️|SAT NEWS📡|SAT ТАБЛИЦА ЧАСТОТ\n🛰|Погода☔️)$"
                    ),
                    kategor,
                ),
            ],
            city: [MessageHandler(Filters.text, sity)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
