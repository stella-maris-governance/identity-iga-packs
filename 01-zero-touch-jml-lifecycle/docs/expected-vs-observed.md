# Expected vs Observed — Zero-Touch JML Lifecycle

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

### 1 — Joiner Workflow Fires on Start Date

| Field | Detail |
|-------|--------|
| **Expected State** | Lifecycle workflow triggers automatically when employeeHireDate equals current date. Account enabled, dynamic groups populated, welcome email sent — all before 8 AM on start date. |
| **Observed State** | Workflow **active** since 2026-01-20. Trigger: employeeHireDate. **6 joiner executions** in 30 days — all completed successfully. Average execution time: **4 minutes 12 seconds** from trigger to all tasks complete. Last execution: 2026-02-03, user jdoe@stellamarisgov.onmicrosoft.com onboarded at 06:47 UTC (before 8 AM local). |
| **Evidence** | Screenshot #01, #02 |
| **NIST 800-53** | AC-2 |
| **Status** | **Pass** |

---

### 2 — Account Enabled with Correct Attributes

| Field | Detail |
|-------|--------|
| **Expected State** | New user account created with attributes flowing from HR source: displayName, department, jobTitle, manager, employeeId, officeLocation. Account enabled on start date. |
| **Observed State** | Provisioning log confirms attribute flow for all 6 joiners. Spot check on jdoe: displayName = "Jane Doe", department = "Engineering", jobTitle = "Cloud Security Engineer", manager = rmyers, employeeId = "EMP-2026-0047". All attributes match HR source record. Account enabled at 06:47 UTC on hire date. |
| **Evidence** | Screenshot #06 |
| **NIST 800-53** | AC-2 |
| **Status** | **Pass** |

---

### 3 — Dynamic Groups Populate Within 30 Minutes

| Field | Detail |
|-------|--------|
| **Expected State** | When user attributes are set (department, jobTitle), dynamic security groups evaluate and add user within 30 minutes. User receives group-based license and app access automatically. |
| **Observed State** | Dynamic group processing log shows membership evaluation for jdoe: added to grp-dept-engineering at 06:52 UTC (5 minutes after account enabled), added to grp-license-e5 at 06:54 UTC, added to grp-app-jira at 06:55 UTC. **All groups populated within 8 minutes.** 30-minute SLA met for all 6 joiners. |
| **Evidence** | Screenshot #04, #05 |
| **NIST 800-53** | AC-2 |
| **CMMC** | AC.L2-3.1.1 |
| **Status** | **Pass** |

---

### 4 — Mover Triggers Dynamic Group Recalculation

| Field | Detail |
|-------|--------|
| **Expected State** | When HR changes department or jobTitle, dynamic groups recalculate — user removed from old groups, added to new groups. Old app access revoked, new app access granted. No manual intervention. |
| **Observed State** | Test mover 2026-02-05: user asmith moved from Sales to Engineering. Department attribute updated at 14:00 UTC. Dynamic group log: removed from grp-dept-sales at 14:06, removed from grp-app-salesforce at 14:07, added to grp-dept-engineering at 14:08, added to grp-app-jira at 14:09. **Total transition: 9 minutes.** Manager notification delivered at 14:10. |
| **Evidence** | Screenshot #05 |
| **NIST 800-53** | PS-5 |
| **Status** | **Pass** |

---

### 5 — Leaver Workflow Disables Account Within 1 Hour

| Field | Detail |
|-------|--------|
| **Expected State** | Leaver workflow triggers when employeeLeaveDateTime equals current date. Account disabled, all sessions revoked, within 1 hour of trigger. |
| **Observed State** | Workflow **active** since 2026-01-20. **3 leaver executions** in 30 days. All completed within SLA. Last execution: 2026-02-07, user bwilson terminated — workflow triggered at 17:00 UTC, account disabled at 17:03, sessions revoked at 17:04. **Total: 4 minutes.** |
| **Evidence** | Screenshot #01, #03 |
| **NIST 800-53** | AC-2(3), PS-4 |
| **CMMC** | PS.L2-3.9.2 |
| **Status** | **Pass** |

---

### 6 — Leaver Sessions Revoked Immediately

