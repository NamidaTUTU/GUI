import ttkbootstrap as ttk
from base_page import BasePage  # 导入 BasePage
from order_query import OrderQueryPage  # 导入查询订单页面
from other_func import OtherFunc  # 导入订单详情页面


# 主应用页面，继承自 BasePage
class MainApplicationPage(BasePage):
    def __init__(self, master: ttk.Window, controller):
        self.controller = controller
        # 获取当前屏幕的分辨率
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        # 动态计算合适的窗口大小，比如屏幕分辨率的
        width = int(screen_width * 0.8)
        height = int(screen_height * 0.8)
        # 初始化 BasePage 类并设置窗口大小
        super().__init__(master, width=width, height=height)
        self.master.wm_title("Main Application")  # 设置主窗口标题
        self.master = master
        self.notebook = None
        self.order_query_page = None
        self.order_detail_page = None

    def draw(self):
        # 创建 Notebook 容器
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill="both", expand=True)

        # 创建“查询订单”选项卡
        self.order_query_page = OrderQueryPage(self.notebook)
        self.order_query_page.draw()
        # 在查询订单选项卡中嵌入 OrderQueryPage
        self.notebook.add(self.order_query_page, text="查询订单")

        # 创建“其他功能”选项卡
        self.order_detail_page = OtherFunc(self.notebook)
        self.order_detail_page.draw()
        # 在订单详情选项卡中嵌入 OtherFunc
        self.notebook.add(self.order_detail_page, text="其他功能1")

        # 可以添加其他选项卡
        # extra_frame = ttk.Frame(self.notebook)
        # self.notebook.add(extra_frame, text="其他功能2")
        # ttk.Label(extra_frame, text="此处可以添加其他功能").pack(pady=20)

        # 绑定关闭窗口时的回调函数
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """在关闭主窗口时退出程序"""
        self.notebook.destroy()
        # 停止主循环
        self.master.quit()
        # 销毁主窗口
        self.master.destroy()
