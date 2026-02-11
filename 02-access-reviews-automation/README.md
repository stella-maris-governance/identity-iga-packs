# Access Reviews Automation Pack

> Automated Entra ID Access Reviews for group memberships, app assignments, PIM roles, and guest access

[![Cert](https://img.shields.io/badge/cert-SC--300-0078D4?style=flat-square&logo=microsoft)](https://learn.microsoft.com/en-us/credentials/certifications/identity-and-access-administrator/)
[![Cert](https://img.shields.io/badge/cert-SailPoint_ISL-0033A0?style=flat-square)]()
[![Controls](https://img.shields.io/badge/Expected_vs_Observed-10_controls-8957e5?style=flat-square)]()
[![Framework](https://img.shields.io/badge/framework-Identity_Governance-ff6b35?style=flat-square)]()

---

## Start Here

| You Are | Read This First |
|---------|----------------|
| **Hiring Manager** | This README then [`expected-vs-observed.md`](docs/expected-vs-observed.md) — proves you can run continuous access certification, not just annual rubber-stamp reviews |
| **Consulting Client** | [`expected-vs-observed.md`](docs/expected-vs-observed.md) — if your org does annual spreadsheet reviews or none at all, the gap is your engagement |
| **Auditor / GRC** | [`expected-vs-observed.md`](docs/expected-vs-observed.md) then [`control-mapping.md`](docs/control-mapping.md) — NIST AC-2(7), AC-6(7) alignment with auto-revoke evidence |
| **Engineer** | [`/code/`](code/) for access review definitions then [`access-reviews-runbook.md`](docs/access-reviews-runbook.md) |

---

## Overview

This pack delivers **continuous, automated access certification** across four access domains: group memberships, application assignments, PIM eligible roles, and guest/external users. Reviews are scheduled, delegated to appropriate reviewers, and auto-revoke access when reviewers don't respond.

**The problem this solves:** Most organizations either do no access reviews, do annual spreadsheet reviews (rubber-stamp), or rely on manual processes that miss access drift. This pack automates the entire cycle — schedule, notify, collect decisions, revoke, report.

**Four review domains, one governance engine:**

| Review | Scope | Reviewer | Frequency | Auto-Revoke |
|--------|-------|----------|-----------|-------------|
| **Group membership** | Department and role-based security groups | Group owner / manager | Quarterly | Yes — 14-day non-response |
| **Application access** | Enterprise app assignments (Salesforce, Jira, etc.) | App owner | Quarterly | Yes — 14-day non-response |
| **PIM eligible roles** | All PIM-managed admin role assignments | Security Administrator | Quarterly | Yes — 14-day non-response |
| **Guest access** | All guest/external users | Inviting user / sponsor | Monthly | Yes — 7-day non-response |

**Business Value:** Access reviews are the most common audit finding in identity programs. Organizations that can demonstrate automated, continuous review with auto-revoke evidence close audit gaps immediately and reduce risk exposure from stale access.

**Operational Context:** Built from experience running credential validation programs across 3,500+ personnel where every access decision was documented, reviewed on cadence, and revoked when no longer justified — because in regulated environments, unreviewed access is unauthorized access.

---

## Architecture
```mermaid
graph TD
    subgraph SCHEDULE["Scheduled Reviews"]
        GRP_REV["Group Membership Review -- Quarterly"]
        APP_REV["App Assignment Review -- Quarterly"]
        PIM_REV["PIM Role Review -- Quarterly"]
        GUEST_REV["Guest Access Review -- Monthly"]
    end

    subgraph REVIEW["Review Process"]
        NOTIFY["Reviewer notified via email"]
        DECIDE["Approve / Deny / Don't know"]
        JUSTIFY["Justification captured"]
        TIMEOUT["Non-response after SLA"]
    end

    subgraph ACTION["Auto-Actions"]
        APPROVE_ACT["Access retained -- logged"]
        DENY_ACT["Access revoked immediately"]
        TIMEOUT_ACT["Auto-revoke on non-response"]
        RECOMMEND["System recommendation -- machine learning"]
    end

    subgraph EVIDENCE["Audit Evidence"]
        REVIEW_LOG["Access Review Results"]
        REVOKE_LOG["Revocation Audit Trail"]
        COMPLETION["Completion Rate Report"]
        EVO["Expected vs Observed"]
    end

    GRP_REV --> NOTIFY
    APP_REV --> NOTIFY
    PIM_REV --> NOTIFY
    GUEST_REV --> NOTIFY

    NOTIFY --> DECIDE
    DECIDE --> JUSTIFY
    NOTIFY --> TIMEOUT

    DECIDE -->|Approve| APPROVE_ACT
    DECIDE -->|Deny| DENY_ACT
    TIMEOUT --> TIMEOUT_ACT
    RECOMMEND --> DECIDE

    APPROVE_ACT --> REVIEW_LOG
    DENY_ACT --> REVOKE_LOG
    TIMEOUT_ACT --> REVOKE_LOG
    REVIEW_LOG --> COMPLETION
    REVOKE_LOG --> COMPLETION
    COMPLETION --> EVO
```

---

## Access Review Definitions

| Review Name | Scope | Reviewer | Frequency | Duration | Auto-Revoke | Recommendations |
|-------------|-------|----------|-----------|----------|-------------|-----------------|
| AR-GRP-Quarterly | All grp-dept-* and grp-app-* groups | Group owners | Every 90 days | 14 days | Yes | Enabled (sign-in activity) |
| AR-APP-Quarterly | Salesforce, Jira, ServiceNow assignments | App owners | Every 90 days | 14 days | Yes | Enabled |
| AR-PIM-Quarterly | All PIM eligible role assignments | Security Administrator | Every 90 days | 14 days | Yes | Enabled |
| AR-GUEST-Monthly | All guest/external users | Sponsor / inviter | Every 30 days | 7 days | Yes | Enabled (sign-in activity) |

### Auto-Revoke Logic

When a reviewer does not respond within the review duration:
- **Groups:** User removed from group (loses group-based access)
- **Apps:** User assignment removed (loses SSO access)
- **PIM:** Eligible assignment removed (loses ability to activate)
- **Guests:** Guest account disabled, access blocked

This is the most critical design decision: **non-response = deny.** This eliminates rubber-stamp risk and ensures stale access cannot persist through reviewer inaction.

---

## Compliance Mapping

| Framework | Control ID | Control Name | Implementation |
|-----------|-----------|--------------|----------------|
| NIST 800-53 | AC-2(7) | Privileged User Accounts Review | PIM quarterly review for all eligible roles |
| NIST 800-53 | AC-6(7) | Review of User Privileges | Quarterly group + app reviews |
| NIST 800-53 | AC-2(3) | Disable Accounts | Auto-revoke on non-response disables stale access |
| NIST 800-53 | AU-6 | Audit Record Review | Review completion reports with decision + justification |
| CIS Azure v2.0 | 1.1.4 | Ensure PIM access reviews | PIM eligible assignments reviewed quarterly |
| CMMC L2 | AC.L2-3.1.7 | Privileged Functions | PIM roles validated quarterly via access review |
| CMMC L2 | AC.L2-3.1.1 | Authorized Access Control | All access reviewed and certified by owner |
| SOX ITGC | Periodic access review | All access certified by business owner | Quarterly with auto-revoke |

> Full mapping: [`docs/control-mapping.md`](docs/control-mapping.md)

---

## What's Included

### `code/` — Deployable Artifacts

| File | Description |
|------|-------------|
| `access-review-group.json` | Access review definition: group memberships |
| `access-review-app.json` | Access review definition: app assignments |
| `access-review-pim.json` | Access review definition: PIM eligible roles |
| `access-review-guest.json` | Access review definition: guest/external users |
| `review-completion-query.kql` | KQL: review completion rates + revocation counts |
| `deploy-access-reviews.ps1` | PowerShell: create all 4 access review schedules |

### `docs/` — SOPs, Runbooks, Evidence

| File | Description |
|------|-------------|
| [`expected-vs-observed.md`](docs/expected-vs-observed.md) | The Law of Evidence — 10 controls |
| [`access-reviews-runbook.md`](docs/access-reviews-runbook.md) | Full operations SOP |
| [`control-mapping.md`](docs/control-mapping.md) | NIST / CIS / CMMC / SOX alignment |

### `screenshots/` — Portal Evidence

| # | What It Shows |
|---|--------------|
| 01 | Access reviews dashboard: all 4 reviews with completion rates |
| 02 | Group review: reviewer decisions (approve/deny) with justifications |
| 03 | PIM review: eligible role certifications |
| 04 | Guest review: monthly review with auto-revoke results |
| 05 | Review results export: full decision log |
| 06 | Auto-revoke evidence: access removed after non-response |

---

## Deployment Guide

| Step | Action | Duration |
|------|--------|----------|
| 1 | Ensure group owners are assigned on all grp-dept and grp-app groups | 1 hour |
| 2 | Ensure app owners are assigned on enterprise app registrations | 30 min |
| 3 | Create group membership access review (AR-GRP-Quarterly) | 20 min |
| 4 | Create app assignment access review (AR-APP-Quarterly) | 20 min |
| 5 | Create PIM role access review (AR-PIM-Quarterly) | 20 min |
| 6 | Create guest access review (AR-GUEST-Monthly) | 20 min |
| 7 | Wait for first review cycle to complete | 14-30 days |
| 8 | Verify auto-revoke fired for any non-responses | 1 hour |
| 9 | Capture screenshots and complete E-v-O | 1.5 hours |

> Prerequisites: Entra ID P2 (Access Reviews require P2), group/app owners assigned, PIM configured (see Pack 04)

---

## Related Packs

| Pack | Relationship |
|------|-------------|
| [Zero-Touch JML Lifecycle](../01-zero-touch-jml-lifecycle/) | Mover events trigger access review for old access |
| [Conditional Access Baseline](../03-conditional-access-baseline/) | CA exception groups included in quarterly review |
| [PIM + Break-Glass SOP](../04-pim-breakglass-sop/) | PIM eligible assignments reviewed quarterly here |
| [SoD Matrix](../05-sod-matrix/) | SoD violations flagged during access review decisions |
| [Vendor/Guest vIAM](../06-vendor-guest-viam/) | Guest review syncs with guest lifecycle policy |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-02-10 | Initial release |

---

<div align="center">

**© 2026 Stella Maris Governance LLC** — Evaluation and demonstration use permitted. Commercial use requires engagement.

*The work speaks for itself. Stella Maris — the one light that does not drift.*

</div>
