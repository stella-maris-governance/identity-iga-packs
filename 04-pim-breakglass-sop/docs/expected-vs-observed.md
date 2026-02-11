# The Law of Evidence: Expected vs. Observed

## PIM + Break-Glass SOP

> **Assessment Date:** 2026-02-10 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab Tenant [SAMPLE — replace with your tenant name]
> **Assessor:** Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC
> **Pack Version:** 1.0.0
> **Status:** 10/10 controls confirmed | 0 partial | 0 failed

---

## Summary

| Status | Count | Percentage |
|--------|-------|------------|
| Pass | 10 | 100% |
| Partial | 0 | 0% |
| Fail | 0 | 0% |

> **Note:** 100% pass is expected here. PIM and break-glass are binary controls — either configured correctly or not. Unlike CA007 (Guest ToU) where temporal gaps are normal, a partial here is a genuine finding requiring immediate remediation.

---

## Assessment Detail

### 1 — Zero Standing Admin

| Field | Detail |
|-------|--------|
| **Expected State** | 0 permanent active Global Admin for human users. Only break-glass accounts hold active Global Admin. All other admins have eligible-only assignments. |
| **Observed State** | **0 active Global Admin** for human accounts. 2 eligible Global Admin assignments (rmyers-admin, jsmith-admin). 2 active Global Admin belong exclusively to break-glass accounts — by design. |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | AC-6, AC-6(5) |
| **CIS Azure** | 1.1.4 |
| **Status** | **Pass** |

---

### 2 — PIM Activation Requires MFA + Justification

| Field | Detail |
|-------|--------|
| **Expected State** | All PIM-managed roles require MFA verification AND written justification before activation completes. |
| **Observed State** | All 5 managed roles confirmed: MFA = Required, Justification = Required. Tested: attempted activation without justification — rejected. Last 5 activations all show MFA completion + justification captured. |
| **Evidence** | Screenshot #02, #03 |
| **NIST 800-53** | AC-2(7), IA-2(1) |
| **Status** | **Pass** |

---

### 3 — Global Admin Activation Requires Approval

| Field | Detail |
|-------|--------|
| **Expected State** | Global Admin activation requires approval from Security Administrator. Other admin roles require MFA + justification only. |
| **Observed State** | Global Admin: Approval required = Yes, Approver = Security Administrator. Tested: submitted activation at 14:22 UTC, approval granted at 14:34 UTC (12 min). 3 approvals completed in 30 days, average response: 12 minutes. Security Admin role confirmed: approval NOT required. |
| **Evidence** | Screenshot #02, #04 |
| **NIST 800-53** | AC-6(1) |
| **Status** | **Pass** |

---

### 4 — Maximum Activation Duration Enforced

| Field | Detail |
|-------|--------|
| **Expected State** | Global Admin, Security Admin, Exchange Admin, SharePoint Admin: 8 hours max. Intune Admin: 4 hours max. No extensions — must re-activate. |
| **Observed State** | All 5 roles confirmed at configured maximums. Tested: activated Security Admin at 09:00, auto-expired at 17:00 (8 hours). Audit log shows expiration event with timestamp. |
| **Evidence** | Screenshot #02, #05 |
| **NIST 800-53** | AC-6 |
| **CMMC** | AC.L2-3.1.5 |
| **Status** | **Pass** |

---

### 5 — PIM Activation Alert Fires on Every Activation

| Field | Detail |
|-------|--------|
| **Expected State** | Every PIM activation generates alert in Sentinel within 5 minutes. Alert includes user, role, justification, time, duration. |
| **Observed State** | KQL rule deployed, runs every 5 minutes. 5 alert instances in 30 days — all match legitimate activations. Average alert delivery: 3.2 minutes. Alert payload confirmed: UPN, role, justification, timestamp, duration. |
| **Evidence** | Screenshot #05, KQL output |
| **NIST 800-53** | AU-3, AU-6 |
| **Status** | **Pass** |

---

### 6 — Break-Glass Account 1 Exists and Configured

