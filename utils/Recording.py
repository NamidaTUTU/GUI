import clr
import sys
import time

sys.path.append(r'C:\Program Files\HEAD System Integration and Extension (ASX)')
clr.AddReference('HEADacoustics.API.Remote')
clr.AddReference('HEADacoustics.API.License')

import HEADacoustics.API.Remote as ASX02
from HEADacoustics.API.License import License, ProductCode

license_ = License.Create([ProductCode.ASX_04_DataAcquisitionAPI])

remoteClient = ASX02.ASXRemote.ForLatestApplication(True)
if not remoteClient.StandAloneRecorder.IsAvailable:
    artemisSuiteClient = remoteClient.StandAloneRecorder.Start().Wait()

recorder = remoteClient.StandAloneRecorder.GetRecorderService()

recorder.GetControlService().SetFileNamePattern('My_first_Record_01.hdf')
recorder.GetControlService().StartRecord()

time.sleep(3)

recorder.GetControlService().StopRecord()

license_.Dispose()