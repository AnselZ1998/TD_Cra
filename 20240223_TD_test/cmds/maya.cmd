@echo off

set PIPELINE_ROOT=C:\Ansel\TD_PyProject\TD\20240223_TD_test\post_pipeline
set PYTHONPATH=C:\Ansel\TD_PyProject\TD\20240223_TD_test\venv\venv27\Lib\site-packages;%PYTHONPATH%

set PYTHONPATH=%PIPELINE_ROOT%;%PIPELINE_ROOT%/dcc/maya/lib;%PIPELINE_ROOT%/dcc/maya/scripts;%PYTHONPATH%
set PATH=%PIPELINE_ROOT%/bin;%PATH%
set MAYA_SCRIPT_PATH=%PIPELINE_ROOT%/dcc/maya/scripts


"C:\Program Files\Maya2023\Maya2023\bin\maya.exe"


