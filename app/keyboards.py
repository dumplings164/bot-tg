from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_codeRk

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Создать заявку')],
                                     [KeyboardButton(text='Запросить счет')],
                                     [KeyboardButton(text='Контакты'),
                                      KeyboardButton(text='О нас')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')


programm = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Rkeeper', callback_data='rkeeper')],
    [InlineKeyboardButton(text='IIKO', callback_data='iiko')],
    [InlineKeyboardButton(text='Sbis', callback_data='iiko')],
    [InlineKeyboardButton(text='Другое', callback_data='another')]])


get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
                                                           request_contact=True)]],
                                 resize_keyboard=True, one_time_keyboard=True)

remove_markup = ReplyKeyboardRemove()

async def codesRk(tg_id: int):
    codesRk = await get_codeRk(tg_id)
    keyboard = InlineKeyboardBuilder()
    for code in codesRk:
        keyboard.add(InlineKeyboardButton(text=str(code.codeRk), callback_data=str(code.codeRk)))
    keyboard.add(InlineKeyboardButton(text='Добавить код', callback_data='code'))
    return keyboard.adjust(2).as_markup()