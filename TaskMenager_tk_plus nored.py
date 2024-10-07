import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

# Функция для добавления задачи с датой выполнения
def add_task():
    task = task_entry.get()
    date_str = date_entry.get()

    try:
        # Проверка правильности даты
        due_date = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        current_time = datetime.now()
        if due_date < current_time:
            messagebox.showerror("Ошибка", "Дата выполнения задачи не может быть в прошлом!")
            return

        if task:
            task_listBox.insert(tk.END, f"{task} (до: {due_date.strftime('%d.%m.%Y %H:%M')})")
            task_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректную дату в формате ДД.ММ.ГГГГ ЧЧ:ММ")

# Удаление задачи
def delete_task():
    selected_task = task_listBox.curselection()
    if selected_task:
        task_listBox.delete(selected_task)

# Предзаполнение полей для редактирования
def populate_fields_for_edit():
    selected_task = task_listBox.curselection()
    if selected_task:
        task_str = task_listBox.get(selected_task)
        task_text = task_str.split(" (до:")[0]
        date_text = task_str.split("(до: ")[1].split(")")[0]
        task_entry.delete(0, tk.END)
        task_entry.insert(0, task_text)
        date_entry.delete(0, tk.END)
        date_entry.insert(0, date_text)

# Редактирование задачи
def edit_task():
    selected_task = task_listBox.curselection()
    if selected_task:
        task = task_entry.get() or task_listBox.get(selected_task).split(" (до:")[0]
        date_str = date_entry.get() or task_listBox.get(selected_task).split("(до: ")[1].split(")")[0]

        try:
            due_date = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
            task_listBox.delete(selected_task)
            task_listBox.insert(selected_task, f"{task} (до: {due_date.strftime('%d.%м.%Y %H:%M')})")
            task_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную дату в формате ДД.ММ.ГГГ ЧЧ:ММ")

# Отметка выполненной задачи
def mark_task():
    selected_task = task_listBox.curselection()
    if selected_task:
        task_listBox.itemconfig(selected_task, bg="LightBlue")

def open_popup(info):
    # Создание всплывающего окна
    popup = tk.Toplevel(root)
    popup.title("Всплывающее окно")
    
    # Размеры и позиция окна
    popup.geometry("300x150")
    
    message = f"Задача {info} просрочена"
    label = tk.Label(popup, text=message)
    label.pack(pady=20)
    
    # Кнопка для закрытия окна
    close_button = tk.Button(popup, text="Закрыть", command=popup.destroy)
    close_button.pack(pady=10)

# Проверка срока выполнения задачи
def check_task_deadline():
    current_time = datetime.now()
    for i in range(task_listBox.size()):
        task_str = task_listBox.get(i)
        if "(до:" in task_str:
            date_str = task_str.split("(до: ")[1][:-1]  # Извлечение даты
            try:
                due_date = datetime.strptime(date_str, '%d.%m.%Y %H:%M')
                time_diff = due_date - current_time

                if time_diff.total_seconds() > 0:
                    # Задача не просрочена
                    task_listBox.itemconfig(i, bg="LightGreen")
                else:
                     # Задача просрочена
                    open_popup(task_str.split(' (до:')[0])
                    task_listBox.itemconfig(i, bg="red")
                    task_listBox.delete(i)
                    task_listBox.insert(i, f"{task_str.split(' (до:')[0]} — Задача просрочена!")
                    #open_popup.insert(i, f"{task_str.split(' (до:')[0]} — Задача просрочена!")
                    task_listBox.itemconfig(i, bg="red")
                    task_listBox.delete(i)
                    task_listBox.insert(i, f"{task_str.split(' (до:')[0]} — Задача просрочена!")

            except ValueError:
                continue

    root.after(1000, check_task_deadline)  # Проверка каждые 1 секунду

# Настройки интерфейса
root = tk.Tk()
root.title("Task List")
root.configure(background="HotPink")

# Ввод задачи
text1 = tk.Label(root, text="Введите задачу", bg="HotPink")
text1.pack(pady=5)
task_entry = tk.Entry(root, width=30, bg="DeepPink1", fg="black", font=("Helvetica", 12))
task_entry.pack(pady=10, padx=10)

# Ввод даты выполнения
text2 = tk.Label(root, text="Введите дату выполнения (ДД.ММ.ГГГГ ЧЧ:ММ)", bg="HotPink")
text2.pack(pady=5)
date_entry = tk.Entry(root, width=30, bg="DeepPink1", fg="black", font=("Helvetica", 12))
date_entry.pack(pady=10, padx=10)

# Кнопки
add_task_button = tk.Button(root, text="Добавить задачу", command=add_task)
add_task_button.pack(padx=5, pady=5)
del_task_button = tk.Button(root, text="Удалить задачу", command=delete_task)
del_task_button.pack(padx=5, pady=5)
edit_task_button = tk.Button(root, text="Редактировать задачу", command=edit_task)
edit_task_button.pack(padx=5, pady=5)
mark_task_button = tk.Button(root, text="Отметить выполненную задачу", command=mark_task)
mark_task_button.pack(padx=5, pady=5)

# Кнопка для предзаполнения полей задачи и даты
populate_fields_button = tk.Button(root, text="Выбрать задачу для редактирования", command=populate_fields_for_edit)
populate_fields_button.pack(padx=5, pady=5)

# Список задач
text3 = tk.Label(root, text="Список задач:", bg="HotPink")
text3.pack(pady=5)
task_listBox = tk.Listbox(root, height=10, width=50, bg="LightPink1", fg="black", font=("Helvetica", 12))
task_listBox.pack(padx=10, pady=10)

# Запуск проверки срока выполнения задач
check_task_deadline()

root.mainloop()
