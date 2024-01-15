import configparser
from telethon.sync import TelegramClient, events
from faker import Faker
import time

config = configparser.ConfigParser()
config.read("config.ini")

api_id = int(config['Telegram']['api_id'])
api_hash = config['Telegram']['api_hash']
phone = config['Telegram']['phone']
username = config['Telegram']['username']

def generate_random_word():
    fake = Faker(['ru_RU'])
    return fake.word()

bot_username = 'tgdb_bot'

while True:
    try:
        with TelegramClient(username, api_id, api_hash) as client:
            message_text = '/search ' + generate_random_word()

            bot_entity = client.get_entity(bot_username)

            client.send_message(bot_entity, message_text)

            @client.on(events.NewMessage(from_users=bot_entity))
            def handle_response(event):
                try:
                    if event.message.text:
                        print(f"Ответ от бота: {event.message.text}")
                    else:
                        print("Получен пустой текстовый ответ")
                except TypeError as e:
                    print(f"Ошибка обработки ответа от бота: {e}")


    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Unhandled exception: {e}")
        print("Restarting in 300 seconds...")
        time.sleep(10)
