import telebot
from telebot import types
import datetime
from db import init_db
from db import add_message
from datetime import datetime, time
import cfg
import pyowm


client = telebot.TeleBot(cfg.config['token'])

needHelp = []

joinedFile = open("D:/Рабочий стол/tele/joined.txt", "r")
joinedUsers = set()
for line in joinedFile:
	joinedUsers.add(line.strip())
joinedFile.close()

@client.message_handler(commands = ['start'])
def startJoin(message):
	if not str(message.chat.id) in joinedUsers:
		joinedFile = open("D:/Рабочий стол/tele/joined.txt", "a")
		joinedFile.write(str(message.chat.id) + "\n")
		joinedUsers.add(message.chat.id)
	client.send_message(message.chat.id, f'Привет ученичек седьмого Б класса! Ищешь бота для учебы? Я буду тебе как раз, пока что у меня не так много функций, но ты можешь их почитать:\n/start - это то, что вы сейчас читаете, также это список функций\n/info - всевозможная информация по учебе\n/lesson - показывает какой следующий урок(используется во время учебы)\n/audio - найти аудио-параграфы по нужным предметам\n/wish - написать пожелание по боту\n/support (ваша проблема без скобок) - написать в тех. поддержку\n/weather - посмотреть погоду')

@client.message_handler(commands = ['special'])
def mess(message):
	for user in joinedUsers:
		client.send_message(user, message.text[message.text.find(' '):])

@client.message_handler(commands=['support'])
def support(message):
	needHelpFile = open("D:/Рабочий стол/tele/needHelp.txt", "a")
	if message.chat.id > 0:
		needHelpFile.write(str(message.chat.id) + "\n" + str(message.chat.first_name) + "\n")
	else:
		needHelpFile.write(str(message.chat.id) + "\n" + str(message.chat.title) + "\n")
	needHelpFile.close()
	supportFile = open("D:/Рабочий стол/tele/support.txt", "r")
	supportTeam = set ()
	for line in supportFile:
		supportTeam.add(line.strip())
	supportFile.close()
	client.send_message(message.chat.id, 'Подожди немного, {0.first_name}! Я отправил твое сообщение разработчику! \nПожалуйста, не отправляй больше сообщений пока не получишь ответ)'.format(message.from_user, client.get_me()), parse_mode='html')
	for user in supportTeam:
		if message.chat.id > 0:
			client.send_message(int(user), str(message.chat.id) + " (" + message.chat.first_name + ")" + ": " + message.text[message.text.find(' '):])
		else:
			client.send_message(int(user), str(message.chat.id) + " (" + message.chat.title + ")" + ": " + message.text[message.text.find(' '):])


@client.message_handler(commands=['answer'])
def answer(message):
	supportFile = open("D:/Рабочий стол/tele/support.txt", "r")
	supportTeam = set ()
	for line in supportFile:
		supportTeam.add(line.strip())
	supportFile.close()
	if str(message.chat.id) in supportTeam:
		needHelp = []
		needHelpFile = open("D:/Рабочий стол/tele/needHelp.txt", "r")
		for line in needHelpFile:
			needHelp.append(line.strip())
		
		needHelpFile.close()
		for user in supportTeam:
			if message.chat.id > 0:
				client.send_message(user, str(message.chat.id) + " (" + message.chat.first_name +")" + ': Отвечает ' + needHelp[0] + " (" + needHelp[1] + "): " + message.text[message.text.find(' '):].format(message.from_user, client.get_me()), parse_mode='html')
			else:
				client.send_message(user, str(message.chat.id) + " (" + message.chat.title + ")" + ': Отвечает ' + needHelp[0] + " (" + message.chat.title + "): " + message.text[message.text.find(' '):].format(message.from_user, client.get_me()), parse_mode='html')
		client.send_message(int(needHelp[0]), 'Модератор' + ": " + message.text[message.text.find(' '):])

		with open("D:/Рабочий стол/tele/needHelp.txt", "r") as nhf:
			lines = nhf.readlines()
		with open("D:/Рабочий стол/tele/needHelp.txt", "w") as nhf:
			for line in lines:
				if line.strip("\n") != needHelp[0] and line.strip("\n") != needHelp[1]:
					nhf.write(line)
	else:
		client.send_message(message.chat.id, "У тебя нет прав на ответ)".format(message.from_user, client.get_me()), parse_mode='html')

