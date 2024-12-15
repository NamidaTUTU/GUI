import clr
import sys

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

availFrontEnds = recorder.GetControlService().GetAvailableFrontends()
device = None
for availFrontEnd in availFrontEnds:
    print(f'Device with nickname "{availFrontEnd.Name}" is available.')
    if availFrontEnd.DeviceType == ASX04.DeviceType.Squadriga3:
        device = availFrontEnd

assert device

isConnected = recorder.GetControlService().ConnectFrontend(device)
print(isConnected)

license_.Dispose()