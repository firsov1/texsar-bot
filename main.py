import gspread
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

findsku = 0

bot = telebot.TeleBot("6804968897:AAGykUe9O9eZ0S__H4Z911YtJF1f8XWbrUE")


@bot.message_handler(commands=["start"])
def main(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("ЗАПРОС ОДНОГО АРТИКУЛА", "ЗАПРОС БОЛЕЕ ОДНОГО АРТИКУЛА")
    markup.add("СТАТУСЫ ЗАКАЗОВ", "ТРЕК-НОМЕР", "ФОТО")
    markup.add("СВЯЗЬ С МЕНЕДЖЕРОМ")
    bot.send_message(
        message.chat.id,
        "Здравствуйте! Я - ТекссарБот. \nПришлите мне артикул, и я отвечу есть ли он у меня и по какой цене.",
    )
    bot.send_message(
        message.chat.id,
        "Еще я могу подготовить и отправить вам счет на заказ, если вы мне его пришлете в виде файла Excel. Формат данных в файле должен быть такой:\n-  1 колонка: Артикул товара\n-  2 колонка: Количество товара в заказе",
    )
    bot.send_message(
        message.chat.id,
        'С уважением ООО "Текссар", тел. 8 800 600 74 66, info@texsar.net',
        reply_markup=markup,
    )


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.reply_to(message, message.text)


@bot.message_handler(regexp="ЗАПРОС ОДНОГО АРТИКУЛА")
def find_sku(message):
    bot.send_message(message.chat.id, 'Введите артикул:')
    global findsku
    findsku = 1


@bot.message_handler()
def check_sku(message):
    global findsku
    if findsku == 1:
        bot.send_message(message.chat.id, 'Один момент, я уже ищу...')
        sku = message.text
        # bot.send_message(message.chat.id, 'find sku subroutine check')
        gc = gspread.service_account()
        sh = gc.open("1")
        cell = sh.sheet1.find(sku)
        if cell is None:
            bot.send_message(message.chat.id,f'Товара с артикулом {sku} нет наличии. О возможности поставки уточните, пожалуйста, у менеджера по почте info@texsar.ru, либо по телефону 8 800 600 74 66')
        else:
            sku = sh.sheet1.cell(cell.row, cell.col).value
            name = sh.sheet1.cell(cell.row, cell.col + 1).value
            price = sh.sheet1.cell(cell.row, cell.col + 3).value
            quantity = sh.sheet1.cell(cell.row, cell.col + 2).value
            now = datetime.now()
            print("Found something at R%sC%s" % (cell.row, cell.col))
            # print(f'{sku} {name} в наличии в количестве {quantity} шт.. \nЦена по прайсу на {now} равна {price} руб.. Цена включает НДС.')
            # bot.send_message(sku + ' ' + name + 'в наличии в количестве ' + quantity + 'шт.. \nЦена по прайсу на ' + now + 'равна ' + price +' руб.. Цена включает НДС.')
            bot.send_message(message.chat.id, f'{sku} {name} в наличии в количестве {quantity} шт.. \nЦена по прайсу на {now.day}.{now.month}.{now.year} равна {price} руб.. Цена включает НДС.')
        findsku = 0
    else:
        bot.send_message(message.chat.id, 'Эта кнопка еще не задействована')


bot.polling(none_stop=True,timeout=120)