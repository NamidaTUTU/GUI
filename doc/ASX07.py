import clr
from time import sleep
import sys
from System import Action, String

sys.path.append(r'C:\Program Files\HEAD System Integration and Extension (ASX)')
clr.AddReference('HEADacoustics.API.Remote')
clr.AddReference('HEADacoustics.API.License')

import HEADacoustics.API.Remote as ASX02
from HEADacoustics.API.License import License, ProductCode

inputRoutine = r'C:\Users\tingting.jordans\Documents\Beispieldateien\ASX\FFT.hpsx'
inputData = r'C:\Users\tingting.jordans\Documents\Beispieldateien\Training\01 Führungsgrößen\CAN'
resultPath = r'C:\Users\tingting.jordans\Documents\Beispieldateien\Training\01 Führungsgrößen\CAN\results'
prod = '*'

def main():
    license_ = License.Create([ProductCode.ASX_02_DataProcessingAndRepresentationAPI])

    remoteClient = ASX02.ASXRemote.ForLatestApplication(True)
    if not remoteClient.Calculator.IsAvailable:
        remoteClient.Calculator.Start(f'/prod {prod}').Wait()

    delegSummary = Action[String, ASX02.JobSummary](__onJobFinished)
    delegProgress = Action[String, ASX02.JobProgress](__onJobProgress)
    processingService = remoteClient.Calculator.GetProcessingService(delegSummary,
                                                                     delegProgress)

    processingService.StartJob('MyJobName', inputRoutine, resultPath, [inputData])
    while len(processingService.GetRunningJobs()) > 0:
        sleep(1)

###################################################################### wichtig! im Beispielcode ist es nicht da, daher funktioniert es nicht#########################################################################
    sleep(20)
    license_.Dispose()

def __onJobFinished(jobName, jobSummary):
    if jobSummary.Processes:
        for process in jobSummary.Processes:
            print(f'Finished calculating {jobName} --- {process.Name}')

            if process.Errors:
                for error in process.Errors:
                    print(f'Error {error} occurred in {jobName} --- {process.Name}')

    else: print(f'There are no processes in {jobName}!')

def __onJobProgress(jobName, jobProgress):
    if jobProgress:
        print(f'Calculation of {jobName} is at {jobProgress.PercentComplete}%')

if __name__ == '__main__':
    main()