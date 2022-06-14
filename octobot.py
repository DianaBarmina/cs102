import os
import validators
import telebot
import gspread
import json
import pandas as pd
import emoji
from datetime import datetime, timedelta, date

bot = telebot.TeleBot('5522115262:AAHF7ZCKpd3KGA5ic0EpWDkzzdlmO5oloiQ')
help_list = []


def convert_date(date: str = "01/01/00"):
    """ Конвертируем дату из строки в datetime """
    try:
        return datetime.strptime(date, "%d.%m.%Y")
    except ValueError:
        return False


def connect_table(message):
    """ Подключаемся к Google-таблице """
    url = message.text
    sheet_id = "1iCdHwUkZeyaC5aZGosNG-K4VXDnSQudca5dTkzJzWek"
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open('tables.json', 'w') as json_file:
        json.dump(tables, json_file)
    bot.send_message(message.chat.id, "Таблица подключена!")


def access_current_sheet():
    """ Обращаемся к Google-таблице """
    with open("tables.json") as json_file:
        tables = json.load(json_file)

    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    # Преобразуем Google-таблицу в таблицу pandas
    gtab = pd.DataFrame(worksheet.get_values(""), columns=worksheet.row_values(1))
    gtab = gtab.drop(0)
    gtab.index -= 1
    return worksheet, tables[max(tables)]["url"], gtab


