from multiprocessing import Value
import telebot
import get_equipment
from config import TOKEN

TOKEN2 = '5368872375:AAEvUpJg5M8f_NF8LxB2SqrzRJEx2QfSIdQ'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(m, res=False):
    print(f"received message from m.chat.id={m.chat.id}")
    bot.send_message(m.chat.id, 'Холодильное оборудование ВЛМК')

def send_buttons_step0(m):
    menu1 = telebot.types.InlineKeyboardMarkup()
    menu1.add(telebot.types.InlineKeyboardButton(text = 'Поиск по № компрессорной', callback_data ='room'))
    menu1.add(telebot.types.InlineKeyboardButton(text = 'По № оборудования"', callback_data ='id'))

    msg = bot.send_message(m.chat.id, text ='Выбери тип поиска', reply_markup = menu1)

@bot.callback_query_handler(func=lambda call: True)
def sendbuttons(call):
    if call.data == 'room':
        msg = bot.send_message(call.message.chat.id, "Введи номер компрессорной")
        bot.register_next_step_handler(msg, process_room_step)
    elif call.data == 'id':
        msg = bot.send_message(call.message.chat.id, "Введи номер оборудования")
        bot.register_next_step_handler(msg, process_equipment_step)
    else:
        msg = bot.send_message(call.message.chat.id, "Ошибка бота 1")

#@bot.message_handler(content_types=["text"])
def process_room_step(m):
    bot.send_message(m.chat.id, f" поиск по компрессорной {m.text} не реализован")

#@bot.message_handler(content_types=["text"])
def process_equipment_step(m):
    id = int(m.text)
    eq = get_equipment.get_equipment(id)
    id = eq["id"]
    equipment = eq["equipment"]
    parametr = eq["parametr"]
    note = eq["note"]
    strmessage = f"** Название оборудования: ** {equipment} \n** Параметры:** {parametr} \n ** Описание:** {note}"

    bot.send_message(m.chat.id, strmessage)

@bot.message_handler(content_types=["text"])
def handle_text_step0(m):
    print(f'message.chat.id={m.chat.id} You write {m.text}')
    if m.text == "t" or m.text == "T" or m.text == "test":
        return send_buttons_step0(m)
    process_equipment_step(m)

def main():
    print("bot starting")
    bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    main()

