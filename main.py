import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

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


bot.polling(none_stop=True,timeout=120)
