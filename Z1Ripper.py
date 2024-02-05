import os
import time
import shutil
import ctypes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Fore, Style, init
import keyboard
from plyer import notification
import threading

init(autoreset=True)

ctypes.windll.kernel32.SetConsoleTitleW("| Z1 Ripper |")

class AvatarHandler(FileSystemEventHandler):
    def __init__(self):
        self.avatar_count = 0
        self.searching_enabled = False

    def on_created(self, event):
        if self.searching_enabled and event.is_directory:
            current_time = time.strftime(
                f"{Fore.BLUE}{time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
            message = f"{Fore.MAGENTA}[{current_time}{Fore.MAGENTA}] Avatar Found !"
            print(message)
            new_folder_path = os.path.join(vrchat_folder_path, event.src_path)
            self.avatar_count += 1
            destination_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), f"Avatar {self.avatar_count}")
            while os.path.exists(destination_path):
                self.avatar_count += 1
                destination_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), f"Avatar {self.avatar_count}")
            try:
                shutil.copytree(new_folder_path, destination_path, ignore=shutil.ignore_patterns("__lock"))
                self.process_avatar(destination_path)
                self.notify_avatar_found()
            except shutil.Error as e:
                pass

    def process_avatar(self, avatar_folder):
        subdirectories = [d for d in os.listdir(avatar_folder) if os.path.isdir(os.path.join(avatar_folder, d))]
        if len(subdirectories) == 1:
            subdirectory_path = os.path.join(avatar_folder, subdirectories[0])
            self.read_data_file(subdirectory_path)

    def read_data_file(self, subdirectory_path):
        data_file_path = os.path.join(subdirectory_path, "__data")
        if os.path.exists(data_file_path):
            with open(data_file_path, 'r', encoding='utf-8', errors='ignore') as data_file:
                data_content = data_file.read()
                avatar_id = self.extract_avatar_id(data_content)
                if avatar_id:
                    self.create_avatar_id_file(subdirectory_path, avatar_id)


    def extract_avatar_id(self, data_content):
        import re
        match = re.search(r'avtr_([a-zA-Z0-9-]+)', data_content)
        if match:
            return match.group(1)
        return None

    def create_avatar_id_file(self, avatar_folder, avatar_id):
        id_file_path = os.path.join(avatar_folder, "avatar_id.txt")
        with open(id_file_path, 'w') as id_file:
            id_file.write(f"Avatar ID: {avatar_id}\n")
            id_file.write(f"Avatar URL: https://vrchat.com/home/avatar/{avatar_id}")

    def notify_avatar_found(self):
        notification_title = "Z1 Ripper"
        notification_description = "Avatar Found!"
        notification.notify(
            title=notification_title,
            message=notification_description,
            app_name="Z1 Ripper"
        )

def get_vrchat_folder_path():
    home_directory = os.path.expanduser("~")
    vrchat_folder_path = os.path.join(home_directory, 'AppData', 'LocalLow', 'VRChat', 'VRChat', 'Cache-WindowsPlayer')
    return vrchat_folder_path

def toggle_searching():
    event_handler.searching_enabled = not event_handler.searching_enabled
    status = "On" if event_handler.searching_enabled else "Off"
    notification_title = "Z1 Ripper"
    notification_description = f"Searching Toggled {status}"
    notification.notify(
        title=notification_title,
        message=notification_description,
        app_name="Z1 Ripper"
    )

vrchat_folder_path = get_vrchat_folder_path()

if os.path.exists(vrchat_folder_path):
    print(f"{Fore.BLUE}Press 'q' to toggle searching for avatars.")
    
    event_handler = AvatarHandler()  
    
    keyboard.add_hotkey('q', toggle_searching)

    observer = Observer()
    observer.schedule(event_handler, path=vrchat_folder_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join() 
else:
    print("VRChat folder not found. Please check the installation path.")
