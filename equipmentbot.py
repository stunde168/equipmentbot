from multiprocessing import Value
import telebot
import get_equipment
from config import TOKEN

chat_names = {5320223505 : "Сергей", 1041976546 : "Алексей"}
greeteing_sent = {5320223505 : False, 1041976546 : False}


bot = telebot.TeleBot(TOKEN)

def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

@bot.message_handler(commands=["start"])
def start(m, res=False):
    print(f"received message from m.chat.id={m.chat.id}")
    bot.send_message(m.chat.id, f'Здравствуй, {m.first_name}. Для поиска по холодильному оборудованию ВЛМК введите t или номер оборудования')

@bot.message_handler(commands=["id"])
def handler_id(m, res=False):
    print(f"received message from m.chat.id={m.chat.id}")
    # m.
    bot.send_message(m.chat.id, 'введена команда /id')


def send_buttons_step0(m):
    menu1 = telebot.types.InlineKeyboardMarkup()
    menu1.add(telebot.types.InlineKeyboardButton(text = 'Поиск по № компрессорной', callback_data ='room'))
    menu1.add(telebot.types.InlineKeyboardButton(text = 'По № оборудования"', callback_data ='id'))
    menu1.add(telebot.types.InlineKeyboardButton(text = 'Документация по № оборудования"', callback_data ='docs'))
    msg = bot.send_message(m.chat.id, text ='Выбери тип поиска', reply_markup = menu1)

@bot.callback_query_handler(func=lambda call: True)
def sendbuttons(call):
    if call.data == 'room':
        msg = bot.send_message(call.message.chat.id, "Введи номер компрессорной")
        bot.register_next_step_handler(msg, process_room_step)
    elif call.data == 'id':
        msg = bot.send_message(call.message.chat.id, "Введи номер оборудования")
        bot.register_next_step_handler(msg, process_equipment_step)
    elif call.data == 'docs':
        msg = bot.send_message(call.message.chat.id, "Введи номер оборудования - документация")

        bot.register_next_step_handler(msg, process_equipment_docs_step)
    else:
        msg = bot.send_message(call.message.chat.id, "Ошибка бота 1")

def process_room_step(m):
    if not is_int(m.text) :
        msg = bot.send_message(m.chat.id, "Введите номер компрессорной")
        bot.register_next_step_handler(msg, process_room_step)
        return
   
    room = int(m.text)
    eqs = get_equipment.get_room(room)
    strmessage=''
    for eq in eqs:
        id = eq["id"]
        equipment = eq["equipment"]
        strmessage = strmessage + f"{id} : {equipment}\n"
    bot.send_message(m.chat.id, strmessage)

def process_equipment_step(m): 
    if not is_int(m.text) :
        return bot.send_message(m.chat.id, "Введите номер оборудования")

    id = int(m.text)
    eq = get_equipment.get_equipment(id)
    id = eq["id"]
    equipment = eq["equipment"]
    parametr = eq["parametr"]
    note = eq["note"]
    strmessage = f"НАЗВАНИЕ ОБОРУДОВАНИЯ: {equipment} \nПАРАМЕТРЫ: {parametr} \nОПИСАНИЕ: {note}"
    bot.send_message(m.chat.id, strmessage)

def process_equipment_docs_step(m): 
    if not is_int(m.text) :
        msg = bot.send_message(m.chat.id, "Введите номер оборудования - документация")
        bot.register_next_step_handler(msg, process_equipment_docs_step)

    id = int(m.text)
    listfiles = get_equipment.get_listfiles(id)
    print(f'{listfiles=}')
    if len(listfiles) == 0 :
        return bot.send_message(m.chat.id, "ДОКУМЕНТАЦИЯ ОТСУТСТВУЕТ")    
    keys = "\n".join(list(listfiles.keys()))
    strmessage = f"{keys}"
    bot.send_message(m.chat.id, strmessage)


@bot.message_handler(content_types=["text"])
def handle_text_step0(m):
    print(f'message.chat.id={m.chat.id} {chat_names.get(m.chat.id)} message_handler. You write {m.text}')
    if not greeteing_sent.get(m.chat.id):     
        greeteing_sent[m.chat.id] = True
        name = chat_names.get(m.chat.id)
        greetingmessage = f'Здравствуй, {name}. Бот опять работает' if name  != '' else 'Бот опять работает'        
        bot.send_message(m.chat.id, greetingmessage)

    if m.text == "t" or m.text == "T" or m.text == "test" or m.text == 'т' or m.text == 'Т':
        return send_buttons_step0(m)
    process_equipment_step(m)


def main():
    print("bot starting")
    bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    main()

