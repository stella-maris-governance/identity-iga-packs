# PIM Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for Microsoft Entra Privileged Identity Management. Covers role configuration, activation workflows, monitoring, and review cadences.

**Scope:** All Entra ID directory roles managed through PIM.

**Out of Scope:** Azure resource roles, break-glass emergency access (see breakglass-sop.md).

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Entra ID P2 | PIM requires P2 for all users with eligible assignments |
| Break-glass accounts | Must be created and tested BEFORE converting active admins |
| CA Baseline deployed | Break-glass exclusions verified in all CA policies |
| Log Analytics workspace | For PIM event export and alerting |
| Designated approvers | Security Administrator(s) identified for Global Admin approval |

---

## 3. Converting Active to Eligible

**Critical:** ALWAYS verify break-glass accounts work before converting.

1. Verify bg-admin-01 can sign in and access Entra admin center
2. Verify bg-admin-02 can sign in and access Entra admin center
3. For each admin with active Global Admin: Entra ID > Identity Governance > PIM > Entra roles > Assignments > Update > Change Active to Eligible
4. Set eligible duration: 1 year (triggers annual review)
5. Verify user no longer in Active assignments
6. Have user test PIM activation immediately

---

## 4. Role Settings Configuration

Path: Entra ID > Identity Governance > PIM > Entra roles > Settings

| Setting | Global Admin | Security Admin | Exchange Admin | SharePoint Admin | Intune Admin |
|---------|-------------|----------------|----------------|------------------|--------------|
| Max activation | 8 hours | 8 hours | 8 hours | 8 hours | 4 hours |
| Require MFA | Yes | Yes | Yes | Yes | Yes |
| Require justification | Yes | Yes | Yes | Yes | Yes |
| Require approval | Yes | No | No | No | No |
| Approvers | Security Admin | — | — | — | — |
| Permanent eligible | No | No | No | No | No |
| Max eligible duration | 1 year | 1 year | 1 year | 1 year | 1 year |

---

## 5. Activation Procedure (for PIM Users)

1. Navigate to myaccess.microsoft.com > PIM > My roles
2. Find role > click Activate
3. Set duration (up to maximum)
4. Enter justification — be specific (reference ticket number, change request, or incident)
5. Complete MFA
6. If Global Admin: wait for approval
7. Role activates immediately after approval (or immediately for non-approval roles)
8. Auto-expires at configured duration

**Good justification:** "Updating Exchange retention policies per CHG-2026-0042"

**Bad justification:** "Need admin access"

---

## 6. Approval Workflow (for Approvers)

1. Receive notification (email or myaccess.microsoft.com)
2. Review: who, which role, justification, duration
3. Approve or deny with your own justification
4. User notified immediately

---

## 7. Monitoring

KQL analytics rule runs every 5 minutes against AuditLogs. Alerts on every activation with user, role, justification, timestamp.

### Daily Review

- Check Sentinel for PIM activation alerts
- Verify all activations have legitimate justifications
- Confirm no activations outside business hours
- Check for failed activation attempts

---

## 8. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Activation audit | Weekly | IAM Analyst |
| Eligible assignment review | Quarterly | IAM Lead |
| Role settings review | Semi-annual | IAM Lead + Security |
| PIM access review (automated) | Quarterly | Role owners |
| Break-glass test | Monthly | IAM Lead |

---

## 9. Troubleshooting

**User cannot activate — "not eligible":** Check eligible assignment exists and not expired. Check P2 license.

**Activation stuck in pending approval:** Check approver received notification. If unavailable, second approver or break-glass.

**MFA not appearing:** Check registered MFA methods. If MFA infrastructure fully down, this is a break-glass scenario.

---

*Stella Maris Governance — 2026*
