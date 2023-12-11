from telebot import types

from config import bot, emoji_digit, tg_profile_link, vk_profile_link, denied_strings


# преобразование числа в символы
def num_to_emoji(current_number):
    digit_to_emoji = ''
    for digit in range(len(str(current_number))):
        digit_to_emoji += emoji_digit[int(str(current_number)[digit])]
    return digit_to_emoji


def links_from_start():
    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.row(types.InlineKeyboardButton(text='🔗 Telegram', url=tg_profile_link),
                      types.InlineKeyboardButton(text='🔗 VK', url=vk_profile_link))
    markup_inline.add(types.InlineKeyboardButton(text='🔙 Назад', callback_data='back_to_start'))
    return markup_inline


# форма с кнопками ссылок
def links_without_button_back():
    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.row(types.InlineKeyboardButton(text='🔗 Telegram', url=tg_profile_link),
                      types.InlineKeyboardButton(text='🔗 VK', url=vk_profile_link))
    # markup_inline.add(types.InlineKeyboardButton(text='🏠 На главную', callback_data='back_to_start'))
    return markup_inline


# уведомление пользователя о возникшей ошибке при обработке запроса
def error_from_user(message, error_code=None):
    bot.reply_to(message=message,
                 text='Ошибка!\n\nКод ошибки: ' + str(error_code) + '\n\nДля продолжения работы с ботом воспользуйтесь командами (например, /start).\n\nСсылки для обратной связи:',
                 parse_mode='html',
                 reply_markup=links_without_button_back())


# удаление ReplyMarkup при перенаправлении на какую-либо страницу
def delete_reply_markup(message, text_hint='Перенаправление...'):
    chat_id = message.chat.id

    delete_keyboard_markup = types.ReplyKeyboardRemove()
    msg = bot.send_message(chat_id=chat_id,
                           text=f'⏳ {text_hint}',
                           reply_markup=delete_keyboard_markup)
    bot.delete_message(chat_id=chat_id,
                       message_id=msg.message_id)


def info_to_chat(message, info=None, split_method=None):
    chat_id = message.chat.id

    if len(info) > 4000:
        pages_count = int(len(info) / 4000) + 1
        list_info = info.strip().split(str(split_method))
        info = ''
        current_page = 1
        for current_cadet in range(len(list_info)):
            if len(info + list_info[current_cadet]) < 4000:
                info += list_info[current_cadet] + str(split_method)
            else:
                bot.send_message(chat_id=chat_id,
                                 text=f'{info}\n'
                                      f''
                                      f'(часть {current_page} из {pages_count})',
                                 parse_mode='html')
                current_page += 1
                info = list_info[current_cadet] + str(split_method)
        if info:
            bot.send_message(chat_id=chat_id,
                             text=f'{info}\n'
                                  f''
                                  f''
                                  f'(часть {current_page} из {pages_count})',
                             parse_mode='html')
    else:
        bot.send_message(chat_id=chat_id,
                         text=info,
                         parse_mode='html')


def is_right_string(input_string):
    value = True
    if len(input_string) > 40:
        value = False
    else:
        for current_string in denied_strings:
            if current_string in input_string:
                value = False
                break
    return value


def role_from_db_to_text(current_role, process_index=1):
    if process_index == 1:
        if current_role == 'officer':
            return 'Офицер'
        if current_role == 'helper':
            return 'Помощник'
        if current_role == 'cadet':
            return 'Курсант'
        if current_role == 'guest':
            return 'Гость'
    elif process_index == 2:
        if current_role == 'Офицер':
            return 'officer'
        if current_role == 'Помощник':
            return 'helper'
        if current_role == 'Курсант':
            return 'cadet'
        if current_role == 'Гость':
            return 'guest'
