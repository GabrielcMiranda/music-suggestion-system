Write-Host "🚀 Iniciando Rhythmate..." -ForegroundColor Cyan

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

Set-Location docker
docker-compose up --build -d
Set-Location ..

Write-Host ""
Write-Host "✅ Sistema iniciado!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Acesse:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Para ver logs: docker-compose -f docker/docker-compose.yml logs -f" -ForegroundColor Yellow
Write-Host "Para parar: .\scripts\stop.ps1" -ForegroundColor Yellow
