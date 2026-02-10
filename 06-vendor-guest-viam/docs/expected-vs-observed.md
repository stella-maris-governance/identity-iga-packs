# Expected vs Observed — Vendor / Guest vIAM

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

### 1 — Guest Invitation Restricted to Authorized Users

| Field | Detail |
|-------|--------|
| **Expected State** | Only members and specific admin roles can invite guests. Open invitation is disabled. All guests should be invited through entitlement management access packages. |
| **Observed State** | External collaboration settings: Guest invite restrictions = "Member users and users assigned to specific admin roles can invite guest users." External identity providers: Microsoft accounts and email OTP enabled. Unmanaged invitation (anyone in org can invite) = **disabled.** Verified: standard user attempted direct invite — blocked with "You do not have permission to invite external users." |
| **Evidence** | Screenshot #03 |
| **NIST 800-53** | AC-2 |
| **CIS Azure** | 1.1.6 |
| **Status** | **Pass** |

---

### 2 — Access Packages Deployed with Approval Workflow

| Field | Detail |
|-------|--------|
| **Expected State** | Entitlement management access packages exist for each guest access type. Each package requires at least one approver and business justification. |
| **Observed State** | **4 access packages** deployed in External Access catalog: Guest-Project-Collaboration (90 days, sponsor + resource owner approval), Guest-Vendor-Support (90 days, IT manager approval), Guest-Audit-ReadOnly (30 days, GRC lead approval), Guest-Executive-Sponsor (180 days, executive approval). All require justification. **8 assignments** processed in 30 days — all went through approval workflow. |
| **Evidence** | Screenshot #01, #02 |
| **NIST 800-53** | AC-2, PS-7 |
| **Status** | **Pass** |

---

### 3 — Guests Must Accept Terms of Use

| Field | Detail |
|-------|--------|
| **Expected State** | CA007 (from Pack 03) enforces Terms of Use acceptance on every guest sign-in. No guest can access resources without accepting current ToU. |
| **Observed State** | CA007-Guests-RequireToU-AllPlatforms = **enabled.** Scope: all GuestsOrExternalUsers. Grant: MFA AND Terms of Use. Verified: 12 guest sign-ins in 30 days — all show ToU acceptance in sign-in log conditional access tab. 1 guest who did not accept ToU was blocked (sign-in log shows "Failure: Terms of use not accepted"). |
| **Evidence** | Pack 03 Screenshot #01, sign-in logs |
| **NIST 800-53** | IA-8 |
| **Status** | **Pass** |

---

### 4 — Guests Must Complete MFA on Every Sign-In

| Field | Detail |
|-------|--------|
| **Expected State** | CA007 requires MFA for all guest sign-ins. No exceptions. For trusted partner tenants, MFA trust allows honoring home tenant MFA. |
| **Observed State** | CA007 grant control includes MFA. Cross-tenant access settings: 2 trusted partner tenants configured with "Trust multifactor authentication from Microsoft Entra tenants" enabled. Verified: guest from trusted partner — MFA satisfied via home tenant claim. Guest from non-trusted domain — prompted for MFA at our tenant. **12 guest sign-ins, 12 MFA completions.** |
| **Evidence** | Screenshot #03, sign-in logs |
| **NIST 800-53** | IA-8 |
| **CMMC** | AC.L2-3.1.22 |
| **Status** | **Pass** |

---

### 5 — Access Packages Expire Automatically

| Field | Detail |
|-------|--------|
| **Expected State** | All access package assignments have a maximum duration. When the assignment expires, the guest is removed from all package-granted groups and apps. No permanent guest access. |
| **Observed State** | Assignment policies confirmed: Project = 90 days, Vendor = 90 days, Audit = 30 days, Executive = 180 days. **2 expirations** in 30 days: guest-contractor-a (Vendor package) expired Feb 5 — removed from grp-guest-vendor-support and ServiceNow access at 00:01 UTC. guest-auditor-b (Audit package) expired Feb 8 — removed from grp-guest-audit-readonly and SharePoint. Both removals logged in entitlement management audit. |
| **Evidence** | Screenshot #05 |
| **NIST 800-53** | AC-2(2), AC-2(3) |
| **Status** | **Pass** |

---

### 6 — Sponsor Identified for Every Guest

