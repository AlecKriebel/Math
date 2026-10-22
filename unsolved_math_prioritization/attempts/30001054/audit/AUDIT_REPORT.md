# Independent source and mathematical audit

Target: rank 818, problem 30001054 / OWR-2090-003.
Date: 2026-10-06. Gate: **NEEDS_SCOPE_CORRECTION**.

## Decision

The frozen author's unconditional SOLVED_IN_LITERATURE_AFFIRMATIVE disposition is not accepted for the literal four-axiom input definition. The historical affirmative attribution is genuine, but the definition-to-fibration implication has a concrete counterexample. Read SCOPE_CORRECTION.md for the complete finite argument and mandatory replacement wording. This is a definition-level audit finding, with no novelty claim.

## Source verification

Fresh downloads of the EMS report, Habert--Pocchiola manuscript, Goodman--Pollack manuscript, and interval-sequence manuscript all reproduce the previously inspected byte identities. Exact URLs, byte counts, SHA-256 values, pages, and retrieval times are in SOURCES.json. No source PDF or extracted text is distributed in this package.

The original OWR contribution's Question 1 is followed immediately by an affirmative attribution to Habert and Pocchiola on printed p. 2492, continuing on p. 2493. This verifies that the catalog's old open-status summary missed a historical answer. It does not cure the printed input-definition gap documented separately.

Habert--Pocchiola Theorem 49 is the relevant result: preserving only an unmarked double-pseudoline arrangement would be insufficient. Its hypothesis includes the chosen fibration, so the direction-event ordering is retained. The broader mixed pseudocircle setting does not impose a hidden restriction that would exclude genuine simple allowable-interval sequences. It does, however, exclude the weak-axiom witness because its pairwise event data do not form the required arrangement/fibration.

For legitimate fibration inputs, retain the body's index labels, endpoint convention, circular traversal orientation, and chosen phase. Orientation reversal or renaming may transport a realization back to its input labels; neither operation repairs omitted internal events. The OWR convention has i before i' and records the ordered pair after a switch. A tangent is a supporting pseudoline meeting the body; the body stays in one closed side. Each pair receives two internal and two external tangents and a strict separator. General position distinguishes tangent events, while single-swap simplicity alone does not enforce correct multiplicities.

The resulting bodies belong to a real two-dimensional affine topological plane. Under a planar topological model, they are connected and may be taken as topological convex bodies, with compatible pseudoline tangents and separators. This is not simultaneous Euclidean straightening. The separate polygonal-construction request on OWR p. 2551 is not proved here; its shared four-axiom definition is nevertheless directly relevant to scope.

## Publication status

The publisher verifies Luc Habert and Michel Pocchiola, *LR Characterization of Chirotopes of Finite Planar Families of Pairwise Disjoint Convex bodies*, Discrete & Computational Geometry 50, 552--648 (2013), DOI 10.1007/s00454-013-9532-y, published 27 August 2013. The arXiv page describes its version as an accepted manuscript. The checked PDF carries a November 8, 2018 running date; that does not change the publisher's 2013 publication date. All theorem and page references here use the checked manuscript, not assumed journal numbering.

[Publisher record](https://link.springer.com/article/10.1007/s00454-013-9532-y) and [arXiv version record](https://arxiv.org/abs/1101.1022).

## Computational checks

The executable witness confirms all four printed axioms, least period eight, eight genuine adjacent different-body swaps, the half-period identity at every phase, and absence of all four internal switch types. The check passes both ordinarily and under Python optimization.

The rebuilt suite includes 44 CLI controls: normal and optimized baselines, relocation, malformed and duplicate-key JSON, wrong types, endpoint and period failures, bad transitions, a genuine switch-once positive comparison, cyclic shifts, and time reversal. A separate letter-based graph enumeration independently locates the witness among all n=2 primitive eight-term weak-axiom words. It finds 48 rooted words, of which 16 satisfy switch-once and 32 do not; these are not counts of isomorphism classes.

Code certifies this finite obstruction and artifact integrity. It does not formalize the topological representation theorem, prove a realization algorithm, or establish novelty of the definition defect.

## Provenance and replay limits

This is a rebuilt audit package, distinct from the missing original author archive. The initial author archive's declared identity was 9,569 bytes with SHA-256 6f8aa56d3832584a9f687165f57316a04e488d51753f6e844b25e84fd571f89c. The original archive and freeze receipt were inspected before a workspace restoration; their bytes are now unavailable locally. The original ZIP hash is retained from its freeze receipt, not claimed as a fresh or recorded independent ZIP-hash recomputation.

The earlier author verifier run produced PASS for 22 controls including normal, optimized, and relocated checks; its external-PDF checks passed in normal and optimized modes. Those are historical observations, not replayed author-archive checks in this restored workspace. The three supplied full corpora and the target full record were read and hashed earlier; their exact public identity metadata and matches are retained in AUDIT_CERTIFICATE.json. The missing corpora were not silently reconstructed or re-certified as currently present.

A bounded earlier GitHub check searched the repository's default-branch files for the target ID and “double permutation,” and searched matching PRs/issues. It found no substantive prior artifact. This is not an exhaustive history search or a novelty conclusion. No remote repository mutation, publication, or third-party outreach was performed by this audit.
