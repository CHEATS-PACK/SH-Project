import threading
import psutil
import requests
from pynput import keyboard
import webbrowser
from pymem import *
import ctypes
import time
import os
from colorama import init, Fore, Style

def animate_title(title):
    while True:
        for i in range(len(title)):
            ctypes.windll.kernel32.SetConsoleTitleW(title[:i + 1])
            time.sleep(0.1)
        for i in range(len(title), 0, -1):
            ctypes.windll.kernel32.SetConsoleTitleW(title[:i])
            time.sleep(0.1)

response = requests.get("https://cheats-pack.github.io/repohidezz/shproject/version.txt")
if response.status_code == 200:
    version = response.text.strip()
else:
    version = "Unknown"
title = f"SH-Project | {version}"

thread = threading.Thread(target=animate_title, args=(title,))
thread.daemon = True  # Установка флага daemon для потока
thread.start()


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

# Список пунктов
points = ["| 1. External HitBox (Recommend)", "| 2. DLL Hitbox (Maybe Work)", "| 3. Exit",
          "| 4. Clear DLL For Minecraft (Maybe Work for 2 point)"]
current_point = 0

os.system('cls')
print(logo)
for i, point in enumerate(points):
    if i == current_point:
        print(f" {Fore.GREEN}{point}{Style.RESET_ALL} {Fore.YELLOW}<<{Style.RESET_ALL}")
    else:
        print(f" {Fore.BLACK}{point}{Style.RESET_ALL}")


def on_press(key):
    global current_point
    global points
    try:
        if key == keyboard.Key.up:
            current_point = max(0, current_point - 1)
        elif key == keyboard.Key.down:
            current_point = min(len(points) - 1, current_point + 1)
        elif key == keyboard.Key.enter:
            if current_point == 0:  # External HitBox
                check_java_process()
                download_vec_dll()
                inject_explorer()
                show_success_message()
                os._exit(0)  # закрытие программы
            elif current_point == 1:  # DLL Hitbox (Default)
                check_java_process()
                download_dlldefault()
                inject_dlldefault()
                show_success_message_default()
                os._exit(0)  # закрытие программы
            elif current_point == 2:  # Выход
                print(Fore.RED)  # изменяем цвет текста на красный
                os.system('cls')
                print(logo)
                print("  Выход...")
                time.sleep(1)
                os._exit(0)  # закрытие программы
            elif current_point == 3:  # Clear DLL For Minecraft
                check_java_process()
                clear_dll_from_javaw()

    except AttributeError:
        pass
    os.system('cls')
    print(Style.RESET_ALL)  # сбрасываем цвет текста
    print(logo)
    for i, point in enumerate(points):
        if i == current_point:
            print(f" {Fore.GREEN}{point}{Style.RESET_ALL} {Fore.YELLOW}<<{Style.RESET_ALL}")
        else:
            print(f" {Fore.BLACK}{point}{Style.RESET_ALL}")


def check_java_process():
    # проверяем, запущен ли процесс javaw.exe
    if os.system("tasklist | findstr javaw.exe") == 0:
        print("Java process is running")
    else:
        print("Java process is not running")
        time.sleep(3)
        exit(0)


def download_vec_dll():
    # скачиваем vec.dll с ссылки cheats-pack.ru/vec.dll
    url = "https://cheats-pack.ru/vec.dll"
    file_path = "C:\\Windows\\vec.dll"
    if not os.path.exists(file_path):
        response = requests.get(url, stream=True)
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print("vec.dll downloaded successfully")
    else:
        print("vec.dll already exists")


