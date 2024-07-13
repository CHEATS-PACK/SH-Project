import subprocess
import threading
import psutil
import requests
from pypresence import Presence
from pynput.keyboard import Key, Listener
from pymem import *
import ctypes
import time
import os
from colorama import init, Fore, Style

def show_warning_massage():
    ctypes.windll.user32.MessageBoxW(0,
                                     "ВНИМАНИЕ! Перед использованием Hitbox настоятельно рекомендую использовать 8 Java.",
                                     "SH-Project", 0x1000)


CLIENT_ID = 'your_client_id_here'  # Замените 'your_client_id_here' на ваш ID приложения из Discord Developer Portal

def create_default_config():
    config_path = "C:/SH-Prod/config.txt"  # Путь к файлу конфигурации
    if not os.path.exists(config_path):
        with open(config_path, "w") as file:
            file.write("discordrpc: on\n")


if not os.path.exists("C:/SH-Prod/config.txt"):
    create_default_config()


# Функция для чтения значения Discord RPC из файла конфигурации
def read_discord_rpc_config():
    create_default_config()  # Создать файл конфигурации с настройками по умолчанию, если он не существует
    with open("C:/SH-Prod/config.txt", "r") as file:
        for line in file:
            if line.strip() == "discordrpc: on":
                return True
            elif line.strip() == "discordrpc: off":
                return False
    return False


# Переменная для хранения состояния Discord RPC
discord_rpc_enabled = read_discord_rpc_config()


# Функция для проверки файла конфигурации и обновления значения Discord RPC
def check_config_and_update():
    global discord_rpc_enabled
    while True:
        discord_rpc_enabled = read_discord_rpc_config()
        time.sleep(1.5)


# Запуск потока для проверки файла конфигурации и обновления значения Discord RPC
config_thread = threading.Thread(target=check_config_and_update)
config_thread.daemon = True
config_thread.start()


# Функция для включения/выключения Discord RPC
def toggle_discord_rpc(enabled):
    global discord_rpc
    if enabled:
        # Включаем Discord RPC
        if is_discord_running():
            discord_rpc = DiscordRPC(CLIENT_ID)
            print(Fore.BLACK + "Discord RPC запущен." + Style.RESET_ALL)
    else:
        # Выключаем Discord RPC
        if discord_rpc:
            discord_rpc.shutdown()
        discord_rpc = None
        print(Fore.BLACK + "Discord RPC выключен." + Style.RESET_ALL)


def is_discord_running():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'Discord.exe':
            return True
    return False


class DiscordRPC:
    def __init__(self, client_id):
        self.client_id = client_id
        self.rpc = Presence(client_id)
        self.rpc.connect()
        self.state = "[SH-RPC] Запуск..."  # Начальное состояние
        self.details = "Лучший помощник для Minecraft"  # Начальные подробности
        self.large_image = "sh_1_"
        self.large_text = "Wt5u9NnWfN"
        self.small_image = "123"
        self.small_text = "123"
        self.buttons = [
            {"label": "Скачать", "url": "https://discord.gg/P4zJujagHG"},
            {"label": "Disocrd", "url": "https://discord.gg/TgEa5nc3qF"}
        ]
        self.running = True
        self.update_thread = threading.Thread(target=self.update_presence)
        self.update_thread.daemon = True  # Позволяет завершить поток при завершении программы
        self.update_thread.start()

    def update_presence(self):
        while self.running:
            self.rpc.update(
                state=self.state,
                details=self.details,
                large_image=self.large_image,
                large_text=self.large_text,
                small_image=self.small_image,
                small_text=self.small_text,
                buttons=self.buttons
            )
            time.sleep(1)

    def set_state(self, new_state):
        self.state = new_state

    def set_details(self, new_details):
        self.details = new_details

    def set_large_image(self, new_large_image):
        self.large_image = new_large_image

    def set_large_text(self, new_large_text):
        self.large_text = new_large_text

    def set_small_image(self, new_small_image):
        self.small_image = new_small_image

    def set_small_text(self, new_small_text):
        self.small_text = new_small_text

    def shutdown(self):
        self.running = False
        self.update_thread.join()
        self.rpc.close()


