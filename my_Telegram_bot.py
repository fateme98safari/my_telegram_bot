import random
import math
import qrcode
import telebot
import gtts
from khayyam import JalaliDate, JalaliDatetime
from datetime import date, datetime

bot = telebot.TeleBot("5878816228:AAFPKbiVFXATJ3h2P4Zqgn1_LXeEL02IAO8", parse_mode=None)

 

@bot.message_handler(commands = ['start'])
def start(message):
    bot.reply_to(message, "welcome" + message.from_user.first_name)


@bot.message_handler(commands=['help'])
def send_message(message):
	bot.send_message(message.chat.id, "if you Enter /game you can play with me.\n if you enter /max I can show the largest number.\n if you enter /argmax I con show the index of larget number.\n if you enter /voice write a sentence for me so I read it for you.\n if you enter /qrcode write a sentence for me so I send a QRcode for you.\n if you enter /age I can calcute your age " )


@bot.message_handler(commands=["game"])
def send_game(message):
	global computer_choice
	global messagetxt
	computer_choice=random.randint(10,100)
	messagetxt=bot.send_message(message.chat.id, "Enter a number between 10,100: " , reply_markup=markup)
	bot.register_next_step_handler(messagetxt, gameconditions)

def gameconditions(message):
	global computer_choice
	if int(message.text) < computer_choice:
		bot.send_message(message.chat.id, "go up" , reply_markup=markup)
		bot.register_next_step_handler(messagetxt, gameconditions)
	elif int(message.text) > computer_choice:
		bot.send_message(message.chat.id, " go down" , reply_markup=markup)
		bot.register_next_step_handler(messagetxt, gameconditions)
	elif int(message.text)==computer_choice:
		bot.send_message(message.chat.id, "you win" , reply_markup=markup)
		bot.register_next_step_handler(messagetxt, gameconditions)

markup=telebot.types.ReplyKeyboardMarkup(row_width=1)
key1=telebot.types.KeyboardButton("New Game")
markup.add(key1)



@bot.message_handler(commands=["voice"])
def send_voice(message):
	messagetxt=bot.send_message(message.chat.id, " Enter your English sentence: ")	
	bot.register_next_step_handler(messagetxt, sendvoice)

def sendvoice(message):
		x=gtts.gTTS( message.text , lang="en" , slow=False)
		x.save("my-project\session9\Voice2.mp3")
		Voice2 = open("my-project\session9\Voice2.mp3", "rb")
		bot.send_voice(message.chat.id, Voice2)
		

@bot.message_handler(commands=["max"])
def send_message(message):
	
	messagetxt=bot.send_message(message.chat.id, " Enter your numbers: ")	
	bot.register_next_step_handler(messagetxt, findmax)


def findmax(message):
		list_num=[]
		list_num=message.text.split(",")
		max_num=max(list_num)
		bot.send_message(message.chat.id, max_num)


@bot.message_handler(commands=["argmax"])
def send_message(message):
	global list_num
	global max_num
	list_num=[]
	messagetxt=bot.send_message(message.chat.id, " enter your numbers: ")	
	
	bot.register_next_step_handler(messagetxt, findindex)

def findindex(message):
	list_num=message.text.split(",")
	max_num=max(list_num)
	for i in range(len(list_num)):
			if list_num[i]==max_num:
				bot.send_message(message.chat.id, i)


@bot.message_handler(commands=["qrcode"])
def send_photo(message):
	messagetxt=bot.send_message(message.chat.id, " enter your text: ")	
	bot.register_next_step_handler(messagetxt, sendqr)

def sendqr(message):
		img=qrcode.make(message.text)
		img.save("my-project\session9\qrcode.png")
		photo=open("my-project\session9\qrcode.png" , "rb")
		bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=["age"])
def send_age(message):
	messagetxt=bot.send_message(message.chat.id, " enter the date of your birthday(example: 1369,10,18): ")	
	bot.register_next_step_handler(messagetxt, calcuteage)

def calcuteage(message):
		list=message.text. split(",")
		total_day=JalaliDatetime.now() - JalaliDatetime(list[0],list[1],list[2])
		year_age=total_day.days // 365
		k=total_day.days % 365
		month_age= k // 30
		day_age= k % 30	
		bot.send_message(message.chat.id, "you are:" +str(year_age)+ "year"+ str(month_age)+ "month"+ str(day_age)+ "day" )


bot.infinity_polling()