# Expected vs Observed — Conditional Access Baseline

> **Assessment Date:** 2026-02-10 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab Tenant [SAMPLE — replace with your tenant name]
> **Assessor:** Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC
> **Pack Version:** 1.0.0
> **Status:** 9/10 controls confirmed | 1 control partial | 0 controls failed

---

## Summary

| Status | Count | Percentage | Detail |
|--------|-------|------------|--------|
| Pass | 9 | 90% | Control implemented as expected, evidence confirmed |
| Partial | 1 | 10% | Control implemented, minor gap documented with remediation plan |
| Fail | 0 | 0% | — |

---

## Assessment Detail

### 1 — CA001 Require MFA for All Users

| Field | Detail |
|-------|--------|
| **Expected State** | Policy enabled, all users in scope, break-glass accounts (bg-admin-01, bg-admin-02) excluded. MFA enforced on every interactive sign-in. |
| **Observed State** | Policy **enabled** since 2026-01-20. **147 users** in scope. **2 break-glass accounts excluded** via named exclusion group grp-ca-breakglass-exclude. **12,403 sign-ins** enforced MFA in the last 30 days. Zero bypass events outside of break-glass accounts. |
| **Evidence** | Screenshot #01, #02, #03 |
| **NIST 800-53** | IA-2, IA-2(2) |
| **CIS Azure** | 1.1.1 |
| **Status** | **Pass** |

---

### 2 — CA002 Block Legacy Authentication

| Field | Detail |
|-------|--------|
| **Expected State** | Policy enabled, all users, condition = client apps: Exchange ActiveSync, other clients. All legacy authentication protocols blocked (IMAP, POP3, SMTP AUTH, legacy Office). |
| **Observed State** | Policy **enabled** since 2026-01-20. **847 legacy authentication attempts blocked** in 30 days. Breakdown: IMAP (312), POP3 (201), SMTP AUTH (189), Authenticated SMTP (98), Other legacy clients (47). No successful legacy auth sign-ins. |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | IA-5 |
| **CIS Azure** | 1.1.6 |
| **Status** | **Pass** |

---

### 3 — CA003 Require Compliant Device for Corporate Apps

| Field | Detail |
|-------|--------|
| **Expected State** | Policy enabled, all users targeting corporate applications (Exchange Online, SharePoint Online, Teams). Grant control: require device marked compliant OR hybrid Azure AD joined. |
| **Observed State** | Policy **enabled** since 2026-01-25. **89 compliant devices** enrolled in Intune. **12 hybrid Azure AD joined** devices. **3 non-compliant access attempts blocked** in 30 days. |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | AC-17 |
| **Status** | **Pass** |

---

### 4 — CA004 Block High-Risk Sign-ins

| Field | Detail |
|-------|--------|
| **Expected State** | Policy enabled, all users, condition = sign-in risk level: High. Action: block access. Requires Entra ID P2 for risk detection. |
| **Observed State** | Policy **enabled** since 2026-01-25. Entra ID Protection risk detection **active**. **4 high-risk sign-ins blocked** in 30 days: 2 from anonymous proxy (Tor), 1 from malware-linked IP, 1 atypical travel flagged as high risk. All blocks successful. |
| **Evidence** | Screenshot #01, #04 |
| **NIST 800-53** | AC-7 |
| **Status** | **Pass** |

---

### 5 — CA005 Require MFA for Admin Roles

| Field | Detail |
|-------|--------|
| **Expected State** | Policy enabled, targeting directory roles: Global Administrator, Security Administrator, Exchange Administrator, SharePoint Administrator. Grant: require MFA on every sign-in. |
| **Observed State** | Policy **enabled** since 2026-01-20. **6 admin accounts** in scope across 4 roles. MFA enforced on **every** admin sign-in — 78 admin sign-ins in 30 days, 78 MFA completions (100%). |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | IA-2, IA-2(1) |
| **CIS Azure** | 1.1.3 |
| **CMMC** | IA.L2-3.5.3 |
| **Status** | **Pass** |

---

### 6 — CA006 Session Timeout on Unmanaged Devices

