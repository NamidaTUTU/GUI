##########Overview：The ArtemiSproc.exe##########
The ArtemiSproc.exe can be used to execute signal processing operations on the command line without starting the graphical user interface of ArtemiS SUITE. Thus, it can be used efficiently in a fully automated evaluation scenario such as end-of-line tests.

In order to use ArtemiSproc.exe, a dongle with the following license is required:
ASX Processing Core     

##########Usage：##########
1.Execution 
The ArtemiSproc.exe can be found in the installation directory of HEAD System Integration and Extension. Thus, the default installation path is C:\Program Files\HEAD System Integration and Extension (ASX). In order to be able to access the functional range from each directory directly, it is advised to include the working directory of the executable file into the search path. If you use the ArtemiSproc_CmdPrompt.bat from the same directory for starting, the appropriate entry will be set for the started command line automatically for its runtime.

To use the process ArtemiSproc.exe, you have to specify the desired instruction file (*.hpsx) as well as the data to be processed explicitly. In addition, optional parameters are available.

The parameter's name and the corresponding value have to be always separated from each other by a space. Path and file names only have to be enclosed in quotation marks if they contain spaces. All used path indications are possible absolute as well as relative to the current working directory of the command line.

After the execution of all contained instructions, the process will be stopped automatically by default.   

2.Required Parameters
#Job
The Job parameter (/job instructions) specifies the HPSX file that contains the desired processing instructions. You can create an according file from the toolbar of the area Sequences of the corresponding Automation Project.

#Source
The Source parameter (/src source) specifies a source including the relative or absolute path. Hereby HDF and DAT files are allowed as well as folders. Additionally, if all sequences contain appropriate import elements at the beginning, also files of supported formats are possible. As placeholder, * and ? can be used. For example, /src "recordings\*.hdf" would select all HDF files from the folder "recordings" as sources. However, subfolders are not included hereby.

This option can be stated as many times as desired to specify multiple sources at once.

#Source Recursive
The Source Recursive parameter (/srcr source) acts like Source, but in contrast all contained subdirectories are searched recursively, too. As placeholder, * and ? can be used. For example, /srcr "recordings\*.hdf" would select all HDF files from the folder "recordings" and from its subdirectories as sources.

At least one source has to be specified either via Source or via Source Recursive.   

##########Optional Parameters##########
1.Target
The Target parameter (/target target) specifies the base directory below which the result files shall be stored.

Hereby you can overwrite the corresponding Target Directory in the HPSX file. Thereby /target . selects the current working directory as target.

2.Product Code
The Product Code parameter (/prod product code) specifies the products for which licenses shall be derecognized.

Multiple licenses have to be entered separated by semicolon, for example, /prod 5097. The product 5097 (ASX Local Processing Service) is always licensed automatically, as it is required mandatorily for the execution of the ArtemiSproc.exe. /prod * allows to derecognize all available products. However, as far as possible you should limit yourself to the actually needed licenses to reduce the start time and thus to accelerate the processing.

3.Var
The Var parameter (/var variable=value) changes the value of a variable defined in the HPSX file. For example, /var CutValue=200 sets the value of the variable named CutValue to 200. The parameter can be repeated for different variables.

4.Debug
The Debug parameter (/d) activates the extended output and log level (DEBUG).

Only advised for error diagnostics.

5.Pause
The Pause parameter (/p) enforces to wait for any keypress after the end of the processing.

Thereby the command line stays open and thus enables the reading of the output information.

6.Pause on Error
The Pause on Error parameter (/pe) acts like Pause but waits for any keypress only after an occurred error.

7.Single Threaded
The Single Threaded parameter (/st) activates the single thread mode in which multiple processing sequences are not distributed to multiple threads.

This might be useful for example if memory-intensive processings like a MATLAB export cannot be executed successfully due to lack of working memory. As less overhead is produced in the single thread mode, this enables the processing of larger amounts of data. However, the processing performance is reduced thereby, which is why you should only use the option in case of problems.

8.Language
The Language parameter (/lang) determines the language of the text output.

Default setting is en-EN, alternatively you can select de-DE.

9.Help
The Help parameter (/?) displays a listing of all available options on the command line including a short version of the above description.   

##########Examples##########
1.Simple
As an example, a simple signal processing file containing an FFT vs. Time process followed by a Cut 2D from 3D process is performed (see HPSX file). It is assumed to be stored at "C:\processings\simple.hpsx".

In addition, a recording in the HDF format is assumed to be stored at C:\measurements\recording1.hdf. Since an FFT vs. Time is computed, the ASP 001 licence has to be derecognized. With these files, a signal processing can be executed by executing the following command:

ArtemiSproc.exe /job "C:\processings\simple.hpsx" /src "C:\measurements\recording1.hdf" /prod "51001"
Since the 'CutValue' is set to '10.0', the result is stored in the startup directory with the name recording1_10.00_Result.hdf.

2.Extended
In order to specify the target path of the result file, the target path can be specified, too. In addition, the application should run in debug mode and remain open after execution. Then, the command reads as follows:

ArtemiSproc.exe /job "C:\processings\simple.hpsx" /src "C:\measurements\recording1.hdf" /prod "51001" /target "C:\results\" /d /p
The result is stored in C:\results\recording1_10.00_Result.hdf and debug information is logged to the console. Furthermore, the application remains open until the next keypress.

3.Variable Usage
In order to use variables, a variable named CustomCutValue is created with a value of 20 and used instead of the CutValue (see HPSX file). The result of

ArtemiSproc.exe /job "C:\processings\variables.hpsx" /src "C:\measurements\recording1.hdf" /prod "51001"
is stored in C:\results\recording1_20.00_Result.hdf.

In order to change the variable value to 40, the command line has to be extended to

ArtemiSproc.exe /job "C:\processings\variables.hpsx" /src "C:\measurements\recording1.hdf" /prod "51001" /var "CustomCutValue=40"
The result is now computed with a CutValue of 40 and stored in the startup directory with the name recording1_40.00_Result.hdf.