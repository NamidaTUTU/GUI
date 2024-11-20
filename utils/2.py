import clr
import sys

# 加载程序集
sys.path.append(r'C:\Program Files\HEAD System Integration and Extension (ASX)')
clr.AddReference('HEADacoustics.API.Documentation')
clr.AddReference('HEADacoustics.API.License')

import HEADacoustics.API.Documentation as ASX05
from HEADacoustics.API.License import License, ProductCode

# 初始化许可证
license_ = License.Create([ProductCode.ASX_05_DocumentationAndMetadataAPI])

# 定义路径
inPath = r'C:\temp\pump_template.hatx'
outPath = r'C:\temp\pump_template_last.hatx'

# 读取文档
inDoc = ASX05.TemplateReader.Read(inPath)
formDokumentation = inDoc.TryGetForm('Dokumentation')


def add_form_with_fields(parent_form, form_name, fields):
    """添加表单并填充字段"""
    new_form = ASX05.Form.Create(form_name)
    if parent_form.TryAddForm(new_form).ActionIsOk:
        for field_name, field_value in fields.items():
            text_field = ASX05.TextField.Create(field_name, field_value)
            if new_form.TryAddField(text_field).ActionIsOk:
                text_field.IsEditable = True


# 配置表单和字段
forms_to_add = {
    "Prüfling": {
        "Prüfling-Nr.": "240620_Nr06_W711Bue_RUN01_M01"
    },
    "Prüfaufbau": {
        "Prüfaufbau": "frei aufgehängt",
        "Messaufbau": "Halbkugel"
    },
    "Prüfvorgaben": {
        "Prüfvorschrift": "0 140 Y00 2BR",
        "Fördermedium": "Halbkugel",
        "Prüf-Spannung": "12.0",
        "Testdauer": "20.0",
        "Prüf-Art": "Luft + Körperschall",
        "Luftschall - Meßabstand": "30.0",
        "umgerechnet auf": "50.0",
        "Förderdruck / Differenzdruck": "0.0",
        "Durchfluß": "972.0"
    },
    "Toleranzprüfung": {
        "Luftschall-Summengrenzwert": "45.0",
        "Luftschall-Summe-Startfrequenz": "20.0",
        "Luftschall-Summe-Endfrequenz": "20000.0",
        "Luftschall-Terzgrenzwert": "30.0",
        "Luftschall-Terz-Startfrequenz": "100.0",
        "Luftschall-Terz-Endfrequenz": "16000.0",
        "Triax-Summengrenzwert": "15.00",
        "Triax-Summe-Startfrequenz": "0.0",
        "Triax-Summe-Endfrequenz": "12.0",
        "Triax-Terzgrenzwert": "18.0",
        "Triax-Terz-Startfrequenz": "118.0",
        "Triax-Terz-Endfrequenz": "67.0"
    }
}

# 添加所有表单和字段
for form_name, fields in forms_to_add.items():
    add_form_with_fields(formDokumentation, form_name, fields)

# 写入文档
ASX05.TemplateWriter.Write(inDoc, outPath)

# 释放许可证
license_.Dispose()
