# The Law of Evidence: Expected vs. Observed

## SailPoint IdentityIQ Configuration

> **Assessment Date:** 2026-02-10 [SAMPLE — replace with your assessment date]
> **Environment:** SailPoint IIQ 8.4 Sandbox [SAMPLE — replace with your environment]
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

### 1 — Authoritative Source Connected and Aggregating

| Field | Detail |
|-------|--------|
| **Expected State** | HR system configured as authoritative source. Identity attributes (name, department, title, manager, hire date, termination date) flow from HR to IIQ on scheduled aggregation. Correlation rules match identities across connected systems. |
| **Observed State** | HR flat file connector **active** with daily aggregation schedule (06:00 UTC). **147 identities** correlated. Attribute mapping confirmed: firstName, lastName, department, title, manager, startDate, endDate. Correlation rule: match on employeeId (primary), email (secondary). Last successful aggregation: 2026-02-10 06:02 UTC, 0 errors. |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | AC-2 |
| **Status** | **Pass** |

---

### 2 — Joiner Lifecycle Provisions Accounts Automatically

| Field | Detail |
|-------|--------|
| **Expected State** | When a new identity appears with active status and hire date reached, IIQ automatically creates accounts in target systems (AD, Entra) and assigns birthright role. No manual provisioning. |
| **Observed State** | Joiner lifecycle event **active.** Trigger: identity.status == "Active" AND no linked accounts. Actions: create AD account (OU based on department), create Entra account (sync via AD Connect), assign Corporate-Baseline birthright role. **6 joiner events** in 30 days, all completed successfully. Average provisioning time: 3 minutes from trigger to account creation. |
| **Evidence** | Screenshot #02, provisioning audit trail |
| **NIST 800-53** | AC-2 |
| **Status** | **Pass** |

---

### 3 — Mover Lifecycle Recalculates Access

| Field | Detail |
|-------|--------|
| **Expected State** | When department or manager changes during aggregation, IIQ recalculates role assignments. Old department roles removed, new department roles assigned. Manager notified. |
| **Observed State** | Mover event **active.** Trigger: department or manager attribute change detected. **2 mover events** in 30 days. Test case: user asmith moved from Sales to Engineering. Old roles (Sales-Department, Salesforce-Standard-User) removed. New roles (Engineering-Department, Jira-Developer) assigned. Old and new managers notified via email. Total transition: 8 minutes from aggregation to completion. |
| **Evidence** | Provisioning audit trail |
| **NIST 800-53** | PS-5 |
| **Status** | **Pass** |

---

### 4 — Leaver Lifecycle Disables and Removes Access

| Field | Detail |
|-------|--------|
| **Expected State** | When identity status changes to Inactive or termination date is reached, IIQ disables all accounts, removes all entitlements, and archives the identity. No manual deprovisioning. |
| **Observed State** | Leaver event **active.** Trigger: identity.status == "Inactive" OR endDate reached. Actions: disable AD account (move to Disabled OU), disable Entra account, remove all role assignments, remove all direct entitlements. **3 leaver events** in 30 days, all completed. Last event: bwilson terminated Feb 7 — 4 accounts disabled, 7 entitlements removed, identity archived. Total: 6 minutes. |
| **Evidence** | Screenshot #02, provisioning audit trail |
| **NIST 800-53** | AC-2(3), PS-4 |
| **Status** | **Pass** |

---

### 5 — Role Model Implemented with Birthright and Business Roles

| Field | Detail |
|-------|--------|
| **Expected State** | Role hierarchy defined: birthright roles (auto-assigned), IT roles (single-system entitlements), business roles (multi-system bundles). All employees receive birthright role. Department-specific access via organizational roles. |
| **Observed State** | Role model **configured.** 1 birthright role (Corporate-Baseline: email, intranet, HR self-service). 8 IT roles mapped to specific system entitlements. 4 business roles bundling IT roles by function (Engineer, Sales Rep, Finance Analyst, HR Specialist). 5 organizational roles by department. Role assignment: automatic via department attribute. **147 identities** all have birthright role assigned. |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | AC-6 |
| **Status** | **Pass** |

---

### 6 — Quarterly Manager Certification Campaign Completed

| Field | Detail |
|-------|--------|
| **Expected State** | Manager Access Review campaign runs quarterly. Every manager certifies direct reports' access. Non-response auto-revokes after 14 days. Decisions include justification. |
| **Observed State** | Campaign **completed** (Q1 2026, Jan 15 - Jan 29). **12 managers** participated, **87 access items** reviewed. Completion rate: **96.6%** (84 decisions made, 3 auto-revoked). 5 items denied with justification ("user no longer needs Salesforce — transferred"). All deny decisions resulted in automated revocation within 4 hours. |
| **Evidence** | Screenshot #03 |
| **NIST 800-53** | AC-6(7) |
| **SOX** | Periodic access review |
| **Status** | **Pass** |

