import telebot
import config
import random
import time

from telebot import types

bot = telebot.TeleBot(config.TOKEN)
scheduleLasts = {}
scheduleLimit = 30

users = []
with open('users.txt', 'r') as f:
	for i in f:
		users.append(i.replace('\n', ''))
print(users)

@bot.message_handler(commands=['start'])
def welcome(message):
	if message.chat.type == 'private':
		if str(message.chat.id) not in users:
			users.append(message.chat.id)
			with open('users.txt', 'a') as f:
				f.write(str(message.chat.id)+'\n')
				print('+ юзерио',message.chat.id)
		sti = open('static/sticker.webp', 'rb')
		bot.send_sticker(message.chat.id, sti)


		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton("🗓 Узнать расписание")
		item2 = types.KeyboardButton("💎 Предложить функцию")
		item3 = types.KeyboardButton("😊 Как дела?")

		markup.add(item1,item2,item3)

		bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЭто - <b>{1.first_name}</b>, бот для расписания INAI.kg! ".format(message.from_user, bot.get_me()),
			parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['emodel'])
def emodel(message):
	if str(message.chat.id) == str(config.adminID):
		with open('emotions.txt', 'w') as f:
			f.write(str(0) + '\n' + str(0) + '\n' + str(0) + '\n')
		bot.send_message(message.chat.id, "Ты очистил настроения!",
			parse_mode='html')

@bot.message_handler(commands=['send'])
def sender(message):
	if str(message.chat.id) == str(config.adminID):
		for i in users:
			bot.send_message(int(i), message.text[6:], parse_mode='html')