def choose_action(message):
    """ Обрабатываем действия верхнего уровня """
    if message.text == "Подключить Google-таблицу":
        connect_table(message)
    elif message.text == "Узнать свои баллы" or message.text == emoji.emojize("Узнать свои баллы :bookmark_tabs:", variant="emoji_type"):
        vedomosti(message)
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row(emoji.emojize("Спасибо! Это все :smiling_face_with_hearts:", variant="emoji_type"))
        start_markup.row(emoji.emojize("Вернуться в начало :BACK_arrow:", variant="emoji_type"))
        info = bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=start_markup)
        bot.register_next_step_handler(info, finish_work)

    elif message.text == "Редактировать предметы" or message.text == emoji.emojize("Редактировать предметы :pencil:", variant="emoji_type"):
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row(emoji.emojize("Добавить новый предмет :pushpin:", variant="emoji_type"))
        start_markup.row(emoji.emojize("Отредактировать предмет или ссылку на ведомость :memo:", variant="emoji_type"))
        start_markup.row(emoji.emojize("Удалить один из предметов :cross_mark:", variant="emoji_type"))
        start_markup.row(emoji.emojize("Удалить ВСЕ :cross_mark::cross_mark::cross_mark:", variant="emoji_type"))
        start_markup.row(emoji.emojize("В начало :BACK_arrow:", variant="emoji_type"))
        info = bot.send_message(message.chat.id, "Что хочешь сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_subject_action)

    elif message.text == "Изменить дедлайны" or message.text == emoji.emojize("Изменить дедлайны :pencil:", variant="emoji_type"):
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row(emoji.emojize("Добавить дедлайн :pushpin:", variant="emoji_type"))
        start_markup.row(emoji.emojize("Изменить дату одного из дедлайнов :black_nib:", variant="emoji_type"))
        start_markup.row(emoji.emojize("Удалить один из дедлайнов :cross_mark:", variant="emoji_type"))
        start_markup.row(emoji.emojize("В начало :BACK_arrow:", variant="emoji_type"))

        info = bot.send_message(message.chat.id, "Что хочешь сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_deadline_action)

    elif message.text == emoji.emojize("Посмотреть дедлайны на этой неделе :calendar:", variant="emoji_type") or message.text == "Посмотреть дедлайны на этой неделе":
        bot.send_message(message.chat.id, emoji.emojize("Секунду ... :hourglass_not_done:", variant="emoji_type"))
        today = datetime.today()
        week = today + timedelta(days=7)
        worksheet, b, df = access_current_sheet()
        deadlines = ""
        for i in range(2, len(worksheet.col_values(1)) + 1):
            for cur_deadline in worksheet.row_values(i)[2:]:
                if week >= convert_date(cur_deadline) >= today:
                    deadlines += f"{worksheet.cell(i, 1).value}: {cur_deadline}\n"
        if deadlines:
            bot.send_message(message.chat.id, emoji.emojize("Ближайшие дедлайны :fearful_face:", variant="emoji_type"))
            bot.send_message(message.chat.id, f"\n\n{deadlines}")
        else:
            bot.send_message(message.chat.id, emoji.emojize("Выдохни и расслабься, пока дедлайны не горят "
                                                            ":woman_in_lotus_position:", variant="emoji_type"))
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row(emoji.emojize("Спасибо! Это все :smiling_face_with_hearts:", variant="emoji_type"))
        start_markup.row(emoji.emojize("Вернуться в начало :BACK_arrow:", variant="emoji_type"))
        info = bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=start_markup)
        bot.register_next_step_handler(info, finish_work)


def choose_subject_action(message):
    """ Выбираем действие в разделе Редактировать предметы """
    if message.text == "Добавить новый предмет" or message.text == emoji.emojize("Добавить новый предмет :pushpin:", variant="emoji_type"):
        message = bot.send_message(message.chat.id, "Напишите название предмета и через пробел - ссылку на ведомость")
        bot.register_next_step_handler(message, add_new_subject_and_url)

    elif message.text == "Отредактировать предмет или ссылку на ведомость" or message.text == emoji.emojize("Отредактировать предмет или ссылку на ведомость :memo:", variant="emoji_type"):
        worksheet, b, df = access_current_sheet()
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for el in df.subject:
            start_markup.row(el)
        info = bot.send_message(message.chat.id, "Какой предмет редактируем?", reply_markup=start_markup)
        bot.register_next_step_handler(info, update_subject)

    elif message.text == "Удалить один из предметов" or message.text == emoji.emojize("Удалить один из предметов :cross_mark:", variant="emoji_type"):
        worksheet, b, df = access_current_sheet()
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for el in df.subject:
            start_markup.row(el)
        info = bot.send_message(message.chat.id, "Какой предмет удаляем?", reply_markup=start_markup)
        bot.register_next_step_handler(info, delete_subject)

    elif message.text == "Удалить ВСЕ" or message.text == emoji.emojize("Удалить ВСЕ :cross_mark::cross_mark::cross_mark:", variant="emoji_type"):
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Да, я уверена")
        start_markup.row("Нет")
        info = bot.send_message(message.chat.id, "Вы точно хотите удалить ВСЕ?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_removal_option)
    elif message.text == "В начало" or message.text == emoji.emojize("В начало :BACK_arrow:", variant="emoji_type"):
        start(message)
    pass


def choose_deadline_action(message):
    """ Выбираем действие в разделе Редактировать дедлайн """
    if message.text == "Добавить дедлайн" or message.text == emoji.emojize("Добавить дедлайн :pushpin:", variant="emoji_type"):
        worksheet, b, df = access_current_sheet()
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for el in df.subject:
            start_markup.row(el)
        info = bot.send_message(message.chat.id, "Какому предмету добавляем?", reply_markup=start_markup)
        bot.register_next_step_handler(info, add_subject_deadline)

    elif message.text == "Изменить дату одного из дедлайнов" or message.text == emoji.emojize("Изменить дату одного из дедлайнов :black_nib:", variant="emoji_type"):
        worksheet, b, df = access_current_sheet()
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for el in df.subject:
            start_markup.row(el)
        info = bot.send_message(message.chat.id, "Для какого предмета изменяем?", reply_markup=start_markup)
        bot.register_next_step_handler(info, update_subject_deadline)

    elif message.text == "Удалить один из дедлайнов" or message.text == emoji.emojize("Удалить один из дедлайнов :cross_mark:", variant="emoji_type"):
        worksheet, b, df = access_current_sheet()
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for el in df.subject:
            start_markup.row(el)
        info = bot.send_message(message.chat.id, "У какого предмета удаляем дедлайн?", reply_markup=start_markup)
        bot.register_next_step_handler(info, delete_subject_deadline)
    elif message.text == "В начало" or message.text == emoji.emojize("В начало :BACK_arrow:", variant="emoji_type"):
        start(message)
    pass


def choose_removal_option(message):
    """ Уточняем, точно ли надо удалить все """
    if message.text == "Да, я уверена":
        bot.send_message(message.chat.id, "Урааааа!! Свобода!")
        clear_subject_list(message)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Ну ладно.. А счастье было так близко..")
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row(emoji.emojize("Спасибо! Это все :smiling_face_with_hearts:", variant="emoji_type"))
        start_markup.row(emoji.emojize("Вернуться в начало :BACK_arrow:", variant="emoji_type"))
        info = bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=start_markup)
        bot.register_next_step_handler(info, finish_work)
    pass


def add_subject_deadline1(message):
    """ Выбираем предмет, у которого надо отредактировать дедлайн """
    global help_list
    help_list.append(message.text)
    worksheet, b, df = access_current_sheet()
    row = worksheet.find(help_list[0]).row
    col = worksheet.find(help_list[1]).col
    if not worksheet.cell(row, col).value:
        inf = bot.send_message(message.chat.id, "Введи дату в формате 'dd.mm.yyyy'")
        bot.register_next_step_handler(inf, add_subject_deadline2)
    else:
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Да")
        start_markup.row("Нет")
        info = bot.send_message(message.chat.id, f"Дедлайн для этой лабы уже есть: {worksheet.cell(row, col).value}\nИзменить его?",
                                reply_markup=start_markup)
        bot.register_next_step_handler(info, add_or_change)


def add_or_change(message):
    if message.text == "Да":
        info = bot.send_message(message.chat.id, "Введи дату в формате 'dd.mm.yyyy'")
        bot.register_next_step_handler(info, update_subject_deadline3)
    elif message.text == "Нет":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row(emoji.emojize("Спасибо! Это все :smiling_face_with_hearts:", variant="emoji_type"))
        start_markup.row(emoji.emojize("Вернуться в начало :BACK_arrow:", variant="emoji_type"))
        info = bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=start_markup)
        bot.register_next_step_handler(info, finish_work)


