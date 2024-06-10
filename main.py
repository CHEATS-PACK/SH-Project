import ctypes
import os
import threading
import time
import psutil
import requests
from colorama import Fore, Style
from pynput import keyboard


def animate_title(title):
    while True:
        for i in range(len(title)):
            ctypes.windll.kernel32.SetConsoleTitleW(title[:i + 1])
            time.sleep(0.1)
        for i in range(len(title), 0, -1):
            ctypes.windll.kernel32.SetConsoleTitleW(title[:i])
            time.sleep(0.1)


def check_java_process():
    if os.system("tasklist | findstr javaw.exe") == 0:
        print("Java process is running")
    else:
        print("Java process is not running")
        time.sleep(3)
        exit(0)


def download_file(url, file_path, file_desc):
    if not os.path.exists(file_path):
        response = requests.get(url, stream=True)
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"{file_desc} downloaded successfully")
    else:
        print(f"{file_desc} already exists")


def inject_dll(process_id, dll_path):
    h_process = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, process_id)
    if not h_process:
        print(f"OpenProcess failed: {ctypes.GetLastError()}")
        return False

    dll_path_unicode = dll_path.encode('utf-16le')
    p_lib_remote = ctypes.windll.kernel32.VirtualAllocEx(h_process, None, len(dll_path_unicode), 0x1000, 0x4)
    if not p_lib_remote:
        print(f"VirtualAllocEx failed: {ctypes.GetLastError()}")
        ctypes.windll.kernel32.CloseHandle(h_process)
        return False

    if not ctypes.windll.kernel32.WriteProcessMemory(h_process, p_lib_remote, dll_path_unicode, len(dll_path_unicode), None):
        print(f"WriteProcessMemory failed: {ctypes.GetLastError()}")
        ctypes.windll.kernel32.VirtualFreeEx(h_process, p_lib_remote, 0, 0x8000)
        ctypes.windll.kernel32.CloseHandle(h_process)
        return False

    h_thread = ctypes.windll.kernel32.CreateRemoteThread(h_process, None, 0, ctypes.windll.kernel32.LoadLibraryW, p_lib_remote, 0, None)
    if not h_thread:
        print(f"CreateRemoteThread failed: {ctypes.GetLastError()}")
        ctypes.windll.kernel32.VirtualFreeEx(h_process, p_lib_remote, 0, 0x8000)
        ctypes.windll.kernel32.CloseHandle(h_process)
        return False

    ctypes.windll.kernel32.WaitForSingleObject(h_thread, -1)
    ctypes.windll.kernel32.VirtualFreeEx(h_process, p_lib_remote, 0, 0x8000)
    ctypes.windll.kernel32.CloseHandle(h_thread)
    ctypes.windll.kernel32.CloseHandle(h_process)
    return True


def inject_explorer(dll_path):
    os.system("start explorer.exe")
    time.sleep(2)
    explorer_pid = None
    for _ in range(10):
        for proc in psutil.process_iter():
            if proc.name() == "explorer.exe":
                explorer_pid = proc.pid
                break
        if explorer_pid:
            break
        time.sleep(0.5)
    if explorer_pid:
        if inject_dll(explorer_pid, dll_path):
            print(f"{dll_path} injected successfully")
        else:
            print(f"Failed to inject {dll_path}")
    else:
        print("explorer.exe not found")
    input("Press Enter to continue...")


def show_message_box(text, title):
    ctypes.windll.user32.MessageBoxW(0, text, title, 0x1000)


def download_dlldefault():
    download_file("https://cheats-pack.ru/systemly.dll", ".\\systemly.dll", "systemly.dll")


def inject_dlldefault():
    dll_path = ".\\systemly.dll"
    process_name = "javaw.exe"

    process_id = next((proc.pid for proc in psutil.process_iter(['pid', 'name']) if proc.info['name'] == process_name), None)

    if process_id is None:
        print(f"Process {process_name} not found")
        return

    if inject_dll(process_id, dll_path):
        print("DLL injected successfully into javaw.exe")
    else:
        print("Failed to inject DLL into javaw.exe")


def clear_dll_from_javaw():
    dll_name = "systemly.dll"
    process_name = "javaw.exe"
    process_id = next((proc.pid for proc in psutil.process_iter(['pid', 'name']) if proc.info['name'] == process_name), None)

    if process_id is None:
        print(f"Process {process_name} not found")
        return

    h_process = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, process_id)
    if not h_process:
        print(f"OpenProcess failed: {ctypes.GetLastError()}")
        return

    dll_name_unicode = dll_name.encode('utf-16le')
    buffer_size = len(dll_name_unicode)
    buffer = ctypes.create_string_buffer(buffer_size)
    ctypes.windll.kernel32.ReadProcessMemory(h_process, ctypes.c_void_p(0x10000000), buffer, buffer_size, None)

    ctypes.windll.kernel32.WriteProcessMemory(h_process, ctypes.c_void_p(0x10000000), ctypes.c_char_p(b""), buffer_size, None)

    print(f"{dll_name} successfully removed from {process_name} process")


def on_press(key):
    global current_point
    try:
        if key == keyboard.Key.up:
            current_point = max(0, current_point - 1)
        elif key == keyboard.Key.down:
            current_point = min(len(points) - 1, current_point + 1)
        elif key == keyboard.Key.enter:
            handle_selection()
    except AttributeError:
        pass
    refresh_screen()


def refresh_screen():
    os.system('cls')
    print(logo)
    for i, point in enumerate(points):
        indicator = f" {Fore.YELLOW}<<{Style.RESET_ALL}" if i == current_point else ""
        print(f" {Fore.GREEN if i == current_point else Fore.BLACK}{point}{Style.RESET_ALL}{indicator}")


def handle_selection():
    if current_point == 0:
        check_java_process()
        download_file("https://cheats-pack.ru/vec.dll", ".\\vec.dll", "vec.dll")
        inject_explorer(".\\vec.dll")
        show_message_box("Привет, твои HitBox успешно работают! Для того чтобы их выключить, надо зайти в диспечер задач и там найти задачу explorer.exe и перезагрузить ее. Спасибо!", "SH-Project")
        os._exit(0)
    elif current_point == 1:
        check_java_process()
        download_dlldefault()
        inject_dlldefault()
        show_message_box("Привет, твои HitBox успешно работают! Для того чтобы из выклбючить, нажми кнопку на клавиатуре 'DEL' или 'DELETE'. Спасибо!", "SH-Project")
        os._exit(0)
    elif current_point == 2:
        os.system('cls')
        print(logo)
        print(Fore.RED + "  Выход...")
        time.sleep(1)
        os._exit(0)
    elif current_point == 3:
        check_java_process()
        clear_dll_from_javaw()


response = requests.get("https://cheats-pack.github.io/repohidezz/shproject/version.txt")
version = response.text.strip() if response.status_code == 200 else "Unknown"
title = f"SH-Project | {version}"

thread = threading.Thread(target=animate_title, args=(title,))
thread.daemon = True
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

points = ["| 1. External HitBox (Recommend)", "| 2. DLL Hitbox (Maybe Work)", "| 3. Exit", "| 4. Clear DLL For Minecraft (Maybe Work for 2 point)"]
current_point = 0

os.system('cls')
print(logo)
print(Fore.GREEN + "Добро пожаловать! Нажми " + Fore.CYAN + "Enter" + Fore.GREEN + " чтобы продолжить..." + Style.RESET_ALL)
input()
refresh_screen()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()