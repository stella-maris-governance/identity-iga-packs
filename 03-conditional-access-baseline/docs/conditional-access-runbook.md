# Conditional Access Baseline — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

This runbook defines operational procedures for deploying, maintaining, and governing the Conditional Access policy baseline in Microsoft Entra ID.

**Scope:** All user and admin sign-ins to Entra ID-integrated applications.

**Out of Scope:** Application-level authorization, network-level controls, endpoint protection policies.

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|-------------|---------|-------|
| Entra ID License | P1 (P2 for CA004 risk-based) | P2 required for sign-in risk detection |
| Intune | Required for CA003, CA009 | Device compliance policies deployed first |
| Named Locations | Required | At least 1 trusted network, 1 blocked country set |
| Break-Glass Accounts | 2 accounts | Must exist and be excluded BEFORE enabling policies |
| Terms of Use | Required for CA007 | Document published in Entra |
| Log Analytics | Recommended | Required for sign-in log export and KQL monitoring |
| FIDO2 Keys | Required for CA010 | All admin accounts must have FIDO2 registered |

---

## 3. Policy Naming Convention

**Format:** `CA{###}-{Target}-{Control}-{Platform}`

| Component | Description | Examples |
|-----------|-------------|---------|
| CA### | Sequential policy number | CA001, CA002 |
| Target | Who is affected | AllUsers, Admins, Guests |
| Control | What is enforced | RequireMFA, BlockLegacyAuth |
| Platform | Platform scope | AllPlatforms, Mobile, Unmanaged |

Rules: Sequential numbering. Do not reuse numbers. If deprecated, rename with DEPRECATED- prefix and disable. Do not delete.

---

## 4. Deployment Procedure

### Phase 1: Pre-Deployment (Day 0)

1. Verify prerequisites — license, Intune, named locations, break-glass, ToU, FIDO2
2. Create exclusion groups: grp-ca-breakglass-exclude, grp-ca-exception-{policyID}
3. Configure named locations (import named-locations.json or configure manually)
4. Notify stakeholders

### Phase 2: Report-Only Deployment (Day 1)

1. Import policies using deploy-conditional-access.ps1 with -Mode ReportOnly
2. Verify all 10 policies in portal with Report-only status
3. Confirm break-glass exclusions on every policy
4. Screenshot policy list

### Phase 3: Monitor and Validate (Day 1-14)

1. Daily review of CA Insights workbook
2. Identify false positives
3. Adjust scope or add documented exclusions if needed
4. Weekly summary to leadership

### Phase 4: Sequential Enablement (Day 15-21)

Enable one per day in this order (lowest disruption first):

| Day | Policy | Risk Level |
|-----|--------|-----------|
| 15 | CA002 Block Legacy Auth | Low |
| 16 | CA008 Block Countries | Low |
| 17 | CA001 Require MFA All Users | Medium |
| 18 | CA005 Require MFA Admins | Low |
| 19 | CA003 Require Compliant Device | Medium |
| 20 | CA006 Session Timeout | Low |
| 21 | CA007 Guest ToU / CA009 App Protection | Low |
| 22 | CA004 Block High Risk / CA010 Phishing-Resistant | Low |

**Rollback:** Switch policy to Report-Only (do NOT delete). Investigate. Re-enable after fix.

### Phase 5: Post-Deployment (Day 22+)

1. Capture all screenshots per CAPTURE-GUIDE.md
2. Complete Expected vs Observed assessment
3. Archive Report-Only data
4. Schedule recurring reviews

---

## 5. Exception Management

All exceptions require documented approval, maximum 90-day expiration (no permanent exceptions except break-glass), and quarterly review.

### Exception Tracker Template

| Exception ID | Policy | User/Group | Justification | Approved By | Expiry | Status |
|---|---|---|---|---|---|---|
| EXC-CA001-001 | CA001 | svc-integration-01 | Service principal cannot MFA — managed identity migration | R. Myers | 2026-04-01 | Active |

---

## 6. Evidence Collection

| Evidence | Source | Frequency |
|----------|--------|-----------|
| Sign-in logs with CA enforcement | Entra Sign-in Logs via Log Analytics | Continuous |
| CA Insights workbook | Entra Conditional Access | Weekly review |
| Policy change audit trail | Entra Audit Logs | Continuous |
| Policy configuration screenshots | Portal | Monthly or on change |
| Expected vs Observed update | Manual | Quarterly |

### KQL: Sign-ins blocked by CA (last 30 days)
```kql
SigninLogs
| where TimeGenerated > ago(30d)
| where ConditionalAccessStatus == "failure"
| extend CAPolicies = parse_json(ConditionalAccessPolicies)
| mv-expand CAPolicies
| where CAPolicies.result == "failure"
| summarize BlockCount = count() by PolicyName = tostring(CAPolicies.displayName)
| sort by BlockCount desc
```

---

## 7. Troubleshooting

**User Locked Out:** Check sign-in logs, identify blocking policy, determine if correct or misconfiguration, add temp exception if needed.

**Legacy App Blocked:** Confirm legacy auth, check for modern auth alternative, migrate or create scoped 90-day exception with migration plan.

**MFA Prompt Loop:** Check registered MFA methods, clear per-user MFA settings if CA-based MFA is standard.

**Risk-Based False Positive:** Review in Entra Security > Risky sign-ins, dismiss if legitimate, do NOT disable the policy.

---

## 8. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| CA Insights workbook | Weekly | IAM Analyst |
| Exception review | Monthly | IAM Lead |
| Full policy baseline review | Quarterly | IAM Lead + Security |
| Framework alignment | Semi-annual | GRC Lead |
| Break-glass test (related) | Monthly | IAM Lead |

---

*Stella Maris Governance — 2026*