def add_or_change2(message):
    if message.text == "Да":
        info = bot.send_message(message.chat.id, "Введи дату в формате 'dd.mm.yyyy'")
        bot.register_next_step_handler(info, add_subject_deadline2)
    elif message.text == "Нет":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row(emoji.emojize("Спасибо! Это все :smiling_face_with_hearts:", variant="emoji_type"))
        start_markup.row(emoji.emojize("Вернуться в начало :BACK_arrow:", variant="emoji_type"))
        info = bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=start_markup)
        bot.register_next_step_handler(info, finish_work)


def add_subject_deadline(message):
    """ Выбираем предмет, у которого надо отредактировать дедлайн """
    global help_list
    help_list.clear()
    help_list.append(message.text)
    worksheet, b, df = access_current_sheet()
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for el in df.columns[2:]:
        start_markup.row(el)
    info = bot.send_message(message.chat.id, "Для какой лабораторной добавляем?", reply_markup=start_markup)
    bot.register_next_step_handler(info, add_subject_deadline1)


def add_subject_deadline2(message):
    global help_list
    sms = message.text.split()[0]
    if sms == "Вернуться":
        start(message)
    elif not convert_date(message.text):
        info = bot.send_message(message.chat.id,
                                emoji.emojize("Откуда вялись эти непонятные цифры :flushed_face: ?\n"
                                "Загляни-ка в календарь и введи НОРМАЛЬНУЮ дату в НОРМАЛЬНОМ формате\n\nПодсказываю: 'dd.mm.yyyy'", variant="emoji_type"))
        bot.register_next_step_handler(info, add_subject_deadline2)

    else:
        if convert_date(message.text) < datetime.today():
            info = bot.send_message(message.chat.id,
                                    emoji.emojize("Смысла вносить этот дедлайн нет, только если ты не научилась путешествовать в прошлое.\n\n" 
                                           "Введи нормальную дату в формате 'dd.mm.yyyy', а то смысла оставаться здесь у меня нет :confused_face:", variant="emoji_type"))
            bot.register_next_step_handler(info, add_subject_deadline2)
        else:
            worksheet, b, df = access_current_sheet()
            row = worksheet.find(help_list[0]).row
            col = worksheet.find(help_list[1]).col
            worksheet.update_cell(row, col, message.text)
            bot.send_message(message.chat.id, emoji.emojize("Добавлено! :check_mark_button:", variant="emoji_type"))
            start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            start_markup.row(emoji.emojize("Спасибо! Это все :smiling_face_with_hearts:", variant="emoji_type"))
            start_markup.row(emoji.emojize("Вернуться в начало :BACK_arrow:", variant="emoji_type"))
            info = bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=start_markup)
            bot.register_next_step_handler(info, finish_work)


