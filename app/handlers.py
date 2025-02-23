from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.methods import GetFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import os

import app.database.requests as rq
import app.keyboards as kb
from app.appwork.linkRK import *
from app.appwork.pyrus import *

router = Router()



class Register(StatesGroup):
    tg_id = State()
    name = State()
    inn = State()
    soft = State()
    soft_id = State()
    number = State()
    

class Form(StatesGroup):
    problem = State()
    photo = State()
    task = State()

class Rkeeper(StatesGroup):
    tg_id = State()
    codeRk = State()
    addcodeRk = State()
    Buutton_codeRk = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Выберите действие из меню', reply_markup=kb.main)


@router.message(F.text == 'Запросить счет')
async def qurie_check(message: Message):
    await message.answer('Напишите /filerk')


@router.message(F.text == 'Создать заявку')
async def qurie_check(message: Message):
    await message.answer('Напишите /newtask')


@router.message(Command('help'))
async def cmd_help(message: Message,state: FSMContext):
    codesRk = await rq.get_codeRk(message.from_user.id)
    if codesRk == True:
        print("нет")
    else:
        print('есть')
    await message.answer('Вы нажали на кнопку помощи')


@router.message(Command('filerk'))
async def filerk(message: Message, state: FSMContext):
    await state.update_data(tg_id=message.from_user.id)
    codesRk = await rq.get_codeRk(message.from_user.id)
    if codesRk == None:
        await state.set_state(Rkeeper.codeRk)
        await message.answer('Укажите код ресторана')
    else:
        await state.set_state(Rkeeper.Buutton_codeRk)
        await message.answer(f'Выберите Ваш код заведеня!', reply_markup=await kb.codesRk(message.from_user.id))


@router.callback_query(Rkeeper.Buutton_codeRk, F.data == 'code')
async def addcodeRk(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tg_id = int(data['tg_id'])
    len_users = await rq.len_users(tg_id)
    if len(len_users) < 3:
        await state.set_state(Rkeeper.codeRk)
        await callback.answer(f'Добавить код')
        await callback.message.answer('Укажите код ресторана')
    else:
        await callback.answer(f'Добавить код')
        await callback.message.answer('Больше добавить заведений нельзя, если Вам нужно добавить ещё обратитесь в техническую поддержку или создайте заявку /newtask')


@router.callback_query(Rkeeper.Buutton_codeRk)
async def link_for_client(callback: CallbackQuery):
    await callback.answer(f'Ваше заведение {callback.data}')
    links_file, objectName = chekRk(int(callback.data))
    await callback.message.answer(f'Для заведения {objectName} с кодом {callback.data}\n{links_file}', reply_markup=kb.main)
    

@router.message(Rkeeper.codeRk)
async def filerk(message: Message, state: FSMContext):
    await state.update_data(codeRk=message.text)
    data = await state.get_data()
    codeRk = int(data['codeRk'])
    links_file, objectName = chekRk(codeRk)
    if 'неверный' in links_file:
        await message.answer(f'{links_file}. Пропробуйте его ввести ещё раз, для этого нажмите на /filerk')
    else:
        user = await rq.set_codeRk(message.from_user.id, int(message.text))
        if user == True:
            await state.clear()
            await message.answer(f'Для заведения {objectName} с кодом {message.text}\n{links_file}', reply_markup=kb.main)
        else:
            await state.clear()
            await message.answer(f'Такой код вы уже добавили, введите другой код заведения')


@router.message(Command('registration'))
async def register(message: Message, state: FSMContext):
    check = await rq.check_user(message.from_user.id)
    if check == True:
        await state.update_data(tg_id=message.from_user.id)
        await state.set_state(Register.name)
        await message.answer('Введите Ваше имя')
    else:
        await message.answer('Вы уже зарегистрированы!')


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.inn)
    await message.answer('Укажите ИНН Вашей организации')