| Field | Detail |
|-------|--------|
| **Expected State** | Every guest account has an identifiable sponsor (the user who requested the access package). Sponsor is responsible for monthly review and renewal decisions. |
| **Observed State** | Entitlement management tracks requestor as the sponsor for each assignment. **12 active guests**, all with identified sponsors. Spot check: guest-partner-x@external.com — sponsor = jsmith@stellamarisgov.onmicrosoft.com (requested via Guest-Project-Collaboration package Jan 15). Sponsor field populated for all 12 guests. |
| **Evidence** | Screenshot #04 |
| **NIST 800-53** | PS-7 |
| **Finding** | 1 legacy guest (pre-entitlement-management) had no sponsor — manually assigned sponsor on Feb 3. |
| **Status** | **Partial** — all guests now have sponsors, but 1 required manual remediation |

---

### 7 — Monthly Guest Access Review Active

| Field | Detail |
|-------|--------|
| **Expected State** | AR-GUEST-Monthly (from Pack 02) reviews all guest accounts every 30 days. Sponsor reviews and certifies each guest. Non-response auto-revokes in 7 days. |
| **Observed State** | AR-GUEST-Monthly **active** since Jan 2026. 2 cycles completed. Cycle 1: 12 guests reviewed, 10 approved, 2 denied (removed). Cycle 2: 11 guests reviewed, 10 approved, 1 auto-revoked (sponsor non-response). Monthly cadence confirmed. |
| **Evidence** | Pack 02 E-v-O #4, Pack 02 Screenshot #04 |
| **NIST 800-53** | AC-6(7) |
| **Status** | **Pass** |

---

### 8 — Cross-Tenant Access Settings Configured

| Field | Detail |
|-------|--------|
| **Expected State** | Default inbound access blocked. Only trusted organization tenants can collaborate. B2B direct connect disabled. Guest invite restrictions enforced. |
| **Observed State** | Default inbound: **blocked.** Trusted organizations: 2 partner tenants configured (Contoso, Fabrikam — sample). B2B collaboration: enabled for trusted orgs only. B2B direct connect: **disabled.** MFA trust: enabled for both trusted partners. Device compliance trust: disabled (guests use unmanaged devices). |
| **Evidence** | Screenshot #03 |
| **NIST 800-53** | IA-8, AC-2 |
| **Status** | **Pass** |

---

### 9 — Expired Guests Blocked After Grace Period

| Field | Detail |
|-------|--------|
| **Expected State** | Guests whose access packages have all expired are blocked (sign-in disabled) after a 30-day grace period. Deleted after 180 days of inactivity. |
| **Observed State** | KQL expiration scan executed 2026-02-10. **1 guest** in grace period: guest-contractor-a expired Feb 5 (5 days ago, within 30-day grace). Account still enabled but no active access package assignments (groups removed). No sign-in attempts since Feb 5. Will be blocked automatically on Mar 7 (30 days post-expiry) via scheduled automation. |
| **Evidence** | KQL output |
| **NIST 800-53** | AC-2(3) |
| **Status** | **Pass** |

---

### 10 — All Guest Lifecycle Events Export to Log Analytics

| Field | Detail |
|-------|--------|
| **Expected State** | All entitlement management events (requests, approvals, assignments, expirations, removals), guest sign-in events, and access review decisions export to Log Analytics. 90-day retention. |
| **Observed State** | Diagnostic settings active for AuditLogs (entitlement management category), SignInLogs (guest sign-ins). KQL returns **62 guest-related events** in 30 days: 8 access package requests, 8 approvals, 8 assignments, 2 expirations, 24 sign-ins, 12 access review decisions. Retention: 90 days. |
| **Evidence** | KQL output |
| **NIST 800-53** | AU-3, AU-6 |
| **Status** | **Pass** |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 6 | Sponsor tracking | 1 legacy guest had no sponsor (pre-entitlement-management) | R. Myers | Manually assigned sponsor Feb 3. Run scan for any remaining legacy guests without sponsors. | 2026-02-15 | Complete |

---

## Assessment Notes

1. **Intentional partial (control 6):** The legacy guest without a sponsor is a real finding in any tenant that existed before entitlement management was configured. The remediation — manually assigning a sponsor and scanning for others — is exactly the right response. New guests created through access packages always have a sponsor by design.

2. **Cross-tenant MFA trust is a critical usability decision.** Without it, guests from partner tenants must register a second MFA method in your tenant. With trust enabled, their home MFA satisfies your CA policy. This reduces friction without reducing security — but only for explicitly trusted partners.

3. **The 30-day grace period before blocking is deliberate.** Access package expiration removes group memberships (no access). The grace period allows sponsors to renew if they forgot. Blocking after 30 days is the safety net. Deletion at 180 days is cleanup.

4. **Guest governance is where the military credential management experience maps directly.** Every external credential has a sponsor, an expiration, and a purpose. The accountability chain is identical whether it's a guest CAC or a guest Entra account.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