def init_discord_rpc():
    global discord_rpc
    if discord_rpc_enabled and is_discord_running():
        discord_rpc = DiscordRPC(CLIENT_ID)
        print(Fore.BLACK + "Discord RPC запущен." + Style.RESET_ALL)
    else:
        discord_rpc = None
        print(Fore.BLACK + "Discord RPC выключен." + Style.RESET_ALL)


# Запуск функции инициализации Discord RPC
init_discord_rpc()


def animate_title(title):
    while True:
        for i in range(len(title)):
            ctypes.windll.kernel32.SetConsoleTitleW(title[:i + 1])
            time.sleep(0.1)
        for i in range(len(title), 0, -1):
            ctypes.windll.kernel32.SetConsoleTitleW(title[:i])
            time.sleep(0.1)


response = requests.get("") #тут поставьте ссылку на ваш version.txt
if response.status_code == 200:
    version = response.text.strip()
else:
    version = "Unknown"
title = f"SH-Project | {version}"

thread = threading.Thread(target=animate_title, args=(title,))
thread.daemon = True  # Установка флага daemon для потока
thread.start()

def check_java_process():
    # проверяем, запущен ли процесс javaw.exe
    if os.system("tasklist | findstr javaw.exe") == 0:
        print("Java process is running")
    else:
        print("Java process is not running")
        time.sleep(5)
        exit(0)

def download_vec_dll():
    url = "" #тут поставьте ссылку на ваш vec.dll
    file_path = "C:\\Windows\\vec.dll"
    if not os.path.exists(file_path):
        response = requests.get(url, stream=True)
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print("vec.dll downloaded successfully")
    else:
        print("vec.dll already exists")


def start_notepad():
    try:
        subprocess.run(["notepad.exe"], check=True)
        print("Notepad.exe запущен успешно")
    except subprocess.CalledProcessError as e:
        print(f"Не удалось запустить Notepad.exe: {e}")


def inject_externaldllhb():
    try:
        # Запуск InjectExternalHitbox.exe
        subprocess.run(["C:\\SH-Prod\\loader\\InjectExternalHitbox.exe"], check=True)
        print("InjectExternalHitbox.exe запущен успешно")
    except subprocess.CalledProcessError as e:
        print(f"Не удалось запустить InjectExternalHitbox.exe: {e}")
    input("Press Enter to continue...")


def inject_dlldefault():
    try:
        # Запуск InjectHitboxDLL.exe
        subprocess.run(["C:\\SH-Prod\\loader\\InjectHitboxDLL.exe"], check=True)
        print("InjectHitboxDLL.exe запущен успешно")
    except subprocess.CalledProcessError as e:
        print(f"Не удалось запустить InjectHitboxDLL.exe: {e}")
    input("Press Enter to continue...")


def download_dlldefault():
    dll_name = "systemly.dll"
    dll_path = f"C:\\Windows\\{dll_name}"
    # проверяем, скачен ли файл
    if os.path.exists(dll_path):
        print(f"Файл {dll_name} уже скачен")
    else:
        # скачиваем DLL-файл
        url = f"https://example.com/dll/{dll_name}" # Замените на свой домен на скачивание systemly.exe
        response = requests.get(url)
        if response.status_code == 200:
            with open(dll_path, "wb") as f:
                f.write(response.content)
            print(f"Файл {dll_name} скачен успешно в {dll_path}")
        else:
            print("Ошибка: не удалось скачать DLL-файл")
            os._exit(1)  # закрытие программы с ошибкой

