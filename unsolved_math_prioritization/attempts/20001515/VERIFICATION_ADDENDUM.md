# Verification and source addendum

Dated 2026-10-03 UTC. This addendum supersedes the historical pending-review
and provisional-source qualifications in ATTEMPT_1.md without changing that
frozen mathematical proof. Its SHA-256 remains
`c022afdfe003d0692a032cee48855ddf712de22953b358b895c485215875d8a6`.

## Independent review

The fresh full adversarial review in [audit/AUDIT.md](audit/AUDIT.md) returns
**PASS** for the complete affirmative construction and its exact target.
It independently reconstructs the actual two-skeleton, all cube attaching
maps, all sixteen link triangles, and the reversible presentation changes.
Its programs do not import or execute the author's verifier.

There is no mathematical repair. The complete candidate was obtained in
one substantive attempt, so the recorded result is `claimed_solved`, `1/5`.
The review is an independent internal mathematical audit, not external peer
review, formal proof-assistant certification, or certification of novelty.
The packet makes no first-resolution, virtual-specialness, or minimum-dimension
claim.

## Recovered primary-source identity

The reviewer retrieved these two actual archive captures with ordinary
`urllib.request.urlopen` and default TLS verification:

- [AIM section 5, 28 August 2024 capture](https://web.archive.org/web/20240828224508id_/http://aimpl.org/freebycyclic/5/)
- [AIM section 5, 10 March 2026 capture](https://web.archive.org/web/20260310215532id_/http://www.aimpl.org/freebycyclic/5/)

Both responses were HTTP 200, 25,734 bytes, and had identical SHA-256:
`9dfa1624c5743d114c671ea69201a9ea46fe577e707239e245cc7f22b30b8121`.
Displayed Problem 5.2 and its embedded AIM record give the exact automorphism
a -> a, b -> ab, c -> bcb, attribute the question to Rylee Lyman, and ask for
a geometric action on a CAT(0) cube complex. The record identifier is
`0df1011a6fa8a3c46e2c977b7e12c66f`, revision
`6-d5a22eda9ed96ccdc8327e2e9395bb3e`.

Thus archived primary-source identity is verified. Current live AIM and
UnsolvedMath availability remains unverified: their failed live access checks
in SOURCE_GATE.md are retained. The archived record's CAT(0)-space remark does
not already establish the requested cubulation.

The [official workshop report](https://aimath.org/pastworkshops/freebycyclicrep.pdf)
uses the distinct formula b -> aba, c -> bcb and mentions a three-dimensional
candidate. That discrepancy remains explicit. This proof establishes the
ab,bcb formulation in the two archived AIM captures. It does not establish
priority over unpublished or other existing constructions.

## Reproducible checks

Run from this problem's directory with Python 3 and its standard library:

    python verify.py
    python audit/independent_audit.py
    python audit/independent_algebra.py

The independent geometric program reconstructs the eight square boundaries
and the complete two three-cubes, including actual face and corner maps.
Its result is stored in `audit/independent_results.json`. The independent
algebra results are in `audit/independent_algebra_results.json`.

For portability, the published geometric program's original local five-file
manifest lookup was replaced by a direct check of the unchanged proof hash,
and its paths were made relative to this packet. No incidence, group, or
falsification calculation changed. `INITIAL_WIP_FREEZE.json` retains the five
original WIP hashes examined by the reviewer; the later documentation updates
are intentional. The full audit is preserved unchanged.

Raw archived HTML, HTTP headers, corpus extracts and downloaded PDFs are not
part of this packet.
