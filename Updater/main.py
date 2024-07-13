import ctypes
import os
import sys
import time
import requests
from colorama import init, Fore, Style

init()  # инициализируем Colorama

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

def download_file(url, local_path):
    response = requests.get(url, stream=True)
    with open(local_path, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
    print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + f" Файл {os.path.basename(local_path)} скачан и сохранен в {local_path}" + Style.RESET_ALL)

# Проверяем, существует ли папка SH-Prod на диске C
sh_prod_dir = 'C:\\SH-Prod'
if os.path.exists(sh_prod_dir):
    print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + " Папка SH-Prod уже существует на диске C" + Style.RESET_ALL)
else:
    os.makedirs(sh_prod_dir)
    print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + " Папка SH-Prod создана на диске C" + Style.RESET_ALL)

# Проверяем, существует ли папка loader внутри SH-Prod
loader_dir = os.path.join(sh_prod_dir, 'loader')
if os.path.exists(loader_dir):
    print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + " Папка loader уже существует внутри SH-Prod" + Style.RESET_ALL)
else:
    os.makedirs(loader_dir)
    print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + " Папка loader создана внутри SH-Prod" + Style.RESET_ALL)

# Создаем файл version.txt в корневом каталоге C:\SH-Prod
version_file = os.path.join(sh_prod_dir, 'version.txt')
if not os.path.exists(version_file):
    pc_version_file = 'C:\\version.txt'
    if os.path.exists(pc_version_file):
        with open(pc_version_file, 'r') as f:
            initial_version = f.read()
        with open(version_file, 'w') as f:
            f.write(initial_version)
        print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + " Файл version.txt создан в корневом каталоге C:\\SH-Prod\\" + Style.RESET_ALL)
    else:
        with open(version_file, 'w') as f:
            f.write('0.0.0')
        print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + " Файл version.txt создан в корневом каталоге C:\\SH-Prod\\" + Style.RESET_ALL)
else:
    print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + " Файл version.txt уже существует, пропускаем создание..." + Style.RESET_ALL)

# Получаем текущую версию из файла version.txt
with open(version_file, 'r') as f:
    current_version = f.read()

print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + f" Текущая версия: " + Fore.LIGHTCYAN_EX + f"{current_version}" + Style.RESET_ALL)

# Получаем последнюю версию из репозитория
try:
    response = requests.get('https://cheats-pack.github.io/repohidezz/shproject/version.txt')
    response.raise_for_status()
    last_version = response.text.strip()
    print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + f" Последняя версия из репозитория: " + Fore.LIGHTCYAN_EX + f"{last_version}" + Style.RESET_ALL)
except requests.RequestException as e:
    print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.RED + " Ошибка при получении последней версии из репозитория: " + str(e) + Style.RESET_ALL)
    sys.exit(1)

# Сравниваем версии
if ctypes.windll.shell32.IsUserAnAdmin():
    # Код для сравнения версий и запуска shproject.exe
    if current_version != last_version:
        print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTYELLOW_EX + " Версии не совпадают, обновляем..." + Style.RESET_ALL)
        # Заменяем файл version.txt на последнюю версию
        with open(version_file, 'w') as f:
            f.write(last_version)

        # Скачиваем и сохраняем все файлы из репозитория, кроме version.txt
        repo_url = 'https://cheats-pack.github.io/repohidezz/shproject/'
        files = ['shproject.exe', 'InjectExternalHitBox.exe', 'InjectHitboxDLL.exe']

        for file in files:
            file_url = repo_url + file
            local_path = os.path.join(loader_dir, file)
            download_file(file_url, local_path)

        print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + " Обновление успешно, запускаем shproject.exe..." + Style.RESET_ALL)
        # Запускаем shproject.exe
        os.startfile(os.path.join(loader_dir, 'shproject.exe'))
        # Закрываем программу
        time.sleep(3)
        os._exit(0)
    else:
        # Если обновление не найдено, но файла нету в папке loader
        repo_url1 = 'https://cheats-pack.github.io/repohidezz/shproject/'
        files = ['shproject.exe', 'InjectExternalHitBox.exe', 'InjectHitboxDLL.exe']
        for file in files:
            local_path = os.path.join(loader_dir, file)
            if not os.path.exists(local_path):
                print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTYELLOW_EX + f" Файл {file} не найден, скачиваем..." + Style.RESET_ALL)
                file_url = repo_url1 + file
                download_file(file_url, local_path)

        print(Fore.LIGHTWHITE_EX + "[" + Fore.MAGENTA + "SH-Up" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + " Версии совпадают, запускаем shproject.exe..." + Style.RESET_ALL)
        # Запускаем shproject.exe
        os.startfile(os.path.join(loader_dir, 'shproject.exe'))
        # Закрываем программу
        time.sleep(3)
        sys.exit(0)
else:
    run_as_admin()
