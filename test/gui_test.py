import os.path
import time
import unittest
from unittest.mock import patch

import ttkbootstrap as ttk
from tkinter import messagebox, filedialog

from controller import Controller
from login_page import LoginPage
from main_application import MainApplicationPage


# from typing import Callable, Optional


class TestMainAppLogin(unittest.TestCase):
    def setUp(self):
        self.master = ttk.Window()
        # 控制器
        self.controller = Controller(self.master)

    def tearDown(self):
        # 延时销毁以避免 TclError
        self.master.after(100, self.master.destroy)
        # 确保足够的时间完成操作
        time.sleep(0.1)

    def test_login_page_elements(self):
        """Test if login page elements are present."""
        title = self.master.title()
        self.assertEquals("Order Management System", title)

        username_label = self.controller.login_page.nametowidget(self.controller.login_page.username_label)
        password_label = self.controller.login_page.nametowidget(self.controller.login_page.password_label)

        self.assertIsInstance(username_label, ttk.Label)
        self.assertIsInstance(password_label, ttk.Label)

        username_entry = self.controller.login_page.nametowidget(self.controller.login_page.username_entry)
        password_entry = self.controller.login_page.nametowidget(self.controller.login_page.password_entry)
        login_button = self.controller.login_page.nametowidget(self.controller.login_page.login_button)

        self.assertIsInstance(username_entry, ttk.Entry)
        self.assertIsInstance(password_entry, ttk.Entry)
        self.assertIsInstance(login_button, ttk.Button)

    def test_login_to_main(self):
        """Test if login transitions to the main page with correct username."""
        # Simulate entering username and password
        self.controller.login_page.username_entry.insert(0, "admin")
        self.controller.login_page.password_entry.insert(0, "1234")

        with patch("tkinter.messagebox.showinfo") as mock_showinfo:
            # Simulate button click with empty credentials
            self.controller.login_page.login_button.invoke()
            # Assert messagebox was called with correct arguments
            mock_showinfo.assert_called_once_with("Info", "Login successful")

        # 断言login_page有destroy
        login_page_winfo_exists = self.controller.login_page.winfo_exists()
        self.assertEquals(login_page_winfo_exists, False)

        # 判断main_application_page是否存在
        main_application_page_winfo_exists = self.controller.main_application_page.winfo_exists()
        self.assertEquals(main_application_page_winfo_exists, True)

        # 断言是否跳转到main_application_page
        # 断言main_application_page的title是否为Main Application
        main_application_page_title = self.master.title()
        self.assertEquals(main_application_page_title, "Main Application")

    def test_login_failed(self):
        """Test if login fails with incorrect credentials."""
        # Simulate entering incorrect username and password
        self.controller.login_page.username_entry.insert(0, "user")
        self.controller.login_page.password_entry.insert(0, "wrong_password")

        with patch("tkinter.messagebox.showerror") as mock_showerror:
            # Simulate button click with incorrect credentials
            self.controller.login_page.login_button.invoke()
            # Assert messagebox was called with correct arguments
            mock_showerror.assert_called_once_with("Error", "Login failed")

        # 断言login_page没有destroy
        login_page_winfo_exists = self.controller.login_page.winfo_exists()
        self.assertEquals(login_page_winfo_exists, True)

        # 断言main_application_page不存在
        main_application_page = self.controller.main_application_page
        self.assertEquals(main_application_page, None)

        # 断言没有跳转到main_application_page
        # 断言main_application_page的title 不是 Main Application
        main_application_page_title = self.master.title()
        self.assertEquals(main_application_page_title, "Order Management System")


class TestMainApplicationPage(unittest.TestCase):
    def setUp(self):
        self.master = ttk.Window()
        # 控制器
        self.controller = Controller(self.master)
        self.controller.login_page.destroy()
        # 进入主页面
        self.controller.main_application_page = MainApplicationPage(self.master, self)
        self.controller.main_application_page.draw()
        self.master.update_idletasks()

    def tearDown(self):
        # 延时销毁以避免 TclError
        self.master.after(100, self.master.destroy)
        # 确保足够的时间完成操作
        time.sleep(0.1)
        # 停止主循环
        self.master.quit()
        # 销毁主窗口
        self.master.destroy()

    def test_create_main_application_page(self):
        title = self.master.title()
        self.assertEquals("Main Application", title)

        # 断言main_application_page存在
        main_application_page_winfo_exists = self.controller.main_application_page.winfo_exists()
        self.assertEquals(main_application_page_winfo_exists, True)

        # 断言main_application_page的width和height
        main_application_page_width = self.controller.main_application_page.width
        main_application_page_height = self.controller.main_application_page.height
        self.assertEquals(main_application_page_width, self.master.winfo_screenwidth() * 0.8)
        self.assertEquals(main_application_page_height, self.master.winfo_screenheight() * 0.8)

    def test_main_application_page_elements(self):
        """Test if main application page elements are present."""
        # 断言main_application_page的notebook存在
        notebook_winfo_exists = self.controller.main_application_page.notebook.winfo_exists()
        self.assertEquals(notebook_winfo_exists, True)

        # 断言main_application_page的order_query_page存在
        order_query_page_winfo_exists = self.controller.main_application_page.order_query_page.winfo_exists()
        self.assertEquals(order_query_page_winfo_exists, True)

        # 断言main_application_page的order_detail_page存在
        order_detail_page_winfo_exists = self.controller.main_application_page.order_detail_page.winfo_exists()
        self.assertEquals(order_detail_page_winfo_exists, True)

        # 断言main_application_page的order_query_page的title是否为Order Query
        notebook = self.controller.main_application_page.order_query_page.master
        # 获取第一个选项卡的名称
        order_query_page_table_name = notebook.tab(0, "text")
        self.assertEquals(order_query_page_table_name, "查询订单")
        # 获取第二个选项卡的名称
        other_func_page_table_name = notebook.tab(1, "text")
        self.assertEquals(other_func_page_table_name, "其他功能1")
        # 获取所有选项卡的名称
        tab_names = [notebook.tab(i, "text") for i in range(notebook.index("end"))]
        # print(tab_names)  # 输出: ['选项卡 1', '选项卡 2']
        self.assertEquals(tab_names, ["查询订单", "其他功能1"])


