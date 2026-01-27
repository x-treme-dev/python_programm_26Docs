import os
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import shutil
from PyPDF2 import PdfReader
import re
import random

path_source = ''
path_target = ''

params = [
    ["ОСП по Киевскому району г. Симферополя", "Отделение судебных приставов по Киевскому району г. Симферополя", "Киевский ОСП"],
    ["ОСП по Железнодорожному району г. Симферополя", "Отделение судебных приставов по Железнодорожному району г. Симферополя", "Ж_д ОСП"],
    ["ОСП по Симферопольскому району г. Симферополя", "Отделение судебных приставов по Симферопольскому району г. Симферополя", "Симф р-н ОСП"],
    ["ОСП по Центральному району г. Симферополя", "Отделение судебных приставов по Центральному району г. Симферополя", "Центральный ОСП"]
]

list_path = []

def finish():
    root.destroy()
    print("Closing app")


def get_directory(param):
    path = filedialog.askdirectory()
    cat_path = path.rsplit('/', 1)[-1]
    global path_source
    global path_target
   
    if path and param == 'source':
        # Обновляем текст метки
        lb_source.config(text=cat_path)
        print(f"Выбранная папка: {path}")
        path_source = path
    elif path and param == 'target':
        # Обновляем текст метки
        lb_target.config(text=cat_path)
        print(f"Выбранная папка: {path}")
        path_target = path
    elif path == '' and param == 'source':
        lb_source.config(text='Выбор отменен!')
        print("Выбор отменен")
    elif path == '' and param == 'target':
        lb_target.config(text='Выбор отменен!')
        print("Выбор отменен")


def copy_files(path_source, path_target, search_str1, search_str2, folder_name):
    global list_path
    new_path_target = os.path.join(path_target, folder_name)
    list_path = [new_path_target]
    os.makedirs(new_path_target, exist_ok=True)
    #print(f"Копирование в папку: {new_path_target}")
    for root, dirs, files in os.walk(path_source):
        for file in files:
            if file.lower().endswith('.pdf'):
                full_path = os.path.join(root, file)
                #print(f"Обработка файла: {full_path}")
                try:
                    reader = PdfReader(full_path)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""
                    
                    if search_str1 in text or search_str2 in text:
                        #print(f"Файл подходит для копирования: {full_path}")
                        shutil.copy2(full_path, new_path_target)
                        print(f"Файл скопирован в {new_path_target}")
                except Exception as e:
                    print(f"Ошибка при обработке файла {full_path}: {e}")
    
    for l in list_path:
                rename_files(l)
    lb_message.config(text=f'Готово!')
     

def check_values(path_source, path_target):
    if path_source == '' or path_target == '':
        lb_message.config(text = 'Недостаточно данных поиска!')
        print('Недостаточно данных для поиска!')
    else:
        for p in params:
            copy_files(path_source, path_target, *p)


def sanitize_filename(name):
    # Удаляем или заменяем недопустимые символы
    return re.sub(r'[\\/:*?"<>|]', '_', name)

def rename_files(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            try:
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            except Exception:
                continue  # пропускаем файлы, которые не удалось прочитать
            
            # Ищем строку со словом 'Постановление'
            match = re.search(r'([^\n]*Постановление[^\n]*)', text)
            if match:
                line = match.group(1)
                words = line.split()
                if len(words) >= 4:
                    words_copy = words.copy()
                    # сокращаем 2, 3 и 4 слово до 4 букв
                    for idx in [1, 2, 3]:
                        if len(words_copy[idx]) <= 4:
                            words_copy[idx] = words_copy[idx][:4]
                    
                    new_name_base = ' '.join(words_copy)
                    new_name_base = sanitize_filename(new_name_base)
                    rand_num = random.randint(0, 1000)
                    print(f'переименовывю в {new_name_base} {rand_num}')
                    new_filename = f"{new_name_base}_{rand_num}.pdf"

                    new_path = os.path.join(directory, new_filename)
                    # Проверка, чтобы файл с таким именем не существовал
                    if not os.path.exists(new_path):
                        os.rename(file_path, new_path)
                    else:
                        # Можно добавить логику для повторной генерации имени
                        pass


################# interface ##########################################################           
# Создаем главное окно
root = Tk()
root.title("26Docs")
root.geometry("600x250+500+200")
root.update_idletasks()

# Назначаем обработчик закрытия окна
root.protocol("WM_DELETE_WINDOW", finish)

# Создаем интерфейс
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Откуда взять файлы?
ttk.Label(mainframe, text="Откуда взять файлы?").grid(column=1, row=1, sticky=W)
ttk.Button(mainframe, text='Выбрать', command=lambda:get_directory('source')).grid(column=2, row=1, columnspan=2, sticky=(W,E))
ttk.Label(mainframe, text="Выбранная папка: ").grid(column=1, row=2, sticky=W)
lb_source = ttk.Label(mainframe, text="нет данных...")
lb_source.grid(column=2, row=2, sticky=W)

# Куда положить файлы?
ttk.Label(mainframe, text="Куда положить файлы?").grid(column=1, row=3, sticky=W)
ttk.Button(mainframe, text='Выбрать', command=lambda:get_directory('target')).grid(column=2, row=3,columnspan=2,  sticky=(W,E))
ttk.Label(mainframe, text="Выбранная папка: ").grid(column=1, row=4, sticky=W)
lb_target = ttk.Label(mainframe, text="нет данных...")
lb_target.grid(column=2, row=4, sticky=W)


mainframe.grid_columnconfigure(1, weight=1)
mainframe.grid_columnconfigure(2, weight=1)
ttk.Button(mainframe, text='Сортировать', command=lambda:check_values(path_source, path_target)).grid(column=1, row=5, columnspan=2, sticky=(W, E))
lb_message = ttk.Label(mainframe, text='')
lb_message.grid(column=1, row=6, columnspan=2, sticky=(W, E))
 

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# Обработчик закрытия окна
root.protocol("WM_DELETE_WINDOW", finish)

root.mainloop()



 
    

