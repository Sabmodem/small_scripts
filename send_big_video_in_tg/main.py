from telethon import TelegramClient
import sys
import os

bot_name = os.environ.get('BOT_NAME')
session_name = os.environ.get('SESSION_NAME')
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')

filename = sys.argv[1]
filepath = os.path.join(config.filesdir, filename)

with TelegramClient(session_name, api_id, api_hash) as client:
      client.loop.run_until_complete(client.send_file(bot_name, filepath))
