# Access Reviews — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for Entra ID Access Reviews across group memberships, application assignments, PIM eligible roles, and guest access.

**Scope:** All access review schedules and their lifecycle (create, monitor, remediate, report).

**Out of Scope:** Manual one-time reviews, app-level entitlement reviews outside Entra.

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Entra ID P2 | Access Reviews require P2 |
| Group owners assigned | Every grp-dept and grp-app group must have an owner |
| App owners assigned | Every enterprise app must have an owner |
| PIM configured | PIM eligible assignments must exist (see Pack 04) |
| Guest sponsors | Every guest should have an identifiable inviter/sponsor |

---

## 3. Review Schedule

| Review | Start | Recurrence | Duration | Auto-Revoke After |
|--------|-------|------------|----------|-------------------|
| AR-GRP-Quarterly | Jan 15, Apr 15, Jul 15, Oct 15 | 90 days | 14 days | Day 15 |
| AR-APP-Quarterly | Jan 15, Apr 15, Jul 15, Oct 15 | 90 days | 14 days | Day 15 |
| AR-PIM-Quarterly | Jan 15, Apr 15, Jul 15, Oct 15 | 90 days | 14 days | Day 15 |
| AR-GUEST-Monthly | 1st of each month | 30 days | 7 days | Day 8 |

---

## 4. Reviewer Responsibilities

Reviewers receive an email when a review cycle starts. They must:

1. Click the link in the email (goes to myaccess.microsoft.com)
2. For each access item, choose: Approve, Deny, or Don't know
3. Provide written justification for every decision
4. Complete all decisions within the review window
5. If they don't respond, access is auto-revoked

### Guidance for Reviewers

**Approve when:** User actively needs the access for their current role. Verify with recent sign-in activity (system recommendation helps).

**Deny when:** User no longer needs access (transferred, role changed, project ended). User has not signed in during review period and has no documented reason.

**Don't know:** Use sparingly. Escalates to backup reviewer or auto-revokes if no backup.

---

## 5. Monitoring Active Reviews

### During Review Window

Check daily:
- How many decisions are pending vs completed
- Which reviewers have not yet responded
- Send manual reminders at day 7 and day 12 (for 14-day reviews)

Path: Entra ID > Identity Governance > Access Reviews > [review name] > Results

### After Review Window Closes

1. Check completion rate (target: 95%+)
2. Verify auto-revokes executed for non-responses
3. Review any deny decisions for follow-up
4. Export results for audit archive

---

## 6. Handling Denials and Revocations

When access is denied or auto-revoked:

1. User loses access immediately (group removal, app unassignment, PIM removal, or guest disable)
2. User is NOT notified automatically (configure notification if needed)
3. If denial was an error: reviewer or admin can manually re-add access with documented justification
4. All revocations logged in audit trail

### Re-granting Access After Denial

1. User submits new access request (or manager requests on behalf)
2. Request goes through standard approval workflow
3. New assignment is subject to next review cycle
4. Document why the re-grant was necessary

---

## 7. Escalation Procedures

**Reviewer not responding (day 10 of 14):**
1. Send direct email reminder with deadline
2. CC reviewer's manager
3. If still no response by day 14: auto-revoke executes

**Disputed denial:**
1. User contacts their manager
2. Manager reviews with access review owner
3. If re-grant justified: manual re-add with documented approval
4. Include in next review cycle

**System error (review not starting):**
1. Check review schedule in Entra portal
2. Verify review is enabled and start date is correct
3. Check Entra service health
4. If needed, manually trigger review instance

---

## 8. Reporting

### Quarterly Report to Leadership

Include:
- Total access items reviewed across all domains
- Completion rates per review
- Number of denials and auto-revokes
- Trend: is stale access decreasing over time?
- Any escalations or disputes

### Audit Package

For each completed review cycle, archive:
- Exported CSV of all decisions
- Completion rate summary
- Auto-revoke log
- Any exception documentation

---

## 9. Review Cadence (Meta)

| Review | Frequency | Owner |
|--------|-----------|-------|
| Monitor active review progress | Daily during window | IAM Analyst |
| Post-cycle completion analysis | After each cycle | IAM Lead |
| Review configuration check | Semi-annual | IAM Lead + Security |
| Reviewer training refresh | Annual | IAM Lead |

---

## 10. Troubleshooting

**Review not starting on schedule:** Check recurrence settings. Verify start date has not passed without the review being enabled.

**Reviewer says they have no items:** Check scope — group may be empty or user may not be assigned as owner.

**Auto-revoke did not fire:** Check review settings — "If reviewers don't respond" must be set to "Remove access." If set to "No change," auto-revoke is disabled.

**Guest review shows no guests:** Check scope filter — must target userType eq Guest. Verify guests exist in tenant.

---

*Stella Maris Governance — 2026*
