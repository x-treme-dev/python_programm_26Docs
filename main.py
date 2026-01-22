from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import tkinter as tk
from tkinter import filedialog

# Глобальная переменная для хранения пути
directory_path = ''
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
        btn_source_directory.bind(on_press=self.choose_directory)
        # Вторая строка: 2 метки 
        self.lb_path = Label(text='')
        self.lb_source_path = Label(text='')
        # Третья строка: метка и кнопка
        self.lb_target_choice = Label(text='Целевая директорию:')
        btn_target_directory = Button(text='Выбрать')
        #btn_directory.bind(on_press=self.choose_directory)
        
        
        table.add_widget(self.lb_source_choice)
        table.add_widget(btn_source_directory)
        table.add_widget(self.lb_path)
        table.add_widget(self.lb_source_path)
        table.add_widget(self.lb_target_choice)
        table.add_widget(btn_target_directory)
        
        layout.add_widget(table)

        return layout

        #---------------functions----------------------------------------------------------- 
    def choose_directory(self, instance):
        root = tk.Tk()
        root.withdraw()
        global directory_path
        directory_path = filedialog.askdirectory()
        cat_dir_path = directory_path.split('/')[-1]
        print(cat_dir_path)

        if cat_dir_path:
            self.lb_source_path.text = f"{cat_dir_path}"
            print(f"Выбранный путь: {cat_dir_path}")
        else:
            self.lb_source_path.text = f"Выбор отменен!"
            print("Выбор отменен")

    

    def app_window_close(self, *args):
       self.stop()
       Window.close()

    

if __name__ == '__main__':
    MyApp().run()
  

