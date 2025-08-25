@echo off
rem run-backend.bat - inicia o servidor FastAPI usando o Python do sistema

rem Vai para a pasta onde o .bat está
cd /d "%~dp0"

rem Mensagem inicial
echo Starting FastAPI server on http://127.0.0.1:8000 ...

rem Verifica se o módulo fastapi está disponível
python -c "import fastapi" 2>nul
if ERRORLEVEL 1 (
	echo O modulo 'fastapi' nao foi encontrado. Irei tentar instalar automaticamente (requer conexao internet).
	echo Atualizando pip e instalando 'fastapi' e 'uvicorn[standard]'...
	python -m pip install --upgrade pip
	python -m pip install fastapi "uvicorn[standard]"
	if ERRORLEVEL 1 (
		echo Erro ao instalar dependencias automaticamente.
		echo Execute manualmente no PowerShell:
		echo    python -m pip install fastapi "uvicorn[standard]"
		pause
		exit /b 1
	)
)

rem Inicia o servidor FastAPI (uvicorn) usando o python instalado no sistema
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000

rem Mantém a janela aberta após terminar
pause
