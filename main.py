import traceback

import  telebot
from config import keys, TOKEN
from utils import CryptoConverter, ConvertionException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты>\
    \n<в какую валюту перевести>  \n<количество переводимой валюты>\
    \n<Увидеть список всех доступных валют: /values>'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(messege: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
       text = '\n'.join((text, key, ))
    bot.reply_to(messege, text)

@bot.message_handler(content_types=['text', ])
def convert(messege: telebot.types.Message):
    try:
        values = messege.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много/мало параметров')

        answer = CryptoConverter.convert(*values)
    except ConvertionException as e:
        bot.reply_to(messege, f'Ошибка пользователя\n{e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(messege, f'Не удалось обработать команду\n{e}')
    else:
        bot.reply_to(messege, answer)

bot.polling()
