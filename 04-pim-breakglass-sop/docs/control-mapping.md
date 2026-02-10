# Control Mapping — PIM + Break-Glass SOP

---

## NIST 800-53 Rev 5

| Control ID | Control Name | Implementation | Evidence |
|-----------|--------------|----------------|----------|
| AC-2 | Account Management | PIM manages all privileged account lifecycle | E-v-O #1, #6, #7 |
| AC-2(2) | Automated Temporary Accounts | PIM auto-expires activations (4-8 hours) | E-v-O #4 |
| AC-2(7) | Privileged User Accounts | JIT with MFA + justification | E-v-O #1, #2, #3 |
| AC-6 | Least Privilege | Zero standing admin; JIT activation | E-v-O #1 |
| AC-6(1) | Authorize Access to Security Functions | Approval required for Global Admin | E-v-O #3 |
| AC-6(5) | Privileged Accounts | Eligible limited to named individuals | E-v-O #1 |
| AC-6(7) | Review of User Privileges | Quarterly PIM access reviews | Runbook |
| AU-3 | Content of Audit Records | PIM events: user, role, justification, time | E-v-O #5, #10 |
| AU-6 | Audit Record Review | Weekly activation audit; automated alerts | E-v-O #5 |
| CP-2 | Contingency Plan | Break-glass emergency access | E-v-O #6, #7 |
| CP-4 | Contingency Plan Testing | Monthly break-glass test | E-v-O #9 |
| IA-2(1) | MFA to Privileged Accounts | MFA on every PIM activation | E-v-O #2 |
| SI-4 | System Monitoring | Break-glass alert under 90 sec; PIM alert under 5 min | E-v-O #5, #8 |

---

## CIS Microsoft Azure Foundations Benchmark v2.0

| CIS Control | Title | Implementation |
|-------------|-------|----------------|
| 1.1.4 | Ensure PIM is used for admin roles | All 5 admin roles through PIM eligible |
| 1.1.5 | Ensure break-glass accounts configured | 2 accounts, different auth, different locations, monthly tested |
| 1.1.7 | Ensure admin accounts are cloud-only | Admin accounts use .onmicrosoft.com UPN |

---

## CMMC Level 2

| Practice ID | Practice Name | Implementation |
|------------|---------------|----------------|
| AC.L2-3.1.5 | Least Privilege | JIT with time-bound access (4-8 hours) |
| AC.L2-3.1.6 | Non-Privileged Accounts | Standard accounts daily; PIM for admin |
| AC.L2-3.1.7 | Privileged Functions | PIM governs all privileged functions |
| IA.L2-3.5.3 | Multifactor Authentication | MFA on every PIM activation |

---

## Evidence Cross-Reference

| Control | Evidence Location | Type |
|---------|-------------------|------|
| AC-6 | screenshots/01-pim-roles-overview.html | Zero standing admin |
| AC-6(1) | screenshots/04-pim-approval-workflow.html | Approval for Global Admin |
| CP-2 | screenshots/06-breakglass-account-properties.html | Break-glass config |
| CP-4 | screenshots/08-breakglass-test-log.html | Monthly test evidence |
| SI-4 | screenshots/07-breakglass-alert-rule.html | Alert rule + fire |
| Full | docs/expected-vs-observed.md | All 10 controls |

---

*Stella Maris Governance — 2026*
