from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def choose_gender_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатуре для выбора пола пользователя.

    Returns:
        ReplyKeyboardMarkup: Клавиатура.
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text='Я парень')
    kb.button(text='Я девушка')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def choose_who_looking() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора кого ищет пользователь.

    Returns:
        ReplyKeyboardMarkup: Клавиатура.
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text='Девушки')
    kb.button(text='Парни')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
