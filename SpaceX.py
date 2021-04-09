import requests
import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from googletrans import Translator
import textwrap
# =====================================================================================================
link = 'https://api.spacexdata.com/v4/rockets'

response = requests.get(link)
data = response.json()
# =====================================================================================================
db_name = 'SpaceX Rockets.db'

connect = sqlite3.connect(db_name)
cursor = connect.cursor()

# создание базы данных
cursor.execute('''CREATE TABLE IF NOT EXISTS rockets (
        ID integer PRIMARY KEY AUTOINCREMENT,
        name text,
        height float,
        diameter float,
        mass float,
        propellant text,
        desc text,
        wiki text
)''')
# =====================================================================================================
reverse1, reverse2, reverse3, reverse4, reverse5 = 0, 0, 0, 0, 0

# функция для сортировки
def sort_by(sort_type):
    global reverse1, reverse2, reverse3, reverse4, reverse5
    if sort_type == 1:
        iid = 0

        if reverse1:
            reverse1 = 0
            cursor.execute(f'SELECT name, height, diameter, mass, propellant, desc, wiki FROM rockets ORDER BY name DESC')
        else:
            reverse1 = 1
            cursor.execute(f'SELECT name, height, diameter, mass, propellant, desc, wiki FROM rockets ORDER BY name ASC')

        for line in cursor.fetchall():
            table.delete(iid)
            list2 = []
            for x in line:
                list2.append(wrap(str(x)))
            table.insert('', 'end', iid=iid, values=list2)
            iid += 1
    if sort_type == 2:
        iid = 0

        if reverse2:
            reverse2 = 0
            cursor.execute(f'SELECT name, height, diameter, mass, propellant, desc, wiki FROM rockets ORDER BY height DESC')
        else:
            reverse2 = 1
            cursor.execute(f'SELECT name, height, diameter, mass, propellant, desc, wiki FROM rockets ORDER BY height ASC')

        for line in cursor.fetchall():
            table.delete(iid)
            list2 = []
            for x in line:
                list2.append(wrap(str(x)))
            table.insert('', 'end', iid=iid, values=list2)
            iid += 1
    if sort_type == 3:
        iid = 0

        if reverse3:
            reverse3 = 0
            cursor.execute(f'SELECT name, height, diameter, mass, propellant, desc, wiki FROM rockets ORDER BY diameter DESC')
        else:
            reverse3 = 1
            cursor.execute(f'SELECT name, height, diameter, mass, propellant, desc, wiki FROM rockets ORDER BY diameter ASC')

        for line in cursor.fetchall():
            table.delete(iid)
            list2 = []
            for x in line:
                list2.append(wrap(str(x)))
            table.insert('', 'end', iid=iid, values=list2)
            iid += 1
    if sort_type == 4:
        iid = 0

        if reverse4:
            reverse4 = 0
            cursor.execute(f'SELECT name, height, diameter, mass, propellant, desc, wiki FROM rockets ORDER BY mass DESC')
        else:
            reverse4 = 1
            cursor.execute(f'SELECT name, height, diameter, mass, propellant, desc, wiki FROM rockets ORDER BY mass ASC')

        for line in cursor.fetchall():
            table.delete(iid)
            list2 = []
            for x in line:
                list2.append(wrap(str(x)))
            table.insert('', 'end', iid=iid, values=list2)
            iid += 1
    if sort_type == 5:
        iid = 0
        if reverse5:
            reverse5 = 0
            cursor.execute(f'SELECT name, height, diameter, mass, propellant, desc, wiki FROM rockets ORDER BY propellant DESC')
        else:
            reverse5 = 1
            cursor.execute(f'SELECT name, height, diameter, mass, propellant, desc, wiki FROM rockets ORDER BY propellant ASC')

        for line in cursor.fetchall():
            table.delete(iid)
            list2 = []
            for x in line:
                list2.append(wrap(str(x)))
            table.insert('', 'end', iid=iid, values=list2)
            iid += 1

def wrap(string, lenght = 60):
    return '\n'.join(textwrap.wrap(string, lenght))
# =====================================================================================================
root = tk.Tk()
root.title('Ракеты SpaceX')
root.state('zoomed')
root.resizable(0, 0)
root.configure(background='#7B7B7B')

s = ttk.Style()
s.configure('Treeview', rowheight=120)

columns = (1, 2, 3, 4, 5, 6, 7)

font = ('Consolas', 16)

lbl = tk.Label(text='Ракеты SpaceX', font=('Consolas', 20, 'bold'), background='#7B7B7B', foreground='white')
lbl.place(rely=0.01, relx=0.05)

table = ttk.Treeview(root, columns=columns, show='headings', height=100)

style = ttk.Style()
style.configure("Treeview.Column", foreground='red')
style.configure("Treeview.Heading", foreground='blue', background="blue")

table.column(1, minwidth=120, width=120)
table.column(2, minwidth=70, width=70)
table.column(3, minwidth=70, width=70)
table.column(4, minwidth=90, width=90)
table.column(5, minwidth=200, width=200)
table.column(6, minwidth=400, width=400)
table.column(7, minwidth=252, width=252)

table.heading(1, text='Название', command=lambda: sort_by(1))
table.heading(2, text='Высота', command=lambda: sort_by(2))
table.heading(3, text='Диаметр', command=lambda: sort_by(3))
table.heading(4, text='Масса', command=lambda: sort_by(4))
table.heading(5, text='Вид топлива', command=lambda: sort_by(5))
table.heading(6, text='Описание')
table.heading(7, text='Вики')
# =====================================================================================================
# добавляем данные в базу данных, если в ней ничего нет
cursor.execute(f'SELECT name, height, diameter, mass, propellant, desc, wiki FROM rockets')
idd = 0
if len(cursor.fetchall()) == 0:
    # получение данных и перевод их в базу данных
    for rocket in data:
        trans = Translator()

        name = rocket['wikipedia'].replace('https://en.wikipedia.org/wiki/', '').replace('_', ' ')
        height = rocket['height']['meters']
        diameter = rocket['diameter']['meters']
        mass = rocket['mass']['kg']
        propellant = trans.translate(rocket['engines']['propellant_1'] + " and " + rocket['engines']['propellant_2'], src='en', dest='ru').text
        desc = trans.translate(rocket['description'], src='en', dest='ru').text
        wiki = rocket['wikipedia']

        rocket_info = (name, height, diameter, mass, propellant, desc, wiki)
        list1 = []
        for i in rocket_info:
            list1.append(wrap(str(i)))
        table.insert('', 'end', iid=idd, values=list1)
        idd += 1

        sql_query_add = f"INSERT INTO rockets (name, height, diameter, mass, propellant, desc, wiki) " \
                        f"VALUES ('{name}', '{height}', '{diameter}', '{mass}', '{propellant}', '{desc}', '{wiki}')"
        cursor.execute(sql_query_add)
        connect.commit()
else:
    cursor.execute(f'SELECT name, height, diameter, mass, propellant, desc, wiki FROM rockets')
    for row in cursor.fetchall():
        list1 = []
        for i in row:
            list1.append(wrap(str(i)))
        table.insert('', 'end', iid=idd, values=list1)
        idd += 1
# =====================================================================================================
# table.insert('', 'end', iid=iid, values=)
table.place(rely=0.07, relx=0.00, relwidth=1)
root.mainloop()