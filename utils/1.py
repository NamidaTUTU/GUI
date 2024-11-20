import clr
import sys

# 加载必要的程序集
sys.path.append(r'C:\Program Files\HEAD System Integration and Extension (ASX)')
clr.AddReference('HEADacoustics.API.Documentation')
clr.AddReference('HEADacoustics.API.License')

import HEADacoustics.API.Documentation as ASX05
from HEADacoustics.API.License import License, ProductCode

# 初始化许可证
license_ = License.Create([ProductCode.ASX_05_DocumentationAndMetadataAPI])

# 定义文件路径
outPath = r'C:\temp\pump_template.hatx'

# 创建新的文档
inDoc = ASX05.Documentation.Create('Dokumentation')

# 定义字段内容
fields = [
    ('Kunde', 'Renault'),
    ('Typ-Kurzbezeichnung', 'PDE'),
    ('Sachnummer (SNR)', '0392025000'),
    ('Fertigungsdatum Pumpe', '2024-11-23'),
    ('Prüfung', 'Null-Serie'),
    ('Prüfer', 'Baessler Andreas'),
    ('Prüfdatum', '2024-11-19')
]

# 创建并添加字段到文档
for field_name, field_value in fields:
    textField = ASX05.TextField.Create(field_name, field_value)
    inDoc.AddField(textField)

# 写入模板文件
isWritten = ASX05.TemplateWriter.Write(inDoc, outPath)

# 释放许可证
license_.Dispose()