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

# 定义文件路径
outPath = r'C:\temp\test_pumpe.hatx'

# 创建新的文档
inDoc = ASX05.Documentation.Create('Pumpe_UserDocumentation')

# 创建主表单 "Dokumentation"
dokumentation_form = ASX05.Form.Create('Dokumentation')
inDoc.TryAddForm(dokumentation_form)

# 在 "Dokumentation" 表单中添加字段
dokumentation_form.TryAddField(ASX05.TextField.Create('Kunde', 'Renault'))
dokumentation_form.TryAddField(ASX05.TextField.Create('Typ-Kurzbezeichnung', 'PDE'))
dokumentation_form.TryAddField(ASX05.TextField.Create('Sachnummer (SNR)', '0392025000'))
dokumentation_form.TryAddField(ASX05.DateField.Create('Fertigungsdatum Pumpe', '2014.12.13'))
dokumentation_form.TryAddField(ASX05.TextField.Create('Prüfung', 'Null-Serie'))
dokumentation_form.TryAddField(ASX05.TextField.Create('Prüfer', 'Baessler Andreas'))
dokumentation_form.TryAddField(ASX05.DateField.Create('Prüfdatum', System.DateTime.Now))

# 创建子表单 "Prüfling" 并添加到 "Dokumentation" 中
pruefling_form = ASX05.Form.Create('Prüfling')
dokumentation_form.TryAddForm(pruefling_form)  # 将子表单添加到 Dokumentation 表单
pruefling_form.TryAddField(ASX05.TextField.Create('Prüfling-Nr.', '240620_Nr06_W711Bue_RUN01_M01这里是错的'))#Prüfling-Nr.组成：Sachnummer (SNR)后六位_Fertigungsdatum Pumpe_W318_选择的测试类型(A,Q,S,0)中的一个_Arbeitspunkt(比如AP1)_Teil_NR.（比如N01）

# 创建子表单 "Prüfauefbau" 并添加到 "Dokumentation" 中
pruefaufbau_form = ASX05.Form.Create('Prüfaufbau')
dokumentation_form.TryAddForm(pruefauefbau_form)  # 将子表单添加到 Dokumentation 表单
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
isWritten = ASX05.DocumentationWriter.WriteDirectoryDocumentation(inDoc, outPath)

# 释放许可证
license_.Dispose()