logo = r"""
  /$$$$$$  /$$   /$$         /$$$$$$$  /$$$$$$$   /$$$$$$     /$$$$$ /$$$$$$$$  /$$$$$$  /$$$$$$$$
 /$$__  $$| $$  | $$        | $$__  $$| $$__  $$ /$$__  $$   |__  $$| $$_____/ /$$__  $$|__  $$__/
| $$  \__/| $$  | $$        | $$  \ $$| $$  \ $$| $$  \ $$      | $$| $$      | $$  \__/   | $$   
|  $$$$$$ | $$$$$$$$ /$$$$$$| $$$$$$$/| $$$$$$$/| $$  | $$      | $$| $$$$$   | $$         | $$   
 \____  $$| $$__  $$|______/| $$____/ | $$__  $$| $$  | $$ /$$  | $$| $$__/   | $$         | $$   
 /$$  \ $$| $$  | $$        | $$      | $$  \ $$| $$  | $$| $$  | $$| $$      | $$    $$   | $$   
|  $$$$$$/| $$  | $$        | $$      | $$  | $$|  $$$$$$/|  $$$$$$/| $$$$$$$$|  $$$$$$/   | $$   
 \______/ |__/  |__/        |__/      |__/  |__/ \______/  \______/ |________/ \______/    |__/                                                                      
"""

os.system("cls")
print(logo)
print(
    Fore.GREEN + "Добро пожаловать! Нажми " + Fore.CYAN + "Enter" + Fore.GREEN + " чтобы продолжить..." + Style.RESET_ALL)
input()  # ожидаем нажатия Enter

if discord_rpc_enabled and discord_rpc:
    discord_rpc.set_state("[SH-RPC] Основное меню")
discord_rpc_status = "On" if discord_rpc_enabled else "Off"
main_points = ["| 1. External HitBox ", "| 2. Default Hitbox ", " ", "| 3. Exit",
               f"| 4. Discord RPC ({discord_rpc_status})"]
settings_subpoints = [""]
current_point = 0
in_submenu = False
submenu_index = 0

def print_menu():
    os.system('cls')
    print(logo)
    if in_submenu:
        points = settings_subpoints
    else:
        points = main_points

    for i, point in enumerate(points):
        if not in_submenu and i == current_point:
            if i == 0:
                print(
                    f" {Fore.LIGHTGREEN_EX}{point}{Style.RESET_ALL} {Fore.YELLOW}<<{Style.RESET_ALL} {Fore.GREEN}Vanilla{Style.RESET_ALL}, {Fore.GREEN}Forge{Style.RESET_ALL}, {Fore.GREEN}ForgeOptifine{Style.RESET_ALL}, {Fore.GREEN}Optifine{Style.RESET_ALL}, {Fore.RED}Fabric{Style.RESET_ALL}, {Fore.GREEN}LabyMod3{Style.RESET_ALL}, {Fore.RED}Lunar{Style.RESET_ALL}, {Fore.RED}Labymod4{Style.RESET_ALL}")
            elif i == 1:
                print(
                    f" {Fore.LIGHTGREEN_EX}{point}{Style.RESET_ALL} {Fore.YELLOW}<<{Style.RESET_ALL} {Fore.GREEN}Vanilla{Style.RESET_ALL}, {Fore.GREEN}Forge{Style.RESET_ALL}, {Fore.GREEN}ForgeOptifine{Style.RESET_ALL}, {Fore.RED}Optifine{Style.RESET_ALL}, {Fore.RED}Fabric{Style.RESET_ALL}, {Fore.GREEN}LabyMod3{Style.RESET_ALL}, {Fore.RED}Lunar{Style.RESET_ALL}, {Fore.RED}Labymod4{Style.RESET_ALL}")
            else:
                print(f" {Fore.LIGHTGREEN_EX}{point}{Style.RESET_ALL} {Fore.YELLOW}<<{Style.RESET_ALL}")
        elif in_submenu and i == submenu_index:
            print(f" {Fore.LIGHTGREEN_EX}{point}{Style.RESET_ALL} {Fore.YELLOW}<<{Style.RESET_ALL}")
        else:
            print(f" {Fore.BLACK}{point}{Style.RESET_ALL}")

