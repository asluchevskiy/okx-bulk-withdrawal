import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from main import run_withdraw, setup_logging
from utils import log_formatter
from api import API
import config
import logging


class PrintHandler(logging.Handler):
    def __init__(self, master, callback):
        super().__init__()
        self.master = master
        self.callback = callback

    def emit(self, record):
        message = self.format(record)
        # print(message)
        self.master.after(100, self.callback, message)

    def flush(self):
        pass


class WithdrawApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.master.title("OKX.com bulk withdraw")

        self.stop_event = threading.Event()
        self.api = API(api_key=config.OKX_API_KEY, api_secret_key=config.OKX_API_SECRET_KEY,
                       api_passphrase=config.OKX_API_PASSPHRASE)
        self.api.logger.setLevel(logging.DEBUG)
        if config.LOG_TO_FILE:
            setup_logging(self.api.logger, config.LOG_FILE)
        print_handler = PrintHandler(master=self.master, callback=self.write_log_text)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')  # log message formatting
        print_handler.setFormatter(formatter)
        self.api.logger.addHandler(print_handler)

        self.okx_coins = self.api.get_coins()
        self.okx_networks = self.api.get_networks(config.DEFAULT_TOKEN)

        for i in range(10):
            self.master.grid_rowconfigure(i, weight=1)
        self.master.grid_rowconfigure(9, weight=20)  # Больший вес для строки с выводом лога

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        # self.file_label = tk.Label(self.master, text="Выбери файл c кошельками")
        self.file_label = tk.Label(self.master, text=config.WALLETS_FILE)
        self.file_label.grid(row=0, column=0, sticky='ew')
        self.browse_button = tk.Button(self.master, text="Выбор файла", command=self.browse_file)
        self.browse_button.grid(row=0, column=1, sticky='ew')

        self.min_amount_label = tk.Label(self.master, text="Минимальная сумма")
        self.min_amount_label.grid(row=1, column=0, sticky='ew')
        self.min_amount = tk.DoubleVar(value=config.DEFAULT_MIN_AMOUNT)
        self.min_amount_entry = tk.Entry(self.master, textvariable=self.min_amount)
        self.min_amount_entry.grid(row=1, column=1, sticky='ew')

        self.max_amount_label = tk.Label(self.master, text="Максимальная сумма")
        self.max_amount_label.grid(row=2, column=0, sticky='ew')
        self.max_amount = tk.DoubleVar(value=config.DEFAULT_MAX_AMOUNT)
        self.max_amount_entry = tk.Entry(self.master, textvariable=self.max_amount)
        self.max_amount_entry.grid(row=2, column=1, sticky='ew')

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
        self.network_dropdown = ttk.Combobox(self.master, textvariable=self.network, values=self.okx_networks,
                                             state='readonly')
        self.network_dropdown.grid(row=6, column=1, sticky='ew')

        self.token_label = tk.Label(self.master, text="Токен")
        self.token_label.grid(row=5, column=0, sticky='ew')
        self.token = tk.StringVar(value=config.DEFAULT_TOKEN)
        self.token_dropdown = ttk.Combobox(self.master, textvariable=self.token, values=self.okx_coins,
                                           state='readonly')
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
        run_withdraw(api=self.api,
                     wallets_file=self.file_label.cget('text'),
                     complete_wallets_file=config.COMPLETE_WALLETS_FILE,
                     token=self.token.get(),
                     network=self.network.get(),
                     min_amount=self.min_amount.get(),
                     max_amount=self.max_amount.get(),
                     min_delay=self.min_delay.get(),
                     max_delay=self.max_delay.get(),
                     thread_stop_event=self.stop_event)
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
        if self.max_amount.get() < self.min_amount.get() or self.max_delay.get() < self.min_delay.get():
            messagebox.showerror("Ошибка",
                                 "Максимальная сумма и задержка должны быть больше или равны минимальным значениям")
            return

        self.stop_event.clear()
        self.submit_button.configure(state=tk.DISABLED)
        thread = threading.Thread(target=self.thread_withdraw)
        thread.start()


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    root = tk.Tk()
    app = WithdrawApp(root)
    app.mainloop()
