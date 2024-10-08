import tkinter as tk

def my_summa():
    numbers = entry.get().split()
    result = 0
    for number in numbers:
        number = int(number)
        result += number
    result_label.config(text=f"Сумма чисел - {result}")

root = tk.Tk()
root.title("СумЧис")

label = tk.Label(root, text="Введи числа через пробел")
label.pack()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Суммировать", command=my_summa)
button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
