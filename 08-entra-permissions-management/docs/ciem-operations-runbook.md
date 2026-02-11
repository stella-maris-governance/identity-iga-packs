# CIEM Operations Runbook — Entra Permissions Management

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for cloud infrastructure entitlement management using Entra Permissions Management. Covers discovery, right-sizing, monitoring, and periodic review of cloud permissions across Azure (and AWS/GCP when onboarded).

**Scope:** All cloud identities — users, service principals, managed identities, external identities — across onboarded subscriptions, accounts, and projects.

**Out of Scope:** Directory-level role governance (see Packs 01-07), application-level entitlements not managed through cloud IAM.

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Entra Permissions Management license | Entra Suite or standalone |
| Azure subscriptions onboarded | Data collectors active, minimum 14-day baseline |
| Activity logs enabled | Azure Activity Log, AWS CloudTrail, GCP Activity Logs |
| Remediation permissions | IAM Lead must have User Access Administrator or equivalent |
| PIM configured | Pack 04 — for migrating standing permissions to JIT |

---

## 3. Daily Operations

### Morning Check (5 minutes)

1. Open Permissions Management dashboard
2. Review overnight alerts — any High-Risk First Use or New Privilege Grant
3. Check data collection status — all subscriptions reporting
4. Note any PCI score changes above 10 points

### Alert Response

Every alert follows this chain:

1. Alert fires → notification to IAM Lead (email + Teams)
2. IAM Lead acknowledges within 1 hour
3. Investigate: legitimate or unauthorized?
4. Disposition: close with justification OR escalate + remediate
5. Document: alert ID, timestamp, acknowledgment time, disposition, justification

> **Watchstander Note:** An unacknowledged alert is a failed control. The acknowledgment timestamp is the evidence. If you cannot prove you received and reviewed the alert, the alert did not happen.

---

## 4. Right-Sizing Procedures

### Service Principals (Highest Priority)

Service principals accumulate permissions silently. They are the most over-scoped identity type in every environment.

1. Filter Permissions Management by identity type: Service Principal
2. Sort by PCI descending
3. For each PCI > 80:
   - Review granted vs used permissions (last 30 days)
   - Identify minimum required permission set
   - Check if built-in role exists that matches — if yes, assign it
   - If no built-in role fits, create custom role with exact permissions used
   - Apply at resource scope, not resource group or subscription
4. Verify: re-check PCI after 7 days

### Users

1. Filter by identity type: User, PCI > 67
2. For standing Contributor/Owner: migrate to PIM eligible (Pack 04)
3. For broad Reader assignments: scope to specific resource groups
4. For unused permissions: remove after confirming with user's manager

### Managed Identities

1. Filter by identity type: Managed Identity, PCI > 50
2. Common finding: resource group scope instead of resource scope
3. Re-scope to specific resource (Key Vault, Storage Account, etc.)
4. Verify application still functions after scope change

---

## 5. JIT Access Request Management

### Approving Requests

1. Request notification arrives (email + Teams)
2. Review: who is requesting, what permissions, what justification
3. Check: does the user have a legitimate need for this right now?
4. Check: does granting this create a SoD conflict? (reference Pack 05)
5. Approve or deny with written justification
6. All grants are time-bound — max 4 hours standard, 8 hours with escalation

### Pre-Approved Actions

Low-risk actions can be auto-approved to reduce friction:
- Reader elevation for troubleshooting (max 2 hours)
- Log Analytics query access (max 4 hours)
- Storage Blob Data Reader for data investigation (max 2 hours)

All pre-approved actions still logged and reviewable.

---

## 6. Monthly Permission Review

On the first Monday of each month:

1. Export PCI trend report (CSV)
2. Compare current average PCI to previous month
3. Identify any identity whose PCI increased by more than 15 points
4. For each PCI increase: investigate cause (new deployment? scope expansion? role change?)
5. Right-size any new high-PCI identities
6. Document review results for audit

### Quarterly Deep Review

Every 90 days:

1. Full service principal inventory — any new service principals since last review?
2. Managed identity scope audit — any re-scoped to broader level?
3. Custom role review — are custom roles still accurate to usage?
4. JIT request analysis — any users requesting the same elevation repeatedly? (Consider standing assignment if justified)
5. PCI target assessment — is the organization trending toward < 40 average?

---

## 7. Multi-Cloud Onboarding (When Ready)

### AWS

1. Enable CloudTrail in target accounts
2. Create cross-account IAM role for Permissions Management data collection
3. Configure in Permissions Management: Settings > Data Collectors > AWS
4. Wait 14 days for baseline

### GCP

1. Enable Activity Log export in target projects
2. Create service account with Viewer + Security Reviewer
3. Configure in Permissions Management: Settings > Data Collectors > GCP
4. Wait 14 days for baseline

> **Watchstander Note:** Multi-cloud onboarding doubles or triples the identity surface. Budget additional triage time for the first 30 days after each new cloud onboards.

---

## 8. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Alert response | Daily | IAM Lead |
| Data collection health | Daily | IAM Lead |
| PCI trend review | Monthly | IAM Lead |
| Right-sizing execution | Monthly | IAM Lead + DevOps |
| Service principal deep review | Quarterly | IAM Lead + Security |
| Custom role audit | Quarterly | IAM Lead |
| Full CIEM program assessment | Annual | IAM Lead + GRC |

---

## 9. Troubleshooting

**PCI not calculating:** Verify data collection is active and has been running for at least 14 days. Check subscription onboarding status.

**Right-size recommendation seems wrong:** Verify the baseline period is sufficient. Seasonal workloads may use permissions intermittently. Extend baseline to 30 days before right-sizing.

**Alert not firing:** Check alert rule is enabled. Verify notification channel (email/Teams) is configured. Test with a controlled privilege assignment.

**JIT request stuck:** Check approver received notification. Verify approval workflow is active. Check for conditional access policies blocking the Permissions Management portal.

---

*Stella Maris Governance — 2026*
