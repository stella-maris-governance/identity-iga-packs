# Control Mapping — Conditional Access Baseline

---

## NIST 800-53 Rev 5

| Control ID | Control Name | CA Policies | Evidence |
|-----------|--------------|-------------|----------|
| IA-2 | Identification and Authentication (Org Users) | CA001, CA005, CA010 | Sign-in logs showing MFA enforcement |
| IA-2(1) | MFA to Privileged Accounts | CA005, CA010 | Admin sign-in logs with MFA/FIDO2 |
| IA-2(2) | MFA to Non-Privileged Accounts | CA001 | All-user sign-in logs with MFA |
| IA-5 | Authenticator Management | CA002, CA010 | Legacy auth blocked; phishing-resistant enforced |
| IA-8 | Identification and Auth (Non-Org Users) | CA007, CA008 | Guest ToU acceptance; blocked country enforcement |
| AC-7 | Unsuccessful Logon Attempts | CA004 | High-risk sign-in blocks |
| AC-17 | Remote Access | CA003, CA006 | Compliant device required; session timeout enforced |
| AC-17(1) | Remote Access Monitoring and Control | CA006 | Session frequency logs |

---

## CIS Microsoft Azure Foundations Benchmark v2.0

| CIS Control | Title | CA Policies | Implementation |
|-------------|-------|-------------|----------------|
| 1.1.1 | Ensure MFA is enabled for all users | CA001 | MFA required for all users |
| 1.1.3 | Ensure MFA is enabled for all privileged users | CA005, CA010 | MFA + phishing-resistant for admins |
| 1.1.6 | Block legacy authentication | CA002 | All legacy auth protocols blocked |
| 1.2.1 | Ensure trusted locations are defined | CA008 | Named locations for trusted and blocked |

---

## CMMC Level 2

| Practice ID | Practice Name | CA Policies | Implementation |
|------------|---------------|-------------|----------------|
| IA.L2-3.5.3 | Multifactor Authentication | CA001, CA005, CA010 | MFA all users; phishing-resistant admins |
| AC.L2-3.1.1 | Authorized Access Control | CA001, CA003 | Authenticated + compliant devices |
| AC.L2-3.1.3 | Control CUI Flow | CA008, CA007 | Block restricted countries; guest ToU |
| AC.L2-3.1.5 | Least Privilege | CA005, CA010 | Stronger controls for admin roles |
| AC.L2-3.1.12 | Remote Access Sessions | CA006 | Session timeout for unmanaged devices |
| AC.L2-3.1.22 | Control Public Information | CA007 | Guest access requires ToU |

---

## SOX IT General Controls

| Requirement | CA Policies | Implementation |
|------------|-------------|----------------|
| Logical access controls | CA001, CA003, CA005 | MFA + device compliance + admin controls |
| Access monitoring | All | Sign-in logs capture CA enforcement for every sign-in |
| Periodic access review | — | Exception reviews quarterly; see Access Reviews Pack |

---

## Evidence Cross-Reference

| Control | Evidence Location | Type |
|---------|-------------------|------|
| IA-2 | screenshots/01, screenshots/03 | Policy config, MFA grant |
| IA-2(1) | screenshots/05 | Phishing-resistant auth strength |
| IA-5 | screenshots/01 | Legacy auth block |
| IA-8 | screenshots/06 | Named locations |
| AC-7 | screenshots/04 | Risk-based blocking |
| AC-17 | screenshots/08 | Sign-in log with policy enforcement |
| Full | docs/expected-vs-observed.md | All controls with observed state |

---

*Stella Maris Governance — 2026*
