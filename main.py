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
        # Обработка закрытия окна по крестику
        Window.bind(on_request_close=self.app_window_close)
        # Создаём основной макет
        layout = GridLayout(cols=1, padding=10, spacing=10)

        # Создаём таблицу с двумя строками и двумя столбцами
        table = GridLayout(cols=2, row_force_default=True, row_default_height=50, spacing=10)

        # Первая строка: метка и кнопка
        self.lb_choice = Label(text='Выбрать директорию')
        btn_directory = Button(text='Выбрать')
        btn_directory.bind(on_press=self.choose_directory)

        table.add_widget(self.lb_choice)
        table.add_widget(btn_directory)

        
        self.text_inp_path = TextInput(
            text='',
            multiline=True
        )
 
      
        table.add_widget(self.text_inp_path)
        table.add_widget(Label(text=''))
 
        layout.add_widget(table)

        return layout

    def choose_directory(self, instance):
        root = tk.Tk()
        root.withdraw()
        global directory_path
        directory_path = filedialog.askdirectory()

        if directory_path:
            self.text_inp_path.text = f"Selected path: {directory_path}"
            print(f"Выбранный путь: {directory_path}")
        else:
            print("Выбор отменен")

    def app_window_close(self, *args):
       self.stop()
       Window.close()

if __name__ == '__main__':
    MyApp().run()
  

