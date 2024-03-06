import telebot
from telebot import types
import csv
import datetime
import time

TOKEN = 'YOURTOKEN'

bot = telebot.TeleBot(TOKEN)


markupm = types.ReplyKeyboardMarkup()
btn1 = types.KeyboardButton('📅Расписание📅')
btn2 = types.KeyboardButton('✒️Мои домашки✒️')
markupm.row(btn1, btn2)
btn3 = types.KeyboardButton('📚Сдать домашку📚')
btn4 = types.KeyboardButton('⌛️Дедлайны⌛️')
markupm.row(btn3, btn4)
btn5 = types.KeyboardButton('💰Мои оплаты💰')
btn6 = types.KeyboardButton('🚩CTF🚩')
markupm.row(btn5, btn6)

markupn = types.ReplyKeyboardMarkup()
btn1 = types.KeyboardButton('Назад')
markupn.row(btn1)

a3 = '🟢'
a2 = '🟡'
a1 = '🔴'
a0 = '✖️'


@bot.message_handler(commands=['addpayment020822'])
def start_message(message):
    bot.send_message(message.chat.id, 'Отправь ключ оплачивающего')
    bot.register_next_step_handler(message, payee)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, отправь свой ключ.')
    bot.register_next_step_handler(message, key)


@bot.message_handler(commands=['menu'])
def start_message(message):
    bot.send_message(message.chat.id, 'Ты в главном меню:', reply_markup=markupm)
    bot.register_next_step_handler(message, menu)


def key(message):
    a = 0
    b = 0
    with open('keys.csv', 'r') as fin:
        re = csv.reader(fin)
        for row in re:
            if message.text == row[0]:
                a = 1
                if row[1] == '0':
                    b = 1
                elif row[1] == message.from_user.id:
                    b = 2
                break
    if a == 0:
        bot.send_message(message.chat.id, 'Ключ не сработал, свяжитесь со мной: @raamensavin.')
        bot.send_message(message.chat.id, 'Отправь свой ключ:')
        bot.register_next_step_handler(message, key)
    else:
        if b == 1:
            dic = {}
            with open('keys.csv', 'r') as f:
                re = csv.reader(f)
                for row in re:
                    dic[row[0]] = row[1]

            dic[message.text] = message.from_user.id

            with open('keys.csv', 'w') as fin:
                wr = csv.writer(fin)
                wr.writerows(dic.items())
            with open(f'hw/{message.from_user.id}.csv', 'a') as fin:
                pass
            with open(f'payments/{message.from_user.id}.csv', 'a') as fin:
                pass
            bot.send_message(message.chat.id, 'Кайф, все подошло, доступ открыт.')
            bot.forward_message('726382042', message.chat.id, message.message_id)
            bot.send_message(message.chat.id, 'Ты в главном меню:', reply_markup=markupm)
            bot.register_next_step_handler(message, menu)
        elif b == 2:
            bot.send_message(message.chat.id, 'Ты уже зарегистрирован, можешь использовать меню.')
            bot.send_message(message.chat.id, 'Ты в главном меню:', reply_markup=markupm)
        else:
            bot.send_message(message.chat.id, 'Ключ зарегистрирован другим пользователем,'
                                              ' свяжитесь со мной: @raamensavin.')
            bot.send_message(message.chat.id, 'Отправь свой ключ:')
            bot.register_next_step_handler(message, key)


def menu(message):
    a = 0
    with open('keys.csv', 'r') as f:
        re = csv.reader(f)
        for row in re:
            if int(row[1]) == message.from_user.id:
                a = 1
                break
    if a == 1:
        if message.text == '📅Расписание📅':
            text21 = '[РАСПИСАНИЕ](https://calendar.yandex.ru/embed/week?&layer_ids=28029544&tz_id=Europe/Moscow' \
                     '&layer_names=Sigma_Squared)'
            bot.send_photo(message.chat.id, open('File1.png', 'rb'))
            bot.send_photo(message.chat.id, open('File2.png', 'rb'))
            bot.send_message(message.chat.id, text=text21, parse_mode='MarkdownV2')
            bot.register_next_step_handler(message, menu)
        elif message.text == '✒️Мои домашки✒️':
            at = []
            try:
                with open(f'hw/{message.from_user.id}.csv', 'r') as fin:
                    re = csv.reader(fin)
                    for row in re:
                        at.append(row)
                for i in at:
                    if i[1] == 'a0':
                        i[1] = a0
                    elif i[1] == 'a1':
                        i[1] = a1
                    elif i[1] == 'a2':
                        i[1] = a2
                    elif i[1] == 'a3':
                        i[1] = a3
                text1 = 'Здесь ты можешь посмотреть комментарии к своим домашкам, для этого перейди по ссылке:\n\n\n'
                for i in at:
                    text1 += f'HW{i[0]} {i[1]} --- Комментарии: {i[2]} \n'
                bot.send_message(message.chat.id, text=text1)
                bot.register_next_step_handler(message, menu)
            except:
                bot.send_message(message.chat.id, text='Некоторая техническая неполадка, напишите @raamensavin')
                bot.register_next_step_handler(message, menu)
        elif message.text == '📚Сдать домашку📚':
            bot.send_message(message.chat.id, 'Отправьте домашку ОДНИМ PDF файлом', reply_markup=markupn)
            bot.register_next_step_handler(message, ch4)
        elif message.text == '⌛️Дедлайны⌛️':
            with open('dead.txt', 'r') as f:
                T = f.read().split()
            now = datetime.datetime.today()
            DD = datetime.datetime(int(T[0]), int(T[1]), int(T[2]))
            d = DD - now  # str(d)  '83 days, 2:43:10.517807'
            mm, ss = divmod(d.seconds, 60)
            hh, mm = divmod(mm, 60)
            bot.send_message(message.chat.id, 'До следующего дедлайна домашек: '
                                              '{} дней {} часа {} мин.'.format(d.days, hh, mm))
            bot.register_next_step_handler(message, menu)
        elif message.text == '💰Мои оплаты💰':
            try:
                tete = 'Ваши оплаты:\n\n'
                with open(f'payments/{message.from_user.id}.csv', 'r') as fin:
                    re = csv.reader(fin)
                    for row in re:
                        tete += row[0]+'\n'
                        A = row[0].split()
                    DD = datetime.datetime(int(A[2]), int(A[1]), int(A[0]))
                    nextie = DD + datetime.timedelta(days=28)
                    tete += f'\nСледующая оплата: ' + f'{nextie.day}'.zfill(2) + '.' + f'{nextie.month}'.zfill(2) + '.' + \
                            f'{nextie.year}'
                bot.send_message(message.chat.id, text=tete)
                bot.register_next_step_handler(message, menu)
            except:
                bot.send_message(message.chat.id, text='Некоторая техническая неполадка, напишите @raamensavin')
                bot.register_next_step_handler(message, menu)
        elif message.text == '🚩CTF🚩':
            bot.send_message(message.chat.id, 'Отправь флаг, найденный в последней домашке.', reply_markup=markupn)
            bot.register_next_step_handler(message, ctf)
        elif message.text == 'назадрома':
            bot.send_message(message.chat.id, 'вышел из системы')
        else:
            bot.send_message(message.chat.id, 'Что-то не так, используй кнопки.')
            bot.register_next_step_handler(message, menu)
    else:
        bot.send_message(message.chat.id, 'Ваш код по какой-то причине перестал работать, свяжитесь с @raamensavin.')
        bot.register_next_step_handler(message, menu)

