@echo off
set ROOT_PATH=C:\Ansel\TD_PyProject\TD\20240310_TD_Pra\pipeline_pra
set PYTHONPATH=C:\Ansel\TD_PyProject\TD\20240310_TD_Pra\venv\vemv37\Lib\site-packages;%PYTHONPATH%

set PYTHONPATH=%ROOT_PATH%;%ROOT_PATH%\bin;%PATH%
set PATH=%ROOT_PATH%\bin
set NUKE_PATH=%ROOT_PATH%/dcc/nuke/plugin

"C:\Program Files\Nuke13.2v1\Nuke13.2.exe"