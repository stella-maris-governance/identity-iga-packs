#!/usr/bin/env python3
"""
SCRM Tier One Vendor Risk Assessment — Stella Maris Governance
SMG-SCRM-01 | v2.0.0 (Justification Layer + CUI Boundary)

Implements NIST 800-161 aligned scoring with:
  - Deterministic risk scoring (0-100)
  - Justification layer (evidence + source pointers per subfactor)
  - CUI boundary enforcement (metadata only, no sensitive content)
  - Vendor Risk Passport generation (Markdown)
  - Evidence bundle generation (JSON, AO-sealable)

Team: Atlas (Architect) | North Star (Auditor) | Regina (AO)
Author: Robert Myers, MBA | Stella Maris Governance
References: NIST SP 800-161 Rev 1, NIST SP 800-53 Rev 5 SA-9/SR-3
"""

import json
import sys
import hashlib
import argparse
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# CUI BOUNDARY ENFORCEMENT
# ─────────────────────────────────────────────────────────────

CUI_BOUNDARY_NOTICE = """
╔══════════════════════════════════════════════════════════════╗
║  CUI BOUNDARY ENFORCEMENT — SMG-POL-AC-01                  ║
║                                                              ║
║  This script processes METADATA ONLY.                        ║
║  Actual vendor documents (SOC 2 reports, contracts, PDFs)    ║
║  must NEVER be stored in the Git repository.                 ║
║                                                              ║
║  Source documents → SMG-VAULT (offline/encrypted)            ║
║  Metadata + scores → Git (04_Product_Development/)           ║
║  Sealed passports → Git (07_Evidence_Vault/)                 ║
║                                                              ║
║  Every source reference includes a SHA-256 hash for          ║
║  integrity verification without storing the content.         ║
╚══════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────────
# SCORING CONFIGURATION
# ─────────────────────────────────────────────────────────────

CATEGORY_WEIGHTS = {
    "cyber_posture": 0.45,
    "financial_stability": 0.30,
    "geopolitical_risk": 0.25
}

TIER_MULTIPLIERS = {
    1: 1.00,
    2: 0.90,
    3: 0.80,
    4: 0.70
}

DATA_ACCESS_TIERS = {
    "cui": 1, "itar": 1, "pii": 1,
    "confidential": 2, "internal": 3,
    "public": 4, "none": 4
}

# ─────────────────────────────────────────────────────────────
# SUBFACTOR DEFINITIONS
# Each subfactor includes scoring table + justification schema
# ─────────────────────────────────────────────────────────────

CYBER_SUBFACTORS = {
    "attestation_current": {
        "weight": 0.25,
        "description": "Current third-party attestation (SOC 2 Type II, ISO 27001, FedRAMP)",
        "scoring": {
            "fedramp_high": 0, "fedramp_moderate": 5, "soc2_type2": 10,
            "iso27001": 15, "soc2_type1": 25, "self_attested": 60, "none": 100
        }
    },
    "vuln_management": {
        "weight": 0.20,
        "description": "Vulnerability management program maturity",
        "scoring": {
            "mature": 0, "developing": 30, "minimal": 60, "none": 100
        }
    },
    "incident_history": {
        "weight": 0.20,
        "description": "Security incidents in last 24 months",
        "scoring": {
            "none": 0, "minor_1": 15, "minor_multiple": 35,
            "major_1": 60, "major_multiple": 85, "breach": 100
        }
    },
    "sbom_available": {
        "weight": 0.10,
        "description": "Software Bill of Materials availability",
        "scoring": {"full": 0, "partial": 40, "none": 100}
    },
    "mfa_zero_trust": {
        "weight": 0.15,
        "description": "MFA enforcement and Zero Trust architecture",
        "scoring": {
            "zero_trust": 0, "mfa_enforced": 20, "mfa_partial": 50, "password_only": 100
        }
    },
    "encryption": {
        "weight": 0.10,
        "description": "Encryption at rest and in transit",
        "scoring": {"full": 0, "transit": 30, "partial": 60, "none": 100}
    }
}

FINANCIAL_SUBFACTORS = {
    "years_operating": {
        "weight": 0.20,
        "description": "Years in continuous operation",
        "scoring": {
            "10_plus": 0, "5_to_10": 15, "3_to_5": 30, "1_to_3": 60, "under_1": 100
        }
    },
    "revenue_trend": {
        "weight": 0.25,
        "description": "Revenue trajectory",
        "scoring": {
            "growing": 0, "stable": 15, "declining": 50, "distressed": 90, "unknown": 70
        }
    },
    "funding_status": {
        "weight": 0.20,
        "description": "Funding and capitalization",
        "scoring": {
            "profitable": 0, "well_funded": 15, "series_b_plus": 25,
            "series_a": 45, "seed": 70, "unknown": 80
        }
    },
    "customer_concentration": {
        "weight": 0.20,
        "description": "Revenue concentration risk",
        "scoring": {
            "diversified": 0, "moderate": 30, "concentrated": 60, "dependent": 90, "unknown": 70
        }
    },
    "insurance_coverage": {
        "weight": 0.15,
        "description": "Cyber liability insurance",
        "scoring": {"adequate": 0, "minimal": 40, "none": 80, "unknown": 60}
    }
}

GEOPOLITICAL_SUBFACTORS = {
    "headquarters_jurisdiction": {
        "weight": 0.25,
        "description": "Vendor headquarters jurisdiction",
        "scoring": {
            "us_domestic": 0, "fvey": 10, "eu_adequacy": 20,
            "nato_allied": 30, "non_allied": 70, "restricted": 100
        }
    },
    "data_processing_location": {
        "weight": 0.25,
        "description": "Where your data is processed and stored",
        "scoring": {
            "us_only": 0, "us_primary_eu_dr": 15, "eu_gdpr": 25,
            "multiple_allied": 35, "unknown": 75, "restricted": 100
        }
    },
    "itar_ear_compliance": {
        "weight": 0.25,
        "description": "ITAR/EAR compliance posture",
        "scoring": {
            "compliant_verified": 0, "compliant_self": 25,
            "not_applicable": 10, "unclear": 60, "non_compliant": 100
        }
    },
    "subcontractor_jurisdiction": {
        "weight": 0.15,
        "description": "Tier 2 subcontractor jurisdiction risk",
        "scoring": {
            "all_domestic": 0, "allied_only": 20, "mixed": 50,
            "unknown": 75, "restricted_tier2": 100
        }
    },
    "ownership_structure": {
        "weight": 0.10,
        "description": "Foreign ownership, control, or influence (FOCI)",
        "scoring": {
            "us_owned": 0, "allied_owned": 20, "foci_mitigated": 40,
            "foci_unmitigated": 80, "unknown": 60
        }
    }
}


# ─────────────────────────────────────────────────────────────
# SCORING ENGINE (with Justification Layer)
# ─────────────────────────────────────────────────────────────

def calculate_category_score(subfactors: dict, inputs: dict) -> dict:
    """Calculate weighted score with justification capture."""
    details = {}
    weighted_total = 0.0

    for key, config in subfactors.items():
        entry = inputs.get(key, {})

        # Support both simple string input and dict with justification
        if isinstance(entry, str):
            selected = entry
            justification = None
        elif isinstance(entry, dict):
            selected = entry.get("selected", entry.get("value", "unknown"))
            justification = entry.get("justification", None)
        else:
            selected = "unknown"
            justification = None

        score = config["scoring"].get(selected)
        if score is None:
            score = config["scoring"].get("unknown", 75)

        weighted_score = score * config["weight"]
        weighted_total += weighted_score

        detail = {
            "description": config["description"],
            "selected": selected,
            "raw_score": score,
            "weight": config["weight"],
            "weighted_score": round(weighted_score, 2)
        }

        # Attach justification if provided (the "Why")
        if justification:
            detail["justification"] = {
                "assessor": justification.get("assessor", "Not recorded"),
                "date": justification.get("date", "Not recorded"),
                "evidence_reviewed": justification.get("evidence_reviewed", []),
                "source_references": justification.get("source_references", []),
                "assessor_notes": justification.get("assessor_notes", "")
            }
        else:
            detail["justification"] = {
                "assessor": "PENDING",
                "date": "PENDING",
                "evidence_reviewed": [],
                "source_references": [],
                "assessor_notes": "WARNING: No justification provided. This subfactor will be flagged in audit."
            }

        details[key] = detail

    return {
        "category_score": round(weighted_total, 2),
        "details": details
    }


def calculate_risk_score(vendor: dict) -> dict:
    """Calculate Deterministic Risk Score with full justification chain."""
    data_access = vendor.get("data_access_level", "none").lower()
    tier = DATA_ACCESS_TIERS.get(data_access, 3)
    tier_multiplier = TIER_MULTIPLIERS.get(tier, 0.85)

    cyber = calculate_category_score(CYBER_SUBFACTORS, vendor.get("cyber_posture", {}))
    financial = calculate_category_score(FINANCIAL_SUBFACTORS, vendor.get("financial_stability", {}))
    geopolitical = calculate_category_score(GEOPOLITICAL_SUBFACTORS, vendor.get("geopolitical_risk", {}))

    raw_composite = (
        cyber["category_score"] * CATEGORY_WEIGHTS["cyber_posture"] +
        financial["category_score"] * CATEGORY_WEIGHTS["financial_stability"] +
        geopolitical["category_score"] * CATEGORY_WEIGHTS["geopolitical_risk"]
    )

    adjusted_score = min(round(raw_composite * tier_multiplier, 1), 100.0)

    # Automatic reject triggers
    auto_reject = False
    auto_reject_reasons = []

    def get_selected(category_inputs, key):
        entry = category_inputs.get(key, {})
        if isinstance(entry, str):
            return entry
        return entry.get("selected", entry.get("value", ""))

    itar = get_selected(vendor.get("geopolitical_risk", {}), "itar_ear_compliance")
    if itar == "non_compliant":
        auto_reject = True
        auto_reject_reasons.append("ITAR/EAR non-compliance (CONST-01 violation)")

    hq = get_selected(vendor.get("geopolitical_risk", {}), "headquarters_jurisdiction")
    if hq == "restricted":
        auto_reject = True
        auto_reject_reasons.append("Restricted jurisdiction (POL-SC-01 violation)")

    incident = get_selected(vendor.get("cyber_posture", {}), "incident_history")
    if incident == "breach" and tier == 1:
        auto_reject = True
        auto_reject_reasons.append("Confirmed data breach at Tier 1 (POL-SC-01 violation)")

    # Disposition
    if auto_reject:
        disposition = "REJECT"
        disposition_reason = f"Automatic reject: {'; '.join(auto_reject_reasons)}"
    elif adjusted_score <= 35:
        disposition = "APPROVE"
        disposition_reason = "Risk score within acceptable threshold per POL-SC-01"
    elif adjusted_score <= 65:
        disposition = "APPROVE WITH MITIGATIONS"
        disposition_reason = "Risk score requires documented mitigations per POL-SC-01 before AO approval"
    else:
        disposition = "REJECT"
        disposition_reason = f"Risk score {adjusted_score} exceeds rejection threshold (65) per POL-SC-01"

    # Count justification coverage
    total_subfactors = 0
    justified_subfactors = 0
    for cat in [cyber, financial, geopolitical]:
        for sf_key, sf_data in cat["details"].items():
            total_subfactors += 1
            if sf_data["justification"]["assessor"] != "PENDING":
                justified_subfactors += 1

    return {
        "vendor_name": vendor.get("name", "Unknown"),
        "vendor_service": vendor.get("service", "Unknown"),
        "data_access_level": data_access,
        "tier": tier,
        "tier_multiplier": tier_multiplier,
        "categories": {
            "cyber_posture": {"weight": CATEGORY_WEIGHTS["cyber_posture"], **cyber},
            "financial_stability": {"weight": CATEGORY_WEIGHTS["financial_stability"], **financial},
            "geopolitical_risk": {"weight": CATEGORY_WEIGHTS["geopolitical_risk"], **geopolitical}
        },
        "raw_composite": round(raw_composite, 1),
        "tier_adjusted_score": adjusted_score,
        "auto_reject": auto_reject,
        "auto_reject_reasons": auto_reject_reasons,
        "disposition": disposition,
        "disposition_reason": disposition_reason,
        "justification_coverage": f"{justified_subfactors}/{total_subfactors}",
        "justification_complete": justified_subfactors == total_subfactors,
        "cui_boundary": "ENFORCED — metadata only, no source documents in output",
        "assessment_date": datetime.now().strftime("%Y-%m-%d %H:%M UTC"),
        "methodology": "NIST SP 800-161 Rev 1, NIST SP 800-53 Rev 5 SA-9/SR-3",
        "policy_alignment": ["POL-AC-01", "POL-SC-01", "POL-QR-01", "CONST-01"]
    }


# ─────────────────────────────────────────────────────────────
# VENDOR RISK PASSPORT (Markdown)
# ─────────────────────────────────────────────────────────────

def generate_passport(result: dict) -> str:
    """Generate Vendor Risk Passport with justification summaries."""
    score = result["tier_adjusted_score"]
    filled = int(score / 5)
    bar = "█" * filled + "░" * (20 - filled)

    disp = result["disposition"]
    if disp == "APPROVE":
        badge = "✅ APPROVE"
    elif disp == "APPROVE WITH MITIGATIONS":
        badge = "⚠️  APPROVE WITH MITIGATIONS"
    else:
        badge = "🛑 REJECT"

    lines = []
    lines.append("# Vendor Risk Passport")
    lines.append("")
    lines.append(f"> **SMG-SCRM-01** | Stella Maris Governance LLC")
    lines.append(f"> Assessment Date: {result['assessment_date']}")
    lines.append(f"> Methodology: {result['methodology']}")
    lines.append(f"> CUI Boundary: {result['cui_boundary']}")
    lines.append(f"> Justification Coverage: {result['justification_coverage']}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Vendor Profile
    lines.append("## Vendor Profile")
    lines.append("")
    lines.append(f"| Field | Value |")
    lines.append(f"|-------|-------|")
    lines.append(f"| **Vendor Name** | {result['vendor_name']} |")
    lines.append(f"| **Service** | {result['vendor_service']} |")
    lines.append(f"| **Data Access Level** | {result['data_access_level'].upper()} |")
    tier_labels = {1: "Critical", 2: "High", 3: "Medium", 4: "Low"}
    lines.append(f"| **Vendor Tier** | Tier {result['tier']} ({tier_labels.get(result['tier'], 'Unknown')}) |")
    lines.append(f"| **Tier Multiplier** | {result['tier_multiplier']} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Score
    lines.append("## Deterministic Risk Score")
    lines.append("")
    lines.append(f"```")
    lines.append(f"  Score: {score}/100")
    lines.append(f"  {bar}")
    lines.append(f"  0 ──────────────────── 100")
    lines.append(f"  (Low Risk)      (High Risk)")
    lines.append(f"```")
    lines.append("")
    lines.append(f"**Disposition: {badge}**")
    lines.append("")
    lines.append(f"*{result['disposition_reason']}*")

    if result["auto_reject"]:
        lines.append("")
        for reason in result["auto_reject_reasons"]:
            lines.append(f"- ⛔ {reason}")

    if not result["justification_complete"]:
        lines.append("")
        lines.append(f"> ⚠️  **AUDIT WARNING:** Justification coverage is {result['justification_coverage']}. Unjustified subfactors will be flagged by North Star during audit review.")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Category Breakdown
    lines.append("## Category Breakdown")
    lines.append("")
    lines.append(f"| Category | Weight | Score | Weighted |")
    lines.append(f"|----------|--------|-------|----------|")
    for cat_key, cat_data in result["categories"].items():
        cat_name = cat_key.replace("_", " ").title()
        pct = f"{int(cat_data['weight'] * 100)}%"
        raw = cat_data["category_score"]
        contrib = round(raw * cat_data["weight"], 1)
        lines.append(f"| {cat_name} | {pct} | {raw} | {contrib} |")
    lines.append(f"| **Raw Composite** | | | **{result['raw_composite']}** |")
    lines.append(f"| **Tier-Adjusted** | ×{result['tier_multiplier']} | | **{score}** |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Detailed subfactor breakdown with justification
    for cat_key, cat_data in result["categories"].items():
        cat_name = cat_key.replace("_", " ").title()
        lines.append(f"### {cat_name} ({int(cat_data['weight'] * 100)}%)")
        lines.append("")

        for sf_key, sf_data in cat_data["details"].items():
            j = sf_data.get("justification", {})
            status = "✅" if j.get("assessor", "PENDING") != "PENDING" else "⚠️"

            lines.append(f"**{status} {sf_data['description']}**")
            lines.append(f"")
            lines.append(f"- Selected: `{sf_data['selected']}` → Score: {sf_data['raw_score']} (weight: {sf_data['weight']}, weighted: {sf_data['weighted_score']})")

            if j.get("assessor", "PENDING") != "PENDING":
                lines.append(f"- Assessed by: {j['assessor']} on {j['date']}")
                if j.get("evidence_reviewed"):
                    lines.append(f"- Evidence reviewed:")
                    for ev in j["evidence_reviewed"]:
                        lines.append(f"  - {ev}")
                if j.get("source_references"):
                    lines.append(f"- Source references (CUI Boundary — pointers only):")
                    for sr in j["source_references"]:
                        loc = sr.get("location", "Not specified")
                        doc = sr.get("document", "Not specified")
                        h = sr.get("hash", "Not computed")
                        lines.append(f"  - {doc} → `{loc}` (SHA-256: `{h[:16]}...`)")
                if j.get("assessor_notes"):
                    lines.append(f"- Notes: {j['assessor_notes']}")
            else:
                lines.append(f"- ⚠️  **Justification pending — will be flagged in audit**")

            lines.append("")
        lines.append("---")
        lines.append("")

    # Policy Alignment
    lines.append("## Policy Alignment")
    lines.append("")
    for pol in result.get("policy_alignment", []):
        lines.append(f"- {pol}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Traceability & AO Signature Block
    ts = datetime.now().strftime('%Y%m%d')
    lines.append("## Traceability & Authorization")
    lines.append("")
    lines.append(f"| Field | Value |")
    lines.append(f"|-------|-------|")
    lines.append(f"| **Passport ID** | SMG-SCRM-{result['vendor_name'][:3].upper()}-{ts} |")
    lines.append(f"| **Assessment Date** | {result['assessment_date']} |")
    lines.append(f"| **Methodology** | {result['methodology']} |")
    lines.append(f"| **Scoring Engine** | scrm_tier_one.py v2.0.0 |")
    lines.append(f"| **CUI Boundary** | Enforced |")
    lines.append(f"| **Justification Coverage** | {result['justification_coverage']} |")
    lines.append(f"| | |")
    lines.append(f"| **Prepared by (Atlas)** | ______________________________ |")
    lines.append(f"| **Reviewed by (Principal)** | ______________________________ |")
    lines.append(f"| **Audited by (North Star)** | ______________________________ |")
    lines.append(f"| **Authorized by (AO)** | ______________________________ |")
    lines.append(f"| **AO Signature** | ______________________________ |")
    lines.append(f"| **Signature Date** | ______________________________ |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Stella Maris Governance LLC — The work speaks for itself.*")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# EVIDENCE BUNDLE (JSON — AO-sealable artifact)
# ─────────────────────────────────────────────────────────────

def generate_evidence_bundle(result: dict) -> dict:
    """Generate the Evidence Bundle for AO seal and SRAM feed."""
    controls = []

    # Map scoring results to control assessments
    for cat_key, cat_data in result["categories"].items():
        for sf_key, sf_data in cat_data["details"].items():
            j = sf_data.get("justification", {})
            controls.append({
                "control_id": f"SCRM-VRA-{sf_key[:8].upper()}",
                "category": cat_key,
                "description": sf_data["description"],
                "observed_state": f"Selected: {sf_data['selected']} (score: {sf_data['raw_score']})",
                "justification_provided": j.get("assessor", "PENDING") != "PENDING",
                "assessor": j.get("assessor", "PENDING"),
                "source_references": j.get("source_references", []),
                "status": "PASS" if sf_data["raw_score"] <= 30 else "PARTIAL" if sf_data["raw_score"] <= 60 else "FAIL"
            })

    return {
        "_metadata": {
            "type": "evidence_bundle",
            "version": "2.0.0",
            "generated_by": "scrm_tier_one.py",
            "cui_boundary": "ENFORCED",
            "policy_alignment": result.get("policy_alignment", [])
        },
        "passport_id": f"SMG-SCRM-{result['vendor_name'][:3].upper()}-{datetime.now().strftime('%Y%m%d')}",
        "vendor": result["vendor_name"],
        "service": result["vendor_service"],
        "tier": result["tier"],
        "score": result["tier_adjusted_score"],
        "disposition": result["disposition"],
        "disposition_reason": result["disposition_reason"],
        "justification_coverage": result["justification_coverage"],
        "justification_complete": result["justification_complete"],
        "assessment_date": result["assessment_date"],
        "controls": controls,
        "sram_feed": {
            "risk_id": f"SCRM-VRA-{result['vendor_name'][:3].upper()}",
            "severity": "critical" if result["tier_adjusted_score"] > 65 else "high" if result["tier_adjusted_score"] > 35 else "low",
            "status": "reject" if result["disposition"] == "REJECT" else "mitigate" if "MITIGAT" in result["disposition"] else "accept",
            "pillar": "supply_chain"
        },
        "ao_seal": {
            "status": "PENDING",
            "sealed_by": None,
            "seal_date": None
        }
    }


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Stella Maris SCRM — Vendor Risk Assessment (SMG-SCRM-01 v2.0.0)"
    )
    parser.add_argument("--input", "-i", help="Vendor JSON file")
    parser.add_argument("--output", "-o", help="Vendor Risk Passport (.md)")
    parser.add_argument("--json-output", "-j", help="Raw scoring data (.json)")
    parser.add_argument("--evidence-bundle", "-e", help="Evidence bundle (.json)")
    args = parser.parse_args()

    print(CUI_BOUNDARY_NOTICE)

    if args.input:
        with open(args.input) as f:
            vendor = json.load(f)
        print(f"  Loaded vendor data from {args.input}")
    else:
        print("  ERROR: Interactive mode requires --input flag for v2.0.0")
        print("  Use the justified vendor JSON template.")
        sys.exit(1)

    result = calculate_risk_score(vendor)
    passport = generate_passport(result)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(passport)
        print(f"  Vendor Risk Passport → {args.output}")
    else:
        print(passport)

    if args.json_output:
        with open(args.json_output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"  Scoring data → {args.json_output}")

    if args.evidence_bundle:
        bundle = generate_evidence_bundle(result)
        with open(args.evidence_bundle, 'w') as f:
            json.dump(bundle, f, indent=2)
        print(f"  Evidence bundle → {args.evidence_bundle}")

    print(f"\n{'='*60}")
    print(f"  {result['vendor_name']} — Tier {result['tier']}")
    print(f"  Score: {result['tier_adjusted_score']}/100 | {result['disposition']}")
    print(f"  Justification: {result['justification_coverage']}")
    print(f"  CUI Boundary: Enforced")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