def ctf(message):
    with open('ctf.txt', 'r') as fin:
        flag = fin.read()
    if message.text == flag:
        with open('flag.csv', 'r') as fin:
            re = csv.reader(fin)
            a = 0
            at = []
            for row in re:
                a += 1
                at += row
        if at.count(message.from_user.username) == 0:
            with open('flag.csv', 'a') as f:
                wr = csv.writer(f)
                user = [datetime.datetime.now(), time.time(), message.from_user.username, message.from_user.id,
                        message.text]
                wr.writerow(user)
            bot.send_message(message.chat.id, f'Поздравляю, ты сдал флаг {a+1}-м', reply_markup=markupm)
            bot.register_next_step_handler(message, menu)
        else:
            bot.send_message(message.chat.id, 'Ты уже сдал этот флаг', reply_markup=markupm)
            bot.register_next_step_handler(message, menu)
    elif message.text.lower() == 'назад':
        bot.send_message(message.chat.id, 'Ты в главном меню', reply_markup=markupm)
        bot.register_next_step_handler(message, menu)
    else:
        bot.send_message(message.chat.id, 'Неверный флаг, попробуй еще раз')
        bot.register_next_step_handler(message, ctf)

def payee(message):
    a = ''
    with open('keys.csv', 'r') as fin:
        re = csv.reader(fin)
        for row in re:
            if row[0] == message.text:
                a = row[1]
                break
    try:
        with open(f'payments/{a}.csv', 'a') as f:
            wr = csv.writer(f)
            d = datetime.datetime.today()
            kk = f'{d.day}'.zfill(2) + ' ' + f'{d.month}'.zfill(2) + ' ' + f'{d.year}'
            wr.writerow([kk, a])
        bot.send_message(message.chat.id, 'Готово')
    except:
        bot.send_message(message.chat.id, 'Что-то не так')


def ch4(message):
    if message.photo is not None:
        msg1 = bot.send_message(message.chat.id, 'Это фотография а не файл, отправьте файл.', reply_markup=markupn)
        bot.register_next_step_handler(msg1, ch4)
    elif message.document is not None:
        if message.document.file_name.endswith('.pdf'):
            bot.forward_message('yourid', message.chat.id, message.message_id)
            bot.send_message(chat_id='yourid', text=f"{message.from_user.username} {message.from_user.id} сдал")
            bot.send_message(message.chat.id, 'Принято, для того, чтоб отправить другой файл выберите этот раздел еще раз'
                                              ', проверен будет только последний отправленный файл.', reply_markup=markupm)
            bot.register_next_step_handler(message, menu)
        else:
            msg1 = bot.send_message(message.chat.id, 'Это не pdf, попробуйте еще раз', reply_markup=markupn)
            bot.register_next_step_handler(msg1, ch4)
    else:
        if message.text.lower() == 'назад':
            bot.send_message(message.chat.id, text='Выберите часть:', reply_markup=markupm)
            bot.register_next_step_handler(message, menu)
        else:
            msg1 = bot.send_message(message.chat.id, 'Это не файл, отправьте решение все решение'
                                                     ' домашки одним файлом.', reply_markup=markupn)
            bot.register_next_step_handler(msg1, ch4)


@bot.message_handler()
def penis(message):
    bot.send_message(message.chat.id, "Что-то не так, используйте /start для регистрации с помощью ключа или /menu "
                                      "для использования бота после регистрации.")


bot.infinity_polling()
