from config import bot, telebot, OWNER_ID, CHAT_GROUP_ID
from db_func import *
from generate_buttons import generate_random_button

types = telebot.types
protected = False

# @bot.chat_join_request_handler()
@bot.message_handler(content_types=['new_chat_members'])
def join_user(message: types.Message):
    print(1)
    try:
        if select_capha_yesli_ne_reshil_caphu(message.from_user.id) != None:
            # bot.decline_chat_join_request(CHAT_GROUP_ID, message.from_user.id) # Отклоняем заявку в группу
            # bot.send_message(message, "❌ У вас таймер на час, ваша заявка отконена")
            bot.kick_chat_member(message.chat.id, message.from_user.id)
            return
            
        generate_random_button(4, message, f"❗ {message.from_user.first_name} Выбери правильный ответ, У вас есть 2 минуты на решение.\n Нажмите на  ")
    except Exception as e:
        log_error(e)


@bot.message_handler(content_types=['left_chat_member'])
def left_user(message: types.Message):
    print(1)
    delUserID_DB(message.from_user.id)
    try:
        del_capcha_timer(message.from_user.id)
    except: pass



@bot.callback_query_handler(func=lambda callback: callback.data)
def check(callback: types.CallbackQuery):
    print(callback.data)

    try:
        if len(callback.data) >= 3:
            if '_suc'  in callback.data:
                bot.edit_message_text(text='✅ Заявка одобрена', chat_id=callback.message.chat.id, message_id=callback.message.message_id, )
                message_id = callback.data.replace("_suc", "")
                message = selectPostID_DB(message_id)
                bot.send_message(chat_id=CHAT_GROUP_ID, text=f'Объявление от: {message[2]} \n\nТекст объявления: {message[0]}')
                delPostID_DB(message_id)
                return
            elif '_no' in callback.data:
                message_id = callback.data.replace("_no", "")
                bot.edit_message_text(text='❌ Заявка отклонена', chat_id=callback.message.chat.id, message_id=callback.message.message_id)
                delPostID_DB(message_id)
                
                return
            
        tuple_capha_date = select_capha_timer(callback.from_user.id) 
        print(tuple_capha_date)
        if callback.data == str(tuple_capha_date[2]) and callback.from_user.id == int(tuple_capha_date[0]):
            bot.send_message(callback.message.chat.id, '✅ Успешно пройдено')
            bot.delete_message(callback.message.chat.id, callback.message.message_id)
            addUserID_DB(callback.from_user.id)
            del_capcha_timer(int(tuple_capha_date[0]))
            # bot.approve_chat_join_request(CHAT_GROUP_ID, int(tuple_capha_date[0])) # Принимаем заявку в группу
        else:
            if callback.from_user.id == int(tuple_capha_date[0]):
                bot.delete_message(callback.message.chat.id, callback.message.message_id)
                # bot.send_message(callback.message.chat.id, '⛔️ Вы выбрали неправильный ответ ваша заявка отклонена')
                del_capcha_timer(int(tuple_capha_date[0])) # Удаляем из ожидания ввода капчи.
                # bot.decline_chat_join_request(CHAT_GROUP_ID, int(tuple_capha_date[0])) # Отклоняем заявку в группу
                bot.kick_chat_member(CHAT_GROUP_ID, tuple_capha_date[0])
                potoc_ne_reshil_caphu(callback.from_user.id)
            else:
                pass

    except Exception as e:
        log_error(e)
    

#==========================================================================================================================

@bot.message_handler(commands=['chatid'])
def protect(message: types.Message):
    try:
        bot.reply_to(message, f'{message.chat.id}')

    except Exception as e:
        log_error(e)

@bot.message_handler(commands=['protect'])
def protect(message: types.Message):
    try:
        global protected

        if message.from_user.id == OWNER_ID and not protected:
            bot.reply_to(message, f"✅ Проверка постов включена")
            protected = True

        elif message.from_user.id == OWNER_ID and protected:
            bot.reply_to(message, f"✅ Проверка постов выключена")
            protected = False

    except Exception as e:
        log_error(e)
    
@bot.message_handler(content_types=['photo'])
def check_message(message: types.Message):
    try:
        if selectUserID_DB(message.from_user.id) == None:
            bot.delete_message(message.chat.id, message.message_id)
            return
        if protected == True:
            if OWNER_ID == message.from_user.id:
                return
    except Exception as e:
        log_error(e)

@bot.message_handler(content_types=['file'])
def check_message(message: types.Message):
    try:
        if selectUserID_DB(message.from_user.id) == None:
            bot.delete_message(message.chat.id, message.message_id)
            return
        if protected == True:
            if OWNER_ID == message.from_user.id:
                return
    except Exception as e:
        log_error(e)

@bot.message_handler()
def check_message(message: types.Message):
    try:
        if selecttimer_DB(message.from_user.id) != None:
            bot.delete_message(message.chat.id, message.message_id)
            return
        if selectUserID_DB(message.from_user.id) == None:
            bot.delete_message(message.chat.id, message.message_id)
            return
        if protected == True:
            if OWNER_ID == message.from_user.id:
                return
            addPostID_DB(message.text, message.from_user.first_name, message.content_type, message.message_id)
            add_potoc_timer(message.from_user.id)

            keyboard = types.InlineKeyboardMarkup()

            button_suc = types.InlineKeyboardButton(text='✅', callback_data=f'{message.message_id}_suc')
            button_no = types.InlineKeyboardButton(text='❌', callback_data=f'{message.message_id}_no')

            keyboard.add(button_suc, button_no)

            bot.send_message(OWNER_ID, f"Пользователь: `{message.from_user.first_name}`, отправил объявление\. \nТекст объявления: `{message.text}`", reply_markup=keyboard, parse_mode='MarkdownV2')
            bot.delete_message(message.chat.id, message.message_id)

    except Exception as e:
        log_error(e) 

try:
    bot.infinity_polling()
except Exception as e:
        log_error(e)