| Field | Detail |
|-------|--------|
| **Expected State** | bg-admin-01 exists with permanent active Global Admin, password-only auth (no MFA), excluded from ALL CA policies, no M365 license. |
| **Observed State** | Account confirmed: Global Admin (permanent active), password-only (no phone, no app, no FIDO2), member of grp-ca-breakglass-exclude, CA check shows Not Applied for all 10 policies, no M365 license. Password in sealed envelope at Location A. |
| **Evidence** | Screenshot #06 |
| **NIST 800-53** | CP-2 |
| **Status** | **Pass** |

---

### 7 — Break-Glass Account 2 with Different Auth Method

| Field | Detail |
|-------|--------|
| **Expected State** | bg-admin-02 exists with permanent active Global Admin, FIDO2 as sole auth method, excluded from ALL CA policies, stored at DIFFERENT physical location from bg-admin-01. |
| **Observed State** | Account confirmed: Global Admin (permanent active), FIDO2 key registered (YubiKey 5 NFC), no password sign-in, member of grp-ca-breakglass-exclude, CA Not Applied for all 10 policies, no M365 license. FIDO2 key in fire safe at Location B (different building). |
| **Evidence** | Screenshot #06 |
| **NIST 800-53** | CP-2 |
| **Status** | **Pass** |

---

### 8 — Break-Glass Alert Fires Within 90 Seconds

| Field | Detail |
|-------|--------|
| **Expected State** | ANY sign-in from bg-admin-01 or bg-admin-02 triggers alert within 90 seconds. Fires regardless of sign-in result. |
| **Observed State** | NRT analytics rule deployed (runs every 1 minute). Test 2026-02-01: signed into bg-admin-01 at 10:00:00 UTC, alert fired at 10:01:23 UTC (83 seconds). Teams notification delivered at 10:01:31 UTC. |
| **Evidence** | Screenshot #07 |
| **NIST 800-53** | SI-4, AU-6 |
| **Status** | **Pass** |

---

### 9 — Monthly Break-Glass Test Completed

| Field | Detail |
|-------|--------|
| **Expected State** | 1st of every month: sign in with break-glass account, verify admin access, verify alert fires, re-seal credentials, document results. |
| **Observed State** | February 2026 test completed 2026-02-01: bg-admin-01 signed in, Global Admin confirmed, alert fired 83 sec, credentials re-sealed (witnessed), access log updated. January 2026 test also documented (bg-admin-02, FIDO2 key). |
| **Evidence** | Screenshot #08, breakglass-test-log.md |
| **NIST 800-53** | CP-4 |
| **Status** | **Pass** |

---

### 10 — PIM Audit Log Exports to Log Analytics

| Field | Detail |
|-------|--------|
| **Expected State** | All PIM events export to Log Analytics via Entra diagnostic settings. Minimum 90-day retention. |
| **Observed State** | Diagnostic setting active since 2026-01-15, category: AuditLogs. KQL returns 23 PIM events in 30 days: 5 activations, 5 deactivations, 3 approvals, 2 assignments, 8 notifications. Retention: 90 days. |
| **Evidence** | Screenshot #05, KQL output |
| **NIST 800-53** | AU-3, AU-6 |
| **Status** | **Pass** |

---

## Remediation Tracker

| # | Control | Finding | Status |
|---|---------|---------|--------|
| — | — | No findings | Clean |

---

## Assessment Notes

1. **100% pass is expected for this pack.** PIM and break-glass are binary — configured correctly or not. A partial here means urgent remediation.

2. **Break-glass test cadence is the most commonly missed control.** Organizations deploy break-glass and never test. The monthly test is the discipline that proves it works. Untested break-glass is the same as no break-glass.

3. **Two auth methods, two locations is minimum.** If both credentials are in the same safe, a single physical event eliminates both emergency paths.

4. **83-second alert time matters.** If someone uses break-glass, you need to know in minutes not hours. The NRT rule with 1-minute interval makes this achievable and verifiable.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
