import configparser
import random
import string
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError
import time

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
        phone_num = f'+79873702564'

        with open('numid.txt', 'r') as file:
            existing_entries = file.readlines()
            if any(phone_num in entry for entry in existing_entries):
                print(f"Skipped existing phone: {phone_num}")
                time.sleep(2) 
                continue

        with open('noid.txt', 'r') as file:
            no_id_entries = file.readlines()
            if any(phone_num in entry for entry in no_id_entries):
                print(f"Skipped phone with no id: {phone_num}")
                time.sleep(2)  
                continue

        print(f"Generated phone: {phone_num}")

        try:
            result = client.get_entity(phone_num)
            if result:
                user_id = result.id
                print(f"User found with ID: {user_id}")
                with open('numid.txt', 'a') as file:
                    file.write(f"{phone_num} - {user_id}\n")

            else:
                print(f"User not found for phone: {phone_num}")
                with open('noid.txt', 'a') as file:
                    file.write(phone_num + '\n')

        except FloodWaitError as e:
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
