import configparser
from telethon.sync import TelegramClient, functions
import time
from faker import Faker

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
    client.sign_in(phone, input('Enter the code:'))

async def search_channels(client, search_query):
    try:
        result = await client(functions.contacts.SearchRequest(
            q=search_query,
            limit=100
        ))
        filtered_results = [
            f"Channel: {channel.title}, Participants: {channel.participants_count}\n"
            for channel in result.chats
            if getattr(channel, 'participants_count', 0) > 0
        ]
        return ''.join(filtered_results)
    except Exception as e:
        print(f"Error during channel search: {e}")
        return "Error during channel search."

def save_to_file(filename, data):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(data)

def generate_random_word():
    fake = Faker(['ru_RU'])
    return fake.word()

while True:
    try:
        search_query = generate_random_word()
        channels_file = "channels.txt"
        prompted_file = "prompted.txt"

        with open(prompted_file, 'r', encoding='utf-8') as prompted_file_content:
            prompted_words = prompted_file_content.read().splitlines()
            if search_query in prompted_words:
                print(f"Word '{search_query}' is already prompted. Skipping...")
                time.sleep(1)
                continue

        save_to_file(prompted_file, f"{search_query}\n")

        output_text = client.loop.run_until_complete(search_channels(client, search_query))

        print("\n========== Channel Search Results ==========")
        print(output_text)

        if output_text.strip():
            save_to_file(channels_file, f"\n========== Search Query: {search_query} ==========\n")
            save_to_file(channels_file, output_text)

        time.sleep(1)

    except Exception as e:
        print(f"Error occurred: {e}")
        print("Restarting in 300 seconds...")
        time.sleep(300)
