@echo off
echo ========================================
echo   Probar Juego en Modo Web Local
echo ========================================
echo.
echo Instalando pygbag (si no esta instalado)...
py -m pip install pygbag
echo.
echo Ejecutando juego en navegador...
echo (Presiona Ctrl+C para detener)
echo.
py -m pygbag juego_amor.py
pause
