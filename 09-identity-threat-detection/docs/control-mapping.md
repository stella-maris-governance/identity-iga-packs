# Control Mapping — Identity Threat Detection & Response

---

## NIST 800-53 Rev 5

| Control ID | Control Name | Implementation | Evidence |
|-----------|--------------|----------------|----------|
| SI-4 | System Monitoring | Continuous identity signal monitoring via Sentinel + UEBA | E-v-O #1, #7, #8 |
| SI-4(5) | System-Generated Alerts | Automated alerts on identity anomalies (3 tiers) | E-v-O #2, #3 |
| IR-4 | Incident Handling | Tiered response: auto-contain, investigate, escalate | E-v-O #5, #6 |
| IR-5 | Incident Monitoring | MTTD/MTTR tracking, monthly metrics | E-v-O #9 |
| IR-6 | Incident Reporting | SOC notification chain with timestamps | E-v-O #6 |
| AC-7 | Unsuccessful Logon Attempts | Password spray detection + IP blocking | E-v-O #1, #2 |
| AU-3 | Content of Audit Records | Full incident timeline in logs | E-v-O #10 |
| AU-6 | Audit Record Review | Weekly hunting + daily incident review | E-v-O #4 |

---

## CIS Microsoft Azure Foundations Benchmark v2.0

| CIS Control | Title | Implementation |
|-------------|-------|----------------|
| 1.1.3 | Ensure risky sign-in policies | Entra ID Protection: block high, MFA medium |

---

## CMMC Level 2

| Practice ID | Practice Name | Implementation |
|------------|---------------|----------------|
| IR.L2-3.6.1 | Incident Handling | Documented response with SLAs and playbooks |
| SI.L2-3.14.6 | Monitor Communications | Identity signal monitoring via Sentinel |

---

*Stella Maris Governance — 2026*
