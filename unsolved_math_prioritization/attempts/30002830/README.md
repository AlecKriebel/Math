# Ueno birational modifications, 30002830

**Unsolved, 5/5. Scoped partial results only.** This checkpoint does not prove
rationality or nonrationality of the total space X_{4,6}.

## Reading order and controlling version

Read `audit_corrected_v2/AUDIT.md` and `audit_corrected_v2/CONTROLLING_SCOPE.md`.
The corrected v2 audit controls this checkpoint. The frozen `author/` and
`audit_original_v1/` trees are preserved byte-for-byte as historical evidence.
The original audit's human-review attributions are false and withdrawn.
The audit is AI mathematical review, not human review or peer review.
`audit_corrected_v2/METADATA_CORRECTION.json` and its exact `.diff` preserve
the attribution-only correction history. No mathematical statement, code,
or exact check result was changed by that correction.

Historical statements that independent audit or publication is pending,
that no remote writes occurred, and the author's recommended queue label
describe the original freeze. `release_status.json` is the current disposition:
scoped AI audit pass, unsolved, five of five routes used. The parent reading
guide does not change any historical frozen file.

## What was retained

- A rational covering fourfold with map to X_{4,6} of exact degree three.
  Cyclic descent remains unresolved; this is not a rational inverse.
- Degree-two and degree-24 maps from X_{4,6} to rational quotients. These
  maps point in the opposite direction from the degree-three cover.
- A K3 obstruction for the specified relative generic surface only.
- Minimum Newton lattice width two, obstructing unimodular monomial
  projections of degree one only.

The shared corrected open and q+2 factor remain required. None of the
relative or monomial obstructions is a total-space nonrationality proof.
Adjacent [problem 30002829, draft PR #697](https://github.com/AlecKriebel/Math/pull/697)
has a separate broader target. Its row and attempt budget are unchanged.
Method-specific overlap is disclosed; no novelty or exact-duplicate-absence
claim is made.

## Reproduction

With Python 3 and SymPy 1.14.0, from any working directory:

    python /path/to/30002830/verify_release.py
    python -O /path/to/30002830/verify_release.py

The read-only wrapper checks the exact allowlist, frozen bindings, complete
attribution-only delta and controlling status, then reproduces 73 author
checks (including 11 negative controls) and 120 independent checks (including
10 negative controls). It also reproduces the 14 corruption controls in
temporary copies under optimized Python. These computations supplement
the written mathematical arguments; the geometric dependencies are not
computer-formalized and a check count is not a proof certificate.

The live target returned HTTP 403. The complete imported statement and prior
AI report remain uninspected; raw corpus hashes were not recomputed. No
global-current-openness or priority claim is certified. Source metadata
records the actual retrieval and inspection history without including source
PDFs, extracts, screenshots, raw datasets or private coordination.

The queue patch changes only ID 30002830 Status and Turns. Existing Findings,
Chat, DOI, adjacent rows, all other bytes and the stale embedded header stay
unchanged. No queue regeneration, merge, release, DOI or outreach is part of
this checkpoint. Remote delivery and CI availability are verified separately;
absence of CI is not a pass.
