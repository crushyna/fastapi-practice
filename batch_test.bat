SET script_path=%cd%
cmd /k "cd /d venv\Scripts & activate & start "" http:\\127.0.0.1:8000 & cd /d %script_path% & uvicorn main:app --reload "

PAUSE