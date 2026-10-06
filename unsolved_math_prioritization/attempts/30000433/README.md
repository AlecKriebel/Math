# Five-or-six edge-degree triangulations: audited partial results

Problem 30000433 / OWR-1194-002, rank 812. Status: **UNSOLVED, 4/5 approaches**.

## Mandatory reading and operative certificate

Read [the mathematical note](author/MATHEMATICAL_NOTE.md) together with [A1: the complete self-handle quotient certificate](audit/CORRECTION.md) and [the independent audit](audit/AUDIT_REPORT.md). The original author freeze is preserved byte for byte. Its original no-mixed-simplex guard alone does not fully certify the abstract simplicial self-handle quotient. A1 is a mandatory supplement, not an optional refinement. The publication verifier always runs the independent all-simplex check and tests the actual [A1 patch](audit/verify_quotient_guard.patch) on a temporary copy of the original verifier.

A1 finds exactly 12 vertex, 30 edge, and 20 triangle boundary pairs, no unintended simplex identifications, and no collapses. The patched normal and optimized outputs agree with the frozen mathematical result; the old author manifest correctly rejects the changed verifier. Do not present the unmodified author verifier alone as the complete self-handle certificate.

## Accepted scope and remaining gap

The claims concern finite closed abstract simplicial PL 3-manifolds, with balls separately specified. Four approaches establish necessary link/incidence constraints, barriers to pure positive-dimensional stellar subdivisions and degree-restricted single Pachner moves, an octahedral replacement lower bound, and a conditional vertex-star gluing criterion.

The exact convex 600-cell certificate establishes a PL 3-sphere geometrically. Doubled-puncture S3 and self-handle S2 times S1 examples are reproducible controls of known topological types, not new existence families. Each glued example has exactly 20 TCP-violating seam triangles. The universal weak 5/6 and stronger TCP existence questions remain unresolved. The published 5/6* degree-five restriction is different from TCP's degree-six restriction.

No global construction, arbitrary-manifold reduction, counterexample, novelty, priority, human peer review, or formal proof-assistant certification is claimed. Current-status checks were bounded searches, not an exhaustive proof of openness.

## Reproduce

Python 3 standard library only. Run from any working directory:

    python3 verify_package.py --manifest-sha256 PUBLICATION_MANIFEST_SHA256
    python3 -O verify_package.py --manifest-sha256 PUBLICATION_MANIFEST_SHA256
    python3 package_mutation_tests.py

Replace the placeholder with the externally recorded publication-manifest SHA-256. Both replays validate all package bytes and exact archive inventories; match the extracted author and audit trees to their immutable ZIPs; rerun original clean normal/optimized checks, relocated tests, 16 semantic and four integrity mutation rejections per driver; independently reconstruct the mathematics; and apply and replay the actual A1 patch, including four guard-rejection controls. The package mutation driver separately checks that missing or altered A1 material, author-byte changes, archive corruption, and a rewritten manifest are rejected under the external pin. A manifest cannot authenticate itself.

## Frozen archives

- [Author ZIP](archives/EDGE_DEGREE_30000433_AUTHOR_SAFE_FREEZE.zip): 21,187 bytes; SHA-256 b64c3b92a96f180b51d22ddd343e9458fc7181f7d8117d5117a4b6a7215dcdf7. Author manifest: ac8006591dde3c8d85cbf2bc47dcb375f7b572107c159bc9a4118e16b8ed0873.
- [Independent audit ZIP](archives/EDGE_DEGREE_30000433_INDEPENDENT_AUDIT_SAFE.zip): 21,573 bytes; SHA-256 01d37b0a09da4e568444a3121dd103c773a06ae656333b3d3c8cfc8d6c77de6f. Audit manifest: bf2ac5ab05d4235f6a1bf815b14ab438eac2f3b623cf2670bd062b736669b5db.

The package includes authored mathematics, code, audits, results, and public verification/source metadata. Source PDFs, extracts, corpus contents, and private coordination are excluded. Publication is a draft PR; no merge, release, DOI, or outreach is part of this work.