class TestOrderQueryPage(unittest.TestCase):
    def setUp(self):
        self.master = ttk.Window()
        # 控制器
        self.controller = Controller(self.master)
        self.controller.login_page.destroy()
        # 进入主页面
        self.controller.main_application_page = MainApplicationPage(self.master, self)
        self.controller.main_application_page.draw()
        self.master.update_idletasks()
        #
        self.order_query_page = self.controller.main_application_page.order_query_page
        #
        self.pumpe_messung_template_file_path = "../data/Pumpe_Messung_template.xlsx"
        self.pumpe_messung_template_length = 9

    def tearDown(self):
        # 延时销毁以避免 TclError
        self.master.after(100, self.master.destroy)
        # 确保足够的时间完成操作
        time.sleep(0.1)
        # 停止主循环
        self.master.quit()
        # 销毁主窗口
        self.master.destroy()

    def test_create_order_query_page(self):
        """Test if order query page is created."""
        title = self.master.title()
        self.assertEquals("Main Application", title)

        # 断言order_query_page存在
        order_query_page_winfo_exists = self.controller.main_application_page.order_query_page.winfo_exists()
        self.assertEquals(order_query_page_winfo_exists, True)

        # 断言order_query_page的width和height
        order_query_page_width = self.controller.main_application_page.order_query_page.winfo_width()
        order_query_page_height = self.controller.main_application_page.order_query_page.winfo_height()
        self.assertEquals(order_query_page_width, self.order_query_page.winfo_width())
        self.assertEquals(order_query_page_height, self.order_query_page.winfo_height())

    def test_order_query_page_attributes(self):
        """Test if order query page attributes are set."""
        # 断言order_query_page 包含 test_typs attribute
        self.assertTrue(hasattr(self.controller.main_application_page.order_query_page, "test_typs"))

        # 断言order_query_page 包含 query_mapping attribute
        self.assertTrue(hasattr(self.controller.main_application_page.order_query_page, "query_mapping"))

        # 断言order_query_page 包含 column_mapping attribute
        self.assertTrue(hasattr(self.controller.main_application_page.order_query_page, "column_mapping"))

        # 断言order_query_page 包含 unit_mapping attribute
        self.assertTrue(hasattr(self.controller.main_application_page.order_query_page, "unit_mapping"))

        # 断言order_query_page 包含 button_click_mapping attribute
        self.assertTrue(hasattr(self.controller.main_application_page.order_query_page, "button_click_mapping"))

        # 断言order_query_page 包含 display_columns attribute
        self.assertTrue(hasattr(self.controller.main_application_page.order_query_page, "display_columns"))

        # 断言order_query_page 包含 display_df attribute
        self.assertTrue(hasattr(self.controller.main_application_page.order_query_page, "display_df"))

    def test_order_query_page_elements(self):
        """Test if order query page elements are present."""
        # 输入框和下拉框
        sachnummer_label_winfo_exists = self.order_query_page.sachnummer_label.winfo_exists()
        self.assertEquals(sachnummer_label_winfo_exists, True)
        sachnummer_label = self.order_query_page.sachnummer_label.cget("text")
        self.assertEquals(sachnummer_label, "Sachnummer:")
        sachnummer_entry_winfo_exists = self.order_query_page.sachnummer_entry.winfo_exists()
        self.assertEquals(sachnummer_entry_winfo_exists, True)

        test_typ_label_winfo_exists = self.order_query_page.test_typ_label.winfo_exists()
        self.assertEquals(test_typ_label_winfo_exists, True)
        test_typ_label = self.order_query_page.test_typ_label.cget("text")
        self.assertEquals(test_typ_label, "Type of Measurement:")
        test_typ_entry_winfo_exists = self.order_query_page.test_typ_entry.winfo_exists()
        self.assertEquals(test_typ_entry_winfo_exists, True)

        # 清空
        clear_button_winfo_exists = self.order_query_page.clear_button.winfo_exists()
        self.assertEquals(clear_button_winfo_exists, True)
        clear_button_text = self.order_query_page.clear_button.cget("text")
        self.assertEquals(clear_button_text, "Clear")

        # 查询
        query_button_winfo_exists = self.order_query_page.query_button.winfo_exists()
        self.assertEquals(query_button_winfo_exists, True)
        query_button_text = self.order_query_page.query_button.cget("text")
        self.assertEquals(query_button_text, "Query")

        # 导入
        import_button_winfo_exists = self.order_query_page.import_button.winfo_exists()
        self.assertEquals(import_button_winfo_exists, True)
        import_button_text = self.order_query_page.import_button.cget("text")
        self.assertEquals(import_button_text, "Import File")

        # 导出
        export_button_winfo_exists = self.order_query_page.export_button.winfo_exists()
        self.assertEquals(export_button_winfo_exists, True)
        export_button_text = self.order_query_page.export_button.cget("text")
        self.assertEquals(export_button_text, "Export File")

        # 断言order_query_page的tree存在
        order_query_page_tree_winfo_exists = self.order_query_page.tree.winfo_exists()
        self.assertEquals(order_query_page_tree_winfo_exists, True)

        # 断言order_query_page的scrollbar存在
        order_query_page_scrollbar_winfo_exists = self.order_query_page.scrollbar.winfo_exists()
        self.assertEquals(order_query_page_scrollbar_winfo_exists, True)

        # 断言order_query_page的hscrollbar存在
        order_query_page_hscrollbar_winfo_exists = self.order_query_page.hscrollbar.winfo_exists()
        self.assertEquals(order_query_page_hscrollbar_winfo_exists, True)

        # 断言order_query_page的prev_button存在
        order_query_page_prev_button_winfo_exists = self.order_query_page.prev_button.winfo_exists()
        self.assertEquals(order_query_page_prev_button_winfo_exists, True)
        prev_button_text = self.order_query_page.prev_button.cget("text")
        self.assertEquals(prev_button_text, "Previous Page")

        # 断言order_query_page的next_button存在
        order_query_page_next_button_winfo_exists = self.order_query_page.next_button.winfo_exists()
        self.assertEquals(order_query_page_next_button_winfo_exists, True)
        next_button_text = self.order_query_page.next_button.cget("text")
        self.assertEquals(next_button_text, "Next Page")

        # 断言order_query_page的page_label存在
        order_query_page_page_label_winfo_exists = self.order_query_page.page_label.winfo_exists()
        self.assertEquals(order_query_page_page_label_winfo_exists, True)
        page_label_text = self.order_query_page.page_label.cget("text")
        self.assertTrue("Page" in page_label_text and "/" in page_label_text)

    @patch('tkinter.messagebox.showerror')
    @patch("tkinter.filedialog.askopenfilename")
    def test_import_excel_file_to_failed(self, mock_askopenfilename, mock_showerror):
        """
        测试导入excel文件数据
        找不到文件路径而报错
        """
        # 前置条件设置 mock_askopenfilename 值
        mock_askopenfilename.return_value = "/path/to/excel.xlsx"
        file_path = mock_askopenfilename.return_value
        # 调用函数并断言返回值
        self.assertEquals(file_path, "/path/to/excel.xlsx")

        # Simulate button click
        self.order_query_page.import_button.invoke()
        # 验证 askopenfilename 被调用
        print("call_count:", mock_askopenfilename.call_count)
        mock_askopenfilename.assert_called_once()
        # 验证 askopenfilename 被调用过
        mock_askopenfilename.assert_called()

        # 验证 showerror 被调用，并且传递了正确的参数
        mock_showerror.assert_called_once_with("Error", "An error occurred while importing the file:\n[Errno 2] No such file or directory: '/path/to/excel.xlsx'")

    @patch('tkinter.messagebox.showerror')
    @patch("tkinter.filedialog.askopenfilename")
    def test_import_excel_file_to_failed_by_unsupported_file_format(self, mock_askopenfilename, mock_showerror):
        """
        测试导入excel文件数据
        不能解析的文件格式错误
        """
        # 前置条件设置 mock_askopenfilename 值
        mock_askopenfilename.return_value = "/path/to/excel.txt"  # unsupported_file_format
        file_path = mock_askopenfilename.return_value
        # 调用函数并断言返回值
        self.assertEquals(file_path, "/path/to/excel.txt")

        # Simulate button click
        self.order_query_page.import_button.invoke()
        # 验证 askopenfilename 被调用
        print("call_count:", mock_askopenfilename.call_count)
        mock_askopenfilename.assert_called_once()
        # 验证 askopenfilename 被调用过
        mock_askopenfilename.assert_called()

        # 验证 showerror 被调用，并且传递了正确的参数
        mock_showerror.assert_called_once_with("Error", "Unsupported file format.")

    @patch('tkinter.messagebox.showinfo')
    @patch("tkinter.filedialog.askopenfilename")
    def test_import_excel_file_to_success(self, mock_askopenfilename, mock_showinfo):
        # 前置条件设置 mock_askopenfilename 值 (这里需要设置正确的文件路径, 才能正确导入文件)
        mock_askopenfilename.return_value = self.pumpe_messung_template_file_path
        file_path = mock_askopenfilename.return_value
        # 调用函数并断言返回值
        self.assertEquals(file_path, self.pumpe_messung_template_file_path)

        # 断言 tree 存在并且长度等于0
        order_query_page_tree_winfo_exists = self.order_query_page.tree.winfo_exists()
        self.assertEquals(order_query_page_tree_winfo_exists, True)
        tree_length = len(self.order_query_page.tree.get_children())
        self.assertEquals(tree_length, 0)

        # Simulate button click
        self.order_query_page.import_button.invoke()
        # 验证 askopenfilename 被调用
        print("call_count:", mock_askopenfilename.call_count)
        mock_askopenfilename.assert_called_once()
        # 验证 askopenfilename 被调用过
        mock_askopenfilename.assert_called()

        # 验证 showinfo 被调用，并且传递了正确的参数
        mock_showinfo.assert_called_once_with("Success", "File imported successfully!")

        # 断言 tree 存在并且长度等于导入数据的长度
        order_query_page_tree_winfo_exists = self.order_query_page.tree.winfo_exists()
        self.assertEquals(order_query_page_tree_winfo_exists, True)
        tree_length = len(self.order_query_page.tree.get_children())
        #
        self.assertEquals(tree_length, self.pumpe_messung_template_length)

        # 断言分页内容
        # 断言order_query_page的prev_button存在
        order_query_page_prev_button_winfo_exists = self.order_query_page.prev_button.winfo_exists()
        self.assertEquals(order_query_page_prev_button_winfo_exists, True)
        prev_button_text = self.order_query_page.prev_button.cget("text")
        self.assertEquals(prev_button_text, "Previous Page")
        # 断言order_query_page的prev_button不可用
        order_query_page_prev_button_state = self.order_query_page.prev_button.cget('state').string
        self.assertEquals(order_query_page_prev_button_state, "disabled")

        # 断言order_query_page的next_button存在
        order_query_page_next_button_winfo_exists = self.order_query_page.next_button.winfo_exists()
        self.assertEquals(order_query_page_next_button_winfo_exists, True)
        next_button_text = self.order_query_page.next_button.cget("text")
        self.assertEquals(next_button_text, "Next Page")
        # 断言order_query_page的next_button不可用
        order_query_page_next_button_state = self.order_query_page.next_button.cget('state').string
        self.assertEquals(order_query_page_next_button_state, "disabled")

        # 断言order_query_page的page_label存在
        order_query_page_page_label_winfo_exists = self.order_query_page.page_label.winfo_exists()
        self.assertEquals(order_query_page_page_label_winfo_exists, True)
        page_label_text = self.order_query_page.page_label.cget("text")
        self.assertEquals(page_label_text, "Page 1 / 1")  # 每页10条

    @patch('tkinter.messagebox.showinfo')
    @patch("tkinter.filedialog.askopenfilename")
    def test_query_data(self, mock_askopenfilename, mock_showinfo):
        """Test if query data is correct."""
        # 导入数据
        mock_askopenfilename.return_value = self.pumpe_messung_template_file_path
        file_path = mock_askopenfilename.return_value
        # 调用函数并断言返回值
        self.assertEquals(file_path, self.pumpe_messung_template_file_path)
        # Simulate button click
        self.order_query_page.import_button.invoke()
        # 验证 askopenfilename 被调用
        mock_askopenfilename.assert_called_once()
        # 检查第一次 showinfo 被调用，并且传递了正确的参数
        first_call_args = mock_showinfo.call_args_list[0]
        first_call_args.assert_called_once_with("Success", "File imported successfully!")
        # 断言 tree 存在并且长度等于导入数据的长度
        order_query_page_tree_winfo_exists = self.order_query_page.tree.winfo_exists()
        self.assertEquals(order_query_page_tree_winfo_exists, True)
        tree_length = len(self.order_query_page.tree.get_children())
        self.assertEquals(tree_length, self.pumpe_messung_template_length)

        # 设置查询参数
        self.order_query_page.sachnummer_entry.insert(0, "039020243F")
        # test_typ_entry 参数可选值列表
        # ["A", "Q", "Z", "Null-Serie", "Claim（TKU）", "Sonder", "BlockForce"]
        # self.order_query_page.test_typ_entry.set("Null-Serie")
        self.order_query_page.test_typ_entry.insert(0, "Sonder")

        # Simulate button click
        self.order_query_page.query_button.invoke()

        # 检查第二次 showinfo 被调用，并且传递了正确的参数
        second_call_args = mock_showinfo.call_args_list[1]
        second_call_args.assert_called_once_with("info", "Query successful")

        # 断言 tree 存在并且长度等于筛选后数据的长度
        tree_length = len(self.order_query_page.tree.get_children())
        pumpe_messung_filtered_data_length = 1
        self.assertEquals(tree_length, pumpe_messung_filtered_data_length)

    @patch('tkinter.messagebox.showinfo')
    @patch("tkinter.filedialog.askopenfilename")
    def test_clear_query(self, mock_askopenfilename, mock_showinfo):
        """Test if clear query is correct."""
        # 导入数据
        mock_askopenfilename.return_value = self.pumpe_messung_template_file_path
        file_path = mock_askopenfilename.return_value
        # 调用函数并断言返回值
        self.assertEquals(file_path, self.pumpe_messung_template_file_path)
        # Simulate button click
        self.order_query_page.import_button.invoke()
        # 验证 askopenfilename 被调用
        mock_askopenfilename.assert_called_once()
        # 检查第一次 showinfo 被调用，并且传递了正确的参数
        first_call_args = mock_showinfo.call_args_list[0]
        first_call_args.assert_called_once_with("Success", "File imported successfully!")
        # 断言 tree 存在并且长度等于导入数据的长度
        order_query_page_tree_winfo_exists = self.order_query_page.tree.winfo_exists()
        self.assertEquals(order_query_page_tree_winfo_exists, True)
        tree_length = len(self.order_query_page.tree.get_children())
        self.assertEquals(tree_length, self.pumpe_messung_template_length)

        # 设置查询参数
        self.order_query_page.sachnummer_entry.insert(0, "039020243F")
        # test_typ_entry 参数可选值列表
        # ["A", "Q", "Z", "Null-Serie", "Claim（TKU）", "Sonder", "BlockForce"]
        # self.order_query_page.test_typ_entry.set("Null-Serie")
        self.order_query_page.test_typ_entry.insert(0, "Sonder")

        # Simulate button click
        self.order_query_page.query_button.invoke()

        # 检查第二次 showinfo 被调用，并且传递了正确的参数
        second_call_args = mock_showinfo.call_args_list[1]
        second_call_args.assert_called_once_with("info", "Query successful")

        # 断言 tree 存在并且长度等于筛选后数据的长度
        tree_length = len(self.order_query_page.tree.get_children())
        pumpe_messung_filtered_data_length = 1
        self.assertEquals(tree_length, pumpe_messung_filtered_data_length)

        # Simulate clear_button click
        self.order_query_page.clear_button.invoke()
        # 断言 查询参数清空
        self.assertEquals(self.order_query_page.sachnummer_entry.get(), "")
        self.assertEquals(self.order_query_page.test_typ_entry.get(), "")

        # 检查第三次 showinfo 被调用，并且传递了正确的参数
        # third_call_args = mock_showinfo.call_args_list[2]
        # third_call_args.assert_called_once_with("info", "Query cleared")

        # 断言 tree 存在并且长度等于筛选后数据的长度
        tree_length = len(self.order_query_page.tree.get_children())
        self.assertEquals(tree_length, self.pumpe_messung_template_length)

    def test_detail_page_elements(self):
        """Test if detail page elements are correct."""
        pass


