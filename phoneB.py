import tkinter as tk
import sqlite3

from tkinter import ttk

class Main(tk.Frame):
    def __init__(self, root):  # Инициализация класса
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)  # Создание фрейма для панели инструментов
        toolbar.pack(side=tk.TOP, fill=tk.X)  # Размещение панели инструментов вверху
        self.add_img = tk.PhotoImage(file="./img/add.png")  # Загрузка изображения "Добавить"
        btn_open_dialog = tk.Button(toolbar, bg="#d7d8e0", bd=0,
                                    command=self.open_dialog,
                                    image=self.add_img)  # Создание кнопки с изображением "Добавить"
        btn_open_dialog.pack(side=tk.LEFT)  # Размещение кнопки слева на панели инструментов

        self.tree = ttk.Treeview(self, columns=['ID', 'name', 'tel', 'email'], height=45, show='headings')
        # Создание дерева с колонками и заданием высоты
        self.tree.column('ID', width=30, anchor=tk.CENTER)  # Задание ширины и центрирования для колонки "ID"
        self.tree.column('name', width=300, anchor=tk.CENTER)  # Задание ширины и центрирования для колонки "ФИО"
        self.tree.column('tel', width=150, anchor=tk.CENTER)  # Задание ширины и центрирования для колонки "Телефон"
        self.tree.column('email', width=150, anchor=tk.CENTER)  # Задание ширины и центрирования для колонки "Email"

        self.tree.heading('ID', text='ID')  # Задание заголовка для колонки "ID"
        self.tree.heading('name', text='ФИО')  # Задание заголовка для колонки "ФИО"
        self.tree.heading('tel', text='Телефон')  # Задание заголовка для колонки "Телефон"
        self.tree.heading('email', text='Email')  # Задание заголовка для колонки "Email"

        self.tree.pack(side=tk.LEFT)  # Размещение дерева слева

        self.update_img = tk.PhotoImage(file="./img/update.png")  # Загрузка изображения "Обновить"
        btn_edit_dialog = tk.Button(toolbar, bg="#d7d8e0", bd=0,
                                    image=self.update_img,
                                    command=self.open_update_dialog)  # Создание кнопки с изображением "Обновить"
        btn_edit_dialog.pack(side=tk.LEFT)  # Размещение кнопки слева на панели инструментов

        self.delete_img = tk.PhotoImage(file="./img/delete.png")  # Загрузка изображения "Удалить"
        btn_delete = tk.Button(toolbar, bg="#d7d8e0", bd=0,
                               image=self.delete_img,
                               command=self.delete_records)  # Создание кнопки с изображением "Удалить"
        btn_delete.pack(side=tk.LEFT)  # Размещение кнопки слева на панели инструментов

        self.search_img = tk.PhotoImage(file="./img/search.png")  # Загрузка изображения "Поиск"
        btn_search = tk.Button(toolbar, bg="#d7d8e0", bd=0,
                               image=self.search_img,
                               command=self.open_search_dialog)  # Создание кнопки с изображением "Поиск"
        btn_search.pack(side=tk.LEFT)  # Размещение кнопки слева на панели инструментов

        self.refresh_img = tk.PhotoImage(file="./img/refresh.png")  # Загрузка изображения "Обновить"
        btn_refresh = tk.Button(toolbar, bg="#d7d8e0", bd=0,
                               image=self.refresh_img,
                               command=self.view_records)  # Создание кнопки с изображением "Обновить"
        btn_refresh.pack(side=tk.LEFT)  # Размещение кнопки слева на панели инструментов

        scroll = tk.Scrollbar(self, command=self.tree.yview)  # Создание полосы прокрутки
        scroll.pack(side=tk.LEFT, fill=tk.Y)  # Размещение полосы прокрутки слева и заполнение по оси Y
        self.tree.configure(yscrollcommand=scroll.set)  # Конфигурация дерева для использования пол

    def open_dialog(self):
        Child()  # Открыть дочерний диалог

    def records(self, name, tel, email):
        self.db.insert_data(name, tel, email)  # Вставка данных в базу данных
        self.view_records()  # Обновление представления с новыми записями

    def view_records(self):
        self.db.c.execute('''SELECT * FROM db''')  # Выбор всех записей из базы данных
        [self.tree.delete(i) for i in self.tree.get_children()]  # Удаление всех существующих строк из дерева
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]  # Вставка новых строк в дерево

    def open_update_dialog(self):
        Update()  # Открыть диалог обновления

    def update_record(self, name, tel, email):
        self.db.c.execute('''UPDATE db SET name=?, tel=?, email=? WHERE ID=?''', (name, tel, email, self.tree.set(self.tree.selection()[0], '#1')))
        # Обновление выбранной записи в базе данных
        self.db.conn.commit()  # Применение изменений
        self.view_records()  # Обновление представления с обновленными записями

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM db WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        # Удаление выбранных записей из базы данных
        self.db.conn.commit()  # Применение изменений
        self.view_records()  # Обновление представления с оставшимися записями

    def open_search_dialog(self):
        Search()  # Открыть диалог поиска

    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.c.execute('''SELECT * FROM db WHERE name LIKE ?''', (name,))
        # Поиск записей в базе данных по имени
        [self.tree.delete(i) for i in self.tree.get_children()]  # Удаление всех существующих строк из дерева
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]  # Вставка новых строк в дерево

class Child(tk.Toplevel): #класс для добавления новой записи
    def __init__(self):
        super().__init__()
        self.init_child()
        self.view = app


    def init_child(self):
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)

        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)

        label_sum = tk.Label(self, text='Email')
        label_sum.place(x=50, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        self.button_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.button_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(), self.entry_tel.get(), self.entry_email.get()))

class Update(Child): #добавляет функциональность редактирования записи
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title("Редактировать позицию")
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(), self.entry_tel.get(), self.entry_email.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE id=?''', (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])

class Search(tk.Toplevel): # класс для поиска записей
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)
        
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

class DB: #класс для работы с базой данных SQLite
    def __init__(self):
        self.conn = sqlite3.connect("db.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS db(
            id INTEGER PRIMARY KEY,
            name TEXT, 
            tel TEXT, 
            email TEXT
        )""")

        self.conn.commit()
    
    def insert_data(self, name, tel, email):
        self.c.execute("INSERT INTO db (name, tel, email) VALUES(?, ?, ?)", (name, tel, email))
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Телефонная книга")
    root.geometry("665x450")
    root.resizable(False, False)
    root.mainloop()