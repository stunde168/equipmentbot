#from multiprocessing import Value
import telebot
import get_equipment
from config import TOKEN

# еще про состояние можно прочитать на https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/custom_states.py

chat_states: dict = {}
""" Используй это, чтобы сохранить данные состояния 
    dict[chat_id]:(equipment_id, newlist [(shortfilename, fullfilename), ])
"""
blocked_chats = {-1001539497277}

bot = telebot.TeleBot(TOKEN)

def is_int(str) -> bool:
    try:
        int(str)
        return True
    except ValueError:
        return False

def is_blocked_chat(chat_id: int) -> bool:
    """ если чат заблокирован, то выходим, не обрабатываем сообщения"""
    return chat_id in blocked_chats

@bot.message_handler(commands=["start"])
def start(m, res=False) -> None:
    if is_blocked_chat(m.chat.id) : return
    first_name = m.from_user.first_name 
    last_name = m.from_user.last_name
    print(f"Начинаем чат с {m.chat.id=} {first_name=} {last_name=}")
    # m.from_user.first_name id last_name username
    bot.send_message(m.chat.id, f'👋 Здравствуй, {m.from_user.username}.')    
    handle_text_default(m)

@bot.message_handler(commands=["id"])
def handler_id(m, res=False):
    if is_blocked_chat(m.chat.id) : return
    bot.send_message(m.chat.id, f'Для просмотра карточки оборудования введите номер обрудования')    
    bot.register_next_step_handler(m, equipment_inputid_handler)    

@bot.message_handler(commands=["room"])
def handler_room(m, res=False):
    if is_blocked_chat(m.chat.id) : return
    bot.send_message(m.chat.id, f'Для вывода списка оборудования введите номер компрессорной')    
    bot.register_next_step_handler(m, room_inputroom_handler)

@bot.message_handler(commands=["docs"])
def handler_docs(m, res=False):
    if is_blocked_chat(m.chat.id) : return
    bot.send_message(m.chat.id, f'Для вывода документации введите номер оборудования')    
    bot.register_next_step_handler(m, docs_inputid_handler)

@bot.message_handler(commands=["file"])
def handler_file(m, res=False):
    if is_blocked_chat(m.chat.id) : return
    #docs_inputid_handler(m)    
    bot.send_message(m.chat.id, 'Для получения файла документации введите номер оборудования')
    bot.register_next_step_handler(m, docs_inputid_handler)

@bot.message_handler(commands=["t", "test"])
def handler_test(m, res=False):
    if is_blocked_chat(m.chat.id) : return
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn0 = telebot.types.KeyboardButton('/id')
    btn1 = telebot.types.KeyboardButton('/room')
    btn2 = telebot.types.KeyboardButton('/docs')
    btn3 = telebot.types.KeyboardButton('/file')
    btncancel = telebot.types.KeyboardButton('/cancel')
    markup.add(btn0, btn1, btn2, btn3, btncancel)
    msg = bot.send_message(m.chat.id, 'Клавиатура добавлена в этот чат. Нажмите на кнопку появившейся клавиатуры для выбора действия', reply_markup=markup)
    # bot.register_next_step_handler(msg.msg, handler_switch)


def is_canceled(m) -> bool:
    """ в тексте пришло '/cancel' нужно отменять данный обработчик """
    text = m.text
    return "/cancel" in text

@bot.message_handler(commands=["cancel"])
def handler_cancel(m, res=False):
    if is_blocked_chat(m.chat.id) : return
    # markup = telebot.types.ReplyKeyboardRemove(selective=False)    
    bot.send_message(m.chat.id, 'текущая операция отменена')
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
    if is_blocked_chat(m.chat.id) : return
    if is_canceled(m):
        return handler_cancel(m)
    if not is_int(m.text):
        msg = bot.send_message(m.chat.id, f"Выводим карточку оборудования... Введенный текст не является номером оборудования. Введите номер оборудования, например 767. Для отмены введите /cancel")
        bot.register_next_step_handler(msg, equipment_inputid_handler)
        return

    id = int(m.text)
    eq = get_equipment.get_equipment(id)
    id = eq["id"]
    equipment = eq["equipment"]
    parametr = eq["parametr"]
    note = eq["note"]
    strmessage = f"Выводим карточку оборудования:\nНАЗВАНИЕ ОБОРУДОВАНИЯ: {equipment} \nПАРАМЕТРЫ: {parametr} \nОПИСАНИЕ: {note}"
    msg = bot.send_message(m.chat.id, strmessage)
    bot.register_next_step_handler(msg, equipment_inputid_handler)