@bot.message_handler(commands=['schedule'])
def schedule(message):
	currentChatId = str(message.chat.id)
	try:
		last_used = scheduleLasts[currentChatId]
	except:
		last_used = 1
	if int(time.time()) - last_used > scheduleLimit:
		markup = types.InlineKeyboardMarkup(row_width=2)
		item1 = types.InlineKeyboardButton("⚪️ AIN-1-21 ⚪️", callback_data='ain121')
		item2 = types.InlineKeyboardButton("🔵 AIN-2-21 🔵", callback_data='ain221')
		item3 = types.InlineKeyboardButton("🟣 AIN-3-21 🟣", callback_data='ain321')
		item4 = types.InlineKeyboardButton("🔴 MIN-1-21 🔴", callback_data='min121')
		item5 = types.InlineKeyboardButton("🟠 WIN-1-21 🟠", callback_data='win121')
		markup.add(item1, item2, item3, item4, item5,)
		bot.send_message(message.chat.id, 'Из какой вы группы?', reply_markup=markup)
		last_used = int(time.time())
		scheduleLasts[currentChatId] = last_used
	else:
		markup = types.InlineKeyboardMarkup(row_width=2)
		item1 = types.InlineKeyboardButton("ОК", callback_data='remove')
		markup.add(item1)
		bot.send_message(message.chat.id, 'Команду можно использовать раз через {0} секунд.'.format(scheduleLimit - (int(time.time()) - last_used)), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def main(message):
	if message.chat.type == 'private':
		if message.text == '🗓 Узнать расписание':

			markup = types.InlineKeyboardMarkup(row_width=2)
			item1 = types.InlineKeyboardButton("⚪️ AIN-1-21 ⚪️", callback_data='ain121')
			item2 = types.InlineKeyboardButton("🔵 AIN-2-21 🔵", callback_data='ain221')
			item3 = types.InlineKeyboardButton("🟣 AIN-3-21 🟣", callback_data='ain321')
			item4 = types.InlineKeyboardButton("🔴 MIN-1-21 🔴", callback_data='min121')
			item5 = types.InlineKeyboardButton("🟠 WIN-1-21 🟠", callback_data='win121')
			markup.add(item1, item2, item3, item4, item5,)

			bot.send_message(message.chat.id, 'Из какой вы группы?', reply_markup=markup)
		elif message.text == '💎 Предложить функцию':
			bot.send_message(message.chat.id, 'Предложить какую либо фичу можно сюда: @i_4m_robot')
		elif message.text == '😊 Как дела?':
			markup = types.InlineKeyboardMarkup(row_width=2)
			item1 = types.InlineKeyboardButton("😁 Отлично", callback_data='good')
			item2 = types.InlineKeyboardButton("😐 Норм", callback_data='norm')
			item3 = types.InlineKeyboardButton("😔 Такое себе", callback_data='bad')
			markup.add(item1, item2, item3)

			bot.send_message(message.chat.id, 'У меня хорошо, а у тебя?', reply_markup=markup)
		else:
			bot.send_message(message.chat.id, 'Возможно такой команды уже нет. Напишите /start')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'norm':
				goodEmotions = 0
				normEmotions = 0
				badEmotions = 0
				with open('emotions.txt', 'r') as f:
					mass = []
					for i in f:
						mass.append(int(i))
					goodEmotions = int(mass[0])
					normEmotions = int(mass[1])
					badEmotions = int(mass[2])
				normEmotions += 1
				with open('emotions.txt', 'w') as f:
					f.write(str(goodEmotions) + '\n' + str(normEmotions) + '\n' + str(badEmotions) + '\n')
				markup = types.InlineKeyboardMarkup(row_width=2)
				item1 = types.InlineKeyboardButton("◀️ Вернуться", callback_data='backemo')
				markup.add(item1)
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Надеюсь оно улучшится!*\n\n'+'Статистика за сегодня по настроению студентов:\n'+'С хорошим настроением: '+str(goodEmotions)+'\n'+'С нормальным настроением: '+str(normEmotions)+'\n'+'С плохим настроением: '+str(badEmotions) +'\n', reply_markup=markup, parse_mode='Markdown')
			elif call.data == 'bad':
				goodEmotions = 0
				normEmotions = 0
				badEmotions = 0
				with open('emotions.txt', 'r') as f:
					mass = []
					for i in f:
						mass.append(int(i))
					goodEmotions = int(mass[0])
					normEmotions = int(mass[1])
					badEmotions = int(mass[2])
				badEmotions += 1
				with open('emotions.txt', 'w') as f:
					f.write(str(goodEmotions) + '\n' + str(normEmotions) + '\n' + str(badEmotions) + '\n')
				markup = types.InlineKeyboardMarkup(row_width=2)
				item1 = types.InlineKeyboardButton("◀️ Вернуться", callback_data='backemo')
				markup.add(item1) 
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*НЕ ГРУСТИ!*\n\n'+'Статистика за сегодня по настроению студентов:\n'+'С хорошим настроением: '+str(goodEmotions)+'\n'+'С нормальным настроением: '+str(normEmotions)+'\n'+'С плохим настроением: '+str(badEmotions) +'\n', reply_markup=markup, parse_mode='Markdown')
			
			elif call.data == 'good':
				goodEmotions = 0
				normEmotions = 0
				badEmotions = 0
				with open('emotions.txt', 'r') as f:
					mass = []
					for i in f:
						mass.append(int(i))
					goodEmotions = int(mass[0])
					normEmotions = int(mass[1])
					badEmotions = int(mass[2])
				goodEmotions += 1
				with open('emotions.txt', 'w') as f:
					f.write(str(goodEmotions) + '\n' + str(normEmotions) + '\n' + str(badEmotions) + '\n')

				markup = types.InlineKeyboardMarkup(row_width=2)
				item1 = types.InlineKeyboardButton("◀️ Вернуться", callback_data='backemo')
				markup.add(item1)
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='*Это здорово!*\n\n'+'Статистика за сегодня по настроению студентов:\n'+'С хорошим настроением: '+str(goodEmotions)+'\n'+'С нормальным настроением: '+str(normEmotions)+'\n'+'С плохим настроением: '+str(badEmotions) +'\n', reply_markup=markup, parse_mode='Markdown')

			elif call.data == 'ain121':
				markup = types.InlineKeyboardMarkup(row_width=2)
				item1 = types.InlineKeyboardButton("◀️ Вернуться", callback_data='back')
				markup.add(item1)
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
⚪️ AIN-1-21 ⚪️
--------------				
*Понедельник:*

8:00 - Немецкий язык
9:30 - АСД
11:00 - ВЧК

*Вторник:*

8:00 - Английский язык
9:30 - Математика
11:00 - АСД
12:30 - Математика

*Среда:*

9:30 - Языки программирования
11:00 - Немецкий язык

*Четверг:*

8:00 - Английский язык
9:30 - ВЧК

*Пятница:*

8:00 - Английский язык
9:30 - Языки программирования
11:00 - Немецкий язык

*Суббота:*

