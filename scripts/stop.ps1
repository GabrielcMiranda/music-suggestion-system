Write-Host "🛑 Parando Music Suggestion System..." -ForegroundColor Yellow

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

Set-Location docker
docker-compose down
Set-Location ..

Write-Host ""
Write-Host "✅ Todos os serviços foram parados!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Dica: Os dados do banco foram preservados." -ForegroundColor Cyan
Write-Host "   Para apagar tudo: .\scripts\start.ps1 e escolha opção 4" -ForegroundColor Yellow