def inject_dll(process_id, dll_path):
    h_process = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, process_id)
    if h_process == 0:
        print(f"OpenProcess failed: {ctypes.GetLastError()}")
        return False

    dll_path_unicode = dll_path.encode('utf-16le')
    p_lib_remote = ctypes.windll.kernel32.VirtualAllocEx(h_process, None, len(dll_path_unicode), 0x1000, 0x4)
    if p_lib_remote == 0:
        print(f"VirtualAllocEx failed: {ctypes.GetLastError()}")
        ctypes.windll.kernel32.CloseHandle(h_process)
        return False

    if not ctypes.windll.kernel32.WriteProcessMemory(h_process, p_lib_remote, dll_path_unicode, len(dll_path_unicode),
                                                     None):
        print(f"WriteProcessMemory failed: {ctypes.GetLastError()}")
        ctypes.windll.kernel32.VirtualFreeEx(h_process, p_lib_remote, 0, 0x8000)
        ctypes.windll.kernel32.CloseHandle(h_process)
        return False

    h_thread = ctypes.windll.kernel32.CreateRemoteThread(h_process, None, 0, ctypes.windll.kernel32.LoadLibraryW,
                                                         p_lib_remote, 0, None)
    if h_thread == 0:
        print(f"CreateRemoteThread failed: {ctypes.GetLastError()}")
        ctypes.windll.kernel32.VirtualFreeEx(h_process, p_lib_remote, 0, 0x8000)
        ctypes.windll.kernel32.CloseHandle(h_process)
        return False

    ctypes.windll.kernel32.WaitForSingleObject(h_thread, -1)
    ctypes.windll.kernel32.VirtualFreeEx(h_process, p_lib_remote, 0, 0x8000)
    ctypes.windll.kernel32.CloseHandle(h_thread)
    ctypes.windll.kernel32.CloseHandle(h_process)
    return True


def inject_explorer():
    dll_path = "C:\\Windows\\vec.dll"
    os.system("start explorer.exe")  # запускаем explorer.exe
    time.sleep(2)  # ждем 2 секунды, чтобы explorer.exe запустился
    explorer_pid = None
    for i in range(10):  # пытаемся найти процесс explorer.exe 10 раз
        for proc in psutil.process_iter():
            if proc.name() == "explorer.exe":
                explorer_pid = proc.pid
                break
        if explorer_pid is not None:
            break
        time.sleep(0.5)  # ждем 0.5 секунды перед следующей попыткой
    if explorer_pid is not None:
        if inject_dll(explorer_pid, dll_path):
            print("vec.dll injected successfully")
        else:
            print("Failed to inject vec.dll")
    else:
        print("explorer.exe not found")
    input("Press Enter to continue...")


def show_success_message():
    # показываем окно с текстом "Успешно!"
    ctypes.windll.user32.MessageBoxW(0,
                                     "Привет, твои HitBox успешно работают! Для того чтобы их выключить, надо зайти в диспечер задач и там найти задачу explorer.exe и перезагрузить ее. Спасибо!",
                                     "SH-Project", 0x1000)


def inject_dlldefault():
    dll_path = "C:\\Windows\\systemly.dll"
    process_name = "javaw.exe"

    # Получаем список процессов
    process_list = []
    for proc in psutil.process_iter(['pid', 'name']):
        info = proc.info
        process_list.append((info['pid'], info['name']))

    # Ищем процесс по имени
    process_id = None
    for pid, name in process_list:
        if name == process_name:
            process_id = pid
            break

    if process_id is None:
        print(f"Процесс {process_name} не найден")
        return

    # Открываем процесс javaw.exe
    h_process = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, process_id)
    if h_process == 0:
        print(f"OpenProcess failed: {ctypes.GetLastError()}")
        return

    # Алокируем память в processo для DLL-файла
    dll_path_unicode = dll_path.encode('utf-16le')
    p_lib_remote = ctypes.windll.kernel32.VirtualAllocEx(h_process, None, len(dll_path_unicode), 0x1000, 0x4)
    if p_lib_remote == 0:
        print(f"VirtualAllocEx failed: {ctypes.GetLastError()}")
        ctypes.windll.kernel32.CloseHandle(h_process)
        return

    # Копируем DLL-файл в память процесса
    if not ctypes.windll.kernel32.WriteProcessMemory(h_process, p_lib_remote, dll_path_unicode, len(dll_path_unicode),
                                                     None):
        print(f"WriteProcessMemory failed: {ctypes.GetLastError()}")
        ctypes.windll.kernel32.VirtualFreeEx(h_process, p_lib_remote, 0, 0x8000)
        ctypes.windll.kernel32.CloseHandle(h_process)
        return

    # Создаем новый поток в processo для инъекции DLL-файла
    h_thread = ctypes.windll.kernel32.CreateRemoteThread(h_process, None, 0, ctypes.windll.kernel32.LoadLibraryW,
                                                         p_lib_remote, 0, None)
    if h_thread == 0:
        print(f"CreateRemoteThread failed: {ctypes.GetLastError()}")
        ctypes.windll.kernel32.VirtualFreeEx(h_process, p_lib_remote, 0, 0x8000)
        ctypes.windll.kernel32.CloseHandle(h_process)
        return

    # Ждем завершения потока
    ctypes.windll.kernel32.WaitForSingleObject(h_thread, -1)
    ctypes.windll.kernel32.VirtualFreeEx(h_process, p_lib_remote, 0, 0x8000)
    ctypes.windll.kernel32.CloseHandle(h_thread)
    ctypes.windll.kernel32.CloseHandle(h_process)
    print("DLL-файл успешно инжектирован в процесс javaw.exe")


