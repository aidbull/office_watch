from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, Updater, Filters
from telegram.utils.request import Request
from data_base import get_photo_from_office


button_help = 'Что там в офисе?'


def button_help_handler(update: Update, context: CallbackContext, bot: Bot):
    print('Got to button_help_handler')
    time, temperature, humidity, filename = get_photo_from_office()
    text = 'Время: {}\nТемпература: {}\nВлажность: {}\n'.format(time, temperature, humidity),
    chat_id = update.message.chat_id
    print(text, chat_id)
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_help),
            ],
        ],
        resize_keyboard=True,
    )
    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
    )

    bot.send_photo(chat_id=chat_id, photo=open(filename, 'rb'))

# Telegram UID для RBAC 
list_of_chat_id = []


def message_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    print('chat_id: ', chat_id)

    if chat_id in list_of_chat_id:
        print('chat_id in the list')
        text = update.message.text
        print(text)
        if text == button_help:
            print('text = button_help')
            return button_help_handler(update=update, context=context)

        reply_markup = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=button_help),
                ],
            ],
            resize_keyboard=True,
        )

        time, temperature, humidity, filename = get_photo_from_office()
        text = 'Время: {}\nТемпература: {}\nВлажность: {}\n'.format(time, temperature, humidity),
        update.message.reply_text(
            text=text,
            reply_markup=reply_markup,
        )


    else:
        update.message.reply_text(
            text='Goodbye',
        )

def main():
    print('Start')

    req = Request(
        connect_timeout=0.5,
    )

    bot = Bot(
        request=req,
        token='',
    )

    updater = Updater(
        bot=bot,
        use_context=True,
    )

    print(updater.bot.get_me())
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))

    updater.start_polling()
    updater.idle()

    print('Finish')


if __name__ == '__main__':
    main()