8:00 - ВЧК
9:30 - АСД
11:00 - Языки программирования
12:30 - Математика
--------------
⚪️ AIN-1-21 ⚪️''', reply_markup=markup, parse_mode='Markdown')
			elif call.data == 'ain221':
				markup = types.InlineKeyboardMarkup(row_width=2)
				item1 = types.InlineKeyboardButton("◀️ Вернуться", callback_data='back')
				markup.add(item1)
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''

🔵 AIN-2-21 🔵
--------------
*Понедельник:*

8:00 - АСД
9:30 - Немецкий язык
11:00 - Математика

*Вторник:*

8:00 - ВЧК
9:30 - АСД
11:00 - Английский язык

*Среда:*

8:00 - Языки программирования
9:30 - Немецкий язык
11:00 - Математика

*Четверг:*

9:30 - ВЧК
11:00 - Английский язык

*Пятница:*

8:00 - Языки программирования
9:30 - Немецкий язык
11:00 - Английский язык

*Суббота:*

8:00 - ВЧК
9:30 - АСД
11:00 - Языки программирования
12:30 - Математика
--------------
🔵 AIN-2-21 🔵''', reply_markup=markup, parse_mode='Markdown')
			elif call.data == 'ain321':
				markup = types.InlineKeyboardMarkup(row_width=2)
				item1 = types.InlineKeyboardButton("◀️ Вернуться", callback_data='back')
				markup.add(item1)
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
🟣 AIN-3-21 🟣
--------------
*Понедельник:*

8:00 - Английский язык
9:30 - Математика
11:00 - Немецкий язык

*Вторник:*

8:00 - АСД
9:30 - Языки программирования
11:00 - ВЧК

*Среда:*

9:30 - Английский язык
11:00 - Английский язык
12:30 - Немецкий язык

*Четверг:*

8:00 - ВЧК
9:30 - АСД

*Пятница:*

8:00 - Немецкий язык
9:30 - Математика
11:00 - Языки программирования

*Суббота:*

8:00 - ВЧК
9:30 - АСД
11:00 - Языки программирования
12:30 - Математика
--------------
🟣 AIN-3-21 🟣''', reply_markup=markup, parse_mode='Markdown')

			elif call.data == 'min121':
				markup = types.InlineKeyboardMarkup(row_width=2)
				item1 = types.InlineKeyboardButton("◀️ Вернуться", callback_data='back')
				markup.add(item1)
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
🔴 MIN-1-21 🔴
--------------
*Понедельник:*

8:00 - Математика
9:30 - Английский язык
11:00 - Английский язык

*Вторник:*

8:00 - Языки программирования
9:30 - Немецкий язык
11:00 - Немецкий язык

*Среда:*

8:00 - Английский язык
9:30 - Математика
11:00 - ВЧК
12:30 - Языки программирования

*Четверг:*

8:00 - АСД
9:30 - Немецкий язык

*Пятница:*

9:30 - ВЧК
11:00 - АСД

*Суббота:*

8:00 - ВЧК
9:30 - АСД
11:00 - Языки программирования
12:30 - Математика
--------------
🔴 MIN-1-21 🔴''', reply_markup=markup, parse_mode='Markdown')
				markup = types.InlineKeyboardMarkup(row_width=2)
				item1 = types.InlineKeyboardButton("◀️ Вернуться", callback_data='back')
				markup.add(item1)
			elif call.data == 'win121':
				markup = types.InlineKeyboardMarkup(row_width=2)
				item1 = types.InlineKeyboardButton("◀️ Вернуться", callback_data='back')
				markup.add(item1)
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
🟠 WIN-1-21 🟠
--------------
*Понедельник:*

9:30 - ВЧК
11:00 - АСД

*Вторник:*

8:00 - Немецкий язык
9:30 - Английский язык
11:00 - Языки программирования

*Среда:*

8:00 - Математика
9:30 - АСД
11:00 - Языки программирования

*Четверг:*

8:00 - Немецкий язык
9:30 - Английский язык
11:00 - Немецкий язык

*Пятница:*

8:00 - Математика
9:30 - Английский язык
11:00 - ВЧК

*Суббота:*

8:00 - ВЧК
9:30 - АСД
11:00 - Языки программирования
12:30 - Математика
--------------
🟠 WIN-1-21 🟠''', reply_markup=markup, parse_mode='Markdown')
			elif call.data == 'back':
				markup = types.InlineKeyboardMarkup(row_width=2)
				item1 = types.InlineKeyboardButton("⚪️ AIN-1-21 ⚪️", callback_data='ain121')
				item2 = types.InlineKeyboardButton("🔵 AIN-2-21 🔵", callback_data='ain221')
				item3 = types.InlineKeyboardButton("🟣 AIN-3-21 🟣", callback_data='ain321')
				item4 = types.InlineKeyboardButton("🔴 MIN-1-21 🔴", callback_data='min121')
				item5 = types.InlineKeyboardButton("🟠 WIN-1-21 🟠", callback_data='win121')
				markup.add(item1, item2, item3, item4, item5,)
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Из какой ты группы?", reply_markup=markup)
			elif call.data == 'backemo':
				
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Привет!\nВыбери что то из меню:", reply_markup=None)
			
			elif call.data == 'remove':
				bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	except Exception as e:
		print('защита нахой', e)

bot.polling(none_stop=True)