@client.message_handler(commands=['weather'])
def getweather(message):
	owm = pyowm.OWM('dbf1c716cecbf43263218e4e0505968c')
	mgr = owm.weather_manager()

	observation = mgr.weather_at_place("Anzhero-Sudzhensk")
	w = observation.weather

	temp = w.temperature('celsius')
	temp2 = w.temperature('celsius')['temp']
	wi = w.wind()['speed']
	t2 = temp['feels_like']
	detal = w.detailed_status
	shock = (-30, -31, -32, -33, -34, -35, -36, -37, -38, -39, -40)
	vcold = (-17,-18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28 ,-29)
	cold = (-4, -3, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16)
	prohl = (-2, -1, 0, 1,  2, 3, 4, 5, 6, 7, 8, 9)
	sred = (10, 11, 12, 13, 14, 15, 16, 17)
	warm = (18, 19, 20, 21, 22)
	hot = (23, 25, 26, 27, 27, 28, 29, 30, 31, 32, 33, 34, 35)
	if int(temp2) in hot:
		client.send_message(message.chat.id, f'Ох, на улице очень жарко!🥵 Одевайся очень легко) (Температура:{int(temp2)}°C, ощущается как {int(t2)}°C, скорость ветра {wi} м/с)')
	if int(temp2) in prohl:
		client.send_message(message.chat.id, f'Там достаточно прохладно💨 (Температура:{int(temp2)}°C, ощущается как {int(t2)}°C, скорость ветра {wi} м/с)')
	if int(temp2) in sred:
		client.send_message(message.chat.id, f'Температура умеренная!☀️ (Температура:{int(temp2)}°C, ощущается как {int(t2)}°C, скорость ветра {wi} м/с)')
	if int(temp2) in warm:
		client.send_message(message.chat.id, f'На улице тепло, можно надеть легкую одежду :) (Температура:{int(temp2)}°C, ощущается как {int(t2)}°C, скорость ветра {wi} м/с)')
	if int(temp2) in cold:
		client.send_message(message.chat.id, f'Там довольно холодно, стоит надеть теплую одежду!❄️ (Температура:{int(temp2)}°C, ощущается как {int(t2)}°C, скорость ветра {wi} м/с)')
	if int(temp2) in vcold:
		client.send_message(message.chat.id, f'На улице дубак, одевайся тепло!☃️(или превратишься в этого снеговика! xD (Температура:{int(temp2)}°C, ощущается как {int(t2)}°C, скорость ветра {wi} м/с)')
	if int(temp2) in shock:
		client.send_message(message.chat.id, f'ТАМ ПРОСТО МОРОЗИНА, ты можешь не идти в школу, если температура от -31! (Температура:{int(temp2)}°C, ощущается как {int(t2)}°C, скорость ветра {wi} м/с)')

@client.message_handler(commands = ['wish'])
def ask(message):
	msg = client.send_message(message.chat.id, 'Привет, напиши свое пожелание по боту(только текстом, смайлики можно)')
	client.register_next_step_handler(msg, messagee)
def messagee(message):
	client.send_message(message.chat.id, f'Хорошо, жди ответ в лс!')

	text1 = message.text
	user_id1 = message.from_user.id
	username1 = message.from_user.username
	dev = '1175527638'
	init_db()

	add_message(user_id=user_id1, username=username1, text=text1)
	client.send_message(dev, f'Кто-то написал пожелание, посмотри его!')

@client.message_handler(commands = ['info'])
def get_user_info(message):
	markup_inline = types.InlineKeyboardMarkup()
	item_ucheba = types.InlineKeyboardButton(text = 'учеба📒', callback_data = 'ucheba')
	item_uchitelya = types.InlineKeyboardButton(text = 'учителя👩‍🏫', callback_data = 'uchitelya')


	markup_inline.add(item_ucheba, item_uchitelya)
	client.send_message(message.chat.id, 'Что ты хочешь узнать? (Псс, нажми на кнопку)',
		reply_markup = markup_inline 
	)

