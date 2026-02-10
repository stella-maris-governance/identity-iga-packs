# Screenshot Capture Guide — Vendor / Guest vIAM

---

### 01 — Access Packages List
**Path:** Entra ID > Identity Governance > Entitlement Management > Access packages
**Show:** All 4 guest packages with status, assignments, catalog

### 02 — Access Package Assignment with Approval
**Path:** Access package > Assignments
**Show:** Active assignment with requestor, approver, justification, expiry date

### 03 — Cross-Tenant Access Settings
**Path:** Entra ID > External Identities > Cross-tenant access settings
**Show:** Default inbound blocked, trusted orgs listed, MFA trust enabled

### 04 — Guest Account Properties
**Path:** Entra ID > Users > [guest user] > Properties
**Show:** userType = Guest, sponsor field, creation date, source

### 05 — Guest Expiration Scan Results
**Source:** Log Analytics > guest-expiration-scan.kql output
**Show:** Expired or inactive guests identified by scan
