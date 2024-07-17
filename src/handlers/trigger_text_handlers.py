from aiogram import Router, F
from aiogram.types import Message

from keyboards import main_keyboards as m_kb

router = Router()


@router.message(F.text == 'Начать просмотр анкет!')
async def begin(message: Message):
    """Handler реагирует на текст 'Начать просмотр анкет!'."""
    await message.answer(text='добавляем просмотр анкет...', reply_markup=m_kb.actions_for_card_keyboard())


@router.message()
async def show_photo(message: Message):
    if message.content_type == 'photo':
        await message.answer('Вы отправили фото')
