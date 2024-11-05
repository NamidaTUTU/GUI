import ttkbootstrap as ttk


class BasePage(ttk.Frame):
    def __init__(self, master, width=None, height=None):
        super().__init__(master)
        self.master = master
        self.width = width
        self.height = height

        # 如果 master 是顶层窗口（Tk 或 Toplevel），则设置窗口大小和居中
        if isinstance(self.master, (ttk.Window, ttk.Frame)):  # ttk.Toplevel
            self.master.geometry(f'{self.width}x{self.height}')
            self.center_window()  # 让窗口居中

    # 让窗口居中显示
    def center_window(self):
        # 获取屏幕宽高
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # 计算窗口居中的位置
        x = int((screen_width / 2) - (self.width / 2))
        y = int((screen_height / 2) - (self.height / 2))

        # 设置窗口位置为居中
        self.master.geometry(f'{self.width}x{self.height}+{x}+{y}')
