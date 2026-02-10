# Expected vs Observed — Separation of Duties Matrix

> **Assessment Date:** 2026-02-10 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab Tenant [SAMPLE — replace with your tenant name]
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

### 1 — SoD Conflict Matrix Defined and Approved

| Field | Detail |
|-------|--------|
| **Expected State** | Conflict matrix exists documenting all prohibited role combinations across Entra ID directory roles and business applications. Matrix is reviewed and approved by security leadership. |
| **Observed State** | Matrix **defined** with **12 conflicts** across 3 tiers: 4 Critical (Tier 1), 4 High (Tier 2), 4 Business Application (Tier 3). Covers Entra directory roles (SOD-001 through SOD-008) and finance/HR/ITSM application roles (SOD-009 through SOD-012). Approved by tenant owner 2026-01-20. Machine-readable version in sod-conflict-matrix.json. |
| **Evidence** | README conflict matrix, code/sod-conflict-matrix.json |
| **NIST 800-53** | AC-5 |
| **Status** | **Pass** |

---

### 2 — Tier 1 Critical Conflicts Scanned — No Violations

| Field | Detail |
|-------|--------|
| **Expected State** | Weekly KQL scan confirms zero Tier 1 (Critical) SoD violations. No user holds both roles in any Tier 1 conflict pair simultaneously. |
| **Observed State** | Scan executed 2026-02-10. **SOD-001 (GA + SecAdmin):** 1 user flagged — rmyers-admin holds eligible assignments for both Global Admin and Security Admin. This is a **known exception** (EXC-SOD-001-01) documented in exception register. Lab tenant has single admin. **SOD-002, SOD-003, SOD-004:** 0 violations. |
| **Evidence** | KQL scan output, Screenshot #01 |
| **NIST 800-53** | AC-5 |
| **Finding** | SOD-001 exception is documented with compensating controls. See control 7. |
| **Status** | **Partial** — exception exists, documented and compensated |

---

### 3 — Tier 2 High Conflicts Scanned — No Violations

| Field | Detail |
|-------|--------|
| **Expected State** | Weekly scan confirms zero unexcepted Tier 2 (High) violations. Any exceptions are documented with compensating controls. |
| **Observed State** | Scan executed 2026-02-10. **SOD-005 through SOD-008:** 0 violations found. No users hold any Tier 2 conflict pairs. Clean scan. |
| **Evidence** | KQL scan output |
| **NIST 800-53** | AC-5 |
| **Status** | **Pass** |

---

### 4 — Tier 3 Business Application Conflicts Documented

| Field | Detail |
|-------|--------|
| **Expected State** | Business application SoD conflicts (finance, HR, ITSM) are defined in the matrix. Detection queries exist for each system or are documented for manual review. |
| **Observed State** | 4 business application conflicts defined (SOD-009 through SOD-012). Entra-native detection covers role group memberships. For ERP-specific roles (AP Clerk, AP Approver, Vendor Master), detection requires application-level query — documented in runbook as manual quarterly check until ERP integration is built. Finance team acknowledged 2026-01-25. |
| **Evidence** | sod-conflict-matrix.json, runbook section 5 |
| **NIST 800-53** | AC-5 |
| **SOX** | Segregation of duties |
| **Status** | **Pass** |

---

### 5 — Weekly Automated SoD Scan Running

| Field | Detail |
|-------|--------|
| **Expected State** | Sentinel analytics rule runs weekly SoD detection query against all Entra directory role assignments. Alert generated on any new violation. |
| **Observed State** | Sentinel scheduled rule **active** since 2026-01-22. Frequency: every 7 days (Sunday 02:00 UTC). Query checks all active and eligible role assignments against conflict matrix. **4 weekly scans completed.** 1 consistent finding: SOD-001 exception (rmyers-admin). No new violations detected across 4 weeks. Alert delivered via email and Teams. |
| **Evidence** | Screenshot #04 |
| **NIST 800-53** | AC-6(7) |
| **Status** | **Pass** |

---

### 6 — SoD Scan Covers Both Active and Eligible Assignments

| Field | Detail |
|-------|--------|
| **Expected State** | Detection query scans PIM eligible assignments in addition to active assignments. A user who is eligible for two conflicting roles is a violation even if not currently activated. |
| **Observed State** | KQL query joins both roleAssignmentScheduleInstances (active) and roleEligibilityScheduleInstances (eligible). Confirmed: rmyers-admin flagged via eligible assignments (not active — no standing admin per Pack 04). Detection correctly identifies future conflict potential, not just current state. |
| **Evidence** | KQL query source, scan output |
| **NIST 800-53** | AC-5(1) |
| **Status** | **Pass** |

