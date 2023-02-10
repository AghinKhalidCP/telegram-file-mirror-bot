import logging

import os

import telegram

from telegram import InputFile

from telegram.ext import Updater, CommandHandler

import google.auth

from googleapiclient.discovery import build

from googleapiclient.errors import HttpError

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Replace "TELEGRAM_BOT_TOKEN" with your bot's token

TOKEN = "TELEGRAM_BOT_TOKEN"

# Replace "GOOGLE_DRIVE_FOLDER_ID" with the ID of the Google Drive folder you want to mirror the files to

DRIVE_FOLDER_ID = "GOOGLE_DRIVE_FOLDER_ID"

def start(update, context):

    update.message.reply_text("Hi, it's me working perfectly")

def mirror_file(update, context):

    file_id = update.message.document.file_id

    file = context.bot.get_file(file_id)

    

    try:

        # Authenticate to Google Drive

        credentials, project = google.auth.default()

        drive_service = build('drive', 'v3', credentials=credentials)

        

        # Save the file to Google Drive

        file_metadata = {

            'name': update.message.document.file_name,

            'parents': [DRIVE_FOLDER_ID],

            'mimeType': update.message.document.mime_type

        }

        media = InputFile(file.download_as_bytearray(),

                          filename=update.message.document.file_name)

        drive_service.files().create(body=file_metadata, media_body=media,

                                     fields='id').execute()

        update.message.reply_text("File mirrored to Google Drive")

    except HttpError as error:

        update.message.reply_text(f"An error occurred while trying to mirror the file: {error}")

        logger.error(f"An error occurred while trying to mirror the file: {error}")

def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.document, mirror_file))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()