def update_subject_deadline(message):
    """ Обновляем дедлайн """
    global help_list
    help_list.clear()
    help_list.append(message.text)
    worksheet, b, df = access_current_sheet()
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for el in df.columns[2:]:
        start_markup.row(el)
    info = bot.send_message(message.chat.id, "Для какой лабораторной изменяем?", reply_markup=start_markup)
    bot.register_next_step_handler(info, update_subject_deadline2)


def update_subject_deadline2(message):
    global help_list
    help_list.append(message.text)
    worksheet, b, df = access_current_sheet()
    row = worksheet.find(help_list[0]).row
    col = worksheet.find(help_list[1]).col
    if worksheet.cell(row, col).value:
        inf = bot.send_message(message.chat.id, "Введи дату в формате 'dd.mm.yyyy'")
        bot.register_next_step_handler(inf, update_subject_deadline3)
    else:
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Да")
        start_markup.row("Нет")
        info = bot.send_message(message.chat.id,
                                f"Дедлайна для этой лабы еще нет!\nДобавить его?",
                                reply_markup=start_markup)
        bot.register_next_step_handler(info, add_or_change2)


def update_subject_deadline3(message):
    global help_list
    sms = message.text.split()[0]
    if sms == "Вернуться":
        start(message)
    elif not convert_date(message.text):
        info = bot.send_message(message.chat.id, emoji.emojize("Откуда вялись эти непонятные цифры :flushed_face: ?\n"
                                "Загляни-ка в календарь и введи НОРМАЛЬНУЮ дату в НОРМАЛЬНОМ формате\n\nПодсказываю: 'dd.mm.yyyy'", variant="emoji_type"))
        bot.register_next_step_handler(info, update_subject_deadline3)

    else:
        if convert_date(message.text) < datetime.today():
            info = bot.send_message(message.chat.id,
                             emoji.emojize("Смысла вносить этот дедлайн нет, только если ты не научилась путешествовать в прошлое.\n\n" 
                                           "Введи нормальную дату в формате 'dd.mm.yyyy', а то смысла оставаться здесь у меня нет :confused_face:", variant="emoji_type"))
            bot.register_next_step_handler(info, update_subject_deadline3)
        else:
            worksheet, b, df = access_current_sheet()
            row = worksheet.find(help_list[0]).row
            col = worksheet.find(help_list[1]).col
            worksheet.update_cell(row, col, message.text)
            bot.send_message(message.chat.id, emoji.emojize("Изменено! :check_mark_button:", variant="emoji_type"))
            start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            start_markup.row(emoji.emojize("Спасибо! Это все :smiling_face_with_hearts:", variant="emoji_type"))
            start_markup.row(emoji.emojize("Вернуться в начало :BACK_arrow:", variant="emoji_type"))
            info = bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=start_markup)
            bot.register_next_step_handler(info, finish_work)