def room_inputroom_handler(m):
    if is_blocked_chat(m.chat.id) : return
    if is_canceled(m):
        return handler_cancel(m)
    if not is_int(m.text) :
        msg = bot.send_message(m.chat.id, "Вывод списка оборудования по номеру компрессорной. Введенный текст не является номер компрессорной. Для отмены введите /cancel")
        bot.register_next_step_handler(msg, room_inputroom_handler)
        return
   
    room = int(m.text)
    eqs = get_equipment.get_room(room)
    strmessage=''
    for eq in eqs:
        id = eq["id"]
        equipment = eq["equipment"]
        strmessage = strmessage + f"{id}: {equipment}\n"
    msg = bot.send_message(m.chat.id, strmessage)
    bot.register_next_step_handler(msg, room_inputroom_handler)

def docs_inputid_handler(m): 
    if is_blocked_chat(m.chat.id): return
    if is_canceled(m): return handler_cancel(m)

    if not is_int(m.text) :
        msg = bot.send_message(m.chat.id, "Вывод документации по номеру оборудования. Введенный текст не является номером оборудования. Для отмены введите /cancel")
        bot.register_next_step_handler(msg, docs_inputid_handler)
        return

    id = int(m.text)
    listfiles = get_equipment.get_listfiles(id)
    print(f'{listfiles=}')
    if listfiles == None or len(listfiles) == 0 :
        msg = bot.send_message(m.chat.id, f"Документация по оборудованию №{id} отсутствует")    
        bot.register_next_step_handler(msg, docs_inputid_handler)
        return

    # для каждого chat_id хрантся пара (equipment_id и список пар(короткое название файла, длинное название файла))
    # number - индекс файла в списке используется для выбора пользователем
    newlist = list(map(lambda item: (item[0], item[1]), listfiles.items()))
    chat_states[m.chat.id] = (id, newlist)

    # вывести строки формата "number1: filename1[\n]number2: filename2..."
    strnumberkeys = "\n".join(f"{number}: {pair[0]}" for number, pair in enumerate(newlist))
    strmessage = f"{strnumberkeys}"
    msg = bot.send_message(m.chat.id, strmessage)
    msg = bot.send_message(m.chat.id, "Введите номер файла")
    bot.register_next_step_handler(msg, file_inputnumber_handler)

def file_inputnumber_handler(m) -> None: 
    if is_blocked_chat(m.chat.id) : return
    if is_canceled(m):
        return handler_cancel(m)

    (id, newlist) = chat_states.get(m.chat.id)

    if not is_int(m.text) :
        msg = bot.send_message(m.chat.id, f"Запрос файла документации для оборудования №{id}. Введенный текст не является номер файла для оборудования. Для отмены введите /cancel")
        bot.register_next_step_handler(msg, file_inputnumber_handler)
        return

    number = int(m.text)
    if number < 0 or number >= len(newlist):
        msg = bot.send_message(m.chat.id, f"Запрос файла документации для оборудования №{id}. Введенный номер вне диапазона списка файлов. Введите число от 0 до {len(listfiles) - 1}.Для отмены введите /cancel")
        bot.register_next_step_handler(msg, file_inputnumber_handler)
        return

    pair = newlist[number]
    shortfilename = pair[0]    
    fullfilename = pair[1]

    strmessage = f"запрашиваем файл {number}: {shortfilename} для оборудования №{id}"
    msg = bot.send_message(m.chat.id, strmessage)
    
    file = get_equipment.get_file(fullfilename)

    print(f'{m.chat.id} Попытка скачать {id=} файл №{number} {shortfilename} по адресу {fullfilename}')
    if file == None or not file.ok:
        msg = bot.send_message(m.chat.id, f"Файл {number} для оборудования №{id} отсутствует")    
        bot.register_next_step_handler(msg, file_inputnumber_handler)
        return

    strmessage = f"Прикрепляем файл {number} для оборудования №{id}"
    msg = bot.send_message(m.chat.id, strmessage)

    msg = bot.send_document(m.chat.id, file.content, caption=shortfilename)
    #msg = bot.send_document(m.chat.id, file.content, caption="qqq.jpg")
    bot.register_next_step_handler(msg, file_inputnumber_handler)


@bot.message_handler(content_types=["text"])
def handle_text_default(m):
    if is_blocked_chat(m.chat.id) : return
    print(f'message.chat.id={m.chat.id} {m.from_user.username} message_handler. You write {m.text}')
    bot.send_message(m.chat.id, 'Для работы с холодильным оборудованием ВЛМК выбери одну из следующих команд: \n/id - просмотр карточки по номеру оборудования \n/room - список оборудования по номеру компрессорной \n/docs - вывод документации по номеру оборудования \n/file - просмотр файла документации по номеру оборудования \n/help - для вывода данного сообщения \n/cancel - отмена выбранной команды \n/test - тоже для чего-то')

def main():
    print("bot starting")
    bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    main()