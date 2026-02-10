<#
.SYNOPSIS
    Deploy Access Review schedules to Entra ID.
.PARAMETER Mode
    DryRun (default) or Deploy.
.NOTES
    Author: Robert Myers, MBA — Stella Maris Governance
    Requires: Microsoft.Graph PowerShell SDK
#>

[CmdletBinding()]
param(
    [ValidateSet("DryRun", "Deploy")]
    [string]$Mode = "DryRun"
)

$ErrorActionPreference = "Stop"

Write-Host "=== Stella Maris Access Reviews Deploy ==="
Write-Host "Mode: $Mode"

Connect-MgGraph -Scopes "AccessReview.ReadWrite.All","Directory.Read.All" -NoWelcome

$reviewFiles = @(
    "access-review-group.json",
    "access-review-app.json",
    "access-review-pim.json",
    "access-review-guest.json"
)

foreach ($file in $reviewFiles) {
    $filePath = Join-Path $PSScriptRoot $file
    if (-not (Test-Path $filePath)) { Write-Host "[SKIP] Not found: $file"; continue }

    $config = Get-Content $filePath -Raw | ConvertFrom-Json
    $reviewName = $config.displayName

    $existing = Get-MgIdentityGovernanceAccessReviewDefinition -Filter "displayName eq '$reviewName'" -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Host "[EXISTS] $reviewName — already configured"
    } elseif ($Mode -eq "Deploy") {
        $body = $config | Select-Object -Property * -ExcludeProperty _metadata | ConvertTo-Json -Depth 10
        New-MgIdentityGovernanceAccessReviewDefinition -BodyParameter $body
        Write-Host "[CREATED] $reviewName"
    } else {
        Write-Host "[DRYRUN] Would create: $reviewName"
    }
}

Write-Host ""
Write-Host "=== Complete ==="
Disconnect-MgGraph
