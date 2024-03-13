@echo off

set PIPELINE_ROOT=C:\Ansel\TD_PyProject\TD\20240223_TD_test\post_pipeline
set PYTHONPATH=C:\Ansel\TD_PyProject\TD\20240223_TD_test\venv\venv27\Lib\site-packages;%PYTHONPATH%

set PYTHONPATH=%PIPELINE_ROOT%;%PIPELINE_ROOT%/dcc/nuke/lib;%PYTHONPATH%
set PATH=%PIPELINE_ROOT%/bin;%PATH%
set NUKE_PATH=%PIPELINE_ROOT%/dcc/nuke/plugin

"C:\Program Files\Nuke13.2v1\Nuke13.2.exe"