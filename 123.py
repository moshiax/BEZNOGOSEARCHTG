import os
import configparser
import PySimpleGUI as sg
from telethon import TelegramClient, functions
import random
import hashlib
import winsound
import pyperclip

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
phone = config['Telegram']['phone']
username = config['Telegram']['username']

def play_random_sound():
    sound_files = ['1.wav', '2.wav', '3.wav', '4.wav', '5.wav', '6.wav']
    random_sound = random.choice(sound_files)
    
    winsound.PlaySound(random_sound, winsound.SND_FILENAME)

async def search_channels(client, search_query, max_participants):
    await client.start()
    try:
        result = await client(functions.contacts.SearchRequest(
            q=search_query,
            limit=100
        ))
        filtered_results = [f"{channel.title}, {channel.participants_count}\n" for channel in result.chats if getattr(channel, 'participants_count', 0) < max_participants]
        return ''.join(filtered_results)
    finally:
        await client.disconnect()

def authenticate(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    stored_hash = config.get('Security', 'PasswordHash', fallback='')

    if hashed_password == stored_hash:
        return TelegramClient(username, api_id, api_hash)
    else:
        play_random_sound()
        return None

def create_layout():
    image_path = os.path.join(os.path.dirname(__file__), 'beznogym.png')
    return [
        [
            sg.Column([
                [sg.Text("Введите пароль: "), sg.InputText(key='-PASSWORD-', password_char='*', size=(15, 1))],
                [sg.Text("Запрос поиска: ", text_color='white'), sg.InputText(key='-QUERY-', size=(20, 1))],
                [sg.Text("Количество участников:", text_color='white'), sg.InputText(key='-MAX_PARTICIPANTS-', size=(10, 1))],
                [sg.Multiline(size=(35, 10), key='-OUTPUT-', autoscroll=True, right_click_menu=['&Right', ['&Copy', '&Paste']],
                              background_color='black', text_color='white')],
                [
                    sg.Button('Поиск', button_color=('white', 'black')),
                    sg.Button('Выход', button_color=('white', 'black')),
                    sg.Button('Копировать', button_color=('white', 'black')),
                ],
            ]),
            sg.Column([
                [sg.Image(filename=image_path, size=(76, 250))],
            ]),
        ],
    ]

def main():
    sg.theme('Black') 
    layout = create_layout()
    window = sg.Window('BEZNOGOSEARCH', layout, finalize=True)
    
    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED or event == 'Выход':
            break
        elif event == 'Поиск':
            password = values['-PASSWORD-']
            client = authenticate(password)
            
            if client:
                search_query = values['-QUERY-']
                max_participants = int(values['-MAX_PARTICIPANTS-'])
                print("\n========== BEZNOGOSEARCH ==========")
                output_text = client.loop.run_until_complete(search_channels(client, search_query, max_participants))
                window['-OUTPUT-'].update(output_text) 
            else:
                sg.popup_error('Неправильна')

        elif event == 'Копировать':
            clipboard_text = window['-OUTPUT-'].get()  
            pyperclip.copy(clipboard_text)  # Обновление буфера обмена с помощью pyperclip  
    
    window.close()
    error_log.close()

if __name__ == '__main__':
    main()