def on_press(key):
    global current_point, in_submenu, submenu_index
    try:
        if not in_submenu:
            if key == Key.up:
                current_point = max(0, current_point - 1)
                while not main_points[current_point].strip() and current_point > 0:
                    current_point -= 1
            elif key == Key.down:
                current_point = min(len(main_points) - 1, current_point + 1)
                while not main_points[current_point].strip() and current_point < len(main_points) - 1:
                    current_point += 1
            elif key == Key.enter:
                if current_point == 0:  # External HitBox
                    if discord_rpc_enabled and discord_rpc:
                        discord_rpc.set_state("[SH-RPC] Запуск External HitBox")
                        time.sleep(1.5)
                    show_warning_massage()
                    check_java_process()
                    download_vec_dll()
                    start_notepad()
                    time.sleep(1.5)
                    inject_externaldllhb()
                    if discord_rpc_enabled and discord_rpc:
                        discord_rpc.set_state("[SH-RPC] Использует External HitBox")
                    time.sleep(5)
                    os.exit(1)
                elif current_point == 1:  # Default Hitbox
                    if discord_rpc_enabled and discord_rpc:
                        discord_rpc.set_state("[SH-RPC] Запуск Default HitBox")
                        time.sleep(3)
                    show_warning_massage()
                    check_java_process()
                    download_vec_dll()
                    time.sleep(1.5)
                    inject_dlldefault()
                    if discord_rpc_enabled and discord_rpc:
                        discord_rpc.set_state("[SH-RPC] Использует Default HitBox")
                    time.sleep(5)
                    os.exit(1)
                elif current_point == 3:  # Exit
                    if discord_rpc_enabled and discord_rpc:
                        discord_rpc.set_state("[SH-RPC] Выход... Bye bye!")
                    print(Fore.RED)
                    os.system('cls')
                    print(logo)
                    print("  Выход...")
                    time.sleep(5)
                    os._exit(0)
                elif current_point == 4:  # Управление Discord RPC через меню
                    toggle_discord_rpc_setting()
        else:
            if key == Key.up:
                submenu_index = max(0, submenu_index - 1)
            elif key == Key.down:
                submenu_index = min(len(settings_subpoints) - 1, submenu_index + 1)
            elif key == Key.left and submenu_index == 0:
                in_submenu = False
            elif key == Key.enter:
                # Обработка выбора подменю
                pass

    except AttributeError:
        pass
    print_menu()

def on_release(key):
    if key == Key.esc:
        return False


print_menu()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Функция для обновления текста меню в зависимости от значения Discord RPC
def update_menu_text():
    global points
    discord_rpc_status = "On" if discord_rpc_enabled else "Off"
    points[5] = f"| 4. Discord RPC ({discord_rpc_status})"


# Обновление текста меню при запуске программы
update_menu_text()


def toggle_discord_rpc_setting():
    global discord_rpc_enabled
    discord_rpc_enabled = not discord_rpc_enabled
    write_discord_rpc_config(discord_rpc_enabled)
    toggle_discord_rpc(discord_rpc_enabled)
    update_menu_text()  # Обновляем текст меню
    print_menu()  # Обновляем меню после изменения настройки


def write_discord_rpc_config(enabled):
    config_path = "C:/SH-Prod/config.txt"  # Путь к файлу конфигурации
    with open(config_path, "w") as file:
        file.write(f"discordrpc: {'on' if enabled else 'off'}\n")


def check_java_process_not8java():
    # проверяем, запущен ли процесс javaw.exe
    if os.system("tasklist | findstr javaw.exe") == 0:
        print("Java process is running")
    else:
        print("Java process is not running")
        time.sleep(5)
        exit(0)
