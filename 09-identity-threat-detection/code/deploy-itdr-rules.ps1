<#
.SYNOPSIS
    Deploy ITDR detection rules to Sentinel.
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

Write-Host "=== Stella Maris ITDR Rule Deployment ==="
Write-Host "Mode: $Mode"

$rules = @(
    @{ Name = "ITDR-001: Compromised Account Auto-Contain"; File = "itdr-001-compromised-account.kql"; Severity = "High"; Frequency = "PT15M"; Period = "PT15M"; Tier = "1" },
    @{ Name = "ITDR-004: Privilege Escalation Outside PIM"; File = "itdr-004-privilege-escalation.kql"; Severity = "High"; Frequency = "PT15M"; Period = "PT15M"; Tier = "2" },
    @{ Name = "ITDR-005: Dormant Account Reactivation"; File = "itdr-005-dormant-reactivation.kql"; Severity = "Medium"; Frequency = "PT1H"; Period = "P1D"; Tier = "2" },
    @{ Name = "ITDR-006: Service Principal Anomaly"; File = "itdr-006-sp-anomaly.kql"; Severity = "Medium"; Frequency = "PT1H"; Period = "P1D"; Tier = "2" }
)

foreach ($rule in $rules) {
    $kqlPath = Join-Path $PSScriptRoot $rule.File
    if (-not (Test-Path $kqlPath)) { Write-Host "[SKIP] Not found: $($rule.File)"; continue }

    if ($Mode -eq "Deploy") {
        $kql = Get-Content $kqlPath -Raw
        New-AzSentinelAlertRule -ResourceGroupName $ResourceGroupName `
            -WorkspaceName $WorkspaceName `
            -Kind Scheduled `
            -DisplayName $rule.Name `
            -Severity $rule.Severity `
            -Query $kql `
            -QueryFrequency ([System.Xml.XmlConvert]::ToTimeSpan($rule.Frequency)) `
            -QueryPeriod ([System.Xml.XmlConvert]::ToTimeSpan($rule.Period)) `
            -TriggerOperator GreaterThan `
            -TriggerThreshold 0 `
            -Enabled
        Write-Host "[CREATED] $($rule.Name) (Tier $($rule.Tier))"
    } else {
        Write-Host "[DRYRUN] Would create: $($rule.Name) (Tier $($rule.Tier), $($rule.Severity))"
    }
}

Write-Host ""
Write-Host "Tier 3 hunting queries: deploy as saved searches manually"
Write-Host "Playbook: deploy playbook-revoke-contain.json via Logic App"
Write-Host ""
Write-Host "=== Complete ==="
