# Control Mapping — Access Reviews Automation

---

## NIST 800-53 Rev 5

| Control ID | Control Name | Implementation | Evidence |
|-----------|--------------|----------------|----------|
| AC-2(7) | Privileged User Accounts Review | PIM quarterly review for all eligible role assignments | E-v-O #3 |
| AC-6(7) | Review of User Privileges | Quarterly reviews for groups + apps; monthly for guests | E-v-O #1, #2, #4 |
| AC-2(3) | Disable Accounts | Auto-revoke on reviewer non-response | E-v-O #5 |
| AU-6 | Audit Record Review | Justification captured on every decision; exportable | E-v-O #6, #9, #10 |
| AU-3 | Content of Audit Records | Review events: reviewer, decision, justification, timestamp | E-v-O #10 |

---

## CIS Microsoft Azure Foundations Benchmark v2.0

| CIS Control | Title | Implementation |
|-------------|-------|----------------|
| 1.1.4 | Ensure PIM access reviews | PIM eligible assignments reviewed quarterly |

---

## CMMC Level 2

| Practice ID | Practice Name | Implementation |
|------------|---------------|----------------|
| AC.L2-3.1.1 | Authorized Access Control | All access reviewed and certified by owner |
| AC.L2-3.1.7 | Privileged Functions | PIM roles validated quarterly |

---

## SOX IT General Controls

| Requirement | Implementation | Evidence |
|------------|----------------|----------|
| Periodic access review | Quarterly automated with auto-revoke | E-v-O #1-4 |
| Evidence of review decisions | Exportable CSV with reviewer, decision, justification | E-v-O #9 |
| Segregation of reviewer | Group owners review groups; app owners review apps; Security Admin reviews PIM | Review definitions |

---

## Evidence Cross-Reference

| Control | Evidence Location | Type |
|---------|-------------------|------|
| AC-2(7) | screenshots/03 | PIM review certifications |
| AC-6(7) | screenshots/01, 02 | Review dashboard + decisions |
| AC-2(3) | screenshots/06 | Auto-revoke evidence |
| AU-6 | screenshots/05 | Results export |
| Full | docs/expected-vs-observed.md | All 10 controls |

---

*Stella Maris Governance — 2026*