if __name__ == "__main__":
    unittest.main()


#
# class TestPoisonDartCase(unittest.TestCase):
#
#     def setUp(self) -> None:
#         self.poison_dart = PoisonDart()
#
#     def test_get_name(self):
#         self.assertEquals(self.poison_dart.get_name(), 'PoisonDart')
#
#     def test_get_symbol(self):
#         self.assertEquals(self.poison_dart.get_symbol(), 'D')
#
#     def test_get_effect(self):
#         self.assertEquals(self.poison_dart.get_effect(), {'poison': 2})
#
#     def test_get_targets(self):
#         position = (1, 1)
#         self.assertEquals(self.poison_dart.get_targets(position),
#                           [(1, 2), (1, 0), (2, 1), (0, 1), (1, 3), (1, -1),
#                            (3, 1), (-1, 1)])
#         position = (8, 8)
#         self.assertEquals(self.poison_dart.get_targets(position),
#                           [(8, 9), (8, 7), (9, 8), (7, 8), (8, 10), (8, 6),
#                            (10, 8), (6, 8)])
#
#     def test_str(self):
#         self.assertEquals(str(self.poison_dart), 'PoisonDart')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.poison_dart), 'PoisonDart()')
#
#
# class TestPoisonSwordCase(unittest.TestCase):
#
#     def setUp(self) -> None:
#         self.poison_sword = PoisonSword()
#
#     def test_get_name(self):
#         self.assertEquals(self.poison_sword.get_name(), 'PoisonSword')
#
#     def test_get_symbol(self):
#         self.assertEquals(self.poison_sword.get_symbol(), 'S')
#
#     def test_get_effect(self):
#         self.assertEquals(self.poison_sword.get_effect(),
#                           {'damage': 2, 'poison': 1})
#
#     def test_get_targets(self):
#         position = (1, 1)
#         self.assertEquals(self.poison_sword.get_targets(position),
#                           [(1, 2), (1, 0), (2, 1), (0, 1)])
#         position = (0, 0)
#         self.assertEquals(self.poison_sword.get_targets(position),
#                           [(0, 1), (0, -1), (1, 0), (-1, 0)])
#
#     def test_str(self):
#         self.assertEquals(str(self.poison_sword), 'PoisonSword')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.poison_sword), 'PoisonSword()')
#
#
# class TestHealingRockCase(unittest.TestCase):
#
#     def setUp(self) -> None:
#         self.healing_rock = HealingRock()
#
#     def test_get_name(self):
#         self.assertEquals(self.healing_rock.get_name(), 'HealingRock')
#
#     def test_get_symbol(self):
#         self.assertEquals(self.healing_rock.get_symbol(), 'H')
#
#     def test_get_effect(self):
#         self.assertEquals(self.healing_rock.get_effect(), {'healing': 2})
#
#     def test_get_targets(self):
#         position = (1, 1)
#         self.assertEquals(self.healing_rock.get_targets(position),
#                           [(1, 2), (1, 0), (2, 1), (0, 1), (1, 3), (1, -1),
#                            (3, 1), (-1, 1)])
#
#     def test_str(self):
#         self.assertEquals(str(self.healing_rock), 'HealingRock')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.healing_rock), 'HealingRock()')
#
#
# class TestTileCase(unittest.TestCase):
#
#     def setUp(self) -> None:
#         self.tile = Tile("#", True)
#
#     def test_is_blocking(self):
#         self.assertEquals(self.tile.is_blocking(), True)
#
#     def test_get_weapon(self):
#         self.assertEquals(self.tile.get_weapon(), None)
#
#     def test_get_weapon2(self):
#         healing_rock = HealingRock()
#         self.tile.set_weapon(healing_rock)
#         self.assertEquals(self.tile.get_weapon(), healing_rock)
#         self.assertEquals(self.tile.get_weapon().get_effect(), {'healing': 2})
#
#     def test_remove_weapon(self):
#         healing_rock = HealingRock()
#         self.tile.set_weapon(healing_rock)
#         self.assertEquals(self.tile.get_weapon(), healing_rock)
#         self.assertEquals(self.tile.get_weapon().get_effect(), {'healing': 2})
#         #
#         self.tile.remove_weapon()
#         self.assertEquals(self.tile.get_weapon(), None)
#
#     def test_str(self):
#         self.assertEquals(str(self.tile), '#')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.tile), "Tile('#', True)")
#
#     def test_custom_repr(self):
#         tile = Tile("hello", False)
#         self.assertEquals(repr(tile), "Tile('hello', False)")
#         self.assertEquals(tile.is_blocking(), False)
#
#
# class TestCreateTileCase(unittest.TestCase):
#
#     def test_create_tile(self):
#         wall = create_tile('#')
#         self.assertEquals(repr(wall), "Tile('#', True)")
#         self.assertEquals(wall.is_blocking(), True)
#         self.assertEquals(wall.get_weapon(), None)
#         #
#         floor = create_tile(' ')
#         self.assertEquals(repr(floor), "Tile(' ', False)")
#         #
#         weapon_tile = create_tile('D')
#         self.assertEquals(repr(weapon_tile), "Tile(' ', False)")
#         self.assertEquals(repr(weapon_tile.get_weapon()), "PoisonDart()")
#
#
# class TestEntityCase(unittest.TestCase):
#
#     def setUp(self):
#         self.entity = Entity(10)
#
#     def test_get_symbol(self):
#         self.assertEquals(self.entity.get_symbol(), 'E')
#
#     def test_get_name(self):
#         self.assertEquals(self.entity.get_name(), 'Entity')
#
#     def test_get_poison(self):
#         self.assertEquals(self.entity.get_poison(), 0)
#
#     def test_get_weapon(self):
#         self.assertEquals(self.entity.get_weapon(), None)
#
#     def test_get_weapon_targets(self):
#         self.assertEquals(self.entity.get_weapon_targets((1, 1)), [])
#
#     def test_get_weapon_effect(self):
#         self.assertEquals(self.entity.get_weapon_effect(), {})
#
#     def test_equip(self):
#         poison_sword = PoisonSword()
#         self.entity.equip(poison_sword)
#         self.assertEquals(self.entity.get_weapon(), poison_sword)
#         self.assertEquals(self.entity.get_weapon_targets((0, 0)),
#                           [(0, 1), (0, -1), (1, 0), (-1, 0)])
#         self.assertEquals(self.entity.get_weapon_effect(),
#                           {'damage': 2, 'poison': 1})
#
#     def test_apply_effects_and_apply_poison(self):
#         self.entity.apply_effects({'poison': 4, 'damage': 3})
#         self.assertEquals(self.entity.get_health(), 7)
#         self.assertEquals(self.entity.get_poison(), 4)
#         #
#         self.entity.apply_poison()
#         self.assertEquals(self.entity.get_health(), 3)
#         self.assertEquals(self.entity.get_poison(), 3)
#         #
#         self.entity.apply_effects({'healing': 20})
#         self.assertEquals(self.entity.get_health(), 10)
#
#     def test_str(self):
#         self.assertEquals(str(self.entity), 'Entity')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.entity), 'Entity(10)')
#
#
# class TestPlayerCase(unittest.TestCase):
#
#     def setUp(self):
#         self.player = Player(20)
#
#     def test_str(self):
#         self.assertEquals(str(self.player), 'Player')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.player), 'Player(20)')
#
#     def test_equip_and_apply_effects(self):
#         poison_dart = PoisonDart()
#         self.player.equip(poison_dart)
#         self.assertEquals(self.player.get_weapon_effect(), {'poison': 2})
#         self.player.apply_effects({'damage': 25})
#         self.assertEquals(self.player.get_health(), 0)
#
#
# class TestSlugCase(unittest.TestCase):
#
#     def setUp(self):
#         self.slug = Slug(5)
#
#     def test_case(self):
#         healing_rock = HealingRock()
#         self.slug.equip(healing_rock)
#         self.assertEquals(self.slug.get_weapon_effect(), {'healing': 2})
#         #
#         self.assertEquals(self.slug.can_move(), True)
#         #
#         self.slug.end_turn()
#         self.assertEquals(self.slug.can_move(), False)
#         self.assertEquals(self.slug.can_move(), False)
#         self.slug.end_turn()
#         self.assertEquals(self.slug.can_move(), True)
#         #
#         try:
#             self.slug.choose_move([(0, 0), (1, 1)], (1, 0), (2, 4))
#         except NotImplementedError:
#             pass
#
#     def test_str(self):
#         self.assertEquals(str(self.slug), 'Slug')
#
#     def test_repr(self):
#         self.assertEquals(repr(self.slug), 'Slug(5)')
#
#
# class TestNiceSlugCase(unittest.TestCase):
#
#     def setUp(self):
#         self.nice_slug = NiceSlug()
#
#     def test_case(self):
#         self.assertEquals(repr(self.nice_slug), 'NiceSlug()')
#         #
#         self.assertEquals(str(self.nice_slug), 'NiceSlug')
#         #
#         self.assertEquals(self.nice_slug.get_health(), 10)
#         #
#         self.assertEquals(repr(self.nice_slug.get_weapon()), "HealingRock()")
#         #
#         self.assertEquals(self.nice_slug.get_weapon_effect(), {'healing': 2})
#         #
#         self.assertEquals(
#             self.nice_slug.choose_move([(0, 1), (1, 0), (1, 2), (2, 1)], (1, 1),
#                                        (2, 4)), (1, 1))
#
#
# class TestAngrySlugCase(unittest.TestCase):
#
#     def setUp(self):
#         self.angry_slug = AngrySlug()
#
#     def test_case(self):
#         self.assertEquals(repr(self.angry_slug), 'AngrySlug()')
#         #
#         self.assertEquals(str(self.angry_slug), 'AngrySlug')
#         #
#         self.assertEquals(self.angry_slug.get_health(), 5)
#         #
#         self.assertEquals(repr(self.angry_slug.get_weapon()), "PoisonSword()")
#         #
#         self.assertEquals(self.angry_slug.get_weapon_effect(),
#                           {'damage': 2, 'poison': 1})
#         #
#         self.assertEquals(
#             self.angry_slug.choose_move([(0, 1), (1, 0), (1, 2), (2, 1)],
#                                         (1, 1), (2, 4)), (1, 2))
#
#
# class TestScaredSlugCase(unittest.TestCase):
#
#     def setUp(self):
#         self.scared_slug = ScaredSlug()
#
#     def test_case(self):
#         self.assertEquals(repr(self.scared_slug), 'ScaredSlug()')
#         #
#         self.assertEquals(str(self.scared_slug), 'ScaredSlug')
#         #
#         self.assertEquals(self.scared_slug.get_health(), 3)
#         #
#         self.assertEquals(repr(self.scared_slug.get_weapon()), "PoisonDart()")
#         #
#         self.assertEquals(self.scared_slug.get_weapon_effect(), {'poison': 2})
#         #
#         self.assertEquals(
#             self.scared_slug.choose_move([(0, 1), (1, 0), (1, 2), (2, 1)],
#                                          (1, 1), (2, 4)), (1, 0))
#
#
# class TestSlugDungeonModelCase(unittest.TestCase):
#
#     def setUp(self):
#         self.tiles = [
#             [create_tile("#"), create_tile("#"), create_tile("#"),
#              create_tile("#")],
#             [create_tile("#"), create_tile(" "), create_tile(" "),
#              create_tile("#")],
#             [create_tile("#"), create_tile(" "), create_tile(" "),
#              create_tile("#")],
#             [create_tile("#"), create_tile("S"), create_tile("G"),
#              create_tile("#")],
#             [create_tile("#"), create_tile("#"), create_tile("#"),
#              create_tile("#")]
#         ]
#         self.slugs = {(1, 1): AngrySlug()}
#         self.player = Player(20)
#         self.model = SlugDungeonModel(self.tiles, self.slugs, self.player,
#                                       (2, 1))
#
#     def test_case(self):
#         self.assertEquals(self.model.get_tiles(), self.tiles)
#         #
#         self.assertEquals(self.model.get_slugs(), self.slugs)
#         #
#         self.assertEquals(repr(self.model.get_player()), "Player(20)")
#         #
#         self.assertEquals(self.model.get_player_position(), (2, 1))
#         #
#         self.assertEquals(repr(self.model.get_tile((0, 0))),
#                           repr(Tile('#', True)))
#         self.assertEquals(repr(self.model.get_tile((2, 1))),
#                           repr(Tile(' ', False)))
#         self.assertEquals(self.model.get_dimensions(), (5, 4)),
#         #
#         angry_slug = self.model.get_slugs().get((1, 1))
#         self.assertEquals(angry_slug.get_health(), 5)
#         self.assertEquals(angry_slug.get_weapon_effect(),
#                           {'damage': 2, 'poison': 1})
#         self.assertEquals(angry_slug.get_poison(), 0)
#         #
#         self.assertEquals(self.model.get_player().get_health(), 20)
#         self.assertEquals(self.model.get_player().get_poison(), 0)
#         self.assertEquals(self.model.get_player().get_weapon_effect(), {})
#         # TODO
#         # self.assertEquals(self.model.get_valid_slug_positions(angry_slug), [(1, 1), (1, 2)])
#         #
#         self.model.perform_attack(angry_slug, (1, 1))
#         self.assertEquals(self.model.get_player().get_health(), 18)
#         self.assertEquals(self.model.get_player().get_poison(), 1)
#         #
#         self.model.perform_attack(self.player, self.model.get_player_position())
#         self.assertEquals(angry_slug.get_health(), 5)
#         self.assertEquals(angry_slug.get_poison(), 0)
#         #
#         self.model.handle_player_move((1, 0))
#         self.assertEquals(self.model.get_player().get_health(), 15)
#         self.assertEquals(self.model.get_player().get_poison(), 1)
#         #
#         self.assertEquals(repr(self.player.get_weapon()),
#                           "PoisonSword()")  # Player picked up a weapon when it moved
#         self.assertEquals(self.model.get_player().get_weapon_effect(),
#                           {'damage': 2, 'poison': 1})
#         self.assertEquals(
#             self.player.get_weapon_targets(self.model.get_player_position()),
#             [(3, 2), (3, 0), (4, 1), (2, 1)])
#         #
#         self.assertEquals(angry_slug.get_health(), 5)
#         self.assertEquals(angry_slug.get_poison(), 0)
#         #
#         self.assertEquals(self.model.get_slugs(),
#                           self.slugs)  # {(2, 1): AngrySlug()}
#         self.assertEquals(self.model.get_player_position(), (3, 1))
#         #
#         self.assertEquals(self.model.has_won(), False)
#         self.assertEquals(self.model.has_lost(), False)
#
#     def test_end_turn(self):
#         model = load_level('levels/test_player_move')
#         slugs = {
#             (1, 3): ScaredSlug(),
#             (2, 1): NiceSlug(),
#             (2, 2): AngrySlug(),
#             (2, 4): ScaredSlug(),
#             (4, 2): AngrySlug(),
#         }
#         player = Player(25)
#
#         model2 = SlugDungeonModel(
#             model.get_tiles(), slugs, player, (1, 1)
#         )
#
#         # Preparing some poison for bottom angry slug
#         angry_slug_position = (4, 2)
#         angry_slug = model2.get_slugs().get(angry_slug_position)
#         angry_slug.apply_effects({"poison": 1000})
#
#         # Test bottom slug dies and drops weapon
#         model2.end_turn()
#         self.assertEquals(len(model2.get_slugs()), 4)
#         self.assertEquals(model2.get_tile((4, 2)).get_weapon().get_symbol(), "S")
#
#         # Test poison, healing and damage was applied to player
#         self.assertEquals(player.get_health(), 23)
#         self.assertEquals(player.get_poison(), 3)
#
#         # Test slug movement
#         self.assertEqual(
#             set(model2.get_slugs().keys()),
#             set([(2, 1), (1, 3), (1, 2), (2, 4)])
#         )
#
#         for slug in model2.get_slugs().values():
#             self.assertEquals(slug.can_move(), False)
#
#     def test_player_move(self):
#         model = load_level('levels/test_player_move')
#
#         slugs = {
#             (1, 3): ScaredSlug(),
#             (2, 1): NiceSlug(),
#             (2, 2): AngrySlug(),
#             (2, 4): ScaredSlug(),
#             (4, 2): AngrySlug(),
#         }
#         player = Player(25)
#
#         model2 = SlugDungeonModel(
#             model.get_tiles(), slugs, player, (1, 1)
#         )
#
#         # Setup sword to player right
#         sword = PoisonSword()
#         tile_to_right = model2.get_tile((1, 2))
#         tile_to_right.set_weapon(sword)
#
#         # Player moves right
#         player.apply_effects({"poison": 1, "damage": 5})
#         model2.handle_player_move((0, 1))
#         self.assertNotEqual(model2.get_slugs(), slugs)
#         self.assertEquals(player.get_health(), 25 - 5 - 2 - 1)
#
#         # Assert that player damaged the enemies
#         self.assertEquals(len(model2.get_slugs()), 4)
#         angry_slug_position = (2, 2)
#         angry_slug = model2.get_slugs().get(angry_slug_position)
#         self.assertEquals(angry_slug.get_health(), 2)
