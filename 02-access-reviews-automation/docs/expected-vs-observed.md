# Expected vs Observed — Access Reviews Automation

> **Assessment Date:** 2026-02-10 [SAMPLE — replace with your assessment date]
> **Environment:** Stella Maris Lab Tenant [SAMPLE — replace with your tenant name]
> **Assessor:** Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC
> **Pack Version:** 1.0.0
> **Status:** 9/10 controls confirmed | 1 partial | 0 failed

---

## Summary

| Status | Count | Percentage |
|--------|-------|------------|
| Pass | 9 | 90% |
| Partial | 1 | 10% |
| Fail | 0 | 0% |

---

## Assessment Detail

### 1 — Group Membership Review Active and Recurring

| Field | Detail |
|-------|--------|
| **Expected State** | Access review AR-GRP-Quarterly is active, targets all grp-dept and grp-app security groups, assigned to group owners, recurs every 90 days with 14-day review window. |
| **Observed State** | Review **active** since 2026-01-15. Scope: 9 dynamic security groups (5 department, 4 application). Reviewer: group owners. Recurrence: every 90 days. Duration: 14 days. First cycle completed 2026-01-29. **87 memberships reviewed**, 84 approved, 3 denied (access removed). |
| **Evidence** | Screenshot #01, #02 |
| **NIST 800-53** | AC-6(7) |
| **Status** | **Pass** |

---

### 2 — Application Assignment Review Active and Recurring

| Field | Detail |
|-------|--------|
| **Expected State** | Access review AR-APP-Quarterly is active, targets enterprise app assignments (Salesforce, Jira, ServiceNow), assigned to app owners, recurs every 90 days. |
| **Observed State** | Review **active** since 2026-01-15. Scope: 3 enterprise apps. Reviewer: app owners. Recurrence: every 90 days. Duration: 14 days. First cycle completed 2026-01-29. **34 assignments reviewed**, 31 approved, 2 denied, 1 auto-revoked (non-response). |
| **Evidence** | Screenshot #01 |
| **NIST 800-53** | AC-6(7) |
| **CMMC** | AC.L2-3.1.1 |
| **Status** | **Pass** |

---

### 3 — PIM Eligible Role Review Active and Recurring

| Field | Detail |
|-------|--------|
| **Expected State** | Access review AR-PIM-Quarterly is active, targets all PIM eligible role assignments, assigned to Security Administrator, recurs every 90 days. |
| **Observed State** | Review **active** since 2026-01-15. Scope: all eligible assignments across 5 PIM-managed roles. Reviewer: Security Administrator. First cycle completed 2026-01-28. **4 eligible assignments reviewed**, all 4 approved with justification documented. |
| **Evidence** | Screenshot #01, #03 |
| **NIST 800-53** | AC-2(7) |
| **CIS Azure** | 1.1.4 |
| **Status** | **Pass** |

---

### 4 — Guest Access Review Active with Monthly Cadence

| Field | Detail |
|-------|--------|
| **Expected State** | Access review AR-GUEST-Monthly is active, targets all guest/external users, assigned to sponsor or inviter, recurs every 30 days with 7-day review window. |
| **Observed State** | Review **active** since 2026-01-15. Scope: all users with userType = Guest. Reviewer: inviting user (sponsor). Recurrence: every 30 days. Duration: 7 days. **2 cycles completed.** Cycle 1: 12 guests reviewed, 10 approved, 2 denied. Cycle 2: 11 guests reviewed (1 removed from prior cycle), 10 approved, 1 auto-revoked. |
| **Evidence** | Screenshot #01, #04 |
| **NIST 800-53** | AC-6(7), IA-8 |
| **Status** | **Pass** |

---

### 5 — Auto-Revoke Fires on Non-Response

| Field | Detail |
|-------|--------|
| **Expected State** | When a reviewer does not respond within the review window (14 days for groups/apps/PIM, 7 days for guests), access is automatically revoked. |
| **Observed State** | **2 auto-revokes** across all reviews in 30 days. App review: 1 reviewer did not respond for svc-reporting app assignment — access removed on day 15. Guest review: 1 sponsor did not respond for guest contractor-x@partner.com — guest disabled on day 8. Both revocations logged in audit trail with reason "Auto-revoked: reviewer non-response." |
| **Evidence** | Screenshot #06 |
| **NIST 800-53** | AC-2(3) |
| **Status** | **Pass** |

---

### 6 — Reviewer Decisions Include Justification

