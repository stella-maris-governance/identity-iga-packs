# Control Mapping — SailPoint IdentityIQ Configuration

---

## NIST 800-53 Rev 5

| Control ID | Control Name | Implementation | Evidence |
|-----------|--------------|----------------|----------|
| AC-2 | Account Management | Full lifecycle across all connected systems | E-v-O #1, #2, #3, #4 |
| AC-2(3) | Disable Accounts | Leaver event auto-disables all accounts | E-v-O #4 |
| AC-2(4) | Automated Audit Actions | Every provisioning and certification event logged | E-v-O #9 |
| AC-5 | Separation of Duties | SOD policy engine with real-time blocking | E-v-O #7 |
| AC-6 | Least Privilege | Role model with birthright minimum | E-v-O #5 |
| AC-6(7) | Review of User Privileges | Quarterly manager + entitlement owner certifications | E-v-O #6, #10 |
| AU-2 | Event Logging | All identity events auditable and exportable | E-v-O #9 |
| PS-4 | Personnel Termination | Leaver: disable, remove, archive, notify | E-v-O #4 |
| PS-5 | Personnel Transfer | Mover: recalculate roles, notify managers | E-v-O #3 |

---

## SOX IT General Controls

| Requirement | Implementation | Evidence |
|------------|----------------|----------|
| Periodic access review | Quarterly certifications with auto-revoke | E-v-O #6, #10 |
| Segregation of duties | Real-time SOD enforcement with blocking | E-v-O #7 |
| Provisioning audit trail | Every action logged with identity, system, result | E-v-O #9 |

---

## CMMC Level 2

| Practice ID | Practice Name | Implementation |
|------------|---------------|----------------|
| AC.L2-3.1.1 | Authorized Access Control | Role-based access with certification |
| AC.L2-3.1.4 | Separation of Duties | SOD policies with enforcement |
| PS.L2-3.9.2 | Personnel Actions | Automated termination processing |

---

*Stella Maris Governance — 2026*
