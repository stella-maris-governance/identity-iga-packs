# Screenshot Capture Guide — Conditional Access Baseline

> Replace each HTML mockup with a real screenshot from your Entra ID tenant.
> Naming: keep same filenames, change .html to .png
> Resolution: minimum 1920x1080

---

## Pre-Capture Checklist

- [ ] Signed in as admin with CA read permissions
- [ ] All 10 CA policies deployed and Enabled
- [ ] At least 7 days of sign-in data

---

## Screenshots

### 01 — CA Policies List View
**Path:** entra.microsoft.com > Security > Conditional Access > Policies
**Show:** All 10 policies with Name, State (On), Users, Grant controls

### 02 — CA001 Assignments Tab
**Path:** CA001 policy > Users tab
**Show:** Include: All users. Exclude: grp-ca-breakglass-exclude

### 03 — CA001 Grant Controls
**Path:** CA001 policy > Grant section
**Show:** Require multifactor authentication checked

### 04 — CA004 Risk Condition
**Path:** CA004 policy > Conditions > Sign-in risk
**Show:** High checkbox checked

### 05 — CA010 Authentication Strength
**Path:** CA010 policy > Grant > Authentication strength
**Show:** Phishing-resistant MFA selected

### 06 — Named Locations
**Path:** Security > Conditional Access > Named locations
**Show:** Trusted corporate network + blocked countries (RU, CN, KP, IR)

### 07 — CA Insights Workbook
**Path:** Security > Conditional Access > Insights and reporting
**Show:** Policy impact summary over 14-day period

### 08 — Sign-in Log with CA Applied
**Path:** Entra ID > Sign-in logs > click sign-in > Conditional Access tab
**Show:** CA001 as Success — proves policy is enforcing

---

*Stella Maris Governance — 2026*
