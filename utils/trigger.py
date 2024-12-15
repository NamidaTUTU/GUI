import clr
import sys
import time

sys.path.append(r'C:\Program Files\HEAD System Integration and Extension (ASX)')
clr.AddReference('HEADacoustics.API.Remote')
clr.AddReference('HEADacoustics.API.License')

import HEADacoustics.API.Remote as ASX02
from HEADacoustics.API.Remote import Recorder as ASX04
from HEADacoustics.API.License import License, ProductCode

license_ = License.Create([ProductCode.ASX_04_DataAcquisitionAPI])

remoteClient = ASX02.ASXRemote.ForLatestApplication(True)
if not remoteClient.StandAloneRecorder.IsAvailable:
    artemisSuiteClient = remoteClient.StandAloneRecorder.Start().Wait()

recorder = remoteClient.StandAloneRecorder.GetRecorderService()

recorder.GetTriggerService().SetStartSignalTrigger(0, ASX04.SlopeType.Rising, 'axis1', 1.0)
recorder.GetControlService().SetFileNamePattern('Rising_Slope_Axis1_01.hdf')
recorder.GetTriggerService().SetStopDurationTrigger(0, 10)
recorder.GetControlService().StartRecord()

while not recorder.GetControlService().GetIsRecordingEnabled():
    time.sleep(1)

recorder.GetTriggerService().SetStartSignalTrigger(0, ASX04.SlopeType.Falling, 'axis1', 4.0)
recorder.GetControlService().SetFileNamePattern('Falling_Slope_Axis1_01.hdf')
recorder.GetControlService().StartRecord()

license_.Dispose()