@client.message_handler(commands = ['secret'])
def get_user_date(message):
	current_date = datetime.now().date()
	weekday = current_date.weekday()

	datetime_now = datetime.now()
	time_now = datetime_now.time()

	zero_lesson_start = time(hour = 13, minute = 30)
	zero_lesson_end = time(hour = 14, minute = 10)

	first_lesson_start = time(hour = 14, minute = 20)
	first_lesson_end = time(hour = 15, minute = 0)

	second_lesson_start = time(hour = 15, minute = 1)
	second_lesson_end = time(hour = 15, minute = 40)

	third_lesson_start = time(hour = 16, minute = 20)
	third_lesson_end = time(hour = 17, minute = 0)

	fourth_lesson_start = time(hour = 17)
	fourth_lesson_end = time(hour = 17, minute = 40)

	fifth_lesson_start = time(hour = 18, minute = 20)
	fifth_lesson_end = time(hour = 19, minute = 0)

	six_lesson_start = time(hour = 19, minute = 1)
	six_lesson_end = time(hour = 19, minute = 40)

#	if weekday == 0:
#		if zero_lesson_start <= time_now <= zero_lesson_end:
#			client.send_message(message.chat.id, f'Сейчас нет уроков, но в 14.20 будет география в 212')
#		if first_lesson_start <= time_now <= first_lesson_end:
#			client.send_message(message.chat.id, f'Ага, сейчас будет география в 212, потом русский в 306')
#		if second_lesson_start <= time_now <= second_lesson_end:
#			client.send_message(message.chat.id, f'Так-с сейчас русский в 306, потом история в 119)')
#		if third_lesson_start <= time_now <= third_lesson_end:
#			client.send_message(message.chat.id, f'На поле он, а после него у тебя математика в 220!')
#		if fourth_lesson_start <= time_now <= fourth_lesson_end:
#			client.send_message(message.chat.id, f'Фухх, тяжело, после математики английский в 301/304')
#		if fifth_lesson_start <= time_now <= fifth_lesson_end:
#			client.send_message(message.chat.id, f'Ванечкиин...ду ю спик инглиш?! После английского домой))')
#		if six_lesson_start <= time_now <= six_lesson_end:
#			client.send_message(message.chat.id, f'Сейчас нет уроков, ДОМООООООЙЙЙЙЙ!!')
#	if weekday == 1:
#		if zero_lesson_start <= time_now <= zero_lesson_end:
#			client.send_message(message.chat.id, f'Нулевого урока нет, также как и учебы)')
#		if first_lesson_start <= time_now <= first_lesson_end:
#			client.send_message(message.chat.id, f'Первого урока нет, также как и учебы)')
#		if second_lesson_start <= time_now <= second_lesson_end:
#			client.send_message(message.chat.id, f'Второго урока нет, также как и учебы)')
#		if third_lesson_start <= time_now <= third_lesson_end:
#			client.send_message(message.chat.id, f'Третьего урока нет, также как и учебы)')
#		if fourth_lesson_start <= time_now <= fourth_lesson_end:
#			client.send_message(message.chat.id, f'Четвертого урока нет, также как и учебы)')
#		if fifth_lesson_start <= time_now <= fifth_lesson_end:
#			client.send_message(message.chat.id, f'Пятого урока нет, также как и учебы)')
#		if six_lesson_start <= time_now <= six_lesson_end:
#			client.send_message(message.chat.id, f'Дальше уроков нет, иди домой!)')
#	if weekday == 2:
#		if zero_lesson_start <= time_now <= zero_lesson_end:
#			client.send_message(message.chat.id, f'Нулевого урока нет, также как и учебы)')
#		if first_lesson_start <= time_now <= first_lesson_end:
#			client.send_message(message.chat.id, f'Первого урока нет, также как и учебы)')
#		if second_lesson_start <= time_now <= second_lesson_end:
#			client.send_message(message.chat.id, f'Второго урока нет, также как и учебы)')
#		if third_lesson_start <= time_now <= third_lesson_end:
#			client.send_message(message.chat.id, f'Третьего урока нет, также как и учебы)')
#		if fourth_lesson_start <= time_now <= fourth_lesson_end:
#			client.send_message(message.chat.id, f'Четвертого урока нет, также как и учебы)')
#		if fifth_lesson_start <= time_now <= fifth_lesson_end:
#			client.send_message(message.chat.id, f'Пятого урока нет, также как и учебы)')
#		if six_lesson_start <= time_now <= six_lesson_end:
#			client.send_message(message.chat.id, f'Дальше уроков нет, иди домой!)')
#	if weekday == 3:
#		if zero_lesson_start <= time_now <= zero_lesson_end:
#			client.send_message(message.chat.id, f'Нулевого урока нет, также как и учебы)')
#		if first_lesson_start <= time_now <= first_lesson_end:
#			client.send_message(message.chat.id, f'Первого урока нет, также как и учебы)')
#		if second_lesson_start <= time_now <= second_lesson_end:
#			client.send_message(message.chat.id, f'Второго урока нет, также как и учебы)')
#		if third_lesson_start <= time_now <= third_lesson_end:
#			client.send_message(message.chat.id, f'Третьего урока нет, также как и учебы)')
#		if fourth_lesson_start <= time_now <= fourth_lesson_end:
#			client.send_message(message.chat.id, f'Четвертого урока нет, также как и учебы)')
#		if fifth_lesson_start <= time_now <= fifth_lesson_end:
#			client.send_message(message.chat.id, f'Пятого урока нет, также как и учебы)')
#		if six_lesson_start <= time_now <= six_lesson_end:
#			client.send_message(message.chat.id, f'Дальше уроков нет, иди домой!)')
#	if weekday == 4:
#		if zero_lesson_start <= time_now <= zero_lesson_end:
#			client.send_message(message.chat.id, f'Сейчас урока нет, но потом будет Русский язык в 306 кабинете')
#		if first_lesson_start <= time_now <= first_lesson_end:
#			client.send_message(message.chat.id, f'Сейчас Русский, следующий урок математика в 220')
#		if second_lesson_start <= time_now <= second_lesson_end:
#			client.send_message(message.chat.id, f'Щас математика, потом биология в 311')
#		if third_lesson_start <= time_now <= third_lesson_end:
#			client.send_message(message.chat.id, f'Так-с, сейчас биология, после нее английский в 301/304')
#		if fourth_lesson_start <= time_now <= fourth_lesson_end:
#			client.send_message(message.chat.id, f'Ванечкиин..ой, аа.. а, да! После английского у тебя физ-ра')
#		if fifth_lesson_start <= time_now <= fifth_lesson_end:
#			client.send_message(message.chat.id, f'Физра последним, ДОМООЙЙЙ!!')
#		if six_lesson_start <= time_now <= six_lesson_end:
#			client.send_message(message.chat.id, f'Сейчас уже не будет уроков, чапай домой!)')
#	if weekday == 5:
#		if zero_lesson_start <= time_now <= zero_lesson_end:
#			client.send_message(message.chat.id, f'Нулевого урока нет, также как и учебы)')
#		if first_lesson_start <= time_now <= first_lesson_end:
#			client.send_message(message.chat.id, f'Первого урока нет, также как и учебы)')
#		if second_lesson_start <= time_now <= second_lesson_end:
#			client.send_message(message.chat.id, f'Второго урока нет, также как и учебы)')
#		if third_lesson_start <= time_now <= third_lesson_end:
#			client.send_message(message.chat.id, f'Третьего урока нет, также как и учебы)')
#		if fourth_lesson_start <= time_now <= fourth_lesson_end:
#			client.send_message(message.chat.id, f'Четвертого урока нет, также как и учебы)')
#		if fifth_lesson_start <= time_now <= fifth_lesson_end:
#			client.send_message(message.chat.id, f'Пятого урока нет, также как и учебы)')
#		if six_lesson_start <= time_now <= six_lesson_end:
#			client.send_message(message.chat.id, f'Дальше уроков нет, иди домой!)')
#	if weekday == 6:
#		client.send_message(message.chat.id, f'У тебя сегодня нет уроков!')