def download_dlldefault():
    dll_name = "systemly.dll"
    dll_path = f"C:\\Windows\\{dll_name}"
    # проверяем, скачен ли файл
    if os.path.exists(dll_path):
        print(f"Файл {dll_name} уже скачен")
    else:
        # скачиваем DLL-файл
        url = f"https://cheats-pack.ru/{dll_name}"
        response = requests.get(url)
        if response.status_code == 200:
            with open(dll_path, "wb") as f:
                f.write(response.content)
            print(f"Файл {dll_name} скачен успешно в {dll_path}")
        else:
            print("Ошибка: не удалось скачать DLL-файл")
            os._exit(1)  # закрытие программы с ошибкой


def show_success_message_default():
    # показываем окно с текстом "Успешно!"
    ctypes.windll.user32.MessageBoxW(0,
                                     "Привет, твои HitBox успешно работают! Для того чтобы из выклбючить, нажми кнопку на клавиатуре 'DEL' или 'DELETE'. Спасибо!",
                                     "SH-Project", 0x1000)


def clear_dll_from_javaw():
    dll_name = "systemly.dll"
    process_name = "javaw.exe"

    # Получаем список процессов
    process_list = []
    for proc in psutil.process_iter(['pid', 'name']):
        info = proc.info
        process_list.append((info['pid'], info['name']))

    # Ищем процесс по имени
    process_id = None
    for pid, name in process_list:
        if name == process_name:
            process_id = pid
            break

    if process_id is None:
        print(f"Процесс {process_name} не найден")
        return

    # Открываем процесс javaw.exe
    h_process = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, process_id)
    if h_process == 0:
        print(f"OpenProcess failed: {ctypes.GetLastError()}")
        return

    # Ищем строку "systemly.dll" в памяти процесса
    dll_name_unicode = dll_name.encode('utf-16le')
    buffer_size = len(dll_name_unicode)
    buffer = ctypes.create_string_buffer(buffer_size)
    ctypes.windll.kernel32.ReadProcessMemory(h_process, ctypes.c_void_p(0x10000000), buffer, buffer_size, None)

    # Удаляем строку "systemly.dll" из памяти процесса
    ctypes.windll.kernel32.WriteProcessMemory(h_process, ctypes.c_void_p(0x10000000), ctypes.c_char_p(b""), buffer_size,
                                              None)

    print(f"Строка {dll_name} успешно удалена из процесса {process_name}")


def show_success_message_deldll():
    # показываем окно с текстом "Успешно!"
    ctypes.windll.user32.MessageBoxW(0,
                                     "Привет, твои HitBox успешно работают! Для того чтобы их выключить, надо зайти в диспечер задач и там найти задачу explorer.exe и перезагрузить ее. Спасибо!",
                                     "SH-Project", 0x1000)


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
