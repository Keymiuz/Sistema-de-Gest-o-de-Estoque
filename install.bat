@echo off
echo Instalando o Sistema de Gestão...
echo.

:: Verifica se o Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Python não encontrado. Por favor, instale o Python 3.x em https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado. Verificando dependências...
pip install -r requirements.txt

:: Cria atalho na área de trabalho (Windows)
if exist "%USERPROFILE%\Desktop" (
    echo [Desktop] %USERPROFILE%\Desktop
    (
        echo @echo off
        echo cd /d "%~dp0"
        echo start "" "%CD%\main.py"
    ) > "%USERPROFILE%\Desktop\Sistema de Gestão.cmd"
    echo Atalho criado na área de trabalho.
)

echo.
echo Instalação concluída com sucesso!
echo Para iniciar o sistema, execute o arquivo 'main.py' ou use o atalho na área de trabalho.
pause
