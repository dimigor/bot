# -*- coding: utf-8 -*-
import telebot
import unirest
import config
bot = telebot.TeleBot(config.token)



@bot.message_handler(commands=["start"])
def get_name_messages(message):

    bot.send_message(message.chat.id, "Вас вітає musicLyricBot. \nДля того щоб знайти текст пісні, введіть ім'я виконавця та назву пісні латиницею розділивши їх '-'\nНаприкад:\nThe Space Brothers - Shine\nтакож ви можете надіслати або переслати аудіофайл з піснею текст якої ви хочете дізнатися")



@bot.message_handler(content_types=["text"])
def text_messages(message):
    last_message = message.text

    if "-" in last_message :
        list_items = []
        for item in last_message.split('-'):
            list_items.append(item)

        response = unirest.get(
            "https://musixmatchcom-musixmatch.p.mashape.com/wsr/1.1/matcher.lyrics.get?q_artist={}&q_track={}".format(
                list_items[0], list_items[1]),
            headers={
                "X-Mashape-Key": "FAcV4trxZUmshiGXuWRh5NtlRoADp1YZ3kvjsnTezlPZM4aSv6",
                "Accept": "application/json"
            }
            ).body
        if response != "" :
            lyricsText = response['lyrics_body']
            lyricsText = lyricsText.split('*****')
            bot.send_message(message.chat.id, lyricsText)
        else :
            bot.send_message(message.chat.id, "У нашому каталозі немає такої пісні. \nПеревірте правильність вводу, або введіть іншу пісню")




    else :
        bot.send_message(message.chat.id, "Введіть ім'я артиста та назву треку через тире ' - ' \nНаприклад: \nArmin van Buuren - I Need you")


@bot.message_handler(content_types=['audio'])
def audio_message(message):
    title_audio = message.audio.title
    performer_audio = message.audio.performer

    response = unirest.get(
        "https://musixmatchcom-musixmatch.p.mashape.com/wsr/1.1/matcher.lyrics.get?q_artist={}&q_track={}".format(
            performer_audio, title_audio),
        headers={
            "X-Mashape-Key": "FAcV4trxZUmshiGXuWRh5NtlRoADp1YZ3kvjsnTezlPZM4aSv6",
            "Accept": "application/json"
        }
    ).body
    if response != "":
        lyricsText = response['lyrics_body']
        lyricsText = lyricsText.split('*****')
        bot.send_message(message.chat.id, lyricsText)
    else:
        bot.send_message(message.chat.id,
                         "У нашому каталозі немає такої пісні. \nПеревірте правильність вводу, або введіть іншу пісню")


bot.polling(none_stop=True, interval=0)










