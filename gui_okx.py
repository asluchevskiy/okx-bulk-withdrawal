import tkinter as tk
from app.gui import OkxWithdrawApp

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    root = tk.Tk()
    app = OkxWithdrawApp(root)
    app.mainloop()
