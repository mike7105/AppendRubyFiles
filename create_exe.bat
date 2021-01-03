O:\Progs\Python\AppendRubyFiles\venv\Scripts\activate
pyinstaller --onefile ^
--noconsole ^
--icon=modules\ico\cd.ico ^
--add-data "modules/ico";"modules/ico" ^
-n AppendRubyFiles_v1.5.exe ^
AppendRubyFiles.pyw
pause