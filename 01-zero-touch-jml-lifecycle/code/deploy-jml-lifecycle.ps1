<#
.SYNOPSIS
    Deploy JML Lifecycle Workflows and Dynamic Groups.
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

Write-Host "=== Stella Maris JML Lifecycle Deploy ==="
Write-Host "Mode: $Mode"

Connect-MgGraph -Scopes "IdentityGovernance.ReadWrite.All","Group.ReadWrite.All","Directory.ReadWrite.All" -NoWelcome

# Deploy dynamic groups
$groupConfig = Get-Content "$PSScriptRoot/dynamic-group-rules.json" -Raw | ConvertFrom-Json

foreach ($group in $groupConfig.groups) {
    $existing = Get-MgGroup -Filter "displayName eq '$($group.displayName)'"
    if ($existing) {
        Write-Host "[SKIP] Group exists: $($group.displayName)"
    } elseif ($Mode -eq "Deploy") {
        New-MgGroup -DisplayName $group.displayName `
            -Description $group.description `
            -SecurityEnabled `
            -MailEnabled:$false `
            -MailNickname ($group.displayName -replace "[^a-zA-Z0-9]", "") `
            -GroupTypes @("DynamicMembership") `
            -MembershipRule $group.membershipRule `
            -MembershipRuleProcessingState "On"
        Write-Host "[CREATED] $($group.displayName)"
    } else {
        Write-Host "[DRYRUN] Would create: $($group.displayName) with rule: $($group.membershipRule)"
    }
}

Write-Host ""
Write-Host "Dynamic groups processed. Deploy lifecycle workflows manually in Entra portal"
Write-Host "or via Graph API using the JSON definitions in this directory."
Write-Host ""
Write-Host "=== Complete ==="

Disconnect-MgGraph
