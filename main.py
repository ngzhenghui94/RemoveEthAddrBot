#!/usr/bin/env python
# pylint: disable=C0116,W0613
import os
import re
import logging
from dotenv import load_dotenv
from telegram import Update, ParseMode
from telegram.ext import (
    Updater,
    Filters,
    CallbackContext,
    MessageHandler,
)

load_dotenv()
bot_token = os.getenv('TOKEN')
get_admins = os.getenv('ADMINS')

# Set the Bot's mode. In 'Admin' mode, the bot will delete messages that contains an Ethereum address.
# In 'Warn' mode, the bot will warn users that are posting an Ethereum address.
mode = "Administrate"


# Enable localized logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def doesMsgContainEthAddr(text):
    x = re.findall("0x[a-fA-F0-9]{40}", text)
    return bool(x)


def moderate(update: Update, context: CallbackContext):
    print(update.message)
    if not update.message.text:
        return
    elif doesMsgContainEthAddr(update.message.text):
        update.message.reply_text(
            text="@{} Posting of Ethereum Addresses is not allowed to protect users in this group from scammers.".format(
                update.message.from_user.username),
            parse_mode=ParseMode.MARKDOWN)
        if mode == "Administrate":
            context.bot.delete_message(
                chat_id=update.message.chat_id, message_id=update.message.message_id)

        return


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(bot_token)
    dp = updater.dispatcher

    # Listen for messages and moderate them.
    dp.add_handler(MessageHandler(Filters.text, moderate))

    # Send all errors to the logger.
    dp.add_error_handler(error)

    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
