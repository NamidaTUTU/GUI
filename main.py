import ttkbootstrap as ttk
from controller import Controller


def main():
    master = ttk.Window()
    Controller(master)
    master.mainloop()


if __name__ == "__main__":
    main()
