from multiprocessing import Value
import telebot
import get_equipment

bot = telebot.TeleBot('5368872375:AAEvUpJg5M8f_NF8LxB2SqrzRJEx2QfSIdQ')

@bot.message_handler(commands=["start"])
def start(m, res=False):
    print(f"received message from m.chat.id={m.chat.id}")
    bot.send_message(m.chat.id, 'Холодильное оборудование ВЛМК')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    print(f'message.chat.id={message.chat.id} You write {message.text}')
    id = int(message.text)
    eq = get_equipment.get_equipment(id)
    id = eq["id"]
    equipment = eq["equipment"]
    parametr = eq["parametr"]
    note = eq["note"]
    strmessage = f"** Название оборудования: ** {equipment} \n** Параметры:** {parametr} \n ** Описание:** {note}"

    bot.send_message(message.chat.id, strmessage)


def main():
    print("bot starting")
    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()

