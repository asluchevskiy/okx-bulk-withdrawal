import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from main import run_withdraw, setup_logging
from api import API
import config


class WithdrawApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.master.title("OKX.com bulk withdraw")

        self.stop_event = threading.Event()
        self.api = API(api_key=config.API_KEY, api_secret_key=config.API_SECRET_KEY,
                       api_passphrase=config.API_PASSPHRASE)
        if config.LOG_TO_FILE:
            setup_logging(self.api.log, config.LOG_FILE)

        self.okx_coins = self.api.get_coins()
        self.okx_networks = self.api.get_networks(config.DEFAULT_TOKEN)

        for i in range(10):
            self.master.grid_rowconfigure(i, weight=1)
        self.master.grid_rowconfigure(9, weight=20)  # Больший вес для строки с выводом лога

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self.file_label = tk.Label(self.master, text="Выбери файл c кошельками")
        self.file_label.grid(row=0, column=0, sticky='ew')
        self.browse_button = tk.Button(self.master, text="Выбор файла", command=self.browse_file)
        self.browse_button.grid(row=0, column=1, sticky='ew')

        self.min_value_label = tk.Label(self.master, text="Минимальная сумма")
        self.min_value_label.grid(row=1, column=0, sticky='ew')
        self.min_value = tk.DoubleVar(value=config.DEFAULT_MIN_AMOUNT)
        self.min_value_entry = tk.Entry(self.master, textvariable=self.min_value)
        self.min_value_entry.grid(row=1, column=1, sticky='ew')

        self.max_value_label = tk.Label(self.master, text="Максимальная сумма")
        self.max_value_label.grid(row=2, column=0, sticky='ew')
        self.max_value = tk.DoubleVar(value=config.DEFAULT_MAX_AMOUNT)
        self.max_value_entry = tk.Entry(self.master, textvariable=self.max_value)
        self.max_value_entry.grid(row=2, column=1, sticky='ew')

        self.min_delay_label = tk.Label(self.master, text="Минимальная задержка (в секундах)")
        self.min_delay_label.grid(row=3, column=0, sticky='ew')
        self.min_delay = tk.IntVar(value=config.DEFAULT_MIN_DELAY)
        self.min_delay_entry = tk.Entry(self.master, textvariable=self.min_delay)
        self.min_delay_entry.grid(row=3, column=1, sticky='ew')

        self.max_delay_label = tk.Label(self.master, text="Максимальная задержка (в секундах)")
        self.max_delay_label.grid(row=4, column=0, sticky='ew')
        self.max_delay = tk.IntVar(value=config.DEFAULT_MAX_DELAY)
        self.max_delay_entry = tk.Entry(self.master, textvariable=self.max_delay)
        self.max_delay_entry.grid(row=4, column=1, sticky='ew')

        self.network_label = tk.Label(self.master, text="Сеть")
        self.network_label.grid(row=6, column=0, sticky='ew')
        self.network = tk.StringVar(value=config.DEFAULT_NETWORK)
        self.network_dropdown = ttk.Combobox(self.master, textvariable=self.network, values=self.okx_networks, state='readonly')
        self.network_dropdown.grid(row=6, column=1, sticky='ew')

        self.token_label = tk.Label(self.master, text="Токен")
        self.token_label.grid(row=5, column=0, sticky='ew')
        self.token = tk.StringVar(value=config.DEFAULT_TOKEN)
        self.token_dropdown = ttk.Combobox(self.master, textvariable=self.token, values=self.okx_coins, state='readonly')
        self.token_dropdown.grid(row=5, column=1, sticky='ew')
        self.token.trace('w', self.on_token_change)

        self.submit_button = tk.Button(self.master, text="Отправить", command=self.submit)
        self.submit_button.grid(row=7, column=0, columnspan=2, sticky='ew')

        self.log_label = tk.Label(self.master, text="Лог скрипта")
        self.log_label.grid(row=8, column=0, columnspan=2, sticky='ew')
        self.log = tk.Text(self.master, width=50, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.log.grid(row=9, column=0, columnspan=2, sticky='nsew')

        self.scrollbar = tk.Scrollbar(self.master, command=self.log.yview)
        self.scrollbar.grid(row=9, column=2, sticky='ns')
        self.log.config(yscrollcommand=self.scrollbar.set)

        self.master.protocol("WM_DELETE_WINDOW", self.shutdown)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_label.config(text=file_path)

    def thread_withdraw(self):
        for i in range(10):
            self.master.after(100, self.write_log_text, i)
            time.sleep(1)
            if self.stop_event.is_set():
                return
        self.master.after(100, self.activate_submit_button)

    def shutdown(self):
        self.stop_event.set()
        self.master.destroy()

    def write_log_text(self, text):
        self.log.configure(state=tk.NORMAL)
        self.log.insert(tk.END, f'{text}\n')
        self.log.configure(state=tk.DISABLED)
        self.log.yview(tk.END)

    def on_token_change(self, *args):
        selected_token = self.token.get()
        self.okx_networks = self.api.get_networks(selected_token)
        self.network_dropdown.configure(values=self.okx_networks)
        if self.okx_networks:
            self.network.set(self.okx_networks[0])
        else:
            self.network.set('')


    def activate_submit_button(self):
        self.submit_button.configure(state=tk.NORMAL)

    def submit(self):
        if self.max_value.get() < self.min_value.get() or self.max_delay.get() < self.min_delay.get():
            messagebox.showerror("Ошибка",
                                 "Максимальная сумма и задержка должны быть больше или равны минимальным значениям")
            return

        self.stop_event.clear()
        self.submit_button.configure(state=tk.DISABLED)
        thread = threading.Thread(target=self.thread_withdraw)
        thread.start()

        # self.log.configure(state='normal')
        # self.log.insert(tk.END, f"Файл: {self.file_label.cget('text')}\n")
        # self.log.insert(tk.END, f"Минимальная сумма: {self.min_value.get()}\n")
        # self.log.insert(tk.END, f"Максимальная сумма: {self.max_value.get()}\n")
        # self.log.insert(tk.END, f"Минимальная задержка: {self.min_delay.get()} секунд\n")
        # self.log.insert(tk.END, f"Максимальная задержка: {self.max_delay.get()} секунд\n")
        # self.log.insert(tk.END, f"Сеть: {self.network.get()}\n")
        # self.log.insert(tk.END, f"Токен: {self.token.get()}\n")
        # self.log.insert(tk.END, "-----------\n")
        # self.log.configure(state='disabled')
        # self.log.yview(tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    app = WithdrawApp(root)
    app.mainloop()
