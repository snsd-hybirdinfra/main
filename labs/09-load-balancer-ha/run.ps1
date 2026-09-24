param(
    [string]$EvidencePath = (Join-Path $PSScriptRoot 'evidence\2026-09-24.json')
)

$ErrorActionPreference = 'Stop'
$project = 'news-lab09'
$compose = Join-Path $PSScriptRoot 'compose.yaml'

function Compose {
    & docker compose -p $project -f $compose @args
    if ($LASTEXITCODE -ne 0) { throw "docker compose failed: $args" }
}

function Request-Backend {
    $timer = [System.Diagnostics.Stopwatch]::StartNew()
    $body = (Invoke-RestMethod -Uri 'http://127.0.0.1:18080/' -TimeoutSec 5).Trim()
    $timer.Stop()
    [ordered]@{ backend = $body; elapsed_ms = [math]::Round($timer.Elapsed.TotalMilliseconds, 2) }
}

function Sample([int]$count) {
    $items = @()
    1..$count | ForEach-Object {
        $items += Request-Backend
        Start-Sleep -Milliseconds 100
    }
    $items
}

Compose down --volumes --remove-orphans
try {
    Compose up -d
    $ready = $false
    1..30 | ForEach-Object {
        if (-not $ready) {
            try { $null = Request-Backend; $ready = $true } catch { Start-Sleep -Seconds 1 }
        }
    }
    if (-not $ready) { throw 'load balancer did not become ready' }

    $normal = @(Sample 8)
    Compose stop web01
    $duringFailure = @(Sample 8)
    Compose start web01

    $recovered = $false
    1..30 | ForEach-Object {
        if (-not $recovered) {
            $sample = Request-Backend
            if ($sample.backend -eq 'web01') { $recovered = $true } else { Start-Sleep -Milliseconds 250 }
        }
    }
    if (-not $recovered) { throw 'web01 did not rejoin the pool' }
    $afterRecovery = @(Sample 8)

    $normalBackends = @($normal.backend | Sort-Object -Unique)
    $failureBackends = @($duringFailure.backend | Sort-Object -Unique)
    $recoveryBackends = @($afterRecovery.backend | Sort-Object -Unique)
    $passed = ($normalBackends.Count -eq 2) -and
              ($failureBackends.Count -eq 1) -and ($failureBackends[0] -eq 'web02') -and
              ($recoveryBackends.Count -eq 2)

    $result = [ordered]@{
        tested_at = (Get-Date).ToUniversalTime().ToString('o')
        environment = 'Docker Desktop; nginx:alpine; loopback 127.0.0.1:18080'
        question = 'Does the service remain reachable when one backend stops, and does the backend rejoin after recovery?'
        normal = [ordered]@{ samples = $normal; counts = @($normal.backend | Group-Object | ForEach-Object { [ordered]@{ backend=$_.Name; requests=$_.Count } }) }
        web01_stopped = [ordered]@{ samples = $duringFailure; counts = @($duringFailure.backend | Group-Object | ForEach-Object { [ordered]@{ backend=$_.Name; requests=$_.Count } }) }
        web01_restarted = [ordered]@{ samples = $afterRecovery; counts = @($afterRecovery.backend | Group-Object | ForEach-Object { [ordered]@{ backend=$_.Name; requests=$_.Count } }) }
        assertions = [ordered]@{
            both_backends_seen_before_failure = ($normalBackends.Count -eq 2)
            only_web02_seen_during_web01_failure = (($failureBackends.Count -eq 1) -and ($failureBackends[0] -eq 'web02'))
            both_backends_seen_after_recovery = ($recoveryBackends.Count -eq 2)
        }
        passed = $passed
        limits = @('Synthetic HTTP responses only', 'Nginx passive retry, not an F5 BIG-IP health monitor', 'No TLS, session persistence, WAF, OAuth, exploit, or performance test')
    }
    $result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $EvidencePath -Encoding utf8NoBOM
    $result | ConvertTo-Json -Depth 8
    if (-not $passed) { exit 1 }
}
finally {
    Compose down --volumes --remove-orphans
}