| Field | Detail |
|-------|--------|
| **Expected State** | Policy enabled, all users, condition = device filter: unmanaged. Session control: sign-in frequency = 4 hours, persistent browser session = disabled. |
| **Observed State** | Policy **enabled** since 2026-01-28. Sign-in frequency set to **4 hours**. Persistent browser **disabled** for unmanaged devices. 23 re-authentication prompts triggered in 30 days. |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | AC-17 |
| **CMMC** | AC.L2-3.1.12 |
| **Status** | **Pass** |

---

### 7 — CA007 Require Terms of Use for Guests

| Field | Detail |
|-------|--------|
| **Expected State** | Policy enabled, all guest and external users. Grant: require acceptance of Terms of Use document. |
| **Observed State** | Policy **enabled** since 2026-02-01. Terms of Use document **v2.1** linked. **8 of 12 guest users** have accepted. **4 guests pending** — all invited within last 5 days, have not yet signed in. |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | IA-8 |
| **CMMC** | AC.L2-3.1.22 |
| **Finding** | 4 guests pending acceptance. Not a control failure — guests are within the 14-day acceptance window per Vendor/Guest vIAM SOP. Will be auto-denied if not accepted by 2026-02-15. |
| **Status** | **Partial** — monitoring, within SLA |

---

### 8 — CA008 Block Access from Restricted Countries

| Field | Detail |
|-------|--------|
| **Expected State** | Policy enabled, all users, condition = named location Blocked Countries containing: Russia (RU), China (CN), North Korea (KP), Iran (IR). Action: block access. |
| **Observed State** | Policy **enabled** since 2026-01-20. Named location configured with **4 countries** (RU, CN, KP, IR). **23 blocked access attempts** in 30 days: Russia (12), China (8), Iran (3), North Korea (0). |
| **Evidence** | Screenshot #01, #06 |
| **NIST 800-53** | IA-8 |
| **Status** | **Pass** |

---

### 9 — CA009 App Protection Policy on Mobile

| Field | Detail |
|-------|--------|
| **Expected State** | Policy enabled, all users, condition = device platforms: iOS, Android. Grant: require app protection policy (Intune MAM). |
| **Observed State** | Policy **enabled** since 2026-02-01. Intune MAM policies linked for Outlook, Teams, OneDrive, SharePoint. **31 managed app sessions** on mobile in 30 days. 2 unprotected app attempts blocked. |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | AC-17 |
| **Status** | **Pass** |

---

### 10 — CA010 Phishing-Resistant MFA for Admin Roles

| Field | Detail |
|-------|--------|
| **Expected State** | Policy enabled, targeting admin directory roles. Grant: authentication strength = Phishing-resistant MFA. Requires FIDO2 security key or Windows Hello for Business. |
| **Observed State** | Policy **enabled** since 2026-02-03. Authentication strength **Phishing-resistant MFA** selected. **6 admin accounts** in scope. All 6 have registered FIDO2 security keys. 34 admin sign-ins in last 7 days — all completed with FIDO2. Zero fallback to standard MFA. |
| **Evidence** | Screenshot #01, #05 |
| **NIST 800-53** | IA-2(1), IA-5 |
| **CIS Azure** | 1.1.3 |
| **CMMC** | IA.L2-3.5.3 |
| **Status** | **Pass** |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 7 | CA007 Guest ToU | 4 guests pending ToU acceptance | R. Myers | Monitor; auto-deny at 14-day SLA | 2026-02-15 | Monitoring |

---

## Assessment Notes

1. **Intentional partial finding (CA007):** A 100% pass rate on first assessment is unusual and a potential red flag. This reflects a real observation — newly invited guests within their acceptance window. The control is working as designed; the gap is temporal, not structural.

2. **Break-glass exclusions verified:** Both break-glass accounts confirmed excluded from all 10 policies via grp-ca-breakglass-exclude. See PIM + Break-Glass SOP Pack.

3. **Report-Only period completed:** All policies ran in Report-Only mode for 14 days before enablement. CA Insights workbook data available in Screenshot #07.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