| Field | Detail |
|-------|--------|
| **Expected State** | On leaver execution, all active sessions and refresh tokens revoked. User cannot access any resources even if browser was open. |
| **Observed State** | Leaver workflow includes "Revoke all refresh tokens" task. Execution log for bwilson: revokeSignInSessions completed at 17:04 UTC (1 minute after disable). Verified: attempted sign-in at 17:10 UTC returned "AADSTS50057: User account is disabled." No successful sign-ins after revocation. |
| **Evidence** | Screenshot #03, sign-in logs |
| **NIST 800-53** | AC-2(3), PS-4 |
| **Status** | **Pass** |

---

### 7 — Leaver Licenses and Groups Removed

| Field | Detail |
|-------|--------|
| **Expected State** | Leaver workflow removes all license assignments and group memberships. No orphaned license consumption. |
| **Observed State** | For bwilson: 1 license removed (E5), removed from 4 dynamic groups (grp-dept-sales, grp-license-e5, grp-app-salesforce, grp-all-employees). Dynamic group removal automatic (accountEnabled = false triggers removal from grp-all-employees). License reclaimed within 10 minutes. |
| **Evidence** | Screenshot #03 |
| **NIST 800-53** | AC-2 |
| **Status** | **Pass** |

---

### 8 — Pre-Departure Notification Fires 7 Days Before

| Field | Detail |
|-------|--------|
| **Expected State** | Pre-notify workflow triggers 7 days before employeeLeaveDateTime. Manager receives email with departure date, knowledge transfer reminder, and data export instructions. |
| **Observed State** | Workflow active. **2 pre-notifications sent** in 30 days. For bwilson (leave date Feb 7): pre-notify fired Jan 31 at 08:00 UTC (7 days prior). Manager rmyers received email with departure date, checklist, data export link. Email delivery confirmed in workflow execution log. |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | PS-4 |
| **Status** | **Pass** |

---

### 9 — Zero Orphaned Accounts

| Field | Detail |
|-------|--------|
| **Expected State** | No accounts exist where employeeLeaveDateTime has passed but the account is still enabled. Monthly orphan scan confirms zero drift. |
| **Observed State** | KQL orphan scan executed 2026-02-10. **1 account flagged:** svc-legacy-sync (service account, no employeeLeaveDateTime set). This is a service account, not a human identity — excluded from JML scope by design. **0 human orphaned accounts found.** |
| **Evidence** | KQL output |
| **NIST 800-53** | AC-2 |
| **CIS Azure** | 1.1.2 |
| **Finding** | svc-legacy-sync flagged by scan but is a service account. Recommend adding exclusion filter for service accounts in KQL query. |
| **Status** | **Partial** — scan needs refinement, no actual orphan |

---

### 10 — All Lifecycle Events Export to Log Analytics

| Field | Detail |
|-------|--------|
| **Expected State** | All lifecycle workflow executions, dynamic group changes, and provisioning events export to Log Analytics. Minimum 90-day retention. |
| **Observed State** | Diagnostic settings active for: AuditLogs (lifecycle workflows), ProvisioningLogs (HR sync), SignInLogs (session data). KQL query returns **47 lifecycle-related events** in 30 days: 6 joiner, 1 mover, 3 leaver, 2 pre-notify, 35 dynamic group membership changes. Retention: 90 days. |
| **Evidence** | KQL output |
| **NIST 800-53** | AC-2(4), AU-3 |
| **Status** | **Pass** |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 9 | Orphan scan | Service account flagged as false positive | R. Myers | Add userType/accountType filter to KQL query | 2026-02-17 | In progress |

---

## Assessment Notes

1. **Intentional partial (control 9):** The orphan scan correctly identified an account without a leave date — but it was a service account, not a human identity. The scan works; it just needs a filter refinement. This demonstrates real assessment discipline: flag it, track it, fix it.

2. **4-minute average lifecycle execution** is well within the 1-hour SLA. Entra Lifecycle Workflows process faster than most organizations expect.

3. **Dynamic group processing averaged 8 minutes** — well within 30-minute SLA. Processing time depends on tenant size and group complexity.

4. **Pre-departure notification is the most overlooked lifecycle control.** Most organizations automate disable/revoke but forget the 7-day heads-up. That notification prevents last-minute scrambles and ensures knowledge transfer.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
