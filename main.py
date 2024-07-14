import asyncio
# import requests
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import TOKEN

dp = Dispatcher()
admin_id = "1244894486"

login_user = 'http://localhost:8001/api/v1/accounts/login/'

params = {'user_id': 1244894486}


class Reg(StatesGroup):
    age = State()
    gender = State()
    choose_gender = State()
    name = State()
    city = State()
    description = State()
    photo = State()


@dp.message(CommandStart())
async def registration(message: Message, state: FSMContext):
    await state.set_state(Reg.age)
    await message.answer("Привет, для начала работы с ботом давай познакомимся!🖐\n\nСколько тебе лет?")


@dp.message(Reg.age)
async def age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Введи свой возраст исключая лишние символы!')
    else:
        await state.update_data(age=message.text)
        await state.set_state(Reg.gender)
        text = 'Теперь определимся каков твой пол?'
        male = KeyboardButton(text='Я парень')
        female = KeyboardButton(text='Я девушка')
        markup = ReplyKeyboardMarkup(keyboard=[[male, female]], resize_keyboard=True, one_time_keyboard=True)
        await message.answer(text, reply_markup=markup)


@dp.message(Reg.gender)
async def gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Reg.choose_gender)

    womans = KeyboardButton(text='Девушки')
    men = KeyboardButton(text='Парни')
    markup = ReplyKeyboardMarkup(keyboard=[[womans, men]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Кто тебе интересен?", reply_markup=markup)


@dp.message(Reg.choose_gender)
async def step_two(message: Message, state: FSMContext):
    await state.update_data(choose_gender=message.text)
    await state.set_state(Reg.name)
    await message.answer('Как тебя зовут?')


@dp.message(Reg.name)
async def step_three(message: Message, state: FSMContext):
    if any(map(lambda x: x.isdigit(), message.text)):
        await state.set_state(Reg.name)
        await message.answer('Имя не должно содержать цифры, введите свое имя исключая цифры!🔠')
    else:
        await state.update_data(name=message.text)
        await message.answer('Из какого ты города?🏙')
        await state.set_state(Reg.city)


@dp.message(Reg.city)
async def step_four(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(Reg.description)
    skip = KeyboardButton(text='Пропустить')
    markup = ReplyKeyboardMarkup(keyboard=[[skip]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Расскажи что нибудь о себе', reply_markup=markup)


@dp.message(Reg.description)
async def step_five(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Reg.photo)

    skip = KeyboardButton(text='Пропустить')
    markup = ReplyKeyboardMarkup(keyboard=[[skip]], resize_keyboard=True, one_time_keyboard=True)
    await message.answer('Теперь пришли фото, его смогут увидеть другие пользователи', reply_markup=markup)


@dp.message(Reg.photo)
async def final_reg(message: Message, state: FSMContext):
    # register_user = 'http://localhost:8001/api/v1/accounts/register/'
    await state.update_data(photo=message.photo)
    await message.answer(f"Так выглядит твоя анкета:")
    start = KeyboardButton(text="Начать просмотр анкет!")
    markup = ReplyKeyboardMarkup(keyboard=[[start]], resize_keyboard=True)
    data = await state.get_data()
    body = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "name": data['name'],
        "age": data['age'],
        "description": data['description'] if data['description'] != 'Пропустить' else None,
        "city": data['city'],
        "who_looking": data['choose_gender'],
        "gender": data['gender']
    }
    print(body)
    if data['photo'] is None and data['description'] == 'Пропустить':
        await message.answer(f'{data['name']}, {data['age']}, {data['city']}',
                             reply_markup=markup)
    elif data['photo'] is None:
        await message.answer(f'{data['name']}, {data['age']}, {data['city']}\n{data['description']}',
                             reply_markup=markup)
    elif data['description'] == 'Пропустить':
        await message.answer_photo(data['photo'][-1].file_id,
                                   f'{data['name']}, {data['age']}, {data['city']}',
                                   reply_markup=markup)
    else:
        await message.answer_photo(data['photo'][-1].file_id,
                                   caption=f'{data['name']}, {data['age']}, {data['city']}\n{data['description']}',
                                   reply_markup=markup)

    # response = requests.post(url=register_user, data=body)
    await state.clear()


@dp.message(Command('profile'))
async def send_data(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f'{data['name']}, {data['age']}, {data['description']}')


@dp.message(F.text == 'Начать просмотр анкет!')
async def begin(message: Message):
    heart = KeyboardButton(text='❤️')
    dislike = KeyboardButton(text='👎')
    mini_message = KeyboardButton(text='💌')
    markup = ReplyKeyboardMarkup(keyboard=[[heart, dislike, mini_message]], resize_keyboard=True)
    await message.answer(text='добавляем просмотр анкет...', reply_markup=markup)


async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print('Exit')
