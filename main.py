import os
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import shutil
from PyPDF2 import PdfReader
import re
import hashlib
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
old_filename = []

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
    print('Готово!')
     

def check_values(path_source, path_target):
    if path_source == '' or path_target == '':
        lb_message.config(text = 'Недостаточно данных поиска!')
        print('Недостаточно данных для поиска!')
    else:
        for p in params:
            copy_files(path_source, path_target, *p)


def sanitize_filename(name):
    # Заменяем недопустимые символы на _
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    # Удаляем управляющие символы, например, переносы строк
    name = re.sub(r'[\n\r\t]', '', name)
    # Убираем лишние пробелы
    name = name.strip()
    # Удаляем запятую, если она есть в конце
    name = re.sub(r',\s*$', '', name)
    # Удаляем нижнее подчеркивание и ноль, если они идут в конце
    name = re.sub(r'(_0)$', '', name)
    return name

def extract_sudebny_prikaz(text):
    # Ищем вариации 'Судебный приказ' или 'c судебным приказом'
    pattern = r'(Судебный приказ|судебный приказ|c судебным приказом|по делу)(.*?)(выданный органом|,|предмет исполнения)'
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        # Берем все символы между найденными фразами
        part = match.group(2).strip()
        # Удаляем переносы строк, табуляции, запятые и кириллические символы
        part = re.sub(r'[\n\r\t,а-яА-Я]', '', part).strip()
        return part
    return None


def rename_files(directory):
    for filename in os.listdir(directory):
        old_filename.append(filename)
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            try:
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            except Exception as e:
                print(f"Ошибка чтения {file_path}: {e}")
                continue
            
            # Файл со строкой вида 124567/19/12421-СД Постановление пропускаем
            pattern_doc_number = r'\d+/\d+/\d+-[А-Я]{2}\s*постановление'
            if re.search(pattern_doc_number, text,  re.IGNORECASE):
                continue
            
            # Остальной ваш код обработки...
            if "ИЗВЕЩЕНИЕ" in text:
                new_name_base = "ИЗВЕЩЕНИЕ"
            elif "СООБЩЕНИЕ" in text:
                new_name_base = "СООБЩЕНИЕ"
            else:
                pattern = r'([^\n]*?(Постановление|Документ:\s*Постановление)[^\n]*)'
                matches_post = re.findall(pattern, text, re.IGNORECASE)
                if matches_post:
                    line = matches_post[0][0]
                    words = line.split()
                    try:
                        index_postan = words.index('Постановление')
                    except ValueError:
                        try:
                            index_postan = words.index('Постановление')
                        except ValueError:
                            index_postan = -1
                    if index_postan != -1:
                        replacement_word = 'ПОСТ'
                        post_words = words[index_postan + 1:]
                        post_words = post_words[:4]
                        for i in range(1, len(post_words)):
                            if len(post_words[i]) > 4:
                                post_words[i] = post_words[i][:4]
                        name_parts = [replacement_word] + post_words
                        new_name_base = '_'.join(name_parts)
                    else:
                        new_name_base = "Госусуги"
                else:
                    new_name_base = "Госусуги"
                    
            
            sudebny_part = extract_sudebny_prikaz(text)
            if sudebny_part:
                new_name_base = f"{new_name_base}_{sudebny_part}"
            
            new_name_base = sanitize_filename(new_name_base)
            new_path = os.path.join(directory, new_name_base + '.pdf')

            if not os.path.exists(new_path):
                os.rename(file_path, new_path)
                
    

################# interface ##########################################################           
# Создаем главное окно
root = Tk()
root.title("26Docs")
root.geometry("600x350+500+200")
root.update_idletasks()


style = ttk.Style()
style.configure('.', font=('Courier New', 22))


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



 
    

