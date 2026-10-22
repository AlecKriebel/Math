# Planar multiple-cover thresholds: audited partial results

Problem 30001887 / OWR-11136-013, rank 708. Publication checkpoint: 2026-10-05 UTC.

**Unsolved after five of five substantive approaches.** Independent adversarial audit: **pass with scope limits; no required correction**. This draft preserves the author packet and independent audit byte for byte. It supplies conditional theorems, special cases, and rigorously checked failures of proposed inferences. It does not claim a complete proof, counterexample, verified prior resolution, novelty, or global present-day openness. Estimated completion toward a complete unrestricted resolution: **0% established**; the five-approach investigation and its independent audit are complete.

## Start here

- [Original mathematical dossier](original_author/PROOF.md)
- [Independent audit and exact quantifier checks](independent_audit/AUDIT.md)
- [Five approaches and remaining barriers](original_author/APPROACH_LOG.json)
- [Source scope](original_author/SOURCES.md) and [independent source checks](independent_audit/source_checks.json)
- [Publication verification](PUBLICATION_VERIFICATION.json)

The frozen author's statements that the independent audit is pending, and the frozen packets' statements that no remote publication occurred, describe their historical preparation checkpoints. They are preserved rather than silently rewritten. The current audit disposition is above and in independent_audit/results.json.

## Exact target and strongest retained control

The recovered primary OWR question concerns arbitrary indexed families of translates of one fixed planar set covering the **whole plane**. It does not assume point-finiteness, local finiteness, boundedness, convexity, or openness. The questions whether finite m_2(P) implies finite m_3(P), and whether finite thresholds grow linearly with k, remain unresolved by this investigation.

Every finite hypergraph can be encoded at finitely many witness points by translates of an open, unbounded planar set P for which **m_k(P)=1 for every finite k**. The whole-plane proof works for arbitrary indexed covers, including uncountable families and repeated translates: horizontal translation coordinates must be unbounded below, allowing a countable cofinal subsequence to be split cyclically among all k colors. The distant-half-plane method is credited to the 2013 survey, not claimed as a new discovery. This construction explains why a finite incidence obstruction cannot automatically become a whole-plane counterexample. It gives no corresponding bounded or convex example.

Other retained results have their hypotheses explicit: hereditary discrepancy gives a linear finite-edge threshold; shallow subcovers give repeated decompositions; finite intervals and point-finite congruent strips admit special bounds; random coloring retains its constraint-count parameter; finite-type and compactness arguments do not erase their extra hypotheses.

**Balancing-control precision:** the one-below-threshold test shows only failure of a conservative floor lower bound. It is not an optimality certificate and does not prove that a better coloring is impossible.

## Source and evidence limits

The primary OWR formulation was inspected. The exact unsolvedmath page returned HTTP 403, and the raw AI corpus record was not inspected. The independent audit freshly downloaded all five cited public PDFs and matched each recorded byte count and SHA-256. Those matches do not extend the explicitly recorded inspection scope. In particular, the 2024 source certificate was not independently recomputed, and the 2026 note's later probabilistic proof and appendices were not audited. The 2026 note's public manuscript status is reported without a journal-acceptance claim.

Only authored mathematics, audit text, code, finite-control results, and public verification metadata are included. Source PDFs, extracted source text, images, raw records, and private coordination files are excluded. Finite controls validate their stated instances and arithmetic; they are not universal geometric proofs.

## Portable verification

From any working directory, run Python 3 on this folder's verify_publication.py. It uses only the standard library, checks immutable author/audit manifest bindings and the publication file inventory, then runs both original and independent controls in separate empty temporary working directories. Both stdout streams must match the frozen JSON bytes exactly. Use --check-only for integrity checks without the finite-control replays.

The publication report records actual corruptions applied to disposable copies and rejected by the integrity checker. The original files are never altered by these tests. PUBLICATION_MANIFEST.json lists all other files in this attempt folder with SHA-256, Git blob SHA-1, and byte counts. The immutable manifest hashes are additionally pinned in verify_publication.py.

## Repository scope

The queue update changes only this row's Status to unsolved and Turns to 5/5. Findings, Chat, DOI, every other row, and all other bytes, including the pre-existing embedded header, are preserved. No queue regeneration, merge, release, DOI, or outside outreach is part of this draft.
