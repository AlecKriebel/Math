# Anisotropic square-lattice RSW: literature resolution

Problem ID **30000859**, row **1835**, source key **OWR1731-004**.
Disposition: **already_solved**, **1/5**. Inspection and audit date: 2026-10-21 UTC.

Björnberg's 2007 anisotropic square-lattice RSW question is resolved, for fixed interior critical parameters, by Grimmett–Manolescu (2013), Theorem 1.3(a), with Definition 1.2 and Equation (1.1). This is a literature-resolution record, not a new theorem or a new proof of the cited theorem.

## Scope

Fix p_h,p_v in (0,1) with p_h+p_v=1. At every fixed integer aspect ratio k≥1, lattice-aligned integer rectangles have positive scale-independent crossing lower bounds, with constants depending on the fixed parameters and k. The acceptance audit explains the finite-scale extension, why orientation bounds do not require rotational invariance, the choice f(n)=n, and a boundary-safe dual-crossing argument for the optional upper bounds.

No uniformity at degenerate endpoints, over all anisotropies or over unbounded aspect ratios is claimed. No claim about Cardy's formula, conformal invariance or critical exponents is made.

## Contents and verification

- SOURCE_GATE.md: authored source match and public citations.
- SOURCE_METADATA.json: public PDF titles, URLs, byte counts and hashes; no source PDF is bundled.
- ACCEPTANCE_AUDIT.md and AUDIT_RESULT.json: authored mathematical acceptance reasoning and disposition.
- verify_integrity.py: package file-integrity checker and tamper self-tests.
- MANIFEST.json: byte counts and SHA-256 digests of all other package files.

From this directory run:

    python3 verify_integrity.py
    python3 -O verify_integrity.py
    python3 verify_integrity.py --self-test
    python3 -O verify_integrity.py --self-test

These are file-integrity and tamper-detection checks, not numerical experiments or mathematical theorem verification. The self-tests operate on temporary copies and leave this package unchanged. The manifest does not hash itself; an independently recorded manifest SHA-256 is the external trust anchor. A party able to replace both the files and the manifest can produce another internally consistent package. No external source retrieval is performed by the checker.

This package excludes copied source documents, dataset contents, private sources, private paths and coordination material.
