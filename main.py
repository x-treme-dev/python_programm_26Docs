from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import tkinter as tk
from tkinter import filedialog
import os
import PyPDF2

directory_path_source = ''
directory_path_target = ''

# Установка размера окна
Window.size = (500, 600)


class MyApp(App):
    def build(self):
        #-------------user interface----------------------------------------------------
        # Обработка закрытия окна по крестику
        Window.bind(on_request_close=self.app_window_close)
        # Создаём основной макет
        layout = GridLayout(cols=1, padding=10, spacing=10)

        # Создаём таблицу с двумя строками и двумя столбцами
        table = GridLayout(cols=2, row_force_default=True, row_default_height=50, spacing=10)

        # Первая строка: метка и кнопка
        self.lb_source_choice = Label(text='Исходная директория:')
        btn_source_directory = Button(text='Выбрать')
        btn_source_directory.bind(on_press=self.choose_source_directory)
        # Вторая строка: 2 метки 
        self.lb_source_empty = Label(text='Выбрано:')
        self.lb_source_path = Label(text='0')
        # Третья строка: метка и кнопка
        self.lb_target_choice = Label(text='Целевая директория:')
        btn_target_directory = Button(text='Выбрать')
        btn_target_directory.bind(on_press=self.choose_target_directory)
        # Чертвертая строка: 2 метки
        self.lb_target_empty = Label(text='Выбрано:')
        self.lb_target_path = Label(text='0')
        # Пятная строка: метка и кнопка
        self.lb_message = Label(text='Сортировка:')
        self.button_sort = Button(text='Выполнить')
        self.button_sort.bind(on_press=self.check_val)
       

        
        

        
        
        table.add_widget(self.lb_source_choice)
        table.add_widget(btn_source_directory)
        table.add_widget(self.lb_source_empty)
        table.add_widget(self.lb_source_path)
        table.add_widget(self.lb_target_choice)
        table.add_widget(btn_target_directory)
        table.add_widget(self.lb_target_empty)
        table.add_widget(self.lb_target_path)
        table.add_widget(self.lb_message)
        table.add_widget(self.button_sort) 

        layout.add_widget(table)

        return layout

        #---------------functions----------------------------------------------------------- 
    def choose_source_directory(self, instance):
        global directory_path_source
        root = tk.Tk()
        root.withdraw()
       
        directory_path_source = filedialog.askdirectory()
        cat_dir_path = directory_path_source.split('/')[-1]
        
        if cat_dir_path:
            self.lb_source_path.text = f"{cat_dir_path}"
            print(directory_path_source)
            print(f"Выбранный путь: {cat_dir_path}")
        else:
            self.lb_source_path.text = f"Выбор отменен!"
            print("Выбор отменен")

    def choose_target_directory(self, instance):
        global directory_path_target
        root = tk.Tk()
        root.withdraw()
        
        directory_path_target = filedialog.askdirectory()
        cat_dir_path = directory_path_target.split('/')[-1]
        
        if cat_dir_path:
            self.lb_target_path.text = f"{cat_dir_path}"
            print(directory_path_target)
            print(f"Выбранный путь: {cat_dir_path}")
        else:
            self.lb_target_path.text = f"Выбор отменен!"
            print("Выбор отменен")

    def check_val(self, instance):
        global directory_path_source, directory_path_target
        
        if directory_path_source and directory_path_target:
            self.lb_message.text = 'Сортировка:'
            self.button_sort.text = 'Готово!'
            # Здесь можно вставить код сортировки
            self.search_pdf(instance)
        else:
            self.lb_message.text = 'Недостаточно данных!'

    
    def search_pdf(self, instance):
      global directory_path_source
      global directory_path_target
      search_text = 'ОСП по Киевскому району г. Симферополя'
      for root, dirs, files in os.walk(directory_path_source):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'rb') as file:
                        reader = PyPDF2.PdfReader(file)
                        # Обход всех страниц
                        for page_num in range(len(reader.pages)):
                            page = reader.pages[page_num]
                            text = page.extract_text()
                            if text and search_text in text:
                                print(f"Файл {filepath} содержит искомый текст на странице {page_num + 1}.")
                                break  # Можно остановить поиск по файлу после нахождения
                except (PyPDF2.errors.PdfReadError, PermissionError) as e:
                    print(f"Не удалось прочитать {filepath}: {e}")

        
       

 

        

    

    #------------------------------------end functions --------------------------------------------

    def app_window_close(self, *args):
       self.stop()
       Window.close()

    

if __name__ == '__main__':
    MyApp().run()
  