@client.callback_query_handler(func = lambda call: True)
def answer(call):
	client.answer_callback_query(callback_query_id=call.id)
	if call.data == 'ucheba':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
		item_dz = types.KeyboardButton('дз😉')
		item_raspis = types.KeyboardButton('расписание🗓')

		markup_reply.add(item_dz, item_raspis)
		client.send_message(call.message.chat.id, 'нажми на одну из кнопок',
			reply_markup = markup_reply
		)
	if call.data == 'uchitelya':
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
		item_uchit = types.KeyboardButton('учителя👩‍🏫')
		item_vneuch = types.KeyboardButton('учителя внеурочек👩‍🏫')

		markup_reply.add(item_uchit, item_vneuch)
		client.send_message(call.message.chat.id, 'нажми на одну из кнопок',
			reply_markup = markup_reply
		)

@client.message_handler(commands = ['audio'])
def audio(message):
	markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
	item_history = types.KeyboardButton('история🐋')
	item_geography = types.KeyboardButton('география🐋')
	item_obsh = types.KeyboardButton('обществознание🐋')
	item_biology = types.KeyboardButton('биология🐋')
	item_literature = types.KeyboardButton('литература🐋')

	markup_reply.add(item_history)
	markup_reply.add(item_geography, item_obsh)
	markup_reply.add(item_biology, item_literature)
	client.send_message(message.chat.id, 'по какому уроку ты хочешь послушать параграф?)🐋',
		reply_markup = markup_reply 
	)

