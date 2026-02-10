# Screenshot Capture Guide — PIM + Break-Glass SOP

> Replace HTML mockups with real screenshots from your Entra tenant.

---

## Screenshots

### 01 — PIM Roles Overview
**Path:** Entra ID > Identity Governance > PIM > Entra roles
**Show:** Eligible (your admins) + Active (break-glass only). Key: 0 active human admins.

### 02 — PIM Role Settings (Global Admin)
**Path:** PIM > Entra roles > Settings > Global Administrator
**Show:** 8hr max, MFA required, justification required, approval required

### 03 — PIM Activation Request
**Path:** myaccess.microsoft.com > PIM > Activate Global Administrator
**Show:** Duration selector + justification field

### 04 — PIM Approval Workflow
**Path:** As approver: myaccess.microsoft.com > Approve requests
**Show:** Pending approval with requester, role, justification

### 05 — PIM Audit History
**Path:** PIM > Entra roles > Audit history
**Show:** Activation events with user, role, justification, timestamp

### 06 — Break-Glass Account Properties
**Path:** Entra ID > Users > bg-admin-01 > Auth methods + Assigned roles
**Show:** Global Admin permanent, no MFA, in grp-ca-breakglass-exclude

### 07 — Break-Glass Alert Rule
**Path:** Sentinel > Analytics > break-glass rule > last run
**Show:** NRT rule definition + triggered alert from test

### 08 — Break-Glass Test Log
**Path:** This repo > code/breakglass-test-log.md
**Show:** Completed entries for 2+ months
