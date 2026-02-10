# Control Mapping — Zero-Touch JML Lifecycle

---

## NIST 800-53 Rev 5

| Control ID | Control Name | Implementation | Evidence |
|-----------|--------------|----------------|----------|
| AC-2 | Account Management | Full lifecycle: create, modify, disable, remove — all automated | E-v-O #1, #2, #7 |
| AC-2(2) | Automated Temporary Accounts | Auto-disable on employeeLeaveDateTime | E-v-O #5 |
| AC-2(3) | Disable Accounts | Leaver workflow disables within 1 hour | E-v-O #5, #6 |
| AC-2(4) | Automated Audit Actions | All events export to Log Analytics | E-v-O #10 |
| PS-4 | Personnel Termination | Leaver: disable, revoke, remove licenses, notify | E-v-O #5, #6, #7, #8 |
| PS-5 | Personnel Transfer | Mover: dynamic regroup, access review, notify | E-v-O #4 |
| AU-3 | Content of Audit Records | Lifecycle logs: user, event, timestamp, result | E-v-O #10 |

---

## CIS Microsoft Azure Foundations Benchmark v2.0

| CIS Control | Title | Implementation |
|-------------|-------|----------------|
| 1.1.2 | Ensure unused accounts are disabled | Leaver auto-disables; monthly orphan scan | E-v-O #5, #9 |

---

## CMMC Level 2

| Practice ID | Practice Name | Implementation |
|------------|---------------|----------------|
| AC.L2-3.1.1 | Authorized Access Control | Access granted only by HR attribute match via dynamic groups |
| PS.L2-3.9.2 | Personnel Actions | Automated termination within 1 hour of HR trigger |

---

## Evidence Cross-Reference

| Control | Evidence Location | Type |
|---------|-------------------|------|
| AC-2 | screenshots/01, 02, 03 | Workflow list + execution history |
| AC-2(3) | screenshots/03 | Leaver execution with disable timestamp |
| PS-5 | screenshots/05 | Dynamic group membership change log |
| Full | docs/expected-vs-observed.md | All 10 controls |

---

*Stella Maris Governance — 2026*