| Field | Detail |
|-------|--------|
| **Expected State** | All reviewer decisions (approve, deny, don't know) include a written justification. Justification is captured in the review results and available for audit. |
| **Observed State** | Review settings: justification = **required** for all 4 reviews. Spot check on AR-GRP-Quarterly: 84 approve decisions, all include justification text (e.g., "User is active member of Engineering team, confirmed with manager", "Role required for ongoing project Alpha"). 3 deny decisions include justification (e.g., "User transferred to Finance, no longer needs Engineering group access"). |
| **Evidence** | Screenshot #02 |
| **NIST 800-53** | AU-6 |
| **Status** | **Pass** |

---

### 7 — System Recommendations Enabled

| Field | Detail |
|-------|--------|
| **Expected State** | Machine learning recommendations enabled on all reviews. System flags users who have not signed in during review period or who have low activity, recommending deny. Reviewers can accept or override. |
| **Observed State** | Recommendations **enabled** on all 4 reviews. AR-GRP-Quarterly: system recommended deny for 5 users with no sign-in in 60+ days. Reviewer accepted 3 deny recommendations, overrode 2 with justification ("User on parental leave, returning March"). Recommendation accuracy: useful for identifying stale access. |
| **Evidence** | Screenshot #02 |
| **Status** | **Pass** |

---

### 8 — Review Completion Rate Above 95%

| Field | Detail |
|-------|--------|
| **Expected State** | All reviews achieve 95%+ reviewer completion rate. Non-responses should be rare and trigger auto-revoke, not persist as unreviewed access. |
| **Observed State** | AR-GRP-Quarterly: **97.7%** completion (85 of 87 decisions made, 2 auto-revoked). AR-APP-Quarterly: **97.1%** (33 of 34, 1 auto-revoked). AR-PIM-Quarterly: **100%** (4 of 4). AR-GUEST-Monthly Cycle 2: **90.9%** (10 of 11, 1 auto-revoked). |
| **Finding** | AR-GUEST-Monthly Cycle 2 at 90.9% — below 95% target. One sponsor (jpartner@external.com) did not review their guest. Guest was auto-revoked correctly, but sponsor non-response rate needs monitoring. |
| **Status** | **Partial** — auto-revoke worked correctly, but completion rate below target |

---

### 9 — Review Results Exportable for Audit

| Field | Detail |
|-------|--------|
| **Expected State** | Review results exportable as CSV or available via API. Export includes reviewer, decision, justification, timestamp, and resource reviewed. |
| **Observed State** | All 4 reviews support CSV export. Downloaded AR-GRP-Quarterly results: 87 rows, columns include reviewedBy, decision, justification, reviewedDateTime, resourceDisplayName, resourceId. Data suitable for external audit package. Also available via Graph API: GET /identityGovernance/accessReviews/definitions/{id}/instances/{id}/decisions. |
| **Evidence** | Screenshot #05 |
| **NIST 800-53** | AU-6 |
| **SOX** | Periodic access review evidence |
| **Status** | **Pass** |

---

### 10 — All Review Events Export to Log Analytics

| Field | Detail |
|-------|--------|
| **Expected State** | All access review events (creation, decisions, revocations, completions) export to Log Analytics. Minimum 90-day retention. |
| **Observed State** | Diagnostic settings active for AuditLogs category. KQL query returns **138 access review events** in 30 days: 4 review creations, 121 decisions, 3 revocations, 4 completions, 6 reminder notifications. Retention: 90 days. |
| **Evidence** | KQL output |
| **NIST 800-53** | AU-3, AU-6 |
| **Status** | **Pass** |

---

## Remediation Tracker

| # | Control | Finding | Owner | Remediation | Target Date | Status |
|---|---------|---------|-------|-------------|-------------|--------|
| 8 | Review completion | Guest review Cycle 2 at 90.9% (below 95% target) | R. Myers | Contact sponsor jpartner@external.com, add reminder escalation, consider backup reviewer | 2026-02-20 | In progress |

---

## Assessment Notes

1. **Intentional partial (control 8):** Guest review had one sponsor non-response. The auto-revoke worked correctly — the guest's access was removed. The finding is about reviewer engagement, not access control failure. This demonstrates real operational monitoring.

2. **Non-response = deny is the critical design choice.** Without auto-revoke, a rubber-stamp reviewer who ignores the email means stale access persists indefinitely. Auto-revoke makes reviewer inaction a security control, not a gap.

3. **System recommendations are a force multiplier.** Reviewers managing 50+ decisions benefit from ML-flagged stale accounts. The 2 overrides with justification ("on parental leave") show reviewers engaging thoughtfully, not rubber-stamping.

4. **Monthly guest reviews are intentionally more aggressive** than quarterly employee reviews. Guests represent higher risk, change more frequently, and have weaker organizational accountability.

---

*Assessment conducted by Robert Myers, MBA | SailPoint ISL, Security+, CCSK, CC*
*Stella Maris Governance — 2026*
