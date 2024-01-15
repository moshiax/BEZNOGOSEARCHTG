import configparser
import random
import string
from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact
import time
from telethon.errors.rpcerrorlist import FloodWaitError

config = configparser.ConfigParser()
config.read("config.ini")

api_id = int(config['Telegram']['api_id'])
api_hash = config['Telegram']['api_hash']
phone = config['Telegram']['phone']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

while True:
    try:
        operator_code = random.choice(['39', '50', '63', '66', '67', '68', '73', '89', '91', '92', '93', '94', '95', '96', '97', '98', '99'])
        random_part = ''.join(random.choice(string.digits) for _ in range(7))
        phone_num = f'+380{operator_code}{random_part}'

        first_name = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        last_name = ''.join(random.choice(string.ascii_letters) for _ in range(10))

        with open('added_numbers.txt', 'r') as file:
            existing_numbers = file.readlines()
            if phone_num + '\n' in existing_numbers:
                print(f"Skipped existing number: {phone_num}")
                continue

        contact = InputPhoneContact(client_id=0, phone=phone_num, first_name=first_name, last_name=last_name)
        result = client(ImportContactsRequest([contact]))
        print(f"Added contact with random name: {first_name} {last_name}, phone: {phone_num}")
        
        print(result)

        with open('added_numbers.txt', 'a') as file:
            file.write(phone_num + '\n')

    except FloodWaitError as e:
        # Обработка ошибки FloodWaitError
        print(f"FloodWaitError: Waiting for {e.seconds} seconds. Restarting in {e.seconds + 1} seconds...")
        remaining_seconds = e.seconds
        while remaining_seconds > 0:
            print(f"Time remaining: {remaining_seconds} seconds", end='\r')
            time.sleep(1)
            remaining_seconds -= 1

        print("Restarting...")

    except Exception as e:
        print(f"Error occurred: {e}")
        print("Restarting in 300 seconds...")
        time.sleep(300)
