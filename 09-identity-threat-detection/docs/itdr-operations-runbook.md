# ITDR Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for identity threat detection and response using Microsoft Sentinel, Entra ID Protection, and automated playbooks.

**Scope:** All identity-based threats: credential compromise, privilege escalation, lateral movement, dormant account abuse, service principal compromise.

**Out of Scope:** Network-layer threats, endpoint detection (EDR), application-layer attacks without identity component.

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Sentinel workspace | Connected to Entra sign-in + audit logs |
| Entra ID Protection P2 | Risk policies enabled |
| UEBA enabled | Minimum 14-day baseline |
| Logic App playbook | Deployed with Graph API permissions (User.ReadWrite.All, Directory.ReadWrite.All) |
| PIM configured | Pack 04 — for privilege escalation detection baseline |

---

## 3. Standing Watch: Daily Operations

### 0800 UTC — Morning Watch

1. Open Sentinel > Incidents. Filter: last 24 hours, identity-related.
2. Any unacknowledged Tier 1 incidents? If yes — escalate immediately. Auto-containment should have fired. Verify playbook executed.
3. Any unacknowledged Tier 2 incidents? If yes — investigate now. 30-minute SLA may already be breached.
4. Check Entra ID Protection > Risky users. Any new high-risk users?
5. Check Entra ID Protection > Risky sign-ins. Any new high-risk sign-ins?

### Throughout Watch

- Tier 1 alerts: verify auto-containment executed. Investigate root cause.
- Tier 2 alerts: acknowledge, investigate, contain or close with justification.
- All incidents: document timeline with timestamps.

> **Watchstander Note:** An incident without timestamps is a story, not evidence. Every action you take gets a timestamp. First signal. Alert. Acknowledgment. Investigation start. Containment. Resolution. No exceptions.

---

## 4. Tier 1 Response: Auto-Containment

When the playbook fires automatically:

1. Verify containment actions completed:
   - Account disabled? Check user properties.
   - Sessions revoked? Check sign-in logs for post-revoke activity.
   - SOC notified? Check email + Teams channel.
2. Investigate root cause:
   - How was the credential compromised? Phishing? Brute force? Token theft?
   - What did the attacker do before containment? Check sign-in + audit logs.
   - Was any data accessed? Check resource access logs.
3. Determine blast radius:
   - Did the compromised identity have access to sensitive resources?
   - Were any role assignments or group memberships modified?
   - Were any other identities contacted or impersonated?
4. Remediate:
   - Reset credentials (password + MFA methods)
   - Review and clean any attacker-created persistence (mail rules, OAuth consents, new app registrations)
   - Re-enable account only after credential reset and manager confirmation
5. Document:
   - Full incident timeline with all timestamps
   - Root cause
   - Blast radius assessment
   - Remediation actions

---

## 5. Tier 2 Response: Investigate and Contain

When a Tier 2 alert fires:

1. Acknowledge within 30 minutes
2. Open Sentinel incident > investigate
3. Use entity timeline to map activity
4. Correlate with UEBA anomaly score
5. Determine: is this malicious, suspicious, or benign?

### If malicious:
- Escalate to Tier 1 response (section 4)
- Trigger playbook manually if not auto-triggered

### If suspicious:
- Contact user or user's manager
- Check for correlating signals (other alerts, risk detections)
- If confirmed benign: close with justification
- If unresolved: flag for daily review, increase monitoring

### If benign:
- Close with justification
- If recurring false positive: tune detection rule
- Document tuning decision

---

## 6. Tier 3 Response: Weekly Hunting

Every Monday at 0900 UTC:

1. Run ITDR-007 (stale credentials) — action: flag for credential rotation
2. Run ITDR-008 (token replay) — action: investigate any indicators
3. Run ITDR-009 (consent grants) — action: review and revoke suspicious consents
4. Run ITDR-010 (cross-tenant lateral movement) — action: investigate anomalous guest behavior
5. Document results (even if zero findings)
6. Tune queries based on false positive patterns

> **Watchstander Note:** A hunting query that returns zero results is not wasted time. It is proof of absence — for this week. Next week the answer may be different. The discipline is the cadence, not the result.

---

## 7. Playbook Maintenance

### Monthly

1. Verify Logic App is enabled and not throttled
2. Test with a controlled trigger (flag test account as high risk)
3. Verify all 5 actions complete: disable, revoke, email, Teams, log
4. Check Graph API permissions are still valid (app registration secret expiry)

### Quarterly

1. Review playbook logic: are the actions still appropriate?
2. Review SOC distribution list: are the right people receiving notifications?
3. Review containment scope: should playbook also block IP or revoke OAuth tokens?

---

## 8. Incident Metrics

Track for every identity incident:

| Timestamp | What Happened |
|-----------|---------------|
| T0 | First malicious signal (sign-in, risk detection, activity) |
| T1 | Alert/incident created |
| T2 | Alert acknowledged by human |
| T3 | Containment action completed |
| T4 | Investigation complete |
| T5 | Remediation complete |
| T6 | Incident closed |

**MTTD** = T1 - T0
**MTTR** = T3 - T0

Report monthly:
- Total identity incidents
- MTTD average (Tier 1 and Tier 2 separately)
- MTTR average (Tier 1 and Tier 2 separately)
- False positive rate
- Tier 3 hunting findings

---

## 9. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Incident review | Daily | SOC / IAM Lead |
| Tier 3 hunting | Weekly | IAM Lead |
| Playbook test | Monthly | IAM Lead |
| Detection rule tuning | Monthly | IAM Lead + Security |
| MTTD/MTTR report | Monthly | IAM Lead |
| Full ITDR program review | Quarterly | IAM Lead + CISO |
| Tabletop exercise | Semi-annual | IAM Lead + SOC |

---

## 10. Troubleshooting

**Playbook not firing:** Check Logic App is enabled. Check Sentinel automation rule links to correct playbook. Check managed identity permissions.

**UEBA not producing scores:** Verify 14-day baseline period has passed. Check data sources are connected. UEBA requires sign-in + audit logs minimum.

**False positive flood:** Tune the specific rule. Adjust thresholds. Add exclusion for known-good patterns (document every exclusion). Never disable a rule without replacing it.

**Tier 2 SLA breach:** Review notification channel. If email is being missed, add Teams and mobile push. Consider pager rotation for critical environments.

---

*Stella Maris Governance — 2026*
