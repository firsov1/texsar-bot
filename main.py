# import gspread
import requests, json
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

findsku = 0

bot = telebot.TeleBot("6804968897:AAGykUe9O9eZ0S__H4Z911YtJF1f8XWbrUE")


@bot.message_handler(commands=["start"])
def main(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("ЗАПРОС ОДНОГО АРТИКУЛА")
    # markup.add("СТАТУСЫ ЗАКАЗОВ", "ТРЕК-НОМЕР", "ФОТО")
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


@bot.message_handler(regexp="СВЯЗЬ С МЕНЕДЖЕРОМ")
def find_sku(message):
    bot.send_message(message.chat.id, 'Ваш менеджер: Фирсов Иван\nЭлектронная почта: info@texsar.net\nТелефон:8 800 600 74 66')

# # Поиск по таблице Google Sheets артикула в столбце Артикул и вывод названия, количества и цены из соответствующих столбцов и сегодняшней даты
# @bot.message_handler()
# def check_sku(message):
#     global findsku
#     if findsku == 1:
#         bot.send_message(message.chat.id, 'Один момент, я уже ищу...')
#         sku = message.text
#         # bot.send_message(message.chat.id, 'find sku subroutine check')
#         gc = gspread.service_account()
#         sh = gc.open("1")
#         cell = sh.sheet1.find(sku)
#         if cell is None:
#             bot.send_message(message.chat.id,f'Товара с артикулом {sku} нет наличии. О возможности поставки уточните, пожалуйста, у менеджера по почте info@texsar.ru, либо по телефону 8 800 600 74 66')
#         else:
#             sku = sh.sheet1.cell(cell.row, cell.col).value
#             name = sh.sheet1.cell(cell.row, cell.col + 1).value
#             price = sh.sheet1.cell(cell.row, cell.col + 3).value
#             quantity = sh.sheet1.cell(cell.row, cell.col + 2).value
#             now = datetime.now()
#             print("Found something at R%sC%s" % (cell.row, cell.col))
#             bot.send_message(message.chat.id, f'{sku} {name} в наличии в количестве {quantity} шт.. \nЦена по прайсу на {now.day}.{now.month}.{now.year} равна {price} руб.. Цена включает НДС.')
#         findsku = 0
#     else:
#         bot.send_message(message.chat.id, 'Эта кнопка еще не задействована')


# Поиск по 1С: УНФ и вывод названия, количества и и сегодняшней даты
@bot.message_handler()
def check_sku(message):
    global findsku
    if findsku == 1:
        bot.send_message(message.chat.id, 'Один момент, я уже ищу...')
        sku = message.text
        one_c_url = 'http://192.168.88.155/unf/odata/standard.odata/'
        user, password = 'odata.user', '123456'
        requests.get(one_c_url, auth=(user, password))

        # Запрос названия и ид номенклатурной позиции в 1с
        sku_url = one_c_url + "Catalog_Номенклатура?$filter=Артикул eq '" + sku + "'&$select=Ref_Key, Артикул, Description&$format=json"
        response = requests.get(sku_url, auth=(user, password))
        json_data = json.loads(response.text)
        # print(json_data)
        print(sku_url)
        if json_data["value"] == []:
            bot.send_message(message.chat.id,f'Товара с артикулом {sku} нет наличии. О возможности поставки уточните, пожалуйста, у менеджера по почте info@texsar.ru, либо по телефону 8 800 600 74 66')
        else:
            # now = datetime.now()
            name = json_data["value"][0]["Description"]
            Ref_Key = json_data["value"][0]["Ref_Key"]
            # print(name, Ref_Key)
            # Запрос товарных остатков по ид в 1с
            quantity_url = one_c_url + "InformationRegister_ОстаткиТоваров?$filter=Номенклатура_Key eq guid'" + Ref_Key + "'&$format=json&$select=Количество, СтруктурнаяЕдиница"
            response2 = requests.get(quantity_url, auth=(user, password))
            json_data2 = json.loads(response2.text)
            if json_data2["value"] == []:
                bot.send_message(message.chat.id,f'Товара с артикулом {sku} нет наличии. О возможности поставки уточните, пожалуйста, у менеджера по почте info@texsar.ru, либо по телефону 8 800 600 74 66')
            else:    
                quantity = json_data2["value"][0]["Количество"]
                print(quantity)

                # bot.send_message(message.chat.id, f'{sku} {name} в наличии в количестве {quantity} шт.. \nЦена по прайсу на {now.day}.{now.month}.{now.year} равна {price} руб.. Цена включает НДС.')
                bot.send_message(message.chat.id, f'{name} в наличии в количестве {quantity} шт..')
        findsku = 0
    else:
        bot.send_message(message.chat.id, 'Эта кнопка еще не задействована')


bot.polling(none_stop=True,timeout=120)