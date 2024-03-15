from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext, \
    Application, ContextTypes, Defaults
from texts import hello_message, instructions_dict, instruction_text, buttons, handle_photo_thanks_text, \
    handle_photo_all_letters, handle_photo_wrong_photo, notification_text, wrong_time, news_letter
import random
import pandas as pd
import numpy as np
from datetime import time, timedelta, datetime, timezone
import logging
import os

USER_DATA_PATH = "/data/users_data.csv" if "AMVERA" in os.environ else "users_data.csv"
LOGG_PATH = "/data/temp.log" if "AMVERA" in os.environ else "temp.log"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename=LOGG_PATH
                    )

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

waiting_for_photo = False
moscow_tz = timezone(offset=timedelta(hours=3), name='UTC+3')
dactyl = ["А", "Б", "В", "Г", "Е",
          "Ж", "И", "К", "Л", "М",
          "Н", "О", "П", "Р", "С",
          "Т", "У", "Ф", "Х", "Ч",
          "Ш", "Ы", "Э", "Ю", "Я"]


async def start(update: Update, context: CallbackContext) -> None:
    """
    Handle the /start command.

    Args:
        update (telegram.Update): The update object containing information about the incoming message.
        context (telegram.ext.CallbackContext): The context object for the current update.

    Returns:
        None
    """
    logging.info(f"User {update.effective_chat.id} is started conversation.") # все ок

    keyboard = [[KeyboardButton(buttons['send_photo']),
                 KeyboardButton(buttons['get_instructions'])]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=hello_message,
                                   reply_markup=reply_markup)


def get_info(chat_id):
    """
    Retrieve user information from a CSV file or create a new entry if the user is new.

    Args:
        chat_id (int): The ID of the chat/user.

    Returns:
        str: The current symbol associated with the user.
    """
    user_data = pd.read_csv(USER_DATA_PATH, sep=',', converters={'sended_symbols': pd.eval})
    current_sign = random.choice(dactyl)
    current_user = user_data[user_data['chat_id'] == chat_id]

    if chat_id in user_data['chat_id'].to_list():
        logging.info(f"The {chat_id} is an old user.")
        if not user_data[user_data['chat_id'] == chat_id].current_symbol.isna().all():
            logging.info(f"The {chat_id} already has a letter.")
            current_sign = ''.join(current_user.current_symbol.values)
        else:
            logging.info(f"The {chat_id} do not has a letter.")
            user_data.loc[user_data['chat_id'] == chat_id, 'current_symbol'] = current_sign

    else:
        logging.info(f"The {chat_id} is a new user.")
        new_row = pd.DataFrame([[chat_id, current_sign, list(), int(0)]],
                               columns=["chat_id", 'current_symbol', 'sended_symbols', 'sended_coeff'])
        user_data = pd.concat([user_data, new_row], ignore_index=True)
        logging.info(f"List of current_users: \n {user_data}")

    user_data.to_csv(USER_DATA_PATH, index=False, header=True)
    return current_sign


async def send_instructions(update: Update, context: CallbackContext) -> None:
    """
    Send instructions to the user upon request.

    Args:
        update (telegram.Update): The update object containing information about the incoming message.
        context (telegram.ext.CallbackContext): The context object for the current update.

    Returns:
        None
    """
    if buttons['get_instructions'] in update.message.text:
        await update.message.reply_text(instruction_text)


async def button_click(update: Update, context: CallbackContext) -> None:
    """
    Handle the 'Send Photo' button.

    Args:
        update (telegram.Update): The update object containing information about the incoming message.
        context (telegram.ext.CallbackContext): The context object for the current update.

    Returns:
        None
    """
    global waiting_for_photo
    chat_id = update.effective_chat.id
    current_sign = get_info(chat_id)

    if buttons['send_photo'] in update.message.text:
        waiting_for_photo = True

        message_text = (
            f"Вам попалась буква {current_sign}! "
            f"Инструкция: {instructions_dict[current_sign]}\n"
            "👍 Если вы готовы, сфотографируйте свою руку и отправьте фото в бот:)"
        )
        await update.message.reply_text(message_text)

        photo_path = f'example_images/{current_sign}.jpeg'
        await update.message.reply_photo(photo=open(photo_path, 'rb'))


