@echo off
echo ========================================
echo  Subir Juego a GitHub
echo ========================================
echo.
echo Este script te ayudara a subir el juego a GitHub
echo.
set /p repo="Pega la URL de tu repositorio de GitHub (ej: https://github.com/usuario/repo.git): "
echo.
echo Configurando Git...
git init
git add .
git commit -m "Juego de amor para Lucero - Primera version"
git branch -M main
git remote add origin %repo%
echo.
echo Subiendo a GitHub...
git push -u origin main
echo.
echo ========================================
echo  LISTO!
echo ========================================
echo.
echo Tu juego se esta construyendo automaticamente.
echo En 2-3 minutos estara disponible en:
echo https://TU_USUARIO.github.io/NOMBRE_REPO
echo.
echo Ve a tu repositorio en GitHub para ver el progreso:
echo - Pestaña "Actions" para ver el build
echo - Settings ^> Pages para obtener la URL exacta
echo.
pause
