# Udemy Agent Production Startup Script
# PowerShell script to start the Udemy agent with advanced features

param(
    [switch]$Background,
    [switch]$Test,
    [switch]$Silent
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMessage = "[$Timestamp] [$Level] $Message"

    if (-not $Silent) {
        switch ($Level) {
            "ERROR" { Write-Host $LogMessage -ForegroundColor Red }
            "WARNING" { Write-Host $LogMessage -ForegroundColor Yellow }
            "SUCCESS" { Write-Host $LogMessage -ForegroundColor Green }
            default { Write-Host $LogMessage }
        }
    }

    # Also log to file
    $LogDir = "logs"
    if (-not (Test-Path $LogDir)) {
        New-Item -ItemType Directory -Path $LogDir | Out-Null
    }
    $LogFile = "$LogDir\udemy_agent_startup_$(Get-Date -Format 'yyyyMMdd').log"
    Add-Content -Path $LogFile -Value $LogMessage
}

function Test-Requirements {
    Write-Log "Checking system requirements..."

    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Log "Python found: $pythonVersion"
    } catch {
        Write-Log "Python is not installed or not in PATH" -Level "ERROR"
        exit 1
    }

    # Check .env file
    if (-not (Test-Path ".env")) {
        Write-Log ".env file not found. Email notifications may not work." -Level "WARNING"
        Write-Log "Copy .env.example to .env and configure your email settings." -Level "WARNING"
    } else {
        Write-Log ".env file found"
    }

    # Check required packages
    $requiredPackages = @("selenium", "requests", "beautifulsoup4", "schedule")
    foreach ($package in $requiredPackages) {
        try {
            python -c "import $package" 2>&1 | Out-Null
            Write-Log "$package package found"
        } catch {
            Write-Log "$package package not found. Run 'pip install -r requirements.txt'" -Level "ERROR"
            exit 1
        }
    }
}

function Start-Agent {
    param([bool]$RunInBackground = $false)

    if ($Test) {
        Write-Log "Running in test mode..."
        python udemy_agent_production.py
        return
    }

    if ($RunInBackground) {
        Write-Log "Starting agent in background mode..."

        # Start as background job
        $job = Start-Job -ScriptBlock {
            param($WorkingDir)
            Set-Location $WorkingDir
            python udemy_agent_production.py
        } -ArgumentList (Get-Location)

        Write-Log "Agent started in background with Job ID: $($job.Id)" -Level "SUCCESS"
        Write-Log "To check status: Get-Job -Id $($job.Id)"
        Write-Log "To stop: Stop-Job -Id $($job.Id)"

        return
    }

    Write-Log "Starting Udemy Agent in production mode..."
    Write-Log "Press Ctrl+C to stop the agent"

    try {
        python udemy_agent_production.py
    } catch {
        Write-Log "Agent stopped with error: $_" -Level "ERROR"
    }
}

function Show-Help {
    Write-Host @"
Udemy Agent Startup Script

Usage:
    .\start_udemy_agent.ps1 [options]

Options:
    -Background    Run agent in background as a job
    -Test         Run agent in test mode (single check)
    -Silent       Suppress console output

Examples:
    .\start_udemy_agent.ps1                    # Start interactively
    .\start_udemy_agent.ps1 -Background       # Start in background
    .\start_udemy_agent.ps1 -Test             # Run test mode
    .\start_udemy_agent.ps1 -Background -Silent # Silent background mode

To stop background agent:
    Get-Job | Where-Object {$_.Name -like "*udemy*"} | Stop-Job

For more information, see README.md
"@
}

# Main script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Udemy Free Course Monitor Agent" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host

if ($args -contains "-h" -or $args -contains "--help") {
    Show-Help
    exit 0
}

Test-Requirements

if ($Background) {
    Start-Agent -RunInBackground $true
} else {
    Start-Agent -RunInBackground $false
}