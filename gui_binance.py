import tkinter as tk
from app.gui import BinanceWithdrawApp

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    root = tk.Tk()
    app = BinanceWithdrawApp(root)
    app.mainloop()
