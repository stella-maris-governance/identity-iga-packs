# The Law of Evidence: Expected vs. Observed

## Identity Threat Detection & Response (ITDR)

> **Assessment Date:** 2026-02-10 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab Tenant + Microsoft Sentinel [SAMPLE]
> **Assessor:** Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC
> **Pack Version:** 1.0.0
> **Status:** 8/10 controls confirmed | 2 partial | 0 failed

---

## Summary

| Status | Count | Percentage |
|--------|-------|------------|
| Pass | 8 | 80% |
| Partial | 2 | 20% |
| Fail | 0 | 0% |

---

## Assessment Detail

### 1 — Entra ID Protection Risk Policies Active

| Field | Detail |
|-------|--------|
| **Expected State** | Entra ID Protection configured with user risk policy (block high risk) and sign-in risk policy (require MFA for medium+, block high). Policies apply to all users. |
| **Observed State** | User risk policy: **enabled.** Action at High risk: block sign-in, require secure password change. Sign-in risk policy: **enabled.** Action at Medium: require MFA. Action at High: block sign-in. Scope: all users, no exclusions except break-glass (Pack 04). **47 risk detections** in 30 days: 31 low, 12 medium, 4 high. All 4 high-risk events resulted in blocked sign-in. |
| **Evidence** | Screenshot #02 |
| **NIST 800-53** | SI-4, AC-7 |
| **Status** | **Pass** |

---

### 2 — Tier 1 Auto-Response Rules Deployed and Tested

| Field | Detail |
|-------|--------|
| **Expected State** | ITDR-001, ITDR-002, ITDR-003 deployed as Sentinel analytics rules with automated playbook response. Each rule validated through controlled tabletop exercise. |
| **Observed State** | All 3 Tier 1 rules **active** in Sentinel since Jan 20. Tabletop exercise conducted Feb 7 (see control 6 for full timeline). ITDR-001 validated: test account flagged as high-risk → playbook fired → account disabled + sessions revoked in 97 seconds. ITDR-003 validated: simulated password spray (12 failed attempts from test IP) → IP blocked + accounts flagged in 3 minutes 14 seconds. ITDR-002 not directly testable in lab (requires physical geographic separation) — validated via log injection simulation. |
| **Evidence** | Screenshot #01, #04 |
| **NIST 800-53** | SI-4(5), IR-4 |
| **Status** | **Pass** |

---

### 3 — Tier 2 Alert Rules Deployed and Producing

| Field | Detail |
|-------|--------|
| **Expected State** | ITDR-004, ITDR-005, ITDR-006 deployed as Sentinel analytics rules. Alerts route to SOC/IAM Lead. 30-minute acknowledgment SLA. |
| **Observed State** | All 3 Tier 2 rules **active** since Jan 20. **ITDR-004 (privilege escalation):** 1 alert in 30 days — test direct role assignment detected in 4 minutes, acknowledged at 11 minutes, remediated (assignment removed) at 14 minutes. **ITDR-005 (dormant reactivation):** 1 alert — test account dormant 120 days, sign-in detected in 6 minutes, investigated and confirmed as authorized reactivation (rehire). **ITDR-006 (SP anomaly):** 2 alerts — both correlated with CIEM Pack 08 alerts, acknowledged within 19 minutes. All within 30-minute SLA. |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | SI-4, IR-5 |
| **Status** | **Pass** |

---

### 4 — Tier 3 Hunting Queries Deployed

