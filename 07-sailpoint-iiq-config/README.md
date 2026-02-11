# SailPoint IdentityIQ Configuration Pack

> Enterprise identity governance — lifecycle automation, access certifications, role mining, and SOD enforcement at scale

[![Cert](https://img.shields.io/badge/cert-SailPoint_ISL-0033A0?style=flat-square)]()
[![Cert](https://img.shields.io/badge/cert-SC--300-0078D4?style=flat-square&logo=microsoft)](https://learn.microsoft.com/en-us/credentials/certifications/identity-and-access-administrator/)
[![Controls](https://img.shields.io/badge/Expected_vs_Observed-10_controls-8957e5?style=flat-square)]()
[![Framework](https://img.shields.io/badge/framework-Enterprise_IGA-ff6b35?style=flat-square)]()

---

## Start Here

| You Are | Read This First |
|---------|----------------|
| **Hiring Manager** | This README (architecture + config approach) then [`expected-vs-observed.md`](docs/expected-vs-observed.md) — proves enterprise IGA design and configuration, not just certification |
| **Consulting Client** | [`expected-vs-observed.md`](docs/expected-vs-observed.md) — if your IGA platform is deployed but not governed, the gap is your engagement |
| **Auditor / GRC** | [`expected-vs-observed.md`](docs/expected-vs-observed.md) then [`control-mapping.md`](docs/control-mapping.md) — NIST AC-2, AC-6, AU-2 alignment |
| **Engineer** | [`/code/`](code/) for IIQ config XML then [`iiq-operations-runbook.md`](docs/iiq-operations-runbook.md) |

---

## Overview

This pack demonstrates **enterprise-grade identity governance configuration** using SailPoint IdentityIQ — the platform that governs identity when Entra-native tools aren't enough.

**When you need SailPoint (and when you don't):**

| Scenario | Tool |
|----------|------|
| Single cloud tenant, under 500 users, Microsoft-only | Entra ID Governance (Packs 01-06) |
| Multi-source (AD + Entra + SaaS + on-prem), 500+ users, complex entitlements | **SailPoint IdentityIQ** |
| Regulated industry with SOX, SOD enforcement, role mining at scale | **SailPoint IdentityIQ** |
| Hybrid environment with legacy systems that don't support SCIM | **SailPoint IdentityIQ** |

**What this pack covers:**

| Capability | What It Does | IIQ Component |
|-----------|-------------|---------------|
| **Lifecycle management** | Joiner/mover/leaver across all connected sources | Lifecycle Events + Provisioning Policies |
| **Access certifications** | Manager and entitlement owner campaigns | Certification Campaigns |
| **Role management** | IT roles, business roles, entitlement bundles | Role Model + Role Mining |
| **SOD enforcement** | Policy violations detected and blocked in real time | SOD Policy + Violation Manager |
| **Provisioning** | Automated account create/modify/disable across systems | Provisioning Plans + Connectors |
| **Audit** | Every decision logged, exportable, framework-mapped | Audit Configuration + Reports |

**Business Value:** SailPoint is the enterprise answer to "who has access to what, and why." Organizations with complex environments — multiple directories, SaaS apps, on-prem systems, contractors, and regulatory requirements — need a platform that correlates identity across all sources. This pack delivers the configuration design, not just the install.

*Most SailPoint implementations fail not because the product is wrong, but because the governance design behind it is wrong. This pack is the governance design.*

---

## Architecture
```mermaid
graph TD
    subgraph SOURCES["Identity Sources"]
        AD["Active Directory"]
        ENTRA["Entra ID"]
        HR["HR System -- Authoritative"]
        SAAS["SaaS Apps -- Salesforce, ServiceNow, Jira"]
        ONPREM["On-Prem Systems -- ERP, Databases"]
    end

    subgraph IIQ["SailPoint IdentityIQ"]
        AGG["Aggregation -- Correlate identities across sources"]
        IDENTITY["Identity Cube -- Single view of every user"]
        ROLES["Role Model -- IT roles + business roles"]
        LIFECYCLE["Lifecycle Events -- Joiner / Mover / Leaver"]
        CERT["Certification Campaigns -- Manager + entitlement owner"]
        SOD["SOD Policy Engine -- Real-time violation detection"]
        PROVISION["Provisioning Plans -- Automated fulfillment"]
    end

    subgraph GOVERNANCE["Governance Outputs"]
        APPROVE["Access Request + Approval Workflow"]
        REVOKE["Automated Revocation"]
        REPORT["Audit Reports + Evidence"]
        ALERT["SOD Violation Alerts"]
    end

    subgraph EVIDENCE["Audit Evidence"]
        CERT_LOG["Certification Decision Log"]
        PROVISION_LOG["Provisioning Audit Trail"]
        SOD_LOG["SOD Violation + Resolution Log"]
        EVO["Expected vs Observed"]
    end

    AD --> AGG
    ENTRA --> AGG
    HR --> AGG
    SAAS --> AGG
    ONPREM --> AGG

    AGG --> IDENTITY
    IDENTITY --> ROLES
    IDENTITY --> LIFECYCLE
    IDENTITY --> CERT
    IDENTITY --> SOD

    LIFECYCLE --> PROVISION
    CERT --> REVOKE
    SOD --> ALERT
    PROVISION --> APPROVE

    CERT_LOG --> EVO
    PROVISION_LOG --> EVO
    SOD_LOG --> EVO
    REPORT --> EVO
```

---

## IIQ Configuration Summary

### Lifecycle Events

| Event | Trigger | Actions |
|-------|---------|---------|
| Joiner | Identity detected with no accounts, or hire date reached | Create AD account, create Entra account, assign birthright roles, send welcome notification |
| Mover | Department or manager change detected during aggregation | Recalculate roles, remove stale entitlements, add new entitlements, notify old + new manager |
| Leaver | Termination date reached or HR status = Inactive | Disable all accounts, remove all entitlements, archive identity, notify manager + IT |
| Rehire | Previously terminated identity reappears with active status | Reactivate accounts, reassign birthright roles, flag for manager review |

### Role Model

| Role Type | Purpose | Example |
|-----------|---------|---------|
| IT Role | Maps to a single system entitlement | AD-Engineering-ReadWrite, Salesforce-Standard-User |
| Business Role | Bundles multiple IT roles by job function | Engineer (includes AD group + Jira + GitHub access) |
| Birthright Role | Auto-assigned to all employees | Corporate-Baseline (email, intranet, HR self-service) |
| Organizational Role | Department-scoped access | Finance-Department (ERP read, budget reports, AP viewer) |

### Certification Campaigns

| Campaign | Scope | Reviewer | Frequency | Auto-Revoke |
|----------|-------|----------|-----------|-------------|
| Manager Access Review | All direct reports | People manager | Quarterly | Yes — 14 days |
| Entitlement Owner Review | High-risk entitlements | Entitlement owner | Quarterly | Yes — 14 days |
| SOD Violation Review | All open SOD violations | SOD policy owner | Monthly | Escalate to CISO |
| Privileged Access Review | Admin-level entitlements | Security team | Quarterly | Yes — 7 days |

### SOD Policies

| Policy | Left Role | Right Role | Risk | Action |
|--------|-----------|------------|------|--------|
| SOD-FIN-001 | AP Create Invoice | AP Approve Payment | Critical | Block + alert |
| SOD-FIN-002 | Vendor Master Create | AP Approve Payment | Critical | Block + alert |
| SOD-HR-001 | HR Data Entry | Payroll Approve | High | Alert + require exception |
| SOD-IT-001 | Change Requester | Change Approver | Medium | Alert |

> These mirror Pack 05 (SoD Matrix) Tier 3 conflicts — SailPoint enforces what the matrix defines.

---

## Compliance Mapping

| Framework | Control ID | Control Name | Implementation |
|-----------|-----------|--------------|----------------|
| NIST 800-53 | AC-2 | Account Management | Full lifecycle across all connected systems |
| NIST 800-53 | AC-2(4) | Automated Audit Actions | All provisioning and certification logged |
| NIST 800-53 | AC-5 | Separation of Duties | SOD policy engine with real-time detection |
| NIST 800-53 | AC-6 | Least Privilege | Role model ensures minimum necessary access |
| NIST 800-53 | AC-6(7) | Review of User Privileges | Quarterly certification campaigns |
| NIST 800-53 | AU-2 | Event Logging | Every identity event auditable |
| SOX ITGC | Periodic access review | Quarterly manager + entitlement owner certifications |
| SOX ITGC | Segregation of duties | Real-time SOD enforcement with blocking |
| CMMC L2 | AC.L2-3.1.1 | Authorized Access Control | Role-based access with certification |

> Full mapping: [`docs/control-mapping.md`](docs/control-mapping.md)

---

## What's Included

### `code/` — Configuration Artifacts

| File | Description |
|------|-------------|
| `lifecycle-events.xml` | IIQ lifecycle event triggers and provisioning actions |
| `role-model-sample.xml` | Sample role hierarchy: birthright, IT, business roles |
| `certification-campaigns.xml` | 4 certification campaign definitions |
| `sod-policies.xml` | SOD policy definitions with enforcement actions |
| `audit-configuration.xml` | Audit logging configuration |

### `docs/` — SOPs, Runbooks, Evidence

| File | Description |
|------|-------------|
| [`expected-vs-observed.md`](docs/expected-vs-observed.md) | The Law of Evidence — 10 controls |
| [`iiq-operations-runbook.md`](docs/iiq-operations-runbook.md) | Full IIQ operations SOP |
| [`control-mapping.md`](docs/control-mapping.md) | NIST / SOX / CMMC alignment |

### `screenshots/` — Portal Evidence

| # | What It Shows |
|---|--------------|
| 01 | IIQ Dashboard: identities, certifications, violations summary |
| 02 | Lifecycle event execution: joiner provisioning |
| 03 | Certification campaign: manager decisions |
| 04 | SOD violation: detected and blocked |
| 05 | Provisioning audit trail |

---

## Deployment Guide

| Step | Action | Duration |
|------|--------|----------|
| 1 | Connect authoritative source (HR system) | 2-4 hours |
| 2 | Connect target systems (AD, Entra, SaaS) | 2-8 hours per source |
| 3 | Run initial aggregation and correlation | 2 hours |
| 4 | Define role model (birthright → IT → business) | 1-2 days |
| 5 | Configure lifecycle events (joiner/mover/leaver) | 1 day |
| 6 | Configure certification campaigns | 4 hours |
| 7 | Configure SOD policies | 4 hours |
| 8 | Test full lifecycle: create user in HR → verify provisioning | 1 day |
| 9 | Run first certification campaign in pilot group | 2 weeks |
| 10 | Capture screenshots and complete E-v-O | 1 day |

> SailPoint IIQ is an enterprise platform. Deployment timelines are weeks to months depending on complexity. This pack provides the governance design; implementation requires SailPoint expertise and infrastructure.

---

## Related Packs

| Pack | Relationship |
|------|-------------|
| [Zero-Touch JML Lifecycle](../01-zero-touch-jml-lifecycle/) | Entra-native JML for simpler environments; SailPoint for enterprise |
| [Access Reviews Automation](../02-access-reviews-automation/) | Entra-native reviews; SailPoint certifications for multi-system |
| [SoD Matrix](../05-sod-matrix/) | SoD definitions; SailPoint enforces them at the platform level |
| [Vendor/Guest vIAM](../06-vendor-guest-viam/) | Entra governs guests; SailPoint can extend to external contractors |

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
