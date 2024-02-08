import os
import time
import requests
import fade
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Fore, Style
import re

class NewFolderEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            print("[ + ] New folder created:", event.src_path)
            time.sleep(5)
            process_new_folder(event.src_path)

def process_new_folder(folder_path):
    subfolders = next(os.walk(folder_path))[1]
    if len(subfolders) == 1:
        subfolder_path = os.path.join(folder_path, subfolders[0])
        data_file_path = os.path.join(subfolder_path, "__data")
        if os.path.exists(data_file_path):
            avatar_id = extract_avatar_id(data_file_path)
            if avatar_id:
                script_folder = os.getcwd()
                new_folder_path = os.path.join(script_folder, avatar_id)
                os.makedirs(new_folder_path, exist_ok=True)
                shutil.copy(data_file_path, os.path.join(new_folder_path, "Avatar.vrca"))
                print("[ + ] Avatar folder created and data file copied:", new_folder_path)
            else:
                print("[ - ] Failed to extract avatar ID from data file")
        else:
            print("[ - ] Data file '__data' not found in subfolder")
    else:
        print("[ - ] Expected exactly one subfolder, found:", len(subfolders))

def extract_avatar_id(data_file_path):
    try:
        with open(data_file_path, 'rb') as file:
            data_content = file.read()
            match = re.search(b'avtr_([a-zA-Z0-9-]+)_\d+', data_content)
            if match:
                avatar_id = match.group(1).decode('utf-8')
                return f"avtr_{avatar_id}"
            return None
    except Exception as e:
        print(f"[ - ] Error reading data file: {e}")
        return None
    
def copy_folder(folder_path):
    script_folder = os.getcwd()
    destination_folder = os.path.join(script_folder, os.path.basename(folder_path))
    try:
        shutil.copytree(folder_path, destination_folder)
        avatar_id = extract_avatar_id(destination_folder)
        if avatar_id:
            new_folder_name = os.path.join(os.path.dirname(destination_folder), avatar_id)
            os.rename(destination_folder, new_folder_name)
            print("[ + ] Avatar Ripped and renamed to:", new_folder_name)
        else:
            current_time = time.strftime('%Y-%m-%d_%H-%M-%S')
            new_folder_name = os.path.join(os.path.dirname(destination_folder), f"Avatar_{current_time}")
            os.rename(destination_folder, new_folder_name)
            print("[ - ] Failed to extract avatar ID, folder renamed to:", new_folder_name)
    except Exception as e:
        print("[ - ] Failed to copy folder:", e)

def get_vrchat_folder_path():
    home_directory = os.path.expanduser("~")
    vrchat_folder_path = os.path.join(home_directory, 'AppData', 'LocalLow', 'VRChat', 'VRChat', 'Cache-WindowsPlayer')
    return vrchat_folder_path

def monitor_folder(folder_path):
    event_handler = NewFolderEventHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def display_menu():
    clear_screen()
    text = """
       @@@@@@@@    @@@     @@@@@@@   @@@  @@@@@@@   @@@@@@@   @@@@@@@@  @@@@@@@   
       @@@@@@@@   @@@@     @@@@@@@@  @@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  
            @@!  @@@!!     @@!  @@@  @@!  @@!  @@@  @@!  @@@  @@!       @@!  @@@  
           !@!     !@!     !@!  @!@  !@!  !@!  @!@  !@!  @!@  !@!       !@!  @!@  
          @!!      @!@     @!@!!@!   !!@  @!@@!@!   @!@@!@!   @!!!:!    @!@!!@!   
         !!!       !@!     !!@!@!    !!!  !!@!!!    !!@!!!    !!!!!:    !!@!@!    
        !!:        !!:     !!: :!!   !!:  !!:       !!:       !!:       !!: :!!   
       :!:         :!:     :!:  !:!  :!:  :!:       :!:       :!:       :!:  !:!  
        :: ::::    :::     ::   :::   ::   ::        ::        :: ::::  ::   :::  
       : :: : :     ::      :   : :   :     :         :        : :: ::    :   : :                                               
    """
    faded_text = fade.purplepink(text)
    print(faded_text)

    online_version = fetch_version()
    if online_version:
        local_version = read_local_version()
        if local_version == online_version:
            Menu = f"""                               Active Version: {local_version}
                             -=======================-
                             | Online Searcher [1]   |
                             | Local Searcher  (2)   |
                             -=======================-"""
            faded_text = fade.purplepink(Menu)
            print(faded_text)
            option = input("[ + ] ")
            if option == "1":
                clear_screen()
                vrchat_folder_path = get_vrchat_folder_path()
                if vrchat_folder_path:
                    print("[ + ] VRChat found. Please turn on avatars now.")
                    monitor_folder(vrchat_folder_path)
                else:
                    print("[ - ] VRChat folder not found")
        else:
            print("Active Version: Outdated - Go to GitHub for new update")

def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def fetch_version():
    url = "https://raw.githubusercontent.com/Z3o2/Z1-Ripper/main/Misc/Version.txt"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            print("[ - ] Failed to fetch version from GitHub.")
            return None
    except Exception as e:
        print("[ - ] Failed to fetch version from GitHub:", e)
        return None

def read_local_version():
    folder_path = "misc"
    file_path = os.path.join(folder_path, "Version.txt")
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read().strip()
        else:
            print("[ - ] Local version file not found.")
            return None
    except Exception as e:
        print("[ - ] Error reading local version file:", e)
        return None

def main():
    display_menu()

if __name__ == "__main__":
    main()