| Field | Detail |
|-------|--------|
| **Expected State** | ITDR-007 through ITDR-010 saved as weekly hunting queries. Run every Monday. Results reviewed by IAM Lead. |
| **Observed State** | All 4 hunting queries saved in Sentinel. **3 weeks of execution** (Jan 20, Jan 27, Feb 3). Results by rule: ITDR-007 (stale credentials): 2 service principals with credentials > 365 days — flagged for rotation. ITDR-008 (token replay): 0 indicators across 3 weeks. ITDR-009 (consent grants): 1 suspicious consent grant detected (third-party app requesting Mail.Read + Files.ReadWrite) — investigated, consent revoked. **ITDR-010 (cross-tenant lateral movement): 0 results across 3 weeks.** |
| **Finding** | ITDR-010 returned zero results. This is expected in a lab with only 2 trusted partner tenants and limited guest activity, but it means the rule is **unvalidated against real threat data.** The query logic is sound (validated against synthetic data), but production validation requires higher guest volume. |
| **Status** | **Partial** — ITDR-010 unvalidated against real cross-tenant threat patterns |

---

### 5 — Auto-Containment Playbook Operational

| Field | Detail |
|-------|--------|
| **Expected State** | Logic App playbook deployed: on Tier 1 alert, automatically disable account, revoke all sessions, and notify SOC. Playbook executes without human intervention. |
| **Observed State** | Playbook `playbook-revoke-contain` **deployed** as Sentinel-triggered Logic App. Actions: (1) Get user details from alert entity, (2) Disable account via Graph API, (3) Revoke sessions via Graph API, (4) Send email to SOC distribution list with incident details, (5) Post to Teams SOC channel. **Tested 3 times** during tabletop: all 3 executions completed successfully. Average execution time: 94 seconds from trigger to all actions complete. |
| **Evidence** | Screenshot #04 |
| **NIST 800-53** | IR-4 |
| **Status** | **Pass** |

---

### 6 — Tabletop Exercise Completed with Measured MTTD/MTTR

| Field | Detail |
|-------|--------|
| **Expected State** | Controlled tabletop exercise simulating compromised credential. Full incident timeline documented with timestamps at every stage. MTTD < 15 minutes, MTTR < 30 minutes. |
| **Observed State** | **Tabletop executed Feb 7, 2026.** Scenario: test account "tabletop-user" flagged as compromised via Entra ID Protection risk injection. Full timeline: |
| | **09:00:00 UTC** — Risk signal injected (simulated credential compromise) |
| | **09:01:12 UTC** — Entra ID Protection flags user as High Risk |
| | **09:01:14 UTC** — Sentinel ingests risk detection event |
| | **09:01:18 UTC** — ITDR-001 analytics rule matches, incident created |
| | **09:01:22 UTC** — Playbook triggered automatically |
| | **09:01:44 UTC** — Account disabled (Graph API call completed) |
| | **09:01:47 UTC** — All sessions revoked (Graph API call completed) |
| | **09:01:52 UTC** — SOC notification email sent |
| | **09:01:55 UTC** — Teams SOC channel notification posted |
| | **09:02:37 UTC** — Playbook execution complete (all 5 actions) |
| | |
| | **MTTD: 1 minute 18 seconds** (signal → alert) |
| | **MTTR: 2 minutes 37 seconds** (signal → full containment) |
| | Both well within targets (MTTD < 15 min, MTTR < 30 min). |
| **Evidence** | Screenshot #03 |
| **NIST 800-53** | IR-4, IR-5 |
| **Status** | **Pass** |

---

### 7 — UEBA Enabled and Producing Behavioral Baselines

| Field | Detail |
|-------|--------|
| **Expected State** | Sentinel UEBA enabled. Behavioral baselines established for all active identities. Anomaly scores available for investigation enrichment. |
| **Observed State** | UEBA **enabled** since Jan 15. Identity data sources: sign-in logs, audit logs, Azure activity. **147 user baselines** established (minimum 14-day learning period complete). UEBA anomaly scores available in entity pages and incident investigation. Top anomaly in 30 days: user asmith flagged for unusual resource access pattern after department transfer — correlated with Pack 01 mover event, confirmed legitimate. |
| **Evidence** | Screenshot #05 |
| **NIST 800-53** | SI-4 |
| **Status** | **Pass** |

---

### 8 — Sentinel Fusion Detection Active