---

### 7 — SOD Policies Active with Real-Time Detection

| Field | Detail |
|-------|--------|
| **Expected State** | SOD policies defined for financial and IT role conflicts. Violations detected during access request, certification, and aggregation. Critical conflicts (SOD-FIN-001, SOD-FIN-002) block access. High conflicts alert and require exception. |
| **Observed State** | **4 SOD policies** active (SOD-FIN-001, SOD-FIN-002, SOD-HR-001, SOD-IT-001). Detection runs during: access request workflow, certification campaign, scheduled scan (weekly). **1 violation detected** in 30 days: SOD-IT-001 (Change Requester + Change Approver) for user jdoe — alert generated, exception required. No critical (blocking) violations in 30 days. |
| **Evidence** | Screenshot #04 |
| **NIST 800-53** | AC-5 |
| **SOX** | Segregation of duties |
| **Status** | **Pass** |

---

### 8 — Access Request Workflow with Approval

| Field | Detail |
|-------|--------|
| **Expected State** | Users request access through IIQ self-service portal. Requests route to manager and/or entitlement owner for approval. SOD check runs before approval. Provisioning executes automatically after approval. |
| **Observed State** | Self-service portal **active.** Request workflow: user submits → SOD pre-check → manager approval → entitlement owner approval (for high-risk) → auto-provisioning. **14 access requests** in 30 days: 11 approved (auto-provisioned), 2 denied by manager, 1 blocked by SOD pre-check (SOD-FIN-001). Average approval-to-provisioning time: 22 minutes. |
| **Evidence** | Provisioning audit trail |
| **NIST 800-53** | AC-2 |
| **Status** | **Pass** |

---

### 9 — Provisioning Audit Trail Complete

| Field | Detail |
|-------|--------|
| **Expected State** | Every provisioning action (create, modify, disable, enable, remove entitlement) logged with identity, target system, action, timestamp, result, and triggering event. Exportable for audit. |
| **Observed State** | Audit configuration **active** for all provisioning plans. **243 audit events** in 30 days: 18 account creates, 4 account disables, 14 entitlement grants, 8 entitlement revokes, 87 certification decisions, 14 access requests, and 98 aggregation events. All events include identity, system, action, timestamp, result. CSV export confirmed functional. |
| **Evidence** | Screenshot #05 |
| **NIST 800-53** | AU-2, AC-2(4) |
| **Status** | **Pass** |

---

### 10 — Entitlement Owner Certification for High-Risk Access

| Field | Detail |
|-------|--------|
| **Expected State** | High-risk entitlements (admin roles, financial system access, PII access) have designated owners. Entitlement owner certification runs quarterly alongside manager certification. |
| **Observed State** | Entitlement Owner Review campaign configured for quarterly execution. Scope: 12 high-risk entitlements across AD, ERP, and HR system. **First campaign in progress** — started Feb 1, due Feb 14. 8 of 12 entitlements reviewed so far (66.7% completion with 4 days remaining). On track for completion. |
| **Finding** | Campaign still in progress — cannot confirm final completion rate yet. |
| **Status** | **Partial** — campaign on track but not yet complete |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 10 | Entitlement owner cert | First campaign still in progress (66.7% with 4 days remaining) | R. Myers | Monitor daily, send reminders at day 12 | 2026-02-14 | In progress |

---

## Assessment Notes

1. **Intentional partial (control 10):** The entitlement owner certification is in its first cycle. Marking it partial until the cycle completes is honest assessment practice. After completion, this moves to pass with documented completion rate.

2. **SailPoint ISL certification validates this pack.** The SailPoint Identity Security Learner credential demonstrates platform knowledge beyond basic administration. The configuration designs here reflect ISL-level understanding of lifecycle events, role modeling, and policy enforcement.

3. **This pack complements Packs 01-06, not replaces them.** Entra-native governance (Packs 01-06) works for Microsoft-only environments. SailPoint is for enterprise complexity — multiple directories, on-prem systems, legacy apps, and regulatory requirements that exceed what Entra Governance can handle alone.

4. **Role model design is where most IIQ implementations fail.** Organizations dump entitlements into IIQ without designing the role hierarchy. The birthright → IT → business role structure ensures every access decision is role-based, auditable, and reviewable. This is governance design, not product configuration.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
