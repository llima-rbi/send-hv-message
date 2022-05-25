@IF EXIST .\venv\Scripts\activate.bat GOTO HASENV
@CALL virtualenv venv
:HASENV
@CALL .\venv\Scripts\activate.bat
@pip install -r requirements.txt
@pyinstaller -F -n "Remote HV" --distpath . main.py
@CALL .\venv\Scripts\deactivate.bat