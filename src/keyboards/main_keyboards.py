from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def skip_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для пропуска чего-либо.

    Returns:
        ReplyKeyboardMarkup: Клавиатура.
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text='Пропустить')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def start_looking_cards() -> ReplyKeyboardMarkup:
    """Клавиатура для начала просмотра анкет.

    Returns:
        ReplyKeyboardMarkup: Клавиатура.
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text='Начать просмотр анкет!')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def actions_for_card_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура с действиями над анкетой.

    Returns:
        ReplyKeyboardMarkup: Клавиатура.
    """
    kb = ReplyKeyboardBuilder()
    kb.button(text='❤️')
    kb.button(text='👎')
    kb.button(text='💌')
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)
