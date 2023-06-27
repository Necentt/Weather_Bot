from config import tg_token, weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import requests
import datetime as dt
bot = Bot(token=tg_token)
dp = Dispatcher(bot, storage=MemoryStorage())
name_city = ['Элиста']


class GetCity(StatesGroup):
    waiting_for_get_city = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['/help', '/today', '/for5days', '/set_name']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer(
        f"Привет! Я твой личный бот ассистент, буду облегчать тебе жизнь. \n"
        f'Для того, чтобы я смог выдать тебе погоду, ты должен нажать на "/set_name" и указать там его название'
        f"Хочешь узнать больше, пиши /help",
        reply_markup=keyboard
    )


@dp.message_handler(commands='help')
async def tg_help(message: types.Message):
    await message.reply(
        f"Привет! На данный момент я могу только выдавать погоду. \n"
        f"Ты можешь ввести название города и я дам тебе погоду на сегодняшний день или на пять дней. \n"
        f"/start - Там я тебя поприветствую и попрошу название города, в котором тебя интересует погода. \n"
        f'/feedback - нужна для того, чтобы я понимал, что я могу добавить или убрать из этого бота. \n'
        f'/set_name - ввод названия нужного города. \n'
        f'/today - погода на сегодняшний день(прежде чем использовать эту команду, нужно ввести название города. \n'
        f'/for5days - погода на пять дней(прежде чем использовать эту команду, нужно ввести название города. \n'
    )


@dp.message_handler(commands='feedback')
async def feedback(message: types.Message):
    await message.reply(f"Привет! Спасибо, что пользуешься моим ботом.\n"
                        f"если есть предложения, то прошу писать на necent@vk.com")


@dp.message_handler(commands='today')
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
    global name_city
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q='
                     f'{name_city[-1]}&appid={weather_token}&units=metric')

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


@dp.message_handler(commands='for5days')
async def get_weather_5_days(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    global name_city
    r = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q='
                     f'{name_city[-1]}&appid={weather_token}&units=metric')
    data = r.json()
    #  pprint(data)
    s = ''
    city = data['city']['name']
    for i in range(0, 33, 8):
        date = dt.datetime.fromtimestamp(data['list'][i]['dt']).strftime('%d.%m.%Y')
        day_temp = data['list'][i]['main']['temp']
        weather_description = data["list"][i]["weather"][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"
        s += f'Погода на пять дней в городе: {city} \nДата: {date} \nТемпература: {day_temp}C° {wd} \n'
    await message.answer(s)


@dp.message_handler(commands='set_name', state='*')
async def start_city(message: types.Message, state: FSMContext):
    await message.answer('Введите название вашего города')
    await state.set_state(GetCity.waiting_for_get_city.state)


@dp.message_handler(state=GetCity.waiting_for_get_city)
async def get_city(message: types.Message, state: FSMContext):
    try:
        global name_city
        r = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q='
                         f'{message.text}&appid={weather_token}&units=metric')
        data = r.json()
        city = data['city']['name']
        await message.answer('Название города установлено')
        name_city.append(message.text)
        await state.finish()
    except:
        await message.answer('\U00002620 Проверьте и заново введите название города \U00002620')
        return

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
