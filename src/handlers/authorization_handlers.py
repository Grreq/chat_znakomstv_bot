from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from keyboards import registration_keyboards as reg_kb, main_keyboards as m_kb

router = Router()


class Reg(StatesGroup):
    """Класс состояний для регистрации."""
    age = State()
    gender = State()
    choose_gender = State()
    name = State()
    city = State()
    description = State()
    photo = State()


@router.message(CommandStart())
async def registration(message: Message, state: FSMContext):
    """ Handler реагирует на /start.

    Args:
        message (Message): сообщение пользователя.
        state (State): Машина состояний.
    """
    await state.set_state(Reg.age)
    await message.answer("Привет, для начала работы с ботом давай познакомимся!🖐\n\nСколько тебе лет?")


@router.message(Reg.age)
async def age(message: Message, state: FSMContext):
    """ Handler состояния age.

    Args:
        message (Message): сообщение пользователя.
        state (State): Машина состояний.
    """
    if not message.text.isdigit():
        await message.answer('Введи свой возраст исключая лишние символы!')
    else:
        await state.update_data(age=message.text)
        await state.set_state(Reg.gender)
        await message.answer('Теперь определимся каков твой пол?', reply_markup=reg_kb.choose_gender_keyboard())


@router.message(Reg.gender)
async def gender(message: Message, state: FSMContext):
    """ Handler состояния gender.

    Args:
        message (Message): сообщение пользователя.
        state (State): Машина состояний.
    """
    await state.update_data(gender=message.text)
    await state.set_state(Reg.choose_gender)
    await message.answer("Кто тебе интересен?", reply_markup=reg_kb.choose_who_looking())


@router.message(Reg.choose_gender)
async def choose_gender(message: Message, state: FSMContext):
    """ Handler состояния choose_gender.

    Args:
        message (Message): сообщение пользователя.
        state (State): Машина состояний.
    """
    await state.update_data(choose_gender=message.text)
    await state.set_state(Reg.name)
    await message.answer('Как тебя зовут?')


@router.message(Reg.name)
async def name(message: Message, state: FSMContext):
    """ Handler состояния name.

    Args:
        message (Message): сообщение пользователя.
        state (State): Машина состояний.
    """
    if any(map(lambda x: x.isdigit(), message.text)):
        await state.set_state(Reg.name)
        await message.answer('Имя не должно содержать цифры, введите свое имя исключая цифры!🔠')
    else:
        await state.update_data(name=message.text)
        await message.answer('Из какого ты города?🏙')
        await state.set_state(Reg.city)


@router.message(Reg.city)
async def city(message: Message, state: FSMContext):
    """ Handler состояния city.

    Args:
        message (Message): сообщение пользователя.
        state (State): Машина состояний.
    """
    await state.update_data(city=message.text)
    await state.set_state(Reg.description)
    await message.answer('Расскажи что нибудь о себе', reply_markup=m_kb.skip_keyboard())


@router.message(Reg.description)
async def description(message: Message, state: FSMContext):
    """ Handler состояния description.

    Args:
        message (Message): сообщение пользователя.
        state (State): Машина состояний.
    """
    await state.update_data(description=message.text)
    await state.set_state(Reg.photo)
    await message.answer('Теперь пришли фото, его смогут увидеть другие пользователи',
                         reply_markup=m_kb.skip_keyboard())


@router.message(Reg.photo)
async def final_step_registration(message: Message, state: FSMContext):
    """ Handler состояния photo.

    Args:
        message (Message): сообщение пользователя.
        state (State): Машина состояний.
    """
    await state.update_data(photo=message.photo)
    await message.answer(f"Так выглядит твоя анкета:")
    data = await state.get_data()
    # body = {
    #     "user_id": message.from_user.id,
    #     "username": message.from_user.username,
    #     "name": data['name'],
    #     "age": data['age'],
    #     "description": data['description'] if data['description'] != 'Пропустить' else None,
    #     "city": data['city'],
    #     "who_looking": data['choose_gender'],
    #     "gender": data['gender']
    # }
    if data['photo'] is None and data['description'] == 'Пропустить':
        text = f'{data["name"]}, {data["age"]}, {data["city"]}'
        await message.answer(f'{data["name"]}, {data["age"]}, {data["city"]}',
                             reply_markup=reg_kb.start_looking_cards())
    elif data['photo'] is None:
        text = f'{data["name"]}, {data["age"]}, {data["city"]}\n{data["description"]}'
        await message.answer(f'{data["name"]}, {data["age"]}, {data["city"]}\n{data["description"]}',
                             reply_markup=reg_kb.start_looking_cards())
    elif data['description'] == 'Пропустить':
        text = f'{data["name"]}, {data["age"]}, {data["city"]}'
        photo = data['photo'][-1].file_id
    else:
        text = f'{data["name"]}, {data["age"]}, {data["city"]}\n{data["description"]}'
        photo = data['photo'][-1].file_id
    if data['photo']:
        await message.answer_photo(photo, caption=text, reply_markup=m_kb.start_looking_cards())
    else:
        await message.answer(text, reply_markup=m_kb.start_looking_cards())

    # response = requests.post(url='http://localhost:8001/api/v1/accounts/register/', data=body)
    await state.clear()
