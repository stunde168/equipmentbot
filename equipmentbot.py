from multiprocessing import Value
import telebot
import get_equipment
from config import TOKEN, TOKENSCADA

# еще про состояние можно прочитать на https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/custom_states.py

chat_states = {}

bot = telebot.TeleBot(TOKENSCADA)

def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

@bot.message_handler(commands=["start"])
def start(m, res=False):
    print(f"Начинаем чат с {m.chat.id=}")
    # m.from_user.first_name id last_name username
    bot.send_message(m.chat.id, f'👋 Здравствуй, {m.from_user.username}.')    
    handle_text_default(m)

@bot.message_handler(commands=["id"])
def handler_id(m, res=False):
    bot.send_message(m.chat.id, f'Для просмотра карточки оборудования введите номер обрудования')    
    bot.register_next_step_handler(m, equipment_inputid_handler)    

@bot.message_handler(commands=["room"])
def handler_room(m, res=False):
    bot.send_message(m.chat.id, f'Для вывода списка оборудования введите номер компрессорной')    
    bot.register_next_step_handler(m, room_inputroom_handler)

@bot.message_handler(commands=["docs"])
def handler_docs(m, res=False):
    bot.send_message(m.chat.id, f'Для вывода документации введите номер оборудования')    
    bot.register_next_step_handler(m, docs_inputid_handler)

@bot.message_handler(commands=["file"])
def handler_file(m, res=False):
    bot.send_message(m.chat.id, 'введена команда /file - она будет добавлена позже')

@bot.message_handler(commands=["t", "test"])
def handler_test(m, res=False):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn0 = telebot.types.KeyboardButton('/id')
    btn1 = telebot.types.KeyboardButton('/room')
    btn2 = telebot.types.KeyboardButton('/docs')
    btn3 = telebot.types.KeyboardButton('/file')
    btncancel = telebot.types.KeyboardButton('/cancel')
    markup.add(btn0, btn1, btn2, btn3, btncancel)
    msg = bot.send_message(m.chat.id, 'Клавиатура добавлена. Что хотите сделать?',
                           reply_markup=markup)
    # bot.register_next_step_handler(msg.msg, handler_switch)

def is_canceled(m):
    text = m.text
    return "/cancel" in text

@bot.message_handler(commands=["cancel"])
def handler_cancel(m, res=False):
    markup = telebot.types.ReplyKeyboardRemove(selective=False)    
    bot.send_message(m.chat.id, 'текущая операция отменена', reply_markup=markup)
    handle_text_default(m)
    

# def send_buttons_step0(m):
#     menu1 = telebot.types.InlineKeyboardMarkup()
#     menu1.add(telebot.types.InlineKeyboardButton(text = '№ компрессорной', callback_data ='room'))
#     menu1.add(telebot.types.InlineKeyboardButton(text = 'Карточка', callback_data ='id'))
#     menu1.add(telebot.types.InlineKeyboardButton(text = 'Документация', callback_data ='docs'))
#     msg = bot.send_message(m.chat.id, text ='Выбери тип поиска: список оборудования по номеру компрессорной, карточка оборудования по номеру оборудования, документация по номеру оборудования', reply_markup = menu1)

# @bot.callback_query_handler(func=lambda call: True)
# def sendbuttons(call):
#     if call.data == 'room':
#         msg = bot.send_message(call.message.chat.id, "Введи номер компрессорной")
#         bot.register_next_step_handler(msg, process_room_step)
#     elif call.data == 'id':
#         msg = bot.send_message(call.message.chat.id, "Введи номер оборудования")
#         bot.register_next_step_handler(msg, process_equipment_step)
#     elif call.data == 'docs':
#         msg = bot.send_message(call.message.chat.id, "Введи номер оборудования - документация")
#         bot.register_next_step_handler(msg, docs_handler)
#     else:
#         msg = bot.send_message(call.message.chat.id, "Ошибка бота 1")

