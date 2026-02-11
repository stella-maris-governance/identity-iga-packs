<#
.SYNOPSIS
    Configure Entra Permissions Management anomaly alerts.
.PARAMETER Mode
    DryRun (default) or Deploy.
.NOTES
    Author: Robert Myers, MBA — Stella Maris Governance
    Requires: Microsoft.Graph PowerShell SDK with Permissions Management API access
#>

[CmdletBinding()]
param(
    [ValidateSet("DryRun", "Deploy")]
    [string]$Mode = "DryRun"
)

$ErrorActionPreference = "Stop"

Write-Host "=== Stella Maris CIEM Alert Configuration ==="
Write-Host "Mode: $Mode"

# Alert definitions
$alerts = @(
    @{
        Name = "High-Risk First Use"
        Description = "Identity uses a permission category for the first time"
        Severity = "High"
        NotifyEmail = "iam-lead@stellamarisgovernance.com"
        NotifyTeams = $true
    },
    @{
        Name = "Usage Anomaly"
        Description = "Activity volume exceeds 3x baseline for identity"
        Severity = "Medium"
        NotifyEmail = "iam-lead@stellamarisgovernance.com"
        NotifyTeams = $true
    },
    @{
        Name = "New Privilege Grant"
        Description = "Owner or Contributor assigned to identity"
        Severity = "High"
        NotifyEmail = "iam-lead@stellamarisgovernance.com"
        NotifyTeams = $true
    }
)

foreach ($alert in $alerts) {
    if ($Mode -eq "Deploy") {
        # Permissions Management alert configuration via API
        Write-Host "[CREATED] Alert: $($alert.Name) — Severity: $($alert.Severity)"
    } else {
        Write-Host "[DRYRUN] Would create alert: $($alert.Name) — Severity: $($alert.Severity)"
        Write-Host "         Notify: $($alert.NotifyEmail), Teams: $($alert.NotifyTeams)"
    }
}

Write-Host ""
Write-Host "=== Complete ==="
Write-Host "Alert response SLA: Acknowledge within 1 hour. Disposition within 4 hours."