---

### 7 — All Exceptions Documented with Compensating Controls

| Field | Detail |
|-------|--------|
| **Expected State** | Every SoD exception has: business justification, compensating controls, executive approval, expiration date (max 90 days), and quarterly review schedule. |
| **Observed State** | **1 active exception:** EXC-SOD-001-01 (rmyers-admin, GA + SecAdmin in lab tenant). Justification: single administrator in lab environment. Compensating controls: all PIM activations require MFA + justification, weekly audit log review, PIM activation alert fires on every use. Approved by: tenant owner. Expiry: 2026-04-01 (90 days). Quarterly review: scheduled. |
| **Evidence** | code/sod-exception-register.md, Screenshot #03 |
| **NIST 800-53** | AC-5 |
| **SOX** | Compensating controls |
| **Status** | **Pass** |

---

### 8 — PIM Approval Workflow References SoD Matrix

| Field | Detail |
|-------|--------|
| **Expected State** | PIM approvers are instructed to check the SoD matrix before approving Global Admin activations. Approval justification should reference SoD review. |
| **Observed State** | PIM approval guidance updated in Pack 04 runbook to include SoD check step. Approver checklist: "Before approving, verify requesting user does not hold a conflicting role per SoD matrix." Last 3 Global Admin approvals include justification noting no SoD conflict. Process is manual (no automated block) — documented as acceptable for current tenant size. |
| **Evidence** | Pack 04 runbook, PIM approval logs |
| **NIST 800-53** | AC-5(1), AC-6(1) |
| **Status** | **Pass** |

---

### 9 — Access Reviews Flag SoD Conflicts

| Field | Detail |
|-------|--------|
| **Expected State** | Quarterly access reviews (Pack 02) include SoD conflict awareness. Reviewers are guided to check for role conflicts when certifying access. |
| **Observed State** | Access review descriptions updated to include: "When approving, verify user does not hold a conflicting role per the SoD conflict matrix in Pack 05." AR-PIM-Quarterly reviewer (Security Admin) confirmed: reviewed 4 eligible assignments against conflict matrix during January cycle. 1 known exception noted in review justification. |
| **Evidence** | Pack 02 review definitions, review decision justifications |
| **NIST 800-53** | AC-6(7) |
| **Status** | **Pass** |

---

### 10 — SoD Scan Results Export to Log Analytics

| Field | Detail |
|-------|--------|
| **Expected State** | All SoD scan results, alerts, and exception changes export to Log Analytics. Minimum 90-day retention. |
| **Observed State** | Sentinel analytics rule outputs to SecurityAlert table. KQL query returns **4 weekly scan events** and **1 alert instance** (SOD-001 exception, consistent across all scans). Diagnostic settings active, retention 90 days. Historical trend available for audit: violations detected, exceptions active, remediation status. |
| **Evidence** | KQL output |
| **NIST 800-53** | AU-3, AU-6 |
| **Status** | **Pass** |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 2 | Tier 1 scan | SOD-001 exception (GA + SecAdmin, single admin) | R. Myers | Add second admin to tenant OR accept exception with quarterly renewal | 2026-04-01 | Exception active |

---

## Assessment Notes

1. **Intentional partial (control 2):** The SOD-001 exception is real and honest. In a lab tenant with one administrator, holding both GA and Security Admin eligible is operationally necessary. The compensating controls (PIM with MFA + justification, weekly audit review, activation alerts) are robust. In a production environment with multiple admins, this would be remediated by assigning different people.

2. **Eligible assignments count as violations.** This is a critical design choice. A user who is eligible for two conflicting roles has the capability to activate both simultaneously. Detection must cover PIM eligible, not just active.

3. **Business application SoD (Tier 3) requires application-level integration.** Entra can detect Entra role conflicts natively. For ERP/finance role conflicts (AP Clerk + AP Approver), detection requires SailPoint, Saviynt, or application-native reporting. This pack documents the conflicts; implementation depends on the IGA platform.

4. **SoD is where accounting background differentiates.** Most identity engineers can configure PIM. Knowing that AP Clerk + AP Approver is a SOX-critical conflict — and why — comes from understanding financial controls. BS Accounting matters here.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
