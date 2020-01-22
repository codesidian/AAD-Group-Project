@ECHO OFF
pushd CustomerSite
WHERE npm >nul 2>nul
IF %ERRORLEVEL% NEQ 0 GOTO FAIL_NPM

CALL npm i
CALL npm run build
GOTO END

:FAIL_NPM
ECHO Failed to find NPM, please install Node.JS
PAUSE
GOTO END

:END
popd
