# SoD Matrix — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for maintaining, detecting, and enforcing Separation of Duties across Entra ID directory roles and business application access.

**Scope:** All role assignments (active and eligible) in Entra ID, plus documented business application role conflicts.

**Out of Scope:** Application-internal permissions not managed through Entra groups or SSO.

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| PIM configured | Pack 04 deployed — eligible assignments exist for detection |
| Log Analytics workspace | For scan result export and historical trending |
| Sentinel | For scheduled weekly scan deployment |
| Conflict matrix approved | Stakeholder sign-off on prohibited role combinations |
| Exception process defined | Approval chain, compensating controls template, expiration policy |

---

## 3. Weekly Scan Procedure

The automated scan runs every Sunday at 02:00 UTC via Sentinel analytics rule.

### What the scan checks:
- All active Entra directory role assignments
- All PIM eligible role assignments
- Cross-references every user's roles against the conflict matrix
- Flags any user holding both roles in a conflict pair

### After each scan:
1. Review alert output (email + Teams notification)
2. For each violation: is it a known exception or new finding?
3. Known exceptions: verify still in exception register with valid expiry
4. New findings: open remediation item, notify user's manager

---

## 4. Handling New Violations

1. Identify which conflict pair is violated (SOD-001 through SOD-012)
2. Determine tier (Critical, High, Business Application)
3. Contact the user and their manager
4. Decision: **remediate** (remove one role) or **exception** (document and compensate)

### Remediation (preferred)
- Remove the less critical role from the user
- Assign that role to a different person
- Verify next weekly scan shows clean

### Exception (when remediation is not possible)
- User submits exception request with business justification
- Identify compensating controls (enhanced monitoring, dual approval, etc.)
- Executive approval (minimum Director level)
- Set expiry: maximum 90 days
- Add to exception register
- Schedule quarterly review

---

## 5. Business Application SoD (Tier 3)

Entra-native detection covers directory role conflicts (Tier 1 and Tier 2). Business application conflicts require additional detection methods:

| Application | Detection Method | Frequency |
|-------------|-----------------|-----------|
| ERP/Finance | Application role report export + manual cross-reference | Quarterly |
| HR System | Application role report export + manual cross-reference | Quarterly |
| ITSM | ServiceNow role audit report | Quarterly |

Until IGA platform integration (SailPoint, Saviynt) is deployed, business application SoD is a manual quarterly review using exported role reports cross-referenced against SOD-009 through SOD-012.

---

## 6. Maintaining the Conflict Matrix

### When to update:
- New Entra admin roles introduced
- New business applications onboarded
- Organizational structure changes (new business functions)
- Audit findings or risk assessment identifies new conflicts
- Regulatory changes (new SOX controls, new CMMC practices)

### Update process:
1. Propose new conflict pair with risk rating and rationale
2. Review with security and business stakeholders
3. Add to sod-conflict-matrix.json
4. Update KQL detection query if new Entra roles
5. Run immediate scan to identify existing violations
6. Document in changelog

---

## 7. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Weekly scan results | Weekly | IAM Analyst |
| Exception register review | Quarterly | IAM Lead + GRC |
| Conflict matrix review | Semi-annual | IAM Lead + Security + Business |
| Business application SoD (Tier 3) | Quarterly | IAM Lead + App Owners |
| Full SoD program assessment | Annual | GRC Lead |

---

## 8. Troubleshooting

**Scan returns no results:** Verify KQL query has correct role template IDs. Check that diagnostic settings are exporting AuditLogs and DirectoryRole data.

**False positive:** User holds roles that appear in the matrix but one is a read-only variant. Verify role template IDs match exactly. Adjust matrix if needed.

**Exception expired but not remediated:** Escalate to exception approver. Either renew with re-approval or force remediation within 14 days.

---

*Stella Maris Governance — 2026*
