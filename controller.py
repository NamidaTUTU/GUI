import ttkbootstrap as ttk
from login_page import LoginPage


class Controller:
    """
    控制器
    """

    def __init__(self, master: ttk.Window) -> None:
        """
        初始化
        """
        self.master = master
        self.master.wm_title("Order Management System")
        self.style = ttk.Style()
        # 设置主题
        self.style.theme_use('flatly')
        # 创造面板
        self.login_page = LoginPage(self.master, self)
        self.main_application_page = None
        # 绘制
        self.draw()

    def draw(self):
        """
        绘制
        :return: None
        """
        self.login_page.draw()
