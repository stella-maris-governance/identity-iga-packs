# SailPoint IdentityIQ — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for SailPoint IdentityIQ identity governance platform. Covers aggregation, lifecycle events, certification campaigns, SOD enforcement, and provisioning operations.

**Scope:** All identities, entitlements, and governance workflows managed through IIQ.

**Out of Scope:** IIQ infrastructure (app server, database), connector installation, patch management.

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| SailPoint IIQ 8.x | Licensed and deployed |
| Connectors | AD, Entra, HR source, SaaS apps connected and tested |
| Authoritative source | HR system designated, correlation rules configured |
| Role model | Birthright, IT, and business roles defined |
| Owners assigned | Entitlement owners, certification reviewers, SOD policy owners |

---

## 3. Daily Operations

### Aggregation Schedule

| Source | Schedule | Type |
|--------|----------|------|
| HR system | 06:00 UTC daily | Account + identity |
| Active Directory | 07:00 UTC daily | Account + entitlement |
| Entra ID | 07:30 UTC daily | Account + entitlement |
| SaaS apps | 08:00 UTC daily | Account + entitlement |

### Daily Checks

1. Review aggregation task results — all sources show "Success"
2. Check for correlation failures (unmatched accounts)
3. Review provisioning queue — no stuck items
4. Check lifecycle event log — joiners/movers/leavers processed
5. Review SOD violation alerts

---

## 4. Lifecycle Event Management

### Joiner Not Triggering

1. Verify identity has status = Active and no linked accounts
2. Check hire date has been reached
3. Verify lifecycle event is enabled
4. Check aggregation ran successfully for HR source
5. Review system log for errors

### Mover Not Recalculating

1. Verify attribute change was detected during aggregation
2. Check identity comparison shows previous vs current values
3. Verify mover event trigger conditions match
4. Check role assignment rules reference the changed attribute

### Leaver Not Disabling

1. Verify identity status = Inactive or termination date reached
2. Check leaver event is enabled
3. Verify provisioning plan includes disable action for each target
4. Check target system connector is operational

---

## 5. Certification Campaign Operations

### Launching a Campaign

1. Navigate to Certifications > Schedule Certification
2. Select campaign type (Manager, Entitlement Owner, SOD, Privileged)
3. Verify scope and reviewer assignments
4. Set duration (14 days standard, 7 days for privileged)
5. Enable auto-revoke on non-response
6. Launch

### During Campaign

- Day 3: check completion rate, send reminders if under 30%
- Day 7: send targeted reminders to non-responders
- Day 12: escalation email to non-responder managers
- Day 14: campaign closes, auto-revoke executes

### Post-Campaign

1. Export results (CSV)
2. Review completion rate (target: 95%+)
3. Verify auto-revokes executed
4. Document any exceptions
5. Archive results for audit

---

## 6. SOD Policy Management

### When a Violation Is Detected

1. IIQ generates SOD violation alert
2. Violation appears in SOD Violation Manager
3. For Critical (blocking): access request denied automatically
4. For High (alerting): exception workflow triggered
5. SOD policy owner reviews and approves exception or requires remediation
6. All violations logged with identity, conflicting roles, timestamp, resolution

### Adding a New SOD Policy

1. Define conflict pair (left role + right role)
2. Set risk level (Critical = block, High = alert + exception, Medium = alert)
3. Configure in IIQ: Setup > Policies > SOD
4. Test with known conflict scenario
5. Run full scan to identify existing violations
6. Document in SoD Matrix (Pack 05)

---

## 7. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Aggregation health | Daily | IIQ Admin |
| Provisioning queue | Daily | IIQ Admin |
| Lifecycle event audit | Weekly | IAM Lead |
| Certification progress | Daily during campaigns | IAM Lead |
| SOD violation review | Weekly | SOD Policy Owner |
| Role model review | Semi-annual | IAM Lead + Business |
| Connector health | Monthly | IIQ Admin |
| Full IIQ configuration review | Annual | IAM Lead + Security |

---

## 8. Troubleshooting

**Aggregation fails:** Check connector credentials, network connectivity, source system availability. Review task result details for specific error.

**Provisioning stuck in queue:** Check target system connector. Verify provisioning plan syntax. Check for approval workflow waiting on response.

**Certification not appearing for reviewer:** Verify reviewer is correctly assigned. Check campaign scope includes their direct reports or entitlements.

**SOD false positive:** Review policy definitions. Verify role membership is current (may need re-aggregation). Adjust policy if roles have changed.

---

*Stella Maris Governance — 2026*