def delete_subject_deadline(message):
    """ Обновляем дедлайн """
    global help_list
    help_list.clear()
    help_list.append(message.text)
    worksheet, b, df = access_current_sheet()
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for el in df.columns[2:]:
        start_markup.row(el)
    info = bot.send_message(message.chat.id, "У какой лабораторной удаляем дедлайн?", reply_markup=start_markup)
    bot.register_next_step_handler(info, delete_subject_deadline2)


def delete_subject_deadline2(message):
    global help_list
    help_list.append(message.text)
    worksheet, b, df = access_current_sheet()
    row = worksheet.find(f"{help_list[0]}").row
    col = worksheet.find(f"{help_list[1]}").col
    if not worksheet.cell(row, col).value:
        bot.send_message(message.chat.id, emoji.emojize("А нечего удалять... \nУ этой лабы еще нет дедлайна :grimacing_face:", variant="emoji_type"))
    else:
        worksheet.update_cell(row, col, "")
        bot.send_message(message.chat.id, emoji.emojize("Удалено! :cross_mark:", variant="emoji_type"))
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row(emoji.emojize("Спасибо! Это все :smiling_face_with_hearts:", variant="emoji_type"))
    start_markup.row(emoji.emojize("Вернуться в начало :BACK_arrow:", variant="emoji_type"))
    info = bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=start_markup)
    bot.register_next_step_handler(info, finish_work)


def add_new_subject_and_url(message):
    """ Вносим новое название предмета в Google-таблицу """
    try:
        name = message.text.split()[0]
        url = message.text.split()[1]
        if name == "В" and url == "начало":
            start(message)
        elif not validators.url(url):
            info = bot.send_message(message.chat.id,
                                    emoji.emojize("Кажется, что-то не так с ссылкой на ведомость :thinking_face: "
                                                  "\nМожеть, снова отправишь название предмета и корректную ссылку?", variant="emoji_type"))
            bot.register_next_step_handler(info, add_new_subject_and_url)
        else:
            worksheet, b, df = access_current_sheet()
            worksheet.append_row([name, url])
            bot.send_message(message.chat.id, emoji.emojize("Добавлено! :check_mark_button:", variant="emoji_type"))
            start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            start_markup.row(emoji.emojize("Спасибо! Это все :smiling_face_with_hearts:", variant="emoji_type"))
            start_markup.row(emoji.emojize("Вернуться в начало :BACK_arrow:", variant="emoji_type"))
            info = bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=start_markup)
            bot.register_next_step_handler(info, finish_work)
    except IndexError:
        info = bot.send_message(message.chat.id,
                                emoji.emojize("Ошибочка вышла...:face_with_hand_over_mouth:"
                                "\nНазвание и ссылка должны быть отправлены одним сообщением через пробел!", variant="emoji_type"))
        bot.register_next_step_handler(info, add_new_subject_and_url)


def update_subject(message):
    """ Обновляем информацию о предмете в Google-таблице """
    global help_list
    help_list.clear()
    help_list.append(message.text)
    info = bot.send_message(message.chat.id,
                            emoji.emojize("Отправь название предмета и ссылку на ведомость через пробел."
                            " Если что-то из этого не должно изменяться, просто напиши его заново :smiling_face_with_open_hands:", variant="emoji_type"))
    bot.register_next_step_handler(info, update_subject2)


def update_subject2(message):
    global help_list
    try:
        name = message.text.split()[0]
        url = message.text.split()[1]
        if name == "В" and url == "начало":
            start(message)
        elif not validators.url(url):
            info = bot.send_message(message.chat.id,
                                    emoji.emojize("Кажется, что-то не так с ссылкой на ведомость :thinking_face: "
                                                  "\nМожет, снова отправишь название предмета и корректную ссылку?", variant="emoji_type"))
            bot.register_next_step_handler(info, update_subject2)
        else:
            worksheet, b, df = access_current_sheet()
            ind = df.loc[df.isin(help_list).any(axis=1)].index[0] + 2
            cell_list = worksheet.range(f'A{ind}:B{ind}')
            cell_list[0].value = name
            cell_list[1].value = url
            worksheet.update_cells(cell_list)
            bot.send_message(message.chat.id, emoji.emojize("Изменено! :check_mark_button:", variant="emoji_type"))
            start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            start_markup.row(emoji.emojize("Спасибо! Это все :smiling_face_with_hearts:", variant="emoji_type"))
            start_markup.row(emoji.emojize("Вернуться в начало :BACK_arrow:", variant="emoji_type"))
            info = bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=start_markup)
            bot.register_next_step_handler(info, finish_work)
    except IndexError:
        info = bot.send_message(message.chat.id,
                                emoji.emojize("Ошибочка вышла...:face_with_hand_over_mouth:"
                                "\nНазвание и ссылка должны быть отправлены одним сообщением через пробел!", variant="emoji_type"))
        bot.register_next_step_handler(info, update_subject2)