async def handle_photo(update: Update, context: CallbackContext) -> None:
    """
    Handle the user sending a photo.

    Args:
        update (telegram.Update): The update object containing information about the incoming message.
        context (telegram.ext.CallbackContext): The context object for the current update.

    Returns:
        None
    """
    logging.info(f"Function handle_photo is started by user {update.effective_chat.id}")

    global waiting_for_photo

    user_id = update.effective_chat.id
    users_data = pd.read_csv(USER_DATA_PATH, sep=',', converters={'sended_symbols': pd.eval})
    current_user = users_data[users_data["chat_id"] == user_id]

    if waiting_for_photo:
        if update.message.photo:
            user_photo = update.message.photo[-1]
            file_id = user_photo.file_id
            new_file = await context.bot.get_file(file_id)
            current_sign = current_user['current_symbol'].values[0]

            path = f"/data/users_photo/{current_sign}/{user_id}_{file_id}.jpg" if "AMVERA" in os.environ \
                else f"users_photo/{current_sign}/{user_id}_{file_id}.jpg"
            await new_file.download_to_drive(custom_path=path)

            await update.message.reply_text(handle_photo_thanks_text)

            user_sended_signs = current_user.sended_symbols.values[0]
            user_sended_signs.append(*current_sign)
            users_data.loc[users_data['chat_id'] == user_id, 'sended_symbols'].values[0] = user_sended_signs

            # Пользователь отправил все символы
            if len(dactyl) == len(user_sended_signs):
                await context.bot.send_message(chat_id=update.effective_chat.id, text=handle_photo_all_letters)

                current_sign = np.nan

                users_data.loc[users_data['chat_id'] == user_id, 'sended_symbols'] = users_data.loc[
                    users_data['chat_id'] == user_id, 'sended_symbols'].apply(lambda x: [])
                users_data.loc[users_data['chat_id'] == user_id, 'sended_coeff'] += 1

            else:
                available_symbols = [sign for sign in dactyl if sign not in user_sended_signs]
                if available_symbols:
                    current_sign = random.choice(available_symbols)
                else:
                    current_sign = np.nan

            users_data.loc[users_data['chat_id'] == user_id, 'current_symbol'] = current_sign

        waiting_for_photo = False

    else:
        await update.message.reply_text(handle_photo_wrong_photo)

    users_data.to_csv(USER_DATA_PATH, index=False, header=True)


start_notification_text = "Отлично! Теперь вы будете ежедневно получать напоминания"


async def send_notification(context: CallbackContext) -> None:
    """
    Send a notification message as a scheduled job.
    """
    job = context.job
    logging.info(f"Notification alarm is active for {job.name}")
    await context.bot.send_message(job.name, text=notification_text)


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    my_timezone = context.bot.defaults.tzinfo
    try:
        # Split the input string by ":" and convert parts to integers
        hours, minutes = map(int, context.args[0].split(':'))
        given_time = time(hours, minutes, tzinfo=moscow_tz)
        datetime_obj = datetime.combine(datetime.min, given_time)
        updated_datetime_obj = datetime_obj
        updated_time = updated_datetime_obj.time()
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_daily(callback=send_notification, time=updated_time, name=str(chat_id))
        text = "Вы успешно установили напоминание!"
        if job_removed:
            text += " Старое напоминание удалено."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text(wrong_time)


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Вы успешно удалили напоминания!" if job_removed else "Активных напоминаний нет."
    await update.message.reply_text(text)


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([('start', 'Начните работу с ботом'),
                                           ('set', 'Установить напоминание'),
                                           ('unset', 'Удалить напоминание')])


async def secret_command(update: Update, context: CallbackContext) -> None:
    """
    Handle the /start command.

    Args:
        update (telegram.Update): The update object containing information about the incoming message.
        context (telegram.ext.CallbackContext): The context object for the current update.

    Returns:
        None
    """
    logging.info(f"News letter sended.")
    users_data = pd.read_csv(USER_DATA_PATH, sep=',',
                             converters={'sended_symbols': pd.eval})
    users_id = [int(i) for i in users_data['chat_id'].values]

    for chat_id in users_id:
        await context.bot.send_message(chat_id=chat_id,
                                       text=news_letter)


def main():
    defaults = Defaults(tzinfo=moscow_tz)

    application = Application.builder().token("6758202098:AAFQG4vmIRHIU0Q5zxiZUfe5w6Jx70KFc6U").post_init(
        post_init).defaults(defaults).build()

    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler(["secret_command"], secret_command))

    application.add_handler(MessageHandler(filters.Regex(r'Отправить фото'), button_click))
    application.add_handler(MessageHandler(filters.Regex(r'Получить инструкции'), send_instructions))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
