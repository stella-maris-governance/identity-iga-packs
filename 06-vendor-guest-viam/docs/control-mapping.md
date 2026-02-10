# Control Mapping — Vendor / Guest vIAM

---

## NIST 800-53 Rev 5

| Control ID | Control Name | Implementation | Evidence |
|-----------|--------------|----------------|----------|
| IA-8 | Identification and Auth (Non-Org Users) | MFA + ToU on every guest sign-in via CA007 | E-v-O #3, #4 |
| AC-2 | Account Management | Full guest lifecycle via entitlement management | E-v-O #1, #2, #5 |
| AC-2(2) | Automated Temporary Accounts | Access packages auto-expire (30-180 days) | E-v-O #5 |
| AC-2(3) | Disable Accounts | Auto-block 30 days post-expiry | E-v-O #9 |
| AC-6(7) | Review of User Privileges | Monthly sponsor review | E-v-O #7 |
| PS-7 | External Personnel Security | Sponsor accountability, scoped access, review | E-v-O #6 |
| AU-3 | Content of Audit Records | All guest events to Log Analytics | E-v-O #10 |

---

## CIS Microsoft Azure Foundations Benchmark v2.0

| CIS Control | Title | Implementation |
|-------------|-------|----------------|
| 1.1.6 | Restrict guest invite permissions | Members + specific roles only |

---

## CMMC Level 2

| Practice ID | Practice Name | Implementation |
|------------|---------------|----------------|
| AC.L2-3.1.22 | Control Public Information | Guest access scoped, monitored, expired |
| AC.L2-3.1.3 | Control CUI Flow | Guests cannot access CUI without explicit package |

---

## Evidence Cross-Reference

| Control | Evidence Location | Type |
|---------|-------------------|------|
| IA-8 | Pack 03 screenshots | CA007 enforcement |
| AC-2 | screenshots/01, 02 | Access packages + approvals |
| PS-7 | screenshots/04 | Sponsor tracking |
| Full | docs/expected-vs-observed.md | All 10 controls |

---

*Stella Maris Governance — 2026*
