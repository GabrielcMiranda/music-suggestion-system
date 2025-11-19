Write-Host "🎵 Music Suggestion System - Docker Setup 🎵" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

if (-not (Test-Path ".env")) {
    Write-Host "❌ Erro: Arquivo .env não encontrado!" -ForegroundColor Red
    Write-Host "Crie um arquivo .env na raiz do projeto com as variáveis necessárias." -ForegroundColor Yellow
    exit 1
}

Write-Host "📋 Verificando Docker..." -ForegroundColor Yellow
docker --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker não está instalado!" -ForegroundColor Red
    exit 1
}

docker ps 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker Desktop não está rodando!" -ForegroundColor Red
    Write-Host "Por favor, inicie o Docker Desktop e tente novamente." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Docker está rodando!" -ForegroundColor Green
Write-Host ""

Write-Host "Escolha uma opção:" -ForegroundColor Cyan
Write-Host "1. Iniciar todos os serviços (build + up)"
Write-Host "2. Iniciar serviços (sem rebuild)"
Write-Host "3. Parar todos os serviços"
Write-Host "4. Parar e remover volumes (APAGA DADOS!)"
Write-Host "5. Ver logs dos containers"
Write-Host "6. Rebuild apenas um serviço"
Write-Host ""
$opcao = Read-Host "Digite o número da opção"

switch ($opcao) {
    "1" {
        Write-Host "🔨 Fazendo build e iniciando serviços..." -ForegroundColor Yellow
        Set-Location docker
        docker-compose up --build -d
        Set-Location ..
        
        Write-Host ""
        Write-Host "✅ Serviços iniciados!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🌐 URLs disponíveis:" -ForegroundColor Cyan
        Write-Host "   Frontend: http://localhost" -ForegroundColor White
        Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
        Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
        Write-Host ""
        Write-Host "📊 Para ver logs: .\scripts\start.ps1 e escolha opção 5" -ForegroundColor Yellow
    }
    
    "2" {
        Write-Host "🚀 Iniciando serviços..." -ForegroundColor Yellow
        Set-Location docker
        docker-compose up -d
        Set-Location ..
        
        Write-Host ""
        Write-Host "✅ Serviços iniciados!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🌐 URLs disponíveis:" -ForegroundColor Cyan
        Write-Host "   Frontend: http://localhost" -ForegroundColor White
        Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
        Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
    }
    
    "3" {
        Write-Host "🛑 Parando serviços..." -ForegroundColor Yellow
        Set-Location docker
        docker-compose down
        Set-Location ..
        Write-Host "✅ Serviços parados!" -ForegroundColor Green
    }
    
    "4" {
        Write-Host "⚠️  ATENÇÃO: Isso vai apagar todos os dados do banco!" -ForegroundColor Red
        $confirma = Read-Host "Tem certeza? (s/N)"
        if ($confirma -eq "s" -or $confirma -eq "S") {
            Write-Host "🗑️  Parando e removendo volumes..." -ForegroundColor Yellow
            Set-Location docker
            docker-compose down -v
            Set-Location ..
            Write-Host "✅ Serviços parados e volumes removidos!" -ForegroundColor Green
        } else {
            Write-Host "❌ Operação cancelada." -ForegroundColor Yellow
        }
    }
    
    "5" {
        Write-Host "📊 Mostrando logs (Ctrl+C para sair)..." -ForegroundColor Yellow
        Write-Host ""
        Set-Location docker
        docker-compose logs -f
        Set-Location ..
    }
    
    "6" {
        Write-Host "Serviços disponíveis: backend, frontend, db" -ForegroundColor Cyan
        $servico = Read-Host "Digite o nome do serviço"
        Write-Host "🔨 Rebuilding $servico..." -ForegroundColor Yellow
        Set-Location docker
        docker-compose up --build -d $servico
        Set-Location ..
        Write-Host "✅ Serviço $servico atualizado!" -ForegroundColor Green
    }
    
    default {
        Write-Host "❌ Opção inválida!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✨ Concluído!" -ForegroundColor Green
