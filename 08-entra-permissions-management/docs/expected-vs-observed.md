# The Law of Evidence: Expected vs. Observed

## Entra Permissions Management (CIEM)

> **Assessment Date:** 2026-02-10 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab Tenant + Azure Subscriptions [SAMPLE]
> **Assessor:** Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC
> **Pack Version:** 1.0.0
> **Status:** 9/10 controls confirmed | 1 partial | 0 failed

---

## Summary

| Status | Count | Percentage |
|--------|-------|------------|
| Pass | 9 | 90% |
| Partial | 1 | 10% |
| Fail | 0 | 0% |

---

## Assessment Detail

### 1 — Permissions Management Onboarded Across All Azure Subscriptions

| Field | Detail |
|-------|--------|
| **Expected State** | All Azure subscriptions onboarded to Entra Permissions Management. Data collectors active and reporting. Identity inventory complete across users, service principals, and managed identities. |
| **Observed State** | **3 subscriptions** onboarded: Production, Development, Shared Services. Data collectors active with hourly collection. **214 identities** inventoried: 147 users, 38 service principals, 22 managed identities, 7 external identities. Last successful collection: 2026-02-10 04:00 UTC. |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | AC-2 |
| **Status** | **Pass** |

---

### 2 — Permission Creep Index Baseline Established

| Field | Detail |
|-------|--------|
| **Expected State** | PCI scores calculated for all identities after minimum 14-day baseline. Organization-wide average PCI documented. Target: average PCI below 40. |
| **Observed State** | Baseline period: Jan 15 — Feb 10 (26 days). Organization-wide average PCI: **62.4** (above target — expected in pre-remediation state). Breakdown: Users average 54.3, Service Principals average 78.1, Managed Identities average 47.2. **38 identities** above PCI 80 (critical). |
| **Evidence** | Screenshot #05 |
| **NIST 800-53** | AC-6 |
| **Status** | **Pass** |

---

### 3 — High-PCI Identities Identified and Triaged

| Field | Detail |
|-------|--------|
| **Expected State** | All identities with PCI above 80 identified, triaged, and assigned remediation owner. Each high-PCI identity has a documented reason for elevated permissions and a right-sizing plan. |
| **Observed State** | **38 identities** with PCI above 80. Triage complete: 31 service principals (over-scoped from initial deployment), 4 users (standing Contributor from past projects), 3 managed identities (resource group scope instead of resource-specific). Top finding: svc-devops-pipeline has PCI 96 — Owner on Production subscription, used only 4 of 412 available actions in 26 days. All assigned remediation owner (IAM Lead). |
| **Evidence** | Screenshot #02 |
| **NIST 800-53** | AC-6, AC-2(7) |
| **Status** | **Pass** |

---

### 4 — Service Principal Right-Sizing Executed

| Field | Detail |
|-------|--------|
| **Expected State** | Service principals with PCI above 80 right-sized to match actual usage. Custom roles created where built-in roles are too broad. Right-sizing verified by post-change PCI recalculation. |
| **Observed State** | **Phase 1 right-sizing complete** (top 10 service principals). svc-devops-pipeline: Owner → custom role with 4 specific actions (PCI dropped 96 → 12). svc-backup-agent: Contributor → Storage Blob Data Contributor (PCI 89 → 18). svc-monitoring: Reader + Log Analytics Contributor scoped to resource group (PCI 82 → 22). 7 additional service principals right-sized. Average service principal PCI: 78.1 → **41.3** after Phase 1. |
| **Evidence** | Screenshot #03 |
| **NIST 800-53** | AC-6(1) |
| **Status** | **Pass** |

---

### 5 — User Standing Permissions Remediated

| Field | Detail |
|-------|--------|
| **Expected State** | Users with standing Contributor or Owner on subscriptions/resource groups right-sized or migrated to PIM JIT activation. No standing high-privilege assignments without documented exception. |
| **Observed State** | 4 users with standing Contributor identified. 3 migrated to PIM eligible assignments (activate on demand, max 8 hours). 1 user (rmyers-admin) retains standing on lab subscription — documented exception (single admin in lab environment, compensated by PIM MFA + justification). Post-remediation: 0 standing Contributor/Owner for standard users. |
| **Evidence** | Pack 04 E-v-O, Screenshot #02 |
| **NIST 800-53** | AC-6(7) |
| **Status** | **Pass** |

---

### 6 — Managed Identity Permissions Scoped to Resource Level

| Field | Detail |
|-------|--------|
| **Expected State** | Managed identities scoped to specific resources, not resource groups or subscriptions. Each managed identity has permissions matching its actual resource access pattern. |
| **Observed State** | 22 managed identities reviewed. 19 already scoped to resource level. **3 managed identities** found with resource group scope: mi-webapp-prod (Key Vault access for 1 vault, scoped to entire RG), mi-function-data (Storage access for 1 account, scoped to entire RG), mi-logic-app (Service Bus access for 1 namespace, scoped to entire RG). All 3 re-scoped to resource level. Post-remediation PCI: all 3 below 25. |
| **Evidence** | Screenshot #03 |
| **NIST 800-53** | AC-6 |
| **Status** | **Pass** |

---

### 7 — Anomaly Alerts Configured and Tested

| Field | Detail |
|-------|--------|
| **Expected State** | Permission anomaly alerts active for: first-time use of high-risk actions, permission usage outside normal pattern, and new high-privilege role assignments. Alerts route to IAM Lead and Security. |