@router.message(Register.inn)
async def register_inn(message: Message, state: FSMContext):
    try:
        inn =  int(message.text)
        await state.update_data(inn=message.text)
        await state.set_state(Register.number)
        await message.answer('Отправьте Ваш номер телефона', reply_markup=kb.get_number)
    except:
        await state.set_state(Register.inn)
        await message.answer('Вы указали не только цифры, пожалуйста, укажите только цифры')
        


@router.message(Register.number)
async def register_number(message: Message, state: FSMContext):
    if message.text:
        await state.set_state(Register.number)
        await message.answer('Пожалуйста, поделитесь свои контактом(нужно нажатать на кнопку "Отрпавить коонтакт"), либо мы не сможем с Вами связаться. Если Вам нужно указать дургой номер телефона, то напишите это в заявке', reply_markup=kb.get_number)
    elif message.contact.phone_number:
        await state.update_data(number=message.contact.phone_number)
        await state.set_state(Register.soft)
        await message.answer('Укажите Вашу программу', reply_markup=kb.programm)

    

@router.callback_query(Register.soft, F.data)
async def register_soft(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'iiko':
        await state.update_data(soft='iiko')
        await state.update_data(soft_id=1)
    elif callback.data == 'rkeeper':
        await state.update_data(soft='rkeeper')
        await state.update_data(soft_id=2)
    elif callback.data == 'sbis':
        await state.update_data(soft='sbis')
        await state.update_data(soft_id=3)
    elif callback.data == 'another':
        await state.update_data(soft='Другое')
        await state.update_data(soft_id=4)
    data = await state.get_data()
    await callback.answer(f'Вы выбрали {callback.data}')
    await rq.set_user(str(data["tg_id"]), str(data["name"]), str(data["inn"]), str(data['soft']), str(data['soft_id']), str(data["number"]))
    await callback.message.answer(f'Вы зарегистрировались!\nИмя: {str(data["name"])}\nИНН: {str(data["inn"])}\nСофт: {str(data['soft'])}\nНомер: {str(data["number"])}\n Теперь вы можете заполнить заявку!', reply_markup=kb.main)
    await state.clear()


@router.message(Command('newtask'))
async def register(message: Message, state: FSMContext):
    user = await rq.check_user(message.from_user.id)
    if user == True:
        await state.set_state(Register.name)
        await message.answer('Вам нужно пройти регистрацию, поэтому укажите Ваше имя') 
    else:
        user = await rq.get_task(message.from_user.id)
        if user == None:
            await state.set_state(Form.problem)
            await message.answer('Опишите подробно какая у Вас проблема')
        else:
            info_close_task = info_task(user.taskID)
            print(info_close_task)
            if info_close_task == True:
                await rq.delet_task(message.from_user.id, user.taskID)
                await state.set_state(Form.problem)
                await message.answer('Опишите подробно какая у Вас проблема')
            elif info_close_task == None:
                await state.set_state(Form.problem)
                await message.answer('Возникла проблема с заявкой, нужно обратиться по телефону чтобы Вы могли дальшке создавать новые заявки')
            elif 'открыта' in info_close_task:
                await state.set_state(Form.problem)
                await message.answer(info_close_task)
        
        


@router.message(Form.problem)
async def problem(message: Message, state: FSMContext):
    await state.update_data(problem=message.text)
    await state.set_state(Form.photo)
    await message.answer('Отправьте ОДНУ фотографию ошибки')


@router.message(Form.photo)
async def photo(message: Message, state: FSMContext):
    data = await state.get_data()
    u = await rq.user(message.from_user.id)
    file = await message.bot.get_file(message.photo[-1].file_id)
    downloaded_file = await message.bot.download_file(file.file_path, f'{message.photo[-1].file_id}.jpg')
    id_task = creat_task(u.name, u.inn, str(data['problem']), u.soft, u.soft_id, u.number, f"{message.photo[-1].file_id}.jpg")
    await rq.set_task(message.from_user.id, id_task)
    await message.answer(f'Ваша заявка создана ее номер {id_task}', reply_markup=kb.main)
    await state.clear()
    os.remove(f"{message.photo[-1].file_id}.jpg")
