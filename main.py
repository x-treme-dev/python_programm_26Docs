import os
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog

path_source = ''
path_target = '' 

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

def check_values(path_source, path_target):
    if path_source == '' or path_target == '':
        lb_message.config(text = 'Недостаточно данных поиска!')
        print('Недостаточно данных для поиска!')
        
    

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



 
    

