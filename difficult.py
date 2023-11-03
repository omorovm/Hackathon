import telebot
from telebot import types
from bs4 import BeautifulSoup as BS
import requests

news_img = {}
news_text = {}
text_links= []
info_text = ''
number = 0
#parsing

def get_html_news(url):
    response = requests.get(url).text
    soup = BS(response, "lxml")
    news = soup.find("div", class_= "Main--all_news").find('a').get("href")
    html_news = requests.get(news).text
    return html_news

def get_data(html):
    global news_img
    global news_text
    global text_links

    soup = BS(html, "lxml")
    all_news = soup.find("div", class_ = "Tag--articles")
    news = all_news.find_all('div', class_ = 'Tag--article') 
    j = 1
    for i in news:
        news_img[j]= i.find("img").get("src")
        news_text[j]= i.find("a", class_='ArticleItem--name').text.lstrip('\r\n').strip(" ")
        text_links += [i.find("a", class_='ArticleItem--name').get("href")]
        j+=1
        if j ==21:
            break
    return all_news

def find_info(number):
    response = requests.get(text_links[number-1]).text
    soup = BS(response, "lxml")
    news = soup.find("div", class_= "Article--text").find('p').text
    return news

def main():
    url = "https://kaktus.media/"
    html = get_html_news(url)
    data = get_data(html)

#bot

bot = telebot.TeleBot("6790757803:AAGHcC5pAQDMR0SDnGEpOcrdRuT5c0Z-bJQ")


@bot.message_handler(commands=["start"])
def start_message(message):
    main()
    bot.send_message(message.chat.id, "Parsing process")


@bot.callback_query_handler(func= lambda call: True)
def answer(call):
    global info_text
    global number
    keyboard_quit = types.InlineKeyboardMarkup()
    buttonquit=  types.InlineKeyboardButton("Quit", callback_data = "Quit")
    keyboard_quit.add(buttonquit) 
    if call.data.isdigit():
        number = int(call.data)
        info_text = find_info(number)
        keyboard_disc = types.InlineKeyboardMarkup()
        button =  types.InlineKeyboardButton("Discription", callback_data = "Discription")
        button2 =  types.InlineKeyboardButton("Photo", callback_data = "Photo")
        keyboard_disc.add(button,button2)  
        bot.send_message(call.message.chat.id, "Some title news you can see Description of this news and Photo", reply_markup = keyboard_disc)
        
    elif call.data == "Discription":

        bot.send_message(call.message.chat.id, info_text, reply_markup = keyboard_quit)

    elif call.data == "Photo":
        
        bot.send_message(call.message.chat.id, news_img[number], reply_markup = keyboard_quit)
    else:
        bot.send_message(call.message.chat.id, "До свидания")
         


@bot.message_handler()
def func(message):
    keyboard = types.InlineKeyboardMarkup()
    button_list = [types.InlineKeyboardButton(text=x, callback_data=x) for x in range(1,21)]
    keyboard.add(*button_list)
    # keyboard = types.InlineKeyboardMarkup()
    # button1 = types.InlineKeyboardButton("1", callback_data = "1")
    # button2 = types.InlineKeyboardButton("2", callback_data = "2")
    # button3 = types.InlineKeyboardButton("3", callback_data = "3")
    # button4 = types.InlineKeyboardButton("4", callback_data = "4")
    # keyboard.add(button1,button2,button3,button4)  
    
    bot.send_message(message.chat.id, f'{news_text}')
    bot.send_message(message.chat.id, "Выберите новость", reply_markup = keyboard)


bot.polling()

