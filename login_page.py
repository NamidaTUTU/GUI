from tkinter import messagebox

import ttkbootstrap as ttk
from base_page import BasePage
from main_application import MainApplicationPage


class LoginPage(BasePage):
    def __init__(self, master: ttk.Window, controller) -> None:
        self.controller = controller
        self.width = 600
        self.height = 400
        super().__init__(master, width=self.width, height=self.height)
        # 配置行列，使内容垂直和水平居中
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.pack(fill='both', expand=True)

        self.font = ("Arial", 14)
        self.username_entry = None
        self.password_entry = None

    def draw(self):
        """绘制"""
        # 使用 grid 布局
        ttk.Label(self, text="Username:", font=self.font).grid(row=1, column=1, sticky=ttk.E)
        self.username_entry = ttk.Entry(self, font=self.font, width=20)
        self.username_entry.grid(row=1, column=2, sticky=ttk.W)

        ttk.Label(self, text="Password:", font=self.font).grid(row=2, column=1, sticky=ttk.E)
        self.password_entry = ttk.Entry(self, show='*', font=self.font, width=20)
        self.password_entry.grid(row=2, column=2, sticky=ttk.W)

        login_button = ttk.Button(self, text="Login", command=self.login, width=10)
        self.master.bind("<Return>", self.login)  # 绑定回车键到登录操作(fix self.bind --> self.master.bind)
        login_button.grid(row=3, column=1, columnspan=2)

        # 为所有元素设置全局的 padx 和 pady
        for widget in self.grid_slaves():
            widget.grid_configure(padx=10, pady=10)

    def login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # TODO test
        username = "admin"
        password = "1234"

        # 登录验证逻辑
        if username == "admin" and password == "1234":  # 示例条件
            messagebox.showinfo("Info", "Login successful")
            # 隐藏登录窗口
            # self.pack_forget()
            # 销毁登录窗口
            self.destroy()
            # 进入主页面
            self.controller.main_application_page = MainApplicationPage(self.master, self)
            self.controller.main_application_page.draw()
            self.master.update_idletasks()
        else:
            messagebox.showerror("Error", "Login failed")
