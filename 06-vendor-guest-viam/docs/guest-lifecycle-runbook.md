# Guest Lifecycle — Operations Runbook

> **Version:** 1.0.0 | **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose and Scope

Operational procedures for external identity lifecycle governance using Entra ID Entitlement Management, cross-tenant access settings, and conditional access.

**Scope:** All guest/external user accounts (userType = Guest) in the tenant.

**Out of Scope:** Employee lifecycle (see Pack 01), service accounts, break-glass accounts.

---

## 2. Prerequisites

| Requirement | Detail |
|-------------|--------|
| Entra ID P2 / Governance | Entitlement Management requires Governance license |
| CA007 deployed | Pack 03 — MFA + ToU for guests |
| AR-GUEST-Monthly active | Pack 02 — monthly guest access review |
| Cross-tenant settings configured | Default inbound blocked, trusted orgs added |
| Guest invite restrictions set | Only members + specific roles can invite |

---

## 3. Inviting a Guest (Access Package Flow)

Sponsors should NEVER invite guests directly. All guests should come through access packages.

### Sponsor Steps

1. Navigate to myaccess.microsoft.com > Access packages
2. Select appropriate package (Project, Vendor, Audit, Executive)
3. Click "Request" on behalf of external user
4. Enter guest email address
5. Provide business justification
6. Submit — request goes to approver

### Approver Steps

1. Receive approval notification (email or myaccess portal)
2. Review: who is being invited, which package, justification
3. Approve or deny with written justification
4. On approval: guest receives invitation email automatically

### Guest Steps

1. Click invitation link in email
2. Accept Terms of Use
3. Register MFA method (or satisfy via home tenant MFA trust)
4. Access scoped resources granted by the access package

---

## 4. Renewing Guest Access

Access packages expire automatically. To continue access:

1. Sponsor receives expiration warning email (7 days before)
2. Sponsor navigates to myaccess > My access packages > Renew
3. Provides renewed justification
4. Approver approves renewal
5. New assignment period begins (same max duration)

If sponsor does not renew: access package expires, guest removed from groups.

---

## 5. Offboarding a Guest (Early Termination)

When a guest's engagement ends before the access package expires:

1. Sponsor navigates to myaccess > Assignments > Remove
2. Or: admin removes assignment in Entra > Identity Governance > Entitlement Management
3. Guest immediately removed from package-granted groups
4. Notify guest that access has been terminated
5. Account enters 30-day grace period (can be re-invited if needed)

---

## 6. Legacy Guest Remediation

For guests that existed before entitlement management:

1. Run guest-expiration-scan.kql to identify guests without access package assignments
2. For each legacy guest:
   - Identify purpose and business owner
   - Assign sponsor
   - Either migrate to access package or set manual expiration
   - If no owner found: disable immediately, delete after 30 days
3. Document all remediations

---

## 7. Managing Trusted Organizations

### Adding a New Partner

1. Entra ID > External Identities > Cross-tenant access settings
2. Add organization (partner tenant ID)
3. Inbound: allow B2B collaboration
4. Trust settings: enable MFA trust if partner uses Entra MFA
5. Do NOT enable B2B direct connect unless explicitly required
6. Document in trusted organization register

### Removing a Partner

1. Remove all active guest accounts from that partner (or let expire)
2. Remove organization from cross-tenant access settings
3. Default block resumes for that tenant
4. Document removal reason and date

---

## 8. Monitoring

### Weekly

- Check entitlement management for pending requests stuck in approval
- Review any guest sign-in failures (CA007 blocks)

### Monthly

- AR-GUEST-Monthly review (Pack 02)
- Run guest-expiration-scan.kql for guests past expiry
- Verify all guests have sponsors

### Quarterly

- Cross-tenant access settings review
- Trusted organization list review
- Full legacy guest sweep

---

## 9. Review Cadence

| Review | Frequency | Owner |
|--------|-----------|-------|
| Guest access review | Monthly | Sponsors via Pack 02 |
| Pending request check | Weekly | IAM Analyst |
| Expiration scan | Monthly | IAM Lead |
| Cross-tenant settings | Quarterly | IAM Lead + Security |
| Trusted org list | Quarterly | IAM Lead + Business |
| Legacy guest sweep | Quarterly | IAM Lead |

---

## 10. Troubleshooting

**Guest cannot sign in:** Check CA007 — did they accept ToU? Check MFA registration. Check cross-tenant settings for their tenant.

**Access package request stuck:** Check approver received notification. If approver unavailable, escalate to backup or admin.

**Guest has access but no package:** Legacy guest. Follow section 6 remediation.

**MFA trust not working:** Verify partner tenant is in trusted organizations AND MFA trust is enabled for that org. Guest must have completed MFA in their home tenant.

---

*Stella Maris Governance — 2026*
