import math
from datetime import datetime

import numpy as np
import ttkbootstrap as ttk
import pandas as pd
import chardet
from tkinter import Scrollbar, messagebox, filedialog
from base_page import BasePage


class OrderQueryPage(BasePage):

    def __init__(self, notebook):
        super().__init__(notebook)
        # Dokumentation：
        # 1.Kunde：
        # 2.Typ-Kurzbezeichung
        # 3.Fertigungsdatum
        # 4.Prüfer
        # 5.Prüfungsdatum
        # 6.Musternummer
        # 7.Prüfnummer
        # 第二部分
        # Prüfling
        # 1.Prüfling-Nr:
        # 2.Bemerkung
        # 第三部分
        # Prüfaufbau
        # 1.Prüfaufbau（下拉的可能性：Schaum，frei aufgehängt, Unter Last)
        # 2.Bemerkung
        # 第四部分
        # Prüfvorgaben
        # 1.Prüfvorschrift
        # 2.Prüfspannung
        # 3.Test dauer
        # 4.Prüf-Art
        # 5.Mikrofon Abstand
        # 6.Drehrichtung
        # 7.Drehzahl
        # 第五部分
        # Toleranzprüfung
        # 1.Luftschall-Summegrenzwert :
        # 2.Luftschall-Summe-Straffrequenz:
        # 3.Luftschall-Summe-Endfrequenz:

        # Dokumentation
        # 1.Kunde==‘Kunden‘
        # 2,Tpy-kurzbezeichnung==‘Typ‘
        # 3.Fertigungsdatum自己输入
        # 4.Prüfer 自己输入
        # 5.Prüfungsdatum==‘Prüfdatum‘
        # 6.Prüfung==‘Type of Measurment ‘
        # 7.Musternummer== ‘Musternummer’
        # 8.Prüfnummer  自己输入

        # Prüfling
        # 1.	Prüfling-Nr.==Prüfdatum_Musternummer_W711Bue_空着
        # 2.	Bemerkung 自己输入
        #
        # Prüfaufbau
        # 1.	Prüfaufbau
        # 2.	Last==‘SOLL Prüflast BODY ‘
        #
        # Prüfvorgabe
        # 1.	Prüfvorschrift==‘PV-Nummer ‘
        # 2.	Prüfspannung==‘SOLL Prüfspannung AIR ‘
        # 3.	Test dauer==‘Prüfzeit IST AIR ‘
        # 4.	Prüf-Art dropdawn 自己输入
        # 5.	Mikrofon Abstand==‘SOLL MikrofonAbstand AIR ‘
        # 6.	Drehrichtung==‘Drehrichtung ‘
        # 7.	Drehzahl==‘SOLL Drehzahl BODY ‘
        #
        # Toleranzprüfung
        # 1.	Luftschall-Summengrenzwert==‘Summenpegel SOLL AIR ‘
        # 2.	Luftschall-Summe-Straffrequenz==‘Frequenzband min AIR ‘
        # 3.	Luftschall-Summe-Endfrequenz==‘Frequenzband Max AIR‘
        self.test_typs = ["A", "Q", "Z", "Null-Serie", "Claim（TKU）", "Sonder",
                          "BlockForce"]
        # query 字典
        self.query_mapping = {
            "Null-Serie": "0",
            "Sonder": "s",
        }
        self.column_mapping = {
            "Type of Measurment": "Type of Measurement",
            "Motorsachnummer": "Sachnummer",
            "Prüfdatum": "Fertigungsdatum",
            "Kunde": "Kunden",
            "Typ-Kurzbezeichnung": "Typ",
            "Prüfungsdatum": "Prüfdatum",
            "Musternummer": "Musternummer",
            "Prüfling-Nr": "Prüfdatum_Musternummer_W711Bue_空着",
            "Last": "SOLL Prüflast BODY",
            "Prüfspannung": "SOLL Prüfspannung AIR",
            "Test dauer": "Prüfzeit IST AIR",
            "Mikrofon Abstand": "SOLL MikrofonAbstand AIR",
            "Drehrichtung": "Drehrichtung",
            "Drehzahl": "SOLL Drehzahl BODY",
            "Luftschall-Summegrenzwert": "Summenpegel SOLL AIR",
            "Luftschall-Summe-Straffrequenz": "Frequenzband min AIR",
            "Luftschall-Summe-Endfrequenz": "Frequenzband Max AIR",
            # beng
            "Arbeitspunkt": "Prüfnummer",
            "Sachnummer(SNR)": "Sachnummer",
            "Fertigungsdatum": "Fertigungsdatum",
            "Prüfung": "Type of Measurement",
            "Teil-Nr.": "Musternummer",
            "Prüfvorschrift": "PV-Nummer",
        }
        # 单位字典
        self.unit_mapping = {
            "Prüf-Spannung": "V",
            "Testdauer": "s",
            "Luftschall - Meßabstand": "cm",
            "Förderdruck / Differenzdruck": "kPa",
            "Durchfluß": "I/h",
            "umgerechnet auf": "cm",
            "Luftschall-Summe-Startfrequenz": "Hz",
            "Luftschall-Summe-Endfrequenz": "Hz",
            "Luftschall-Terz-Startfrequenz": "Hz",
            "Luftschall-Terz-Endfrequenz": "Hz",
            "Triax-Summe-Startfrequenz": "Hz",
            "Triax-Summe-Endfrequenz": "Hz",
            "Triax-Terz-Startfrequenz": "Hz",
            "Triax-Terz-Endfrequenz": "Hz",
        }
        self.df = self.generate_mock_data()  # 创建 pandas DataFrame
        self.display_df = pd.DataFrame()  # 用于列表展示的df
        self.display_columns = ["Prüfnummer", "Sachnummer", "Fertigungsdatum", "Type of Measurement",
                                "Musternummer", "PV-Nummer"]
        # 展示页的数据
        self.items_per_page = 10  # 每页显示 10 条
        self.current_page = 0
        self.total_pages = 0
        # 内部frame
        self.inner_frame = None
        # 内部其他组件
        self.sachnummer_entry = None
        self.test_typ_entry = None
        self.tree = None
        #
        self.font = ("Arial", 12)
        self.title_font = ('Arial', 14, 'bold')

    def draw(self):
        self.create_order_query_page()

    def create_order_query_page(self):
        # 创建顶部布局区域，输入框、下拉框、按钮
        self.inner_frame = ttk.Frame(self)
        self.inner_frame.grid(row=0, column=0, padx=20, pady=20, sticky=ttk.EW)

        # 输入框和下拉框
        sachnummer_label = ttk.Label(self.inner_frame, text="Sachnummer:", font=self.font)
        sachnummer_label.grid(row=0, column=0, padx=10, pady=10, sticky=ttk.E)
        self.sachnummer_entry = ttk.Entry(self.inner_frame, font=self.font, width=29)
        self.sachnummer_entry.grid(row=0, column=1, padx=10, pady=10, sticky=ttk.W)

        test_typ_label = ttk.Label(self.inner_frame, text="Type of Measurement:", font=self.font)
        test_typ_label.grid(row=0, column=2, padx=10, pady=10, sticky=ttk.E)
        self.test_typ_entry = ttk.Combobox(self.inner_frame, font=self.font, width=29, values=self.test_typs)
        self.test_typ_entry.grid(row=0, column=3, padx=10, pady=10, sticky=ttk.W)

        # 清空按钮
        clear_button = ttk.Button(self.inner_frame, text="Clear", command=self.clear_query)
        clear_button.grid(row=0, column=4, padx=10, pady=10, sticky=ttk.W)

        # 查询按钮
        query_button = ttk.Button(self.inner_frame, text="Query", command=self.query_order)
        query_button.grid(row=0, column=5, padx=10, pady=10, sticky=ttk.W)

        # 导入文件按钮
        import_button = ttk.Button(self.inner_frame, text="Import File", command=self.import_file)
        import_button.grid(row=0, column=6, padx=10, pady=10, sticky=ttk.W)

        # 导出文件按钮
        export_button = ttk.Button(self.inner_frame, text="Export File", command=self.export_file)
        export_button.grid(row=0, column=7, padx=10, pady=10, sticky=ttk.W)

        # 导出hatx文件按钮
        # export_button = ttk.Button(self.inner_frame, text="Export Hatx File", command=self.export_hatx_file)
        # export_button = ttk.Button(self.inner_frame, text="Export Hatx File", )
        # export_button.grid(row=0, column=8, padx=0, pady=10, sticky=ttk.W)

        # 确保顶部框架自动调整大小，分配最小权重
        self.grid_rowconfigure(0, weight=0)

        # 创建表格部分
        self.create_table()

        # 添加翻页按钮和分页信息
        self.create_pagination_controls()

    def clear_query(self):
        self.sachnummer_entry.delete(0, ttk.END)
        self.test_typ_entry.set("")
        #
        self.display_df = self.df
        self.current_page = 1
        self.refresh_table()

    def create_table(self):
        # 创建表格 (ttk.Treeview)
        style = ttk.Style()
        # 设置表格行高
        style.configure("Treeview", rowheight=40)
        # 设置Treeview的表头样式
        style.configure("Treeview.Heading", background="gray", foreground="black", font=self.title_font, relief="solid")
        # 创建表格容器,放置滚动条
        tabel_frame = ttk.Frame(self.inner_frame)
        tabel_frame.grid(row=1, column=0, columnspan=8, padx=10, pady=20, sticky=ttk.NSEW)

        self.tree = ttk.Treeview(tabel_frame, height=15, columns=self.display_columns, show="headings")
        # 设置列标题
        for col in self.display_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        #
        self.tree.grid(row=0, column=0, sticky=ttk.NSEW)

        # 创建垂直滚动条
        scrollbar = Scrollbar(tabel_frame, orient=ttk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=ttk.NS)

        # 创建水平滚动条
        hscrollbar = Scrollbar(tabel_frame, orient=ttk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=hscrollbar.set)
        hscrollbar.grid(row=1, column=0, sticky=ttk.EW)

        # Binding double-click event
        self.tree.bind("<Double-1>", self.on_row_double_click)

    def on_row_double_click(self, event):
        print("Row double clicked")
        # 获取双击的行
        items = self.tree.selection()
        if not items:
            print("No row selected")
            return
        item = items[0]
        row_data = self.tree.item(item, "values")
        print("Selected row data:", row_data)

        row_data = [np.nan if r == "nan" else r for r in row_data]
        test_id = row_data[0]  # Prüfnummer
        sachnummer = row_data[1]
        type_of_measurement = row_data[3]
        musternummer = row_data[4]
        pv_nummer = row_data[5]
        data = self.df[(self.df["Sachnummer"] == sachnummer) &
                       (self.df["Type of Measurement"] == type_of_measurement) &
                       (self.df["Musternummer"] == musternummer) &
                       (self.df["PV-Nummer"] == pv_nummer)]

        # # 获取测试id
        # test_id = row_data[0]  # Prüfnummer
        # 从数据集中获取完整的行数据
        # row_data = self.df[self.df["Prüfnummer"] == test_id]
        # 转字典
        data_dict = data.to_dict(orient="records")[0]

        typ = data_dict["Typ"]
        if typ.startswith("P"):
            self.pump_detail(data_dict)
        else:
            self.motro_detail(data_dict, test_id)

    def pump_detail(self, data_dict):
        # 创建一个新的窗口
        edit_window = ttk.Toplevel(self)
        # 设置窗口大小和布局
        edit_window.resizable(False, False)
        edit_window.title("Edit Row Data")

        # 不可编辑字段的列表
        readonly_fields = [
            "Kunde",
            "Typ-Kurzbezeichnung",
            "Sachnummer(SNR)",
            "Fertigungsdatum",
            "Prüfung",
            "Prüfer",
            "Prüfdatum",

            "Prüfling-Nr",
            "Bemerkung",

            "Prüfaufbau",
            "Messaufbau",

            "Prüfvorschrift",
            "Fördermedium",
            "Prüf-Spannung",
            "Testdauer",
            "Prüf-Art",
            "Luftschall - Meßabstand",
            "umgerechnet auf",
            "Förderdruck / Differenzdruck",
            "Durchfluß",

            "Luftschall-Summengrenzwert",
            "Luftschall-Summe-Startfrequenz",
            "Luftschall-Summe-Endfrequenz",
            "Luftschall-Terzgrenzwert",
            "Luftschall-Terz-Startfrequenz",
            "Luftschall-Terz-Endfrequenz",
            "Triax-Summengrenzwert",
            "Triax-Summe-Startfrequenz",
            "Triax-Summe-Endfrequenz",
            "Triax-Terzgrenzwert",
            "Triax-Terz-Startfrequenz",
            "Triax-Terz-Endfrequenz",
        ]

        # 用于存储所有输入框，以便在保存时提取数据
        entries = {}

        # 设置每个部分的标签和字段
        sections = {
            "Dokumentation": ["Kunde", "Typ-Kurzbezeichnung", "Sachnummer(SNR)",
                              "Fertigungsdatum", "Prüfung", "Prüfer",
                              "Prüfdatum"],
            "Prüfling": ["Prüfling-Nr"],
            "Prüfaufbau": ["Prüfaufbau", "Messaufbau"],
            "Prüfvorgaben": ["Prüfvorschrift", "Fördermedium", "Prüf-Spannung",
                             "Testdauer", "Prüf-Art", "Luftschall - Meßabstand",
                             "umgerechnet auf", "Förderdruck / Differenzdruck",
                             "Durchfluß", ],
            "Toleranzprüfung": ["Luftschall-Summengrenzwert",
                                "Triax-Summengrenzwert",
                                "Luftschall-Summe-Startfrequenz",
                                "Triax-Summe-Startfrequenz",
                                "Luftschall-Summe-Endfrequenz",
                                "Triax-Summe-Endfrequenz",
                                "Luftschall-Terzgrenzwert",
                                "Triax-Terzgrenzwert",
                                "Luftschall-Terz-Startfrequenz",
                                "Triax-Terz-Startfrequenz",
                                "Luftschall-Terz-Endfrequenz",
                                "Triax-Terz-Endfrequenz",
                                ]
        }
        # 创建每个部分的框架
        for row, (section, labels) in enumerate(sections.items()):
            # 添加分区标题
            frame_section = ttk.Frame(edit_window, relief="groove", borderwidth=2)
            # frame_section.pack(fill="x", padx=10, pady=10)
            frame_section.grid(row=row, column=0, sticky=ttk.NSEW)

            # 设置分区标题
            section_label = ttk.Label(frame_section, text=section, font=self.title_font)
            section_label.grid(row=0, column=0, columnspan=4, sticky=ttk.W)
            # 水平布局每个字段
            for idx, label in enumerate(labels):
                t_label = ttk.Label(frame_section, text=label)
                t_label.grid(row=1 + idx // 2, column=(idx % 2) * 2, padx=5, pady=5, sticky=ttk.W)
                if section == "" and label == "":
                    # 添加下拉框
                    entry = ttk.Combobox(frame_section, width=30, values=["Schaum", "frei aufgehängt", "Unter Last"])
                    entry.grid(row=1 + idx // 2, column=(idx % 2) * 2 + 1, padx=5, pady=5)
                    entry.set(data_dict.get(label, ""))
                else:
                    # 控制宽度
                    if section == "Prüfling" and label == "Prüfling-Nr":
                        width = 60
                    else:
                        width = 30
                    entry = ttk.Entry(frame_section, width=width)
                    entry.grid(row=1 + idx // 2, column=(idx % 2) * 2 + 1, padx=5, pady=5)
                    # 调整显示的值
                    if section == "Dokumentation" and (label == "Prüfdatum" or label == "Prüfungsdatum"):
                        current_time = datetime.now().strftime('%Y-%m-%d')
                        entry.insert(0, current_time)
                    elif section == "Dokumentation" and label == "Fertigungsdatum":
                        value = data_dict.get(label, "")
                        date_str = self.parse_date(value)
                        entry.insert(0, date_str)  # 填充数据
                    elif section == "Prüfling" and label == "Prüfling-Nr":
                        value = self.get_prufling_nr(data_dict)
                        entry.insert(0, value)
                    else:
                        value = data_dict.get(label, "")
                        unit = self.unit_mapping.get(label, "")
                        entry.insert(0, f"{value} {unit}")  # 填充数据

                # 如果是只读字段
                if label in readonly_fields:
                    entry.config(state="readonly")
                # 保存每个字段的输入框到 entries 字典中
                entries[label] = entry

        # 增加按钮, 按钮布局在 sections 的后面
        generate_user_doc_button = ttk.Button(edit_window, text="Generate UserDoc", width=20,
                                              command=self.export_hatx_file)
        generate_user_doc_button['padding'] = (0, 10)  # 设置内边距来增加button高度
        generate_user_doc_button.grid(row=len(sections) + 1, column=0, padx=0, pady=20)

    def motro_detail(self, data_dict, test_id):
        # 创建一个新的窗口
        edit_window = ttk.Toplevel(self)
        # 设置窗口大小和布局
        edit_window.resizable(False, False)
        edit_window.title("Edit Row Data")

        # 不可编辑字段的列表
        readonly_fields = [
            "Sachnummer", "Kunde", "Typ-Kurzbezeichung", "Fertigungsdatum", "Prüfer",
            "Prüfungsdatum", "Musternummer", "Prüfnummer",
            "Prüfling-Nr", "Prüfaufbau", "Prüfvorschrift", "Prüfspannung", "Test dauer",
            "Prüf-Art", "Mikrofon Abstand", "Drehrichtung", "Drehzahl",
            "Luftschall-Summegrenzwert",
            "Luftschall-Summe-Straffrequenz", "Luftschall-Summe-Endfrequenz"
        ]

        # 用于存储所有输入框，以便在保存时提取数据
        entries = {}

        # 设置每个部分的标签和字段
        sections = {
            "Dokumentation": ["Sachnummer", "Kunde", "Typ-Kurzbezeichung",
                              "Fertigungsdatum", "Prüfer",
                              "Prüfungsdatum",
                              "Musternummer", "Prüfnummer"],
            # "Prüfling": ["Prüfling-Nr", "Prüfling Bemerkung"],
            "Prüfling": ["Prüfling-Nr", ],
            # "Prüfaufbau": ["Prüfaufbau", "Prüfaufbau Bemerkung"],
            "Prüfaufbau": ["Prüfaufbau", ],
            "Prüfvorgaben": ["Prüfvorschrift", "Prüfspannung", "Test dauer",
                             "Prüf-Art", "Mikrofon Abstand",
                             "Drehrichtung", "Drehzahl"],
            "Toleranzprüfung": ["Luftschall-Summegrenzwert",
                                "Luftschall-Summe-Straffrequenz",
                                "Luftschall-Summe-Endfrequenz"]
        }

        # 创建每个部分的框架
        for section, labels in sections.items():
            # 添加分区标题
            frame_section = ttk.Frame(edit_window, relief="groove", borderwidth=2)
            # frame_section.pack(fill="x", padx=10, pady=10)
            frame_section.pack(fill="x", )

            # 设置分区标题
            ttk.Label(frame_section, text=section, font=self.title_font).grid(row=0, column=0,
                                                                              columnspan=4,
                                                                              sticky=ttk.W)
            # 水平布局每个字段
            for idx, label in enumerate(labels):
                ttk.Label(frame_section, text=label).grid(row=1 + idx // 2,
                                                          column=(idx % 2) * 2,
                                                          padx=5, pady=5,
                                                          sticky=ttk.W)
                if section == "" and label == "":
                    # 添加下拉框
                    entry = ttk.Combobox(frame_section, width=30,
                                         values=["Schaum", "frei aufgehängt",
                                                 "Unter Last"])
                    entry.grid(row=1 + idx // 2, column=(idx % 2) * 2 + 1,
                               padx=5, pady=5)
                    entry.set(data_dict.get(label, ""))
                else:
                    entry = ttk.Entry(frame_section, width=30)
                    entry.grid(row=1 + idx // 2, column=(idx % 2) * 2 + 1, padx=5, pady=5)
                    if section == "Dokumentation" and label == "Prüfungsdatum":
                        current_time = datetime.now().strftime('%Y-%m-%d')
                        entry.insert(0, current_time)
                    if section == "Dokumentation" and label == "Fertigungsdatum":
                        value = data_dict.get(label, "")
                        try:
                            value = pd.to_datetime(value, errors='coerce').strftime('%Y-%m-%d')
                        except Exception as e:
                            value = ""
                        entry.insert(0, value)  # 填充数据
                    else:
                        entry.insert(0, data_dict.get(label, ""))  # 填充数据

                # 如果是只读字段
                if label in readonly_fields:
                    entry.config(state="readonly")

                # 保存每个字段的输入框到 entries 字典中
                entries[label] = entry

        # 保存按钮的布局
        def save_data():
            # 从每个输入框中提取新数据
            new_data = {}
            for label, entry in entries.items():
                if entry.cget("state") == "readonly":
                    continue
                elif entry.get() in ["NaN", "nan", None, ""]:
                    new_data[label] = ""
                else:
                    new_data[label] = entry.get()

            # 更新数据框中的对应行
            for label, value in new_data.items():
                self.df.loc[self.df["Prüfnummer"] == test_id, label] = value

            # 更新 Treeview 显示
            self.refresh_table()

            # 关闭编辑窗口
            edit_window.destroy()
            print("Data saved successfully")

        save_button = ttk.Button(edit_window, text="Save", command=save_data)
        save_button.pack(pady=20)

        # 居中窗口
        # edit_window.transient(self)
        edit_window.grab_set()
        edit_window.wait_window()

    @staticmethod
    def get_prufling_nr(data_dict):
        # "Sachnummer(SNR)得后六位(比如02450V)_Fertigungsdatum(比如241105)_
        # Werkstatt(比如W318)_Prüfung(比如S)_Arbeitspunkt(比如AP1)_Teil-Nr.(比如N01)"
        # 是由这六部分值通过_拼凑而成
        part_one = data_dict.get("Sachnummer(SNR)", "")[-6:]
        part_two = data_dict.get("Fertigungsdatum", "")
        try:
            part_two = pd.to_datetime(part_two, errors='coerce').strftime('%Y%m%d')
        except Exception as e:
            part_two = ""
        part_three = data_dict.get("Werkstatt", "")
        part_four = data_dict.get("Prüfung", "")
        part_five = data_dict.get("Arbeitspunkt", "")
        part_six = data_dict.get("Teil-Nr.", "")
        value = f"{part_one}_{part_two}_{part_three}_{part_four}_{part_five}_{part_six}"
        print("value:", value)
        return value

    @staticmethod
    def parse_date(value):
        try:
            date_str = pd.to_datetime(value, errors='coerce').strftime('%Y-%m-%d')
        except Exception as e:
            date_str = ""
        return date_str

    def create_pagination_controls(self):
        # 上一页按钮
        self.prev_button = ttk.Button(self.inner_frame, text="Previous Page", command=self.prev_page)
        self.prev_button.grid(row=2, column=2, padx=10)

        # 分页信息
        self.page_label = ttk.Label(self.inner_frame, text=f"Page {self.current_page} / {self.total_pages}",
                                    font=self.font)
        self.page_label.grid(row=2, column=3, padx=10)

        # 下一页按钮
        self.next_button = ttk.Button(self.inner_frame, text="Next Page", command=self.next_page)
        self.next_button.grid(row=2, column=4, padx=10)

        # 更新按钮状态
        self.update_pagination_buttons()

    def update_pagination_buttons(self):
        self.total_pages = math.ceil(len(self.display_df) / self.items_per_page)
        # 根据当前页数更新翻页按钮状态
        if self.current_page <= 1:
            self.prev_button["state"] = "disabled"
        else:
            self.prev_button["state"] = "normal"

        if self.current_page >= self.total_pages:
            self.next_button["state"] = "disabled"
        else:
            self.next_button["state"] = "normal"

        # 更新分页信息
        self.page_label.config(
            text=f"Page {self.current_page} / {self.total_pages}")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_table()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.refresh_table()

    def generate_mock_data(self):
        # 生成 1000 条数据
        data = []
        # for i in range(1000):
        #     dic = {}
        #     for display_column in self.column_mapping.keys():
        #         if display_column == "Prüfnummer":
        #             dic[display_column] = f"Test-{i}"
        #         elif display_column == "Type of Measurment":
        #             dic[display_column] = random.choice(self.test_typs)
        #         else:
        #             dic[display_column] = random.randint(1000, 9999)
        #
        #     data.append(dic)
        data = pd.DataFrame(data)
        # "Fertigungsdatum", "Bemerkung", "Prüfaufbau"
        # data["Prüfungsdatum"] = pd.to_datetime(data["Prüfungsdatum"], unit="D", origin="2021-01-01")
        # data["Prüfling Bemerkung"] = ""
        # data["Prüfaufbau Bemerkung"] = ""
        return data

    def query_order(self):
        # 获取输入内容
        sachnummer_value = self.sachnummer_entry.get()  # 获取 Motor Serial Number
        test_typ = self.test_typ_entry.get()
        test_typ = self.query_mapping.get(test_typ, test_typ)

        # 如果两个输入框都有值，则使用 pandas 筛选
        if sachnummer_value and test_typ:
            self.display_df = self.df[
                (self.df["Sachnummer"] == sachnummer_value) & (self.df["Type of Measurement"] == test_typ)]

            if not self.display_df.empty:
                self.current_page = 1  # 重新从第一页开始显示
                self.refresh_table()
                messagebox.showinfo("info", "Query successful")
            else:
                messagebox.showwarning("warn", "No results found")
        else:
            messagebox.showwarning("warn", "Please enter complete query information")

    def refresh_table(self):
        # 清空表格
        for row in self.tree.get_children():
            self.tree.delete(row)

        # 获取当前页数据
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_data = self.display_df.iloc[start_idx:end_idx]
        page_data = page_data[self.display_columns]
        # page_data.fillna("", inplace=True)
        # datetime -> date
        page_data['Fertigungsdatum'] = pd.to_datetime(page_data['Fertigungsdatum'], errors='coerce')
        page_data["Fertigungsdatum"] = page_data["Fertigungsdatum"].dt.date

        # 插入新数据
        for _, row in page_data.iterrows():
            self.tree.insert("", "end", values=row.tolist())
        # 更新翻页控件状态
        self.update_pagination_buttons()

    def import_file(self):
        # 打开文件选择对话框，限制文件类型为 xlsx 和 csv
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")],
            title="Select a file"
        )
        if file_path:
            try:
                if file_path.endswith('.xlsx'):
                    # 读取 Excel 文件
                    new_data = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    # 读取 CSV 文件
                    with open(file_path, 'rb') as f:
                        result = chardet.detect(f.read())
                        encoding = result['encoding']
                    new_data = pd.read_csv(file_path, encoding=encoding)
                else:
                    messagebox.showerror("Error", "Unsupported file format.")
                    return
                self.df = new_data  # 更新 DataFrame
                # 根据映射生成新的列, 而不是改名字
                # self.df.rename(columns=self.column_mapping, inplace=True)
                for original_col, new_col in self.column_mapping.items():
                    # 检查原始列是否存在于 DataFrame 中
                    if original_col in self.df.columns:
                        self.df[new_col] = self.df[original_col]
                # 将所有数据转换为字符串
                self.df = self.df.astype(str)
                # Sachnummer 全部转换为string, 部分是int,导致query会查不到
                # self.df["Sachnummer"] = self.df["Sachnummer"].astype(str)

                self.display_df = self.df
                self.current_page = 1  # 重置到第一页
                self.refresh_table()  # 刷新表格
                self.master.update_idletasks()
                messagebox.showinfo("Success", "File imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while importing the file:\n{e}")

    def export_file(self):
        # 打开文件保存对话框，限制文件类型为 xlsx 和 csv
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",  # 默认文件扩展名
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")],
            title="Save the file as"
        )

        if file_path:
            print(file_path)
            try:
                if not (file_path.endswith('.xlsx') or file_path.endswith(
                        '.csv')):
                    # 根据选定的文件类型自动添加扩展名
                    if file_path.endswith('.xlsx'):
                        file_path += '.xlsx'
                    else:
                        file_path += '.csv'
                self.df.rename(columns=self.column_mapping,
                               inplace=True)  # 重命名列
                self.df.fillna("", inplace=True)  # 填充空值
                if file_path.endswith('.xlsx'):
                    # 导出为 Excel 文件
                    self.df.to_excel(file_path, index=False)
                elif file_path.endswith('.csv'):
                    # 导出为 CSV 文件
                    self.df.to_csv(file_path, index=False, encoding='utf-8-sig')

                messagebox.showinfo("Success", "File exported successfully!")
            except Exception as e:
                messagebox.showerror("Error",
                                     f"An error occurred while exporting the file:\n{e}")

    def export_hatx_file(self):
        import clr
        import System
        import sys
        from datetime import datetime

        # 加载必要的程序集
        sys.path.append(r'C:\Program Files\HEAD System Integration and Extension (ASX)')
        clr.AddReference('HEADacoustics.API.Documentation')
        clr.AddReference('HEADacoustics.API.License')

        import HEADacoustics.API.Documentation as ASX05
        from HEADacoustics.API.License import License, ProductCode

        # 初始化许可证
        license_ = License.Create([ProductCode.ASX_05_DocumentationAndMetadataAPI])

        # 创建新的文档
        inDoc = ASX05.Documentation.Create('Pumpe_UserDocumentation')
        # 定义文件路径
        outPath = r'C:\temp\test_pumpe.hatx'

        # 创建主表单 "Dokumentation"
        dokumentation_form = ASX05.Form.Create('Dokumentation')
        inDoc.TryAddForm(dokumentation_form)

        # 在 "Dokumentation" 表单中添加字段
        dokumentation_form.TryAddField(ASX05.TextField.Create('Kunde', 'Renault'))
        dokumentation_form.TryAddField(ASX05.TextField.Create('Typ-Kurzbezeichnung', 'PDE'))
        dokumentation_form.TryAddField(ASX05.TextField.Create('Sachnummer (SNR)', '0392025000'))
        # date_str = '2014-12-13'
        # fertigungsdatum = System.DateTime(date_str, '%Y-%m-%d')
        fertigungsdatum = System.DateTime.Now
        dokumentation_form.TryAddField(ASX05.DateField.Create('Fertigungsdatum Pumpe', fertigungsdatum))

        dokumentation_form.TryAddField(ASX05.TextField.Create('Prüfung', 'Null-Serie'))
        dokumentation_form.TryAddField(ASX05.TextField.Create('Prüfer', 'Baessler Andreas'))
        dokumentation_form.TryAddField(ASX05.DateField.Create('Prüfdatum', System.DateTime.Now))

        # 创建子表单 "Prüfling" 并添加到 "Dokumentation" 中
        pruefling_form = ASX05.Form.Create('Prüfling')
        dokumentation_form.TryAddForm(pruefling_form)  # 将子表单添加到 Dokumentation 表单
        pruefling_form.TryAddField(ASX05.TextField.Create('Prüfling-Nr.',
                                                          '240620_Nr06_W711Bue_RUN01_M01这里是错的'))  # Prüfling-Nr.组成：Sachnummer (SNR)后六位_Fertigungsdatum Pumpe_W318_选择的测试类型(A,Q,S,0)中的一个_Arbeitspunkt(比如AP1)_Teil_NR.（比如N01）

        # 创建子表单 "Prüfauefbau" 并添加到 "Dokumentation" 中
        pruefaufbau_form = ASX05.Form.Create('Prüfaufbau')
        dokumentation_form.TryAddForm(pruefaufbau_form)  # 将子表单添加到 Dokumentation 表单
        pruefaufbau_form.TryAddField(ASX05.TextField.Create('Prüfaufbau', 'frei aufgehängt'))
        pruefaufbau_form.TryAddField(ASX05.TextField.Create('Messaufbau', 'Halbkugel'))

        # 创建子表单 "Prüfvorgaben" 并添加到 "Dokumentation" 中
        pruefvorgaben_form = ASX05.Form.Create('Prüfvorgaben')
        dokumentation_form.TryAddForm(pruefvorgaben_form)  # 将子表单添加到 Dokumentation 表单
        pruefvorgaben_form.TryAddField(ASX05.TextField.Create('Prüfvorschrift', '0 140 Y00 2BR'))
        pruefvorgaben_form.TryAddField(ASX05.TextField.Create('Fördermedium', 'Tyfocor L'))
        pruefvorgaben_form.TryAddField(ASX05.RealField.Create('Prüf-Spannung', 12.0))
        pruefvorgaben_form.TryAddField(ASX05.RealField.Create('Testdauer', 20.0))
        pruefvorgaben_form.TryAddField(ASX05.TextField.Create('Prüf-Art', 'Luft + Körperschall'))
        pruefvorgaben_form.TryAddField(ASX05.RealField.Create('Luftschall - Meßabstand', 30.0))
        pruefvorgaben_form.TryAddField(ASX05.RealField.Create('umgerechnet auf', 50.0))
        pruefvorgaben_form.TryAddField(ASX05.RealField.Create('Förderdruck / Differenzdruck', 0.0))
        pruefvorgaben_form.TryAddField(ASX05.RealField.Create('Durchfluß', 972.0))

        # 创建子表单 "Toleranzprüfung" 并添加到 "Dokumentation" 中
        toleranzpruefung_form = ASX05.Form.Create('Toleranzprüfung')
        dokumentation_form.TryAddForm(toleranzpruefung_form)  # 将子表单添加到 Dokumentation 表单
        toleranzpruefung_form.TryAddField(ASX05.RealField.Create('Luftschall-Summengrenzwert', 45.0))
        toleranzpruefung_form.TryAddField(ASX05.RealField.Create('Luftschall-Summe-Startfrequenz', 20.0))
        toleranzpruefung_form.TryAddField(ASX05.RealField.Create('Luftschall-Summe-Endfrequenz', 20000.0))
        toleranzpruefung_form.TryAddField(ASX05.RealField.Create('Luftschall-Terzgrenzwert', 30.0))
        toleranzpruefung_form.TryAddField(ASX05.RealField.Create('Luftschall-Terz-Startfrequenz', 100.0))
        toleranzpruefung_form.TryAddField(ASX05.RealField.Create('Luftschall-Terz-Endfrequenz', 16000.0))

        # 保存文档到指定路径
        # is_written = ASX05.DocumentationWriter.WriteDirectoryDocumentation(inDoc, outPath)
        is_written = ASX05.DocumentationWriter.Write(inDoc, outPath)
        print("isWritten:", is_written)

        # 释放许可证
        license_.Dispose()

        print(f"数据已成功写入{outPath}")
        messagebox.showinfo("Success", f"File exported successfully! {outPath}")

        # 打开文件保存对话框，限制文件类型为 xlsx 和 csv
        # file_path = filedialog.asksaveasfilename(
        #     defaultextension=".hatx",  # 默认文件扩展名
        #     filetypes=[("Hatx files", "*.hatx")],
        #     title="Save the file as"
        # )
        #
        # if file_path:
        #     print(file_path)
        #     try:
        #         if not file_path.endswith('.hatx'):
        #             file_path += '.hatx'
        #         self.df.rename(columns=self.column_mapping,
        #                        inplace=True)  # 重命名列
        #         self.df.fillna("", inplace=True)  # 填充空值
        #
        #         hatx_outPath = r'C:\temp\Example'
        #         inDoc = ASX05.Documentation.Create('Created by API')
        #
        #         for index, row in self.df.iterrows():
        #             row = row.tolist()
        #             for k, v in row.items():
        #                 textField = ASX05.TextField.Create(k, v)
        #                 inDoc.AddField(textField)
        #         isWritten = ASX05.DocumentationWriter.WriteDirectoryDocumentation(inDoc, hatx_outPath)
        #         license_.Dispose()
        #         if isWritten:
        #             print("数据已成功写入 .hatx 文件！")
        #             messagebox.showinfo("Success",
        #                                 "File exported successfully!")
        #         else:
        #             print("写入 .hatx 文件时出现问题。")
        #             messagebox.showerror("Error",
        #                                  "An error occurred while exporting the file:\n")
        #     except Exception as e:
        #         messagebox.showerror("Error",
        #                              f"An error occurred while exporting the file:\n{e}")
