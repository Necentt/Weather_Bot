import requests
from config import weather_token
from pprint import pprint
import datetime as dt


def get_weather(city, weather_token):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric')

        data = r.json()
        pprint(data)

        """city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_time = dt.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_time = dt.datetime.fromtimestamp(data['sys']['sunset'])
        length_day = dt.datetime.fromtimestamp(data['sys']['sunset']) - \
            dt.datetime.fromtimestamp(data['sys']['sunrise'])
        print(f"Сегодняшняя дата: {dt.datetime.now().strftime('%Y.%m.%d %H:%M')}\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_time}\nЗакат солнца: {sunset_time}\nПродолжительность дня: {length_day}\n"
              f"Хорошего дня!"
              )"""

    except Exception as ex:
        print(ex)
        print('Проверьте название города')


def get_weather_5_days(city, weather_token):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        r = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_token}&units=metric')

        data = r.json()
        #  pprint(data)

        city = data['city']['name']
        print(f'Погода на пять дней в городе: {city} \n')
        for i in range(0, 33, 8):
            date = dt.datetime.fromtimestamp(data['list'][i]['dt']).strftime('%Y.%m.%d')
            day_temp = data['list'][i]['main']['temp']
            weather_description = data["list"][i]["weather"][0]['main']
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Посмотри в окно, не пойму что там за погода!"
            print(f'Дата: {date} \n'
                  f'Температура: {day_temp}C° {wd} \n'
                  )

    except Exception as ex:
        print(ex)
        print('Проверьте название города')


def main():
    city = input('Введите название города: ')
    get_weather_5_days(city, weather_token)


if __name__ == '__main__':
    main()