| Field | Detail |
|-------|--------|
| **Expected State** | Sentinel Fusion ML detection enabled. Fusion correlates signals across multiple data sources to detect multi-stage attacks that individual rules would miss. |
| **Observed State** | Fusion **enabled** with all identity connectors: Entra ID Protection, sign-in logs, audit logs, Office 365, Azure Activity. **1 Fusion incident** in 30 days: "Suspicious sign-in followed by anomalous mailbox activity" — test scenario during tabletop, correlated sign-in anomaly + new inbox rule. Fusion correctly chained two low-confidence signals into one high-confidence incident. |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | SI-4 |
| **Status** | **Pass** |

---

### 9 — Incident Response Metrics Tracked

| Field | Detail |
|-------|--------|
| **Expected State** | MTTD and MTTR tracked for every identity incident. Monthly metrics reported. Targets: MTTD < 15 minutes, MTTR < 30 minutes. |
| **Observed State** | **7 identity incidents** in 30 days (4 Tier 1 auto-contained, 3 Tier 2 investigated). Metrics: Tier 1 average MTTD: 1 min 42 sec. Tier 1 average MTTR: 2 min 51 sec. Tier 2 average MTTD: 5 min 12 sec. Tier 2 average MTTR: 16 min 33 sec. **All incidents within target SLAs.** Monthly report generated and archived. |
| **Evidence** | Screenshot #05 |
| **NIST 800-53** | IR-5, IR-6 |
| **Status** | **Pass** |

---

### 10 — All ITDR Events Export to Log Analytics with Full Chain

| Field | Detail |
|-------|--------|
| **Expected State** | Every detection, alert, playbook execution, and response action logged in Sentinel/Log Analytics. Incident timeline reconstructable from logs alone. 90-day retention. |
| **Observed State** | Diagnostic settings active for: SecurityAlert, SecurityIncident, SentinelAutomation (playbook runs), SigninLogs, AuditLogs. KQL confirmed: full tabletop timeline reconstructable from logs — all 10 timestamps in control 6 are present in SecurityIncident and SentinelAutomation tables. **312 ITDR-related events** in 30 days. Retention: 90 days. |
| **Evidence** | KQL output |
| **NIST 800-53** | AU-3, AU-6, IR-5 |
| **Status** | **Pass** |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 4 | Tier 3 hunting | ITDR-010 (cross-tenant lateral movement) returned 0 results across 3 weeks — unvalidated | R. Myers | Increase guest test scenarios OR validate with synthetic threat data injection | 2026-03-15 | Open |

---

## Watchstander Notes

1. **MTTD of 1:18 means the system works faster than any human could.** The automated detection-to-containment chain (Tier 1) removes the human from the critical path for high-confidence threats. The human investigates after containment, not before. This is the only way to beat an attacker who is already inside your identity plane.

2. **The honest partial on ITDR-010.** Cross-tenant lateral movement detection requires guest activity volume that a lab environment doesn't produce. The query logic is validated against synthetic data, but synthetic is not real. I will not mark a detection rule as "Pass" when its only evidence is that it didn't find anything. Absence of evidence is not evidence of absence. The rule needs production traffic to prove itself.

3. **Tier 3 hunting is where the discipline shows.** Anyone can deploy Tier 1 auto-response rules — they fire and you feel safe. Tier 3 hunting is the weekly grind: running queries that usually return nothing, tuning the ones that return noise, and occasionally finding the signal that no automated rule caught. The consent grant finding (ITDR-009) came from a Tier 3 hunt, not an automated alert. That's why hunting matters.

4. **ITDR is the capstone of the identity pillar.** Packs 01-08 build the governance structure: who has access, how it's managed, how it's reviewed, how permissions are scoped. Pack 09 answers the question those packs can't: what happens when the governance is right but the identity is compromised anyway? Detection and response is the final layer. Without it, governance is a locked door with no alarm system.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
