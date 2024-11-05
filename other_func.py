import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY
from base_page import BasePage  # 继承 BasePage


class OtherFunc(BasePage):  # 继承 BasePage
    def __init__(self, notebook):
        super().__init__(notebook)
        self.inner_frame = None
        self.label = None
        self.entries = None

    def draw(self):
        self.inner_frame = ttk.Frame(self)
        self.inner_frame.pack(fill="both", expand=True)
        self.label = ttk.Label(self.inner_frame, text="其他功能页面", style="primary.TLabel")
        self.label.pack(pady=20)
        # 创建输入框
        self.entries = []
        for i in range(5):
            entry = ttk.Entry(self.inner_frame)
            entry.pack(pady=5)
            self.entries.append(entry)
        # 创建保存按钮
        save_button = ttk.Button(self.inner_frame, text="保存订单", style="primary.TButton", command=self.save_order)
        save_button.pack(pady=10)

    def save_order(self):
        details = [entry.get() for entry in self.entries]
        print("保存订单详细信息:", details)
