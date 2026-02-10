# JML Lifecycle — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for Joiner/Mover/Leaver lifecycle automation using Entra ID Lifecycle Workflows and dynamic security groups.

**Scope:** All employee identity lifecycle events from hire to termination.

**Out of Scope:** Guest/vendor lifecycle (see Vendor/Guest vIAM Pack), service accounts, break-glass accounts.

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Entra ID Governance license | Lifecycle Workflows require Governance add-on or P2 |
| HR source configured | API-driven provisioning or CSV import to Entra |
| Required HR attributes | employeeHireDate, employeeLeaveDateTime, department, jobTitle, manager |
| Dynamic groups | Entra ID P1+ for dynamic membership rules |
| Log Analytics workspace | For lifecycle event export and orphan scanning |
| Mail-enabled account | For sending welcome and notification emails |

---

## 3. HR Attribute Requirements

These attributes MUST flow from HR to Entra for lifecycle automation to work:

| Attribute | Type | Used By | Example |
|-----------|------|---------|---------|
| employeeHireDate | DateTime | Joiner trigger | 2026-03-01T00:00:00Z |
| employeeLeaveDateTime | DateTime | Leaver trigger | 2026-06-15T00:00:00Z |
| department | String | Dynamic groups | Engineering |
| jobTitle | String | Dynamic groups | Cloud Security Engineer |
| manager | Reference | Notifications | rmyers ObjectID |
| employeeId | String | Correlation | EMP-2026-0047 |
| officeLocation | String | Named location mapping | Dallas, TX |

If any attribute is missing from HR, the corresponding automation breaks. Validate attribute flow BEFORE enabling workflows.

---

## 4. Dynamic Group Management

### Creating a New Department Group

1. Entra ID > Groups > New group
2. Type: Security, Membership: Dynamic User
3. Rule: user.department -eq "NewDepartment"
4. Name: grp-dept-newdepartment
5. Wait for initial processing (up to 24 hours for first population)
6. Verify membership matches expected users

### Dynamic Group Processing

- Initial creation: up to 24 hours
- Subsequent changes: typically 5-15 minutes
- Maximum documented: 30 minutes for large tenants
- If stuck: Entra ID > Groups > [group] > Processing status

### Adding App Access via Group

1. Assign enterprise app to the dynamic group
2. When users match the group rule, they get app access automatically
3. When users no longer match, access is removed automatically

---

## 5. Lifecycle Workflow Operations

### Joiner Workflow Tasks (in order)

1. Enable user account
2. Generate Temporary Access Pass (TAP)
3. Send welcome email to user (include TAP, first-day instructions)
4. Send notification to manager (new hire starting, confirm access)
5. Create onboarding ticket in IT service management

### Leaver Workflow Tasks (in order)

1. Send pre-departure reminder to manager (7 days before — separate workflow)
2. On leave date: disable user account
3. Revoke all sign-in sessions
4. Remove user from all groups (dynamic removal via accountEnabled = false)
5. Remove all license assignments
6. Send notification to manager (departure confirmed, data export available)
7. Send notification to IT (account disabled, archive in 90 days)

### Mover Handling

Entra Lifecycle Workflows do not have a native mover trigger. Movers are handled by:

1. HR updates department/jobTitle in source system
2. Attributes sync to Entra (provisioning interval)
3. Dynamic groups recalculate automatically
4. Old group memberships removed, new ones added
5. Optional: scheduled workflow checks for recent attribute changes and triggers access review

---

## 6. Testing Procedures

### Test a Joiner

1. Create test user with employeeHireDate = tomorrow
2. Set department, jobTitle, manager
3. Wait for hire date to arrive
4. Verify: account enabled, groups populated, welcome email sent
5. Check workflow execution history for success

### Test a Leaver

1. Set employeeLeaveDateTime = tomorrow on a test user
2. Wait for leave date to arrive
3. Verify: account disabled, sessions revoked, licenses removed, groups empty
4. Check workflow execution history for success
5. Attempt sign-in — should fail with AADSTS50057

### Test a Mover

1. Change department attribute on test user
2. Wait up to 30 minutes for dynamic group recalculation
3. Verify: removed from old department group, added to new
4. Verify: old app access removed, new app access granted

---

## 7. Orphan Account Scanning

Run monthly to catch any accounts that slipped through automation:
```kql
let threshold = ago(30d);
AuditLogs
| where TimeGenerated > threshold
| where Category == "UserManagement"
| join kind=leftouter (
    SigninLogs
    | where TimeGenerated > threshold
    | summarize LastSignIn = max(TimeGenerated) by UserPrincipalName
) on $left.TargetResources[0].userPrincipalName == $right.UserPrincipalName
| where isempty(LastSignIn) or LastSignIn < ago(90d)
| project UserPrincipalName = tostring(TargetResources[0].userPrincipalName), LastSignIn
```

Review results monthly. Exclude service accounts. Any human account inactive 90+ days without a documented leave date is an orphan finding.

---

## 8. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Workflow execution audit | Weekly | IAM Analyst |
| Dynamic group membership spot check | Monthly | IAM Lead |
| Orphan account scan | Monthly | IAM Lead |
| HR attribute flow validation | Quarterly | IAM Lead + HR |
| Full lifecycle test (J/M/L) | Quarterly | IAM Lead |
| Workflow configuration review | Semi-annual | IAM Lead + Security |

---

## 9. Troubleshooting

**Joiner did not fire:** Check employeeHireDate format (must be UTC ISO 8601). Check workflow is enabled and trigger condition matches.

**Dynamic group not updating:** Check group processing status. Verify user attribute matches rule syntax exactly. Check for typos in department name.

**Leaver did not disable:** Check employeeLeaveDateTime format. Check workflow execution log for errors. If workflow failed, manually disable and investigate.

**Attributes not syncing from HR:** Check provisioning logs. Verify attribute mapping in provisioning configuration. Check HR source for data quality.

---

*Stella Maris Governance — 2026*
