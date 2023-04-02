import tkinter as tk
from tkinter import filedialog, messagebox
import config

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_label.config(text=file_path)

def submit():
    if max_value.get() < min_value.get() or max_delay.get() < min_delay.get():
        messagebox.showerror("Ошибка", "Максимальная сумма и задержка должны быть больше или равны минимальным значениям")
        return

    log.configure(state='normal')
    log.insert(tk.END, f"Файл: {file_label.cget('text')}\n")
    log.insert(tk.END, f"Минимальная сумма: {min_value.get()}\n")
    log.insert(tk.END, f"Максимальная сумма: {max_value.get()}\n")
    log.insert(tk.END, f"Минимальная задержка: {min_delay.get()} секунд\n")
    log.insert(tk.END, f"Максимальная задержка: {max_delay.get()} секунд\n")
    log.insert(tk.END, f"Сеть: {network.get()}\n")
    log.insert(tk.END, f"Токен: {token.get()}\n")
    log.insert(tk.END, "-----------\n")
    log.configure(state='disabled')
    log.yview(tk.END)

root = tk.Tk()
root.title("OKX.com bulk withdraw")

for i in range(10):
    root.grid_rowconfigure(i, weight=1)
root.grid_rowconfigure(9, weight=20)  # Больший вес для строки с выводом лога

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

file_label = tk.Label(root, text="Выбери файл c кошельками")
file_label.grid(row=0, column=0, sticky='ew')
browse_button = tk.Button(root, text="Выбор файла", command=browse_file)
browse_button.grid(row=0, column=1, sticky='ew')

min_value_label = tk.Label(root, text="Минимальная сумма")
min_value_label.grid(row=1, column=0, sticky='ew')
min_value = tk.DoubleVar(value=config.DEFAULT_MIN_AMOUNT)
min_value_entry = tk.Entry(root, textvariable=min_value)
min_value_entry.grid(row=1, column=1, sticky='ew')

max_value_label = tk.Label(root, text="Максимальная сумма")
max_value_label.grid(row=2, column=0, sticky='ew')
max_value = tk.DoubleVar(value=config.DEFAULT_MAX_AMOUNT)
max_value_entry = tk.Entry(root, textvariable=max_value)
max_value_entry.grid(row=2, column=1, sticky='ew')

min_delay_label = tk.Label(root, text="Минимальная задержка (в секундах)")
min_delay_label.grid(row=3, column=0, sticky='ew')
min_delay = tk.IntVar(value=config.DEFAULT_MIN_DELAY)
min_delay_entry = tk.Entry(root, textvariable=min_delay)
min_delay_entry.grid(row=3, column=1, sticky='ew')

max_delay_label = tk.Label(root, text="Максимальная задержка (в секундах)")
max_delay_label.grid(row=4, column=0, sticky='ew')
max_delay = tk.IntVar(value=config.DEFAULT_MAX_DELAY)
max_delay_entry = tk.Entry(root, textvariable=max_delay)
max_delay_entry.grid(row=4, column=1, sticky='ew')

network_label = tk.Label(root, text="Сеть")
network_label.grid(row=5, column=0, sticky='ew')
network = tk.StringVar(value=config.DEFAULT_NETWORK)
network_entry = tk.Entry(root, textvariable=network)
network_entry.grid(row=5, column=1, sticky='ew')

token_label = tk.Label(root, text="Токен")
token_label.grid(row=6, column=0, sticky='ew')
token = tk.StringVar(value=config.DEFAULT_TOKEN)
token_entry = tk.Entry(root, textvariable=token)
token_entry.grid(row=6, column=1, sticky='ew')

submit_button = tk.Button(root, text="Отправить", command=submit)
submit_button.grid(row=7, column=0, columnspan=2, sticky='ew')

log_label = tk.Label(root, text="Лог скрипта")
log_label.grid(row=8, column=0, columnspan=2, sticky='ew')
log = tk.Text(root, width=50, height=10, wrap=tk.WORD, state='disabled')
log.grid(row=9, column=0, columnspan=2, sticky='nsew')


scrollbar = tk.Scrollbar(root, command=log.yview)
scrollbar.grid(row=9, column=2, sticky='ns')
log.config(yscrollcommand=scrollbar.set)

root.mainloop()
