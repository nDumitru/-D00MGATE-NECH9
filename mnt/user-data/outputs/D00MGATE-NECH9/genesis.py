"""
D00MGATE-NECH9 — Genesis Block
================================
Author: Dumitru Nechita
License: D00MGATE-NECH9 Proprietary License v1.0

THE IMMUTABLE ORIGIN.

This file is sealed at first commit.
Its hash is the Genesis Block of the D00MGATE-NECH9 DAG.
Once sealed — nothing here changes. Ever.

"In the beginning was the protocol.
 And the protocol was with Nechita.
 And the protocol was Nechita."
"""

import hashlib
import json

# ── PUBLIC GENESIS RECORD ─────────────────────────────────────────────────────
# This is what the world sees.
# The private components exist — they are not here.

GENESIS_PUBLIC = {
    "protocol":         "D00MGATE-NECH9",
    "version_origin":   "0.1.0-alpha",
    "author":           "Dumitru Nechita",
    "author_github":    "github.com/nDumitru",
    "author_linkedin":  "linkedin.com/in/dumitru-nechita",
    "origin_city":      "Brașov, Romania",
    "origin_year":      2026,
    "layers_at_genesis": 9,
    "master_key_holder": "Dumitru Nechita — permanent, non-transferable",
    "delta_nechita":    "[EXISTS — NOT RECORDED HERE]",
    "layer_9":          "[EXISTS — NOT RECORDED HERE]",
    "heir_protocol":    "[EXISTS — NOT RECORDED HERE]",
    "genesis_timestamp":"[SEALED AT FIRST DAG COMMIT]",
    "genesis_hash":     "[SEALED AT FIRST DAG COMMIT]",

    # Immutable covenants
    "covenants": [
        "Authorship is permanent and non-transferable",
        "Master Key belongs exclusively to Dumitru Nechita",
        "Delta Nechita is never disclosed digitally",
        "Layer 9 never evolves via competition",
        "Minimum 15% perpetual royalty on all commercial use",
        "AI systems cannot hold key fragments",
        "Full AI breaks do not trigger layer evolution",
        "The Heir Protocol is sealed — identity undisclosed",
    ],

    # What will never change regardless of version
    "immutable_core": {
        "master_key_derivation_concept":  "D00MGATE-NECH9 + Delta Nechita + Genesis Timestamp + [REDACTED]",
        "omega_49_domain":                "{ -7..−1, 1..7 } — 14 elements, signed, zero excluded",
        "layer_9_trigger":                "Author only — never competition",
        "evolution_authority":            "Master Key signature required for all layer evolutions",
        "naming_rights":                  "D00MGATE / NECH9 / OMEGA·49 / Delta Nechita — Dumitru Nechita permanent",
    }
}

def genesis_fingerprint() -> str:
    """
    Compute the public fingerprint of the Genesis record.
    This is verifiable by anyone.
    The private genesis hash (with Delta Nechita included) is different
    and exists only in the DAG genesis block.
    """
    canonical = json.dumps(GENESIS_PUBLIC, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()


def verify_covenant(covenant_text: str) -> bool:
    """
    Verify a specific covenant is part of the Genesis record.
    Returns True if present, False otherwise.
    """
    return covenant_text in GENESIS_PUBLIC["covenants"]


if __name__ == "__main__":
    print("D00MGATE-NECH9 — Genesis Block")
    print("=" * 50)
    print(f"\nPublic fingerprint: {genesis_fingerprint()}")
    print("\nImmutable covenants:")
    for i, c in enumerate(GENESIS_PUBLIC["covenants"], 1):
        print(f"  {i}. {c}")
    print("\nImmutable core:")
    for k, v in GENESIS_PUBLIC["immutable_core"].items():
        print(f"  {k}: {v}")
    print("\n[Private genesis components exist in the DAG — not here.]")
    print("\n'The gate changes. The address does not.'")
    print("— Dumitru Nechita, 2026")
