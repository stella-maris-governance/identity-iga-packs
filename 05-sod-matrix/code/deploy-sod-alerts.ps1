<#
.SYNOPSIS
    Deploy SoD detection as Sentinel scheduled analytics rule.
.PARAMETER Mode
    DryRun (default) or Deploy.
.NOTES
    Author: Robert Myers, MBA — Stella Maris Governance
    Requires: Az.SecurityInsights module
#>

[CmdletBinding()]
param(
    [ValidateSet("DryRun", "Deploy")]
    [string]$Mode = "DryRun",
    [Parameter(Mandatory)] [string]$WorkspaceName,
    [Parameter(Mandatory)] [string]$ResourceGroupName
)

$ErrorActionPreference = "Stop"

Write-Host "=== Stella Maris SoD Alert Deploy ==="
Write-Host "Mode: $Mode"
Write-Host "Workspace: $WorkspaceName"

$kqlPath = Join-Path $PSScriptRoot "sod-detection-scan.kql"
$kqlQuery = Get-Content $kqlPath -Raw

if ($Mode -eq "Deploy") {
    Connect-AzAccount
    New-AzSentinelAlertRule -ResourceGroupName $ResourceGroupName `
        -WorkspaceName $WorkspaceName `
        -Kind Scheduled `
        -DisplayName "SoD Conflict Detection — Weekly Scan" `
        -Description "Detects Separation of Duties violations in Entra directory role assignments" `
        -Severity High `
        -Query $kqlQuery `
        -QueryFrequency (New-TimeSpan -Days 7) `
        -QueryPeriod (New-TimeSpan -Days 7) `
        -TriggerOperator GreaterThan `
        -TriggerThreshold 0 `
        -Enabled
    Write-Host "[CREATED] SoD weekly scan analytics rule"
} else {
    Write-Host "[DRYRUN] Would create Sentinel rule: SoD Conflict Detection — Weekly Scan"
    Write-Host "[DRYRUN] Frequency: 7 days, Severity: High, Trigger: >0 results"
}

Write-Host "=== Complete ==="
