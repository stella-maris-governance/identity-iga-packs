<#
.SYNOPSIS
    Deploy guest governance: cross-tenant settings + access packages.
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

Write-Host "=== Stella Maris Guest Governance Deploy ==="
Write-Host "Mode: $Mode"

Connect-MgGraph -Scopes "EntitlementManagement.ReadWrite.All","Policy.ReadWrite.CrossTenantAccess","Directory.ReadWrite.All" -NoWelcome

# Step 1: Configure guest invite restrictions
Write-Host ""
Write-Host "--- Guest Invite Restrictions ---"
if ($Mode -eq "Deploy") {
    Update-MgPolicyAuthorizationPolicy -AllowInvitesFrom "adminsAndGuestInviters"
    Write-Host "[CONFIGURED] Guest invites: admins and guest inviters only"
} else {
    Write-Host "[DRYRUN] Would set guest invites to: adminsAndGuestInviters"
}

# Step 2: Create catalog
Write-Host ""
Write-Host "--- Entitlement Management Catalog ---"
$catalogName = "External Access"
$existing = Get-MgEntitlementManagementCatalog -Filter "displayName eq '$catalogName'" -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "[EXISTS] Catalog: $catalogName"
} elseif ($Mode -eq "Deploy") {
    New-MgEntitlementManagementCatalog -DisplayName $catalogName -Description "Access packages for external/guest users" -IsExternallyVisible
    Write-Host "[CREATED] Catalog: $catalogName"
} else {
    Write-Host "[DRYRUN] Would create catalog: $catalogName"
}

Write-Host ""
Write-Host "Access packages must be created in the Entra portal or via Graph API"
Write-Host "using the JSON definitions in this directory."
Write-Host ""
Write-Host "=== Complete ==="
Disconnect-MgGraph
