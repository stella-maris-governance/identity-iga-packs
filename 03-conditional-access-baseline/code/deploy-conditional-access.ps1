<#
.SYNOPSIS
    Deploy Conditional Access baseline policies to Entra ID.
.DESCRIPTION
    Imports all 10 CA baseline policies from JSON. Supports Report-Only and Enabled modes.
    Requires Microsoft Graph PowerShell SDK.
.PARAMETER Mode
    ReportOnly (default, safe) or Enabled (production).
.PARAMETER BreakGlassGroupId
    Object ID of grp-ca-breakglass-exclude. REQUIRED.
.PARAMETER TermsOfUseId
    Object ID of the Terms of Use document (for CA007).
.PARAMETER BlockedCountriesLocationId
    Named location ID for Blocked Countries (for CA008).
.NOTES
    Author:  Robert Myers, MBA — Stella Maris Governance
    Version: 1.0.0
#>

[CmdletBinding()]
param(
    [ValidateSet("ReportOnly", "Enabled")]
    [string]$Mode = "ReportOnly",
    [string]$PolicyPath = $PSScriptRoot,
    [Parameter(Mandatory)] [string]$BreakGlassGroupId,
    [Parameter(Mandatory)] [string]$TermsOfUseId,
    [Parameter(Mandatory)] [string]$BlockedCountriesLocationId
)

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$logFile = Join-Path $PolicyPath "deployment-log-$timestamp.txt"

$policyOrder = @(
    "CA002-AllUsers-BlockLegacyAuth.json",
    "CA008-AllUsers-BlockRestrictedCountries.json",
    "CA001-AllUsers-RequireMFA.json",
    "CA005-Admins-RequireMFA.json",
    "CA003-AllUsers-RequireCompliantDevice.json",
    "CA006-AllUsers-SessionTimeout-Unmanaged.json",
    "CA007-Guests-RequireToU.json",
    "CA009-AllUsers-AppProtection-Mobile.json",
    "CA004-AllUsers-BlockHighRiskSignIn.json",
    "CA010-Admins-PhishingResistantMFA.json"
)

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $entry = "[$timestamp] [$Level] $Message"
    Write-Host $entry
    Add-Content -Path $logFile -Value $entry
}

function Replace-Placeholders {
    param([string]$Json)
    $Json = $Json -replace '\{\{GROUP_ID_grp-ca-breakglass-exclude\}\}', $BreakGlassGroupId
    $Json = $Json -replace '\{\{TERMS_OF_USE_ID\}\}', $TermsOfUseId
    $Json = $Json -replace '\{\{NAMED_LOCATION_ID_Blocked_Countries\}\}', $BlockedCountriesLocationId
    return $Json
}

Write-Log "=== Stella Maris Governance CA Baseline Deploy ==="
Write-Log "Mode: $Mode"

Connect-MgGraph -Scopes "Policy.ReadWrite.ConditionalAccess","Policy.Read.All","Directory.Read.All" -NoWelcome

$bgGroup = Get-MgGroup -GroupId $BreakGlassGroupId
Write-Log "Break-glass group verified: $($bgGroup.DisplayName)"

$deployed = 0; $failed = 0

foreach ($policyFile in $policyOrder) {
    $filePath = Join-Path $PolicyPath $policyFile
    if (-not (Test-Path $filePath)) { Write-Log "Not found: $policyFile" "WARN"; $failed++; continue }

    try {
        $json = Get-Content $filePath -Raw
        $json = Replace-Placeholders -Json $json
        $policy = $json | ConvertFrom-Json
        $policy.state = if ($Mode -eq "ReportOnly") { "enabledForReportingButNotEnforced" } else { "enabled" }
        $policyObj = $policy | Select-Object -Property * -ExcludeProperty _metadata

        $existing = Get-MgIdentityConditionalAccessPolicy -Filter "displayName eq '$($policy.displayName)'"
        if ($existing) {
            Update-MgIdentityConditionalAccessPolicy -ConditionalAccessPolicyId $existing.Id -State $policy.state
            Write-Log "Updated: $($policy.displayName)" "SUCCESS"
        } else {
            New-MgIdentityConditionalAccessPolicy -BodyParameter ($policyObj | ConvertTo-Json -Depth 10)
            Write-Log "Created: $($policy.displayName) [$($policy.state)]" "SUCCESS"
        }
        $deployed++
    } catch {
        Write-Log "FAILED: $policyFile - $_" "ERROR"
        $failed++
    }
    Start-Sleep -Seconds 2
}

Write-Log "=== Complete: $deployed deployed, $failed failed ==="
Disconnect-MgGraph
