# Break-Glass Emergency Access — Standard Operating Procedure

> **Version:** 1.0.0 | **Classification:** RESTRICTED — Need to Know
> **Author:** Robert Myers, MBA | Stella Maris Governance

---

## 1. Purpose

Emergency access accounts ensure the organization is never permanently locked out of its own tenant. They are the last line of defense when all other authentication mechanisms fail.

---

## 2. Account Design

Two accounts, two methods, two locations.

| Property | bg-admin-01 | bg-admin-02 |
|----------|-------------|-------------|
| UPN | bg-admin-01@{tenant}.onmicrosoft.com | bg-admin-02@{tenant}.onmicrosoft.com |
| Role | Global Administrator (permanent active) | Global Administrator (permanent active) |
| Auth | Password (24+ chars, random) | FIDO2 security key |
| MFA | None configured | FIDO2 only |
| CA status | Excluded from ALL policies | Excluded from ALL policies |
| Storage | Sealed envelope, locked cabinet, Location A | FIDO2 key, fire safe, Location B |
| License | None | None |

### Why Two Different Methods

| Failure | Which Works |
|---------|-------------|
| MFA infrastructure down | bg-admin-01 (password only) |
| Password auth compromised | bg-admin-02 (FIDO2 only) |
| Single location destroyed | The other location |
| CA misconfiguration | Both (excluded) |
| PIM service down | Both (permanent active) |

---

## 3. Account Creation

### bg-admin-01 (Password)

1. Create user: bg-admin-01@{tenant}.onmicrosoft.com (use .onmicrosoft.com, NOT custom domain)
2. Generate 24+ char random password
3. Write password on paper (NOT digital)
4. Assign Global Administrator (permanent)
5. Do NOT assign M365 license
6. Do NOT configure MFA
7. Add to grp-ca-breakglass-exclude

### bg-admin-02 (FIDO2)

1. Create user: bg-admin-02@{tenant}.onmicrosoft.com
2. Assign Global Administrator (permanent)
3. Register FIDO2 key at mysignins.microsoft.com
4. Disable password sign-in
5. Add to grp-ca-breakglass-exclude

### Verify CA Exclusion

For EVERY CA policy: Users > Exclude > confirm grp-ca-breakglass-exclude listed. Test: sign in as bg-admin-01, check sign-in log — CA tab shows Not Applied for all policies.

---

## 4. Credential Storage

### Sealed Envelope (bg-admin-01)

1. Write on paper: account UPN, password, purpose, date, sealed by
2. Place in tamper-evident envelope
3. Sign across the seal
4. Store in locked cabinet at Location A
5. Record in access log

### FIDO2 Key (bg-admin-02)

1. Label key: BG-ADMIN-02 EMERGENCY ONLY
2. Place in fire-rated safe at Location B (DIFFERENT building)
3. Record in access log

### Access Log Template

| Date | Action | Account | Location | Performed By | Witnessed By |
|------|--------|---------|----------|-------------|-------------|
| | | | | | |

---

## 5. Monthly Test Procedure

**Cadence:** 1st of every month (or next business day)

### Checklist

1. Retrieve credentials from storage
2. Verify seal intact
3. Open incognito browser
4. Sign in at portal.azure.com
5. Navigate to Entra ID > Users (confirms Global Admin)
6. Verify Sentinel alert fired within 90 seconds
7. Verify Teams notification received
8. Sign out
9. bg-admin-01: generate new password, update in Entra, seal in new envelope
10. bg-admin-02: return FIDO2 key to safe
11. Update access log
12. Record results in breakglass-test-log.md

---

## 6. Emergency Activation

**STOP.** Confirm this is genuine emergency — all other access exhausted.

1. Confirm emergency — document what failed
2. Notify team (verbal OK, document later)
3. Retrieve credentials from storage (note time, witness if possible)
4. Sign in from known-secure device
5. Perform ONLY the necessary emergency action
6. Document every action taken
7. Sign out immediately
8. Rotate credentials immediately
9. Re-seal and re-store
10. Initiate post-incident review

---

## 7. Post-Incident

### Within 1 Hour
- Credentials rotated and re-sealed
- Incident channel opened
- Timeline started

### Within 24 Hours
- Incident report: root cause, actions taken, duration, alert verification
- Sign-in logs reviewed
- Audit log reviewed for all break-glass actions

### Within 1 Week
- Root cause remediation plan
- Preventive measures identified
- Incident report finalized
- Lessons learned shared

---

*Stella Maris Governance — 2026*
