from config import tg_token, weather_token
import requests
import datetime as dt
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def start_command(message: types.Message):
    await message.reply(
        f"Привет! На данный момент я могу только выдавать погоду. \n"
        f"Ты можешь ввести название города и я дам тебе погоду на сегодняшний день. \n"
        f"У меня пока есть только две команды: \n"
        f"/start - Там я тебя поприветствую и попрошу название города, в котором тебя интересует погода. \n"
        f'/feedback - нужна для того, чтобы я понимал, что я могу добавить или убрать из этого бота'
    )


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(
        f"Привет! Напиши название своего города и я отправлю тебе погоду. \n"
        f"Хочешь узнать больше, пиши /help"
    )


@dp.message_handler(commands=['feedback'])
async def start_command(message: types.Message):
    await message.reply(f"Привет! Спасибо, что пользуешься моим ботом.\n"
                        f"если есть предложения, то прошу писать на necent@vk.com")


@dp.message_handler()
async def get_weather(message: types.Message):
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
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q='
                         f'{message.text}&appid={weather_token}&units=metric')

        data = r.json()

        city = data['name']
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
        await message.reply(
              f"Сегодняшняя дата: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_time}\nЗакат солнца: {sunset_time}\nПродолжительность дня: {length_day}\n"
              f"Хорошего дня!"
              )
    except:
        await message.reply('\U00002620 Проверьте название города \U00002620')


if __name__ == '__main__':
    executor.start_polling(dp)
