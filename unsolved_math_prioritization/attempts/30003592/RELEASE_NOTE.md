# Audited partial checkpoint for problem 30003592

Status: **unsolved**, with five substantive approaches completed. The independent audit accepts the recorded partial mathematics and requires no mathematical correction. Neither this checkpoint nor the audit proves universal rational polyhedrality, produces a nonpolyhedral toric movable cone, certifies novelty, or constitutes peer review.

The 12 original author files remain byte-for-byte unchanged in submission/. The complete nine-file independent audit remains byte-for-byte unchanged in independent-audit/. Their historical audit-pending and no-remote-write fields describe the moments when those packets were frozen. This separate release note supplies the later disposition.

## C1 quotient parameter convention

In the covering-family argument of PARTIAL.md, Approach 2, use

    S = Gr_quot(1,A) x Gr_quot(1,B),

where Gr_quot(1,V) parametrizes one-dimensional quotients of V. The universal quotient line bundles on S produce the rank-two quotient bundle over S x P^1. This removes the ambiguity of writing P(A*) x P(B*) after adopting quotient-projectivization. It leaves the family, numerical class, dominance, and conclusions unchanged. The original notation is preserved as historical input; the audit explains the clarification.

## Scope and known mathematics

All geometric deductions in the notebook concern smooth projective varieties over C. The source's local sentence does not explicitly specify projectivity or a field; no claim is made for the broader literal category. The projective subproblem also remains unresolved in general. The scroll calculation is already covered by Fulger and Lehmann's published projective-bundle results. No first-priority claim is made for the other partial deductions.

## Replay and integrity

From this directory run:

    python3 verify_release.py

This verifies the exact publication allowlist, all frozen hashes, and the original 1,877 controls. It reconstructs the authored-only input ZIP for the full independent replay, which passes 2,003 controls: 1,961 mathematical controls and 42 integrity/replay checks. The mathematical arguments themselves are reviewed in independent-audit/AUDIT.md; check counts are not a confidence score or a formal proof of geometry.

The reproducible ZIP uses fixed metadata and Python DEFLATE compression. An existing byte-identical original ZIP may instead be supplied with --archive PATH. A compression-byte mismatch is an integrity-reproduction issue, not evidence against the mathematics.

RELEASE_MANIFEST.json excludes only itself to avoid circular hashing. Extra or missing files, nested extras, symlinks, and altered bytes are rejected. The final-layout verifier is supplementary and does not edit either frozen packet. No third-party PDF, full-text extraction, corpus, private source, or private coordination inventory is included.

The accompanying queue change modifies only this problem's Status to unsolved and Turns to 5/5; its Findings cells, all other rows, and the header are preserved. The draft PR is a research checkpoint, with no merge, release, DOI, or outreach implied.
