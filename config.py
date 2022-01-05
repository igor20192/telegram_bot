#!/usr/bin/python
# -*- coding: utf-8 -*-

Token = "1611999120:AAEjmujFfVNAZoh4Y2Oq8WtPFnJSuJHnyvA"
kategoria, sity = range(2)


def sity(update, context) -> int:
    import json
    import requests

    cityname = update.message.text.lower()
    try:

        response = requests.get(
            "https://pfa.foreca.com/authorize/token?expire_hours=2",
            params={"user": "igor-ud", "password": "eEdDgN6FrNke9jTpBC"},
        )

        data = response.json()
        authorization = data["access_token"]

        response2 = requests.get(
            (f"https://pfa.foreca.com/api/v1/location/search/{cityname}?lang=ua"),
            headers={"Authorization": (f"Bearer {authorization}")},
        )
        data2 = response2.json()
        print(data2)

        if data2["locations"]:
            index = data2["locations"][0]["id"]
            response3 = requests.get(
                (f"https://pfa.foreca.com/api/v1/forecast/daily/{index}"),
                headers={"Authorization": (f"Bearer {authorization}")},
                params={"windunit": "KMH"},
            )
            response4 = requests.get(
                f"https://pfa.foreca.com/api/v1/current/{index}",
                headers={"Authorization": (f"Bearer {authorization}")},
                params={"windunit": "KMH"},
            )
            datacurrent = response4.json()
            img = requests.get(
                f"https://www.foreca.net/meteogram.php?loc_id={data2['locations'][0]['id']}&mglang=ru&units=metric&tf=24h"
            )
            with open(
                "/home/igor_udovenko2015/telegram_bot/forecapicon/foreca.png", "wb"
            ) as f:
                f.write(img.content)
            winddirstring = datacurrent["current"]["windDirString"]
            directwind = ""
            if winddirstring == "S":
                directwind = "Южный"
            elif winddirstring == "SE":
                directwind = "Юговосточный"
            elif winddirstring == "SW":
                directwind = "Югозападный"
            elif winddirstring == "N":
                directwind = "Северный"
            elif winddirstring == "NE":
                directwind = "Северовосточный"
            elif winddirstring == "NW":
                directwind = "Северозападный"
            elif winddirstring == "E":
                directwind = "Восточный"
            elif winddirstring == "W":
                directwind = "Западный"

            update.message.reply_photo(
                photo=open(
                    f"/home/igor_udovenko2015/telegram_bot/forecapicon/{datacurrent['current']['symbol']}.png",
                    "rb",
                )
            )
            update.message.reply_text(
                f"☔️Температура-{datacurrent['current']['temperature']}°C\nПо ощущениям температура-{datacurrent['current']['feelsLikeTemp']} °C\nОтносительная влажность-{datacurrent['current']['relHumidity']} %\nТочка росы-{datacurrent['current']['dewPoint']} ° C\nСкорость ветра-{datacurrent['current']['windSpeed']} км/ч\nНаправление ветра-{directwind}\nПорыв ветра-{datacurrent['current']['windGust']} км/ч\nВероятность выпадения осадков{datacurrent['current']['precipProb']} % \nИнтенсивность осадков-{datacurrent['current']['precipRate']} мм/ч\nОблачность-{datacurrent['current']['cloudiness']} %\nВероятность грозы поблизости-{datacurrent['current']['thunderProb']} %\nУФ-индекс-{datacurrent['current']['uvIndex']}\nАтмосферное давление, приведенное к уровню моря-{datacurrent['current']['pressure']} гПа\nВидимость-{datacurrent['current']['visibility']} м"
            )
            update.message.reply_photo(
                photo=open(
                    "/home/igor_udovenko2015/telegram_bot/forecapicon/foreca.png", "rb"
                )
            )
            return kategoria

        else:
            update.message.reply_text("☔️Нет города в базе")
            return kategoria

    except requests.exceptions.ConnectTimeout:
        print("Connectimeout")
        return kategoria
