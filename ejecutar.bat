@echo off
REM Instala las dependencias y arranca EcoRutas (requiere MySQL de XAMPP iniciado)
pip install -r requirements.txt
python app.py
pause