def delete_subject(message):
    """ Удаляем предмет в Google-таблице """
    worksheet, b, df = access_current_sheet()
    index = df.loc[df.isin([message.text]).any(axis=1)].index[0] + 2
    worksheet.delete_rows(int(index), int(index))
    bot.send_message(message.chat.id, emoji.emojize("Удалено! :cross_mark:", variant="emoji_type"))
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row(emoji.emojize("Спасибо! Это все :smiling_face_with_hearts:", variant="emoji_type"))
    start_markup.row(emoji.emojize("Вернуться в начало :BACK_arrow:", variant="emoji_type"))
    info = bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=start_markup)
    bot.register_next_step_handler(info, finish_work)


def clear_subject_list(message):
    """ Удаляем все из Google-таблицы """
    with open("tables.json") as json_file:
        tables = json.load(json_file)
    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    sh.del_worksheet(worksheet)
    bot.send_message(message.chat.id, emoji.emojize("Удалено! :cross_mark:", variant="emoji_type"))
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row(emoji.emojize("Спасибо! Это все :smiling_face_with_hearts:", variant="emoji_type"))
    start_markup.row(emoji.emojize("Вернуться в начало :BACK_arrow:", variant="emoji_type"))
    info = bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=start_markup)
    bot.register_next_step_handler(info, finish_work)


@bot.message_handler(content_types=["text"])
def privet(message):
    if message.text == "Привет":
        bot.send_message(message.chat.id, emoji.emojize("Привет! :waving_hand:\nУзнай свои баллы, дедлайны или снеси к чертям все лабы:collision:", variant="emoji_type"))
        start(message)


def vedomosti(message):
    markup = telebot.types.InlineKeyboardMarkup()
    worksheet, b, df = access_current_sheet()
    for i in df.index:
        button1 = telebot.types.InlineKeyboardButton(df.loc[i, 'subject'], url=df.loc[i, 'link'])
        markup.add(button1)
    bot.send_message(message.chat.id, "Твои ведомости:", reply_markup=markup)


def start(message):
    global help_list
    help_list.clear()
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    if not os.path.exists("tables.json"):
        start_markup.row("Подключить Google-таблицу")

    start_markup.row(emoji.emojize("Узнать свои баллы :bookmark_tabs:", variant="emoji_type"))
    start_markup.row(emoji.emojize("Посмотреть дедлайны на этой неделе :calendar:", variant="emoji_type"))
    start_markup.row(emoji.emojize("Изменить дедлайны :pencil:", variant="emoji_type"))
    start_markup.row(emoji.emojize("Редактировать предметы :pencil:", variant="emoji_type"))

    info = bot.send_message(message.chat.id, "Ты хочешь ...", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)


def finish_work(message):
    if message.text == "Вернуться в начало" or message.text == emoji.emojize("Вернуться в начало :BACK_arrow:", variant="emoji_type"):
        start(message)
    elif message.text == "Спасибо! Это все)" or message.text == emoji.emojize("Спасибо! Это все :smiling_face_with_hearts:", variant="emoji_type"):
        bot.send_message(message.chat.id, emoji.emojize("Удачи с лабами! :red_heart:", variant="emoji_type"))


if __name__ == "__main__":
    bot.infinity_polling()
