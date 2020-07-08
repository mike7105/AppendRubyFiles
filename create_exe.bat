pyinstaller --onefile ^
--noconsole ^
--icon=modules\ico\cd.ico ^
--add-data "modules/ico";"modules/ico" ^
AppendRubyFiles.pyw
pause