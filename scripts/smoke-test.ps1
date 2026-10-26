# Smoke test for a running TaskFlow API (Windows / local use)
# Usage: .\scripts\smoke-test.ps1 [-BaseUrl http://127.0.0.1:8000]
param([string]$BaseUrl = "http://127.0.0.1:8000")

$script:failed = $false

function Test-Endpoint {
    param([string]$Path, [int]$Expected)
    try {
        $code = (Invoke-WebRequest -UseBasicParsing -Uri "$BaseUrl$Path" -TimeoutSec 5).StatusCode
    } catch {
        if ($_.Exception.Response) { $code = [int]$_.Exception.Response.StatusCode } else { $code = 0 }
    }
    if ($code -eq $Expected) {
        Write-Host "PASS  $Path  ($code)"
    } else {
        Write-Host "FAIL  $Path  (got $code, expected $Expected)"
        $script:failed = $true
    }
}

Write-Host "Smoke testing $BaseUrl"
Test-Endpoint "/health" 200
Test-Endpoint "/version" 200
Test-Endpoint "/tasks" 200
Test-Endpoint "/does-not-exist" 404

if ($script:failed) { Write-Host "Smoke test FAILED"; exit 1 }
Write-Host "All smoke tests passed"