@client.message_handler(content_types = ['text'])
def get_text(message):
	if message.text == 'дз😉':
		client.send_message(message.chat.id, 'Вот дз на 27.11:\n' + "литература: рассказ о характере Ивана Грозного (оцените его как неоднозначного человека) , эпохе его правления, опричнине\n" + "алгебра: №318, 322\n" + "обществознание: учить конспект")
	if message.text == 'расписание🗓':
		current_date = datetime.now().date()
		weekday1 = current_date.weekday()
		img0 = open('schedule.png', 'rb')
		if weekday1 == 0:
			client.send_photo(message.chat.id, img0)
		if weekday1 == 1:
			client.send_photo(message.chat.id, img0)
		if weekday1 == 2:
			client.send_photo(message.chat.id, img0)
		if weekday1 == 3:
			client.send_photo(message.chat.id, img0)
		if weekday1 == 4:
			client.send_photo(message.chat.id, img0)
		if weekday1 == 5:
			client.send_photo(message.chat.id, img0)
		if weekday1 == 6:
			client.send_photo(message.chat.id, img0) 
	if message.text == 'учителя👩‍🏫':
		imgg = open('teachers.png', 'rb')
		client.send_photo(message.chat.id, imgg)
	if message.text == 'учителя внеурочек👩‍🏫':
		imgg = open('teachers.png', 'rb')
		client.send_photo(message.chat.id, imgg)
	if message.text == 'история🐋':
		client.send_message(message.chat.id, f'https://audioknigi-sv.ru/istoriya-rossii-7-klass-arsentev-i-dr/, держи, на сайте выбери параграф который хочешь прослушать)🤍')
	if message.text == 'география🐋':
		client.send_message(message.chat.id, f'https://audioclassbook.ru/6-класс, держи, к сожалению я не смог найти нормального сайта, но ты можешь найти нужный учебник среди списка!😢')
	if message.text == 'обществознание🐋':
		client.send_message(message.chat.id, f'https://www.youtube.com/watch?v=nxs-11lVVjY&list=PLeHgo1ufLA5rJUG0DtQ6r8CDpBMMhAhgr, держи, в плейлисте на YouTube ты сможешь выбрать параграф!💞')
	if message.text == 'биология🐋':
		client.send_message(message.chat.id, f'https://audioclassbook.ru/6-класс, держи, к сожалению я не смог найти нормального сайта, но ты можешь найти нужный учебник среди списка!😢')
	if message.text == 'литература🐋':
		client.send_message(message.chat.id, f'https://audioclassbook.ru/6-класс, держи, к сожалению я не смог найти нормального сайта, но ты можешь найти нужный учебник среди списка!😢')


client.polling(none_stop = True, interval = 0)