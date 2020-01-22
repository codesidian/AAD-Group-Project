@ECHO OFF
WHERE npm >nul 2>nul
IF %ERRORLEVEL% NEQ 0 GOTO FAIL_NPM

pushd CustomerSite
npm run build
popd
GOTO END

:FAIL_NPM
ECHO Failed to find NPM, please install Node.JS
PAUSE
GOTO END

:END
