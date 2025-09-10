@echo off
rem run-backend.bat - inicia o servidor FastAPI usando o Python do sistema

rem Vai para a pasta onde o .bat está
cd /d "%~dp0"

rem Mensagem inicial
echo Starting FastAPI server on http://127.0.0.1:8000

rem Verifica se o modulo fastapi esta disponivel
python -c "import fastapi" 2>nul
if %ERRORLEVEL% NEQ 0 goto install_deps

goto start_uvicorn

:install_deps
echo O modulo 'fastapi' nao foi encontrado. Tentando instalar dependencias...
python -m pip install --upgrade pip
if exist "requirements.txt" (
	echo Instalando dependencias de requirements.txt...
	python -m pip install -r requirements.txt
) else (
	python -m pip install "fastapi" "uvicorn[standard]"
)
if %ERRORLEVEL% NEQ 0 (
	echo Erro ao instalar dependencias automaticamente.
	echo Execute manualmente no PowerShell:
	echo    python -m pip install -r requirements.txt
	pause
	exit /b 1
)
:start_uvicorn
start chrome.exe http://127.0.0.1:8000/
echo Iniciando uvicorn (abrindo para rede local: 0.0.0.0)...
echo Nota: Para acessar de outro dispositivo na mesma rede, use o IP local desta máquina (ex: 192.168.x.x) na porta 8000.
echo       Verifique o firewall do Windows para permitir conexoes TCP na porta 8000 se necessario.
echo Iniciando uvicorn (abrindo para rede local: 0.0.0.0)...

rem Lista IPs IPv4 locais relevantes
echo Enderecos IPv4 locais encontrados:
powershell -NoProfile -Command "Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notmatch '^(127|169)\.' -and $_.PrefixOrigin -ne 'WellKnown' } | Select-Object -ExpandProperty IPAddress" 

rem Pergunta se deve criar regra de firewall para permitir conexoes na porta 8000
set "OPEN_FW=N"
set /p OPEN_FW=Deseja adicionar (ou atualizar) uma regra de firewall para liberar a porta 8000 (requer UAC)? [y/N]: 
if /I "%OPEN_FW%"=="y" goto create_fw
goto skip_fw

:create_fw
echo Solicitando elevacao para criar regra de firewall (confirme o UAC)...
powershell -NoProfile -Command "Start-Process netsh -Verb runAs -ArgumentList 'advfirewall firewall add rule name=""Allow Uvicorn 8000"" dir=in action=allow protocol=TCP localport=8000'"
echo Regra de firewall solicitada (confirme UAC se solicitado).
goto skip_fw

:skip_fw

echo Nota: Para acessar de outro dispositivo na mesma rede, use o IP local desta maquina (ex: 192.168.x.x) na porta 8000.
echo       Se usar Wifi, confirme que o dispositivo esta na mesma sub-rede e que o roteador nao isola clientes (AP/client isolation).

python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

rem Mantem a janela aberta no fim
pause
