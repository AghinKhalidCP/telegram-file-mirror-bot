import logging

import telegram

from telegram.ext import Updater, MessageHandler, Filters

import requests

import io

import google.auth

from googleapiclient.discovery import build

from googleapiclient.errors import HttpError

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Replace with your own bot token obtained from BotFather

TOKEN = "5197936130:AAFchiMdLgrQvnJ0xxBpw2WoFV9wfxIEW6c"

# Replace with the ID of your Google Drive folder where files will be mirrored

FOLDER_ID = "10JP1RrfVqSm0F76_6idaf61tlaUI-z2_"

# Use google.auth.default() to obtain credentials for the default account

creds = google.auth.default()[0]

# Build the Google Drive API client

drive_service = build('drive', 'v3', credentials=creds)

def mirror(update, context):

    message = update.message

    file = message.document

    file_id = file.file_id

    file_info = context.bot.get_file(file_id)

    file = requests.get(file_info.file_path)

    file_stream = io.BytesIO(file.content)

    file_metadata = {'name': file.document.file_name, 'parents': [FOLDER_ID]}

    file = drive_service.files().create(body=file_metadata, media_body=file_stream, fields='id').execute()

    context.bot.send_message(chat_id=message.chat_id, text="File has been mirrored to Google Drive: https://drive.google.com/file/d/{}".format(file['id']))

def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.document, mirror))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()

