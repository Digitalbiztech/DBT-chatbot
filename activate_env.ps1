# PowerShell script to activate Python virtual environment
Write-Host "Activating Python Virtual Environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"
Write-Host "Virtual environment activated!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the application: python main.py" -ForegroundColor Yellow
Write-Host "To deactivate: deactivate" -ForegroundColor Yellow 