# Control Mapping — Separation of Duties Matrix

---

## NIST 800-53 Rev 5

| Control ID | Control Name | Implementation | Evidence |
|-----------|--------------|----------------|----------|
| AC-5 | Separation of Duties | 12-conflict matrix across 3 tiers | E-v-O #1, #2, #3, #4 |
| AC-5(1) | SoD Through Access Authorization | PIM approval checks conflict matrix | E-v-O #8 |
| AC-6(1) | Authorize Access to Security Functions | Critical roles cannot self-oversee | E-v-O #2 |
| AC-6(7) | Review of User Privileges | Weekly scan + quarterly exception review | E-v-O #5, #9 |
| AU-3 | Content of Audit Records | Scan results logged with user, roles, conflict ID | E-v-O #10 |
| AU-6 | Audit Record Review | Weekly scan review + quarterly exception review | E-v-O #10 |

---

## CMMC Level 2

| Practice ID | Practice Name | Implementation |
|------------|---------------|----------------|
| AC.L2-3.1.4 | Separation of Duties | Defined matrix with automated detection |

---

## SOX IT General Controls

| Requirement | Implementation | Evidence |
|------------|----------------|----------|
| Segregation of duties | 12-conflict matrix including finance roles | E-v-O #1, #4 |
| Compensating controls | All exceptions have documented compensating controls | E-v-O #7 |
| Periodic review | Weekly automated scan + quarterly exception review | E-v-O #5, #9 |

---

## Evidence Cross-Reference

| Control | Evidence Location | Type |
|---------|-------------------|------|
| AC-5 | screenshots/01 | Scan results |
| AC-5 | screenshots/03 | Exception register |
| AC-5(1) | Pack 04 runbook | PIM approval SoD check |
| Full | docs/expected-vs-observed.md | All 10 controls |

---

*Stella Maris Governance — 2026*
