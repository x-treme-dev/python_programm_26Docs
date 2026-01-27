import os
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog


def finish():
    root.destroy()
    print("Closing app")


def get_directory(param):
    path = filedialog.askdirectory()
    path_source = ''
    path_target = '' 
  
    if path and param == 'source':
        # Обновляем текст метки
        lb_source.config(text=path)
        print(f"Выбранный путь: {path}")
        path_source = path
    elif path and param == 'target':
        # Обновляем текст метки
        lb_target.config(text=path)
        print(f"Выбранный путь: {path}")
        path_target = path
    elif path == '' and param == 'source':
        lb_source.config(text='Выбор отменен!')
        print("Выбор отменен")
    elif path == '' and param == 'target':
        lb_target.config(text='Выбор отменен!')
        print("Выбор отменен")

# Создаем главное окно
root = Tk()
root.title("26Docs")
root.geometry("300x250+500+200")
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
ttk.Button(mainframe, text='Выбрать', command=lambda:get_directory('source')).grid(column=2, row=1, sticky=W)
ttk.Label(mainframe, text="Выбранная папка: ").grid(column=1, row=2, sticky=W)
lb_source = ttk.Label(mainframe, text="...")
lb_source.grid(column=2, row=2, sticky=W)

# Куда положить файлы?
ttk.Label(mainframe, text="Куда положить файлы?").grid(column=1, row=3, sticky=W)
ttk.Button(mainframe, text='Выбрать', command=lambda:get_directory('target')).grid(column=2, row=3, sticky=W)
ttk.Label(mainframe, text="Выбранная папка: ").grid(column=1, row=4, sticky=W)
lb_target = ttk.Label(mainframe, text="...")
lb_target.grid(column=2, row=4, sticky=W)
 

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

# Обработчик закрытия окна
root.protocol("WM_DELETE_WINDOW", finish)

root.mainloop()



 
    