def equipment_inputid_handler(m): 
    if is_canceled(m):
        return handler_cancel(m)
    if not is_int(m.text):
        msg = bot.send_message(m.chat.id, f"Введенный текст не является номером оборудования. Введите номер оборудования, например 144")
        bot.register_next_step_handler(msg, equipment_inputid_handler)
        return

    id = int(m.text)
    eq = get_equipment.get_equipment(id)
    id = eq["id"]
    equipment = eq["equipment"]
    parametr = eq["parametr"]
    note = eq["note"]
    strmessage = f"НАЗВАНИЕ ОБОРУДОВАНИЯ: {equipment} \nПАРАМЕТРЫ: {parametr} \nОПИСАНИЕ: {note}"
    msg = bot.send_message(m.chat.id, strmessage)
    bot.register_next_step_handler(msg, equipment_inputid_handler)

def room_inputroom_handler(m):
    if is_canceled(m):
        return handler_cancel(m)
    if not is_int(m.text) :
        msg = bot.send_message(m.chat.id, "Все-таки введите номер компрессорной")
        bot.register_next_step_handler(msg, room_inputroom_handler)
        return
   
    room = int(m.text)
    eqs = get_equipment.get_room(room)
    strmessage=''
    for eq in eqs:
        id = eq["id"]
        equipment = eq["equipment"]
        strmessage = strmessage + f"{id} : {equipment}\n"
    msg = bot.send_message(m.chat.id, strmessage)
    bot.register_next_step_handler(msg, room_inputroom_handler)

def docs_inputid_handler(m): 
    if is_canceled(m):
        return handler_cancel(m)
    if not is_int(m.text) :
        msg = bot.send_message(m.chat.id, "Введите номер оборудования - документация")
        bot.register_next_step_handler(msg, docs_inputid_handler)
        return

    id = int(m.text)
    listfiles = get_equipment.get_listfiles(id)
    print(f'{listfiles=}')
    if len(listfiles) == 0 :
        msg = bot.send_message(m.chat.id, f"Документация по оборудованию №{id} отсутствует")    
        bot.register_next_step_handler(msg, docs_inputid_handler)
        return

    chat_states[m.chat.id] = id

    keys = "\n".join(list(listfiles.keys()))
    strmessage = f"{keys}"
    msg = bot.send_message(m.chat.id, strmessage)
    msg = bot.send_message(m.chat.id, "Введите номер файла")
    bot.register_next_step_handler(msg, file_inputnumber_handler)

def file_inputnumber_handler(m): 
    if is_canceled(m):
        return handler_cancel(m)
    if not is_int(m.text) :
        msg = bot.send_message(m.chat.id, f"Введите номер файла для оборудования №enterid")
        bot.register_next_step_handler(msg, file_inputnumber_handler)
        return

    id = chat_states.get(m.chat.id)

    number = int(m.text)
    strmessage = f"запрашиваем файл {number} для оборудования №{id}"
    msg = bot.send_message(m.chat.id, strmessage)

    (filename, file) = get_equipment.get_file(id, number)
    print(f'{id=} {number=}')
    if file == None:    
        msg = bot.send_message(m.chat.id, f"Файл {number} для оборудования №{id} отсутствует")    
        bot.register_next_step_handler(msg, file_inputnumber_handler)
        return

    strmessage = f"Прикрепляем файл {number} для оборудования №{id}"
    msg = bot.send_message(m.chat.id, strmessage)

    msg = bot.send_document(m.chat.id, file, caption=filename)
    bot.register_next_step_handler(msg, file_inputnumber_handler)


@bot.message_handler(content_types=["text"])
def handle_text_default(m):
    print(f'message.chat.id={m.chat.id} {m.from_user.username} message_handler. You write {m.text}')
    bot.send_message(m.chat.id, 'Для работы с холодильным оборудованием ВЛМК выбери одну из следующих команд: \n/id - просмотр карточки по номеру оборудования \n/room - список оборудования по номеру компрессорной \n/docs - вывод документации по номеру оборудования \n/file - просмотр файла документации по номеру оборудования \n/help - для вывода данного сообщения \n/cancel - отмена выбранной команды \n/test - тоже для чего-то')

def main():
    print("bot starting")
    bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    main()