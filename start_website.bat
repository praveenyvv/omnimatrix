@echo off
title OmniMatrix Website Server
echo ========================================================
echo   OmniMatrix - Starting Local Website Server
echo ========================================================
echo.
echo   - Running live folder auto-scanner (Option B)
echo   - Opening your default browser at http://localhost:8000
echo   - Drop or delete images in website-assets/ and just refresh the browser!
echo.
echo   Press Ctrl+C or close this window to stop the server.
echo ========================================================
echo.
python tools\dev_server.py
pause
