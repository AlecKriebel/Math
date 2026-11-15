# Verification report

**Decision: the candidate gives a complete proof of the mathematical problem.**
The precise linked catalogue asks the equality question for n>2; the proof
settles it for every n≥1. The bounded priority search found no earlier general
resolution. This is an unrefereed result, with independent AI audits, not
external peer review or formal proof-assistant certification.

## Proof obligations

| Obligation | Checkable mechanism | Outcome |
| --- | --- | --- |
| Exact open-problem match | Live catalogue, OWR p. 2908, FPS Theorem 1.1 p. 499 | Exact match |
| Extreme-point exhaustion | Relative separability, finite-dimensional extreme-point theorem, dense convex union contains interior | Valid, even if extreme points are not closed |
| New simplex partition | Strictly visible facet pyramids, vertex-only facet partitions, earlier simplices retained | Valid in all n≥1; no local finiteness needed |
| Null remainder and integrations | Convex boundary is null, countably many simplex boundaries, bounded integrands | Valid; all series converge absolutely |
| Simplex second moment | Barycentric monomial integration, FPS Lemma 3.2 | Exact |
| Nonnegative deficit | Volume-weighted variance identity | Exact identity (4) |
| Equality forces one simplex | Positive weights, common centroid in every simplex interior | Valid; no limiting loss |
| Converse | All vertex norms r in the simplex identity | Valid |
| Alternative strictness check | Two retained simplices give positive bound (5) | Independent finite-approximation proof |

No mathematical gap remains in this statement after the recorded audits.
The retained-pair estimate is a body-dependent certificate of strictness,
not a claimed uniform stability rate for distance from the simplex class.

## What changed from the candidate

The mathematical mechanism is unchanged. The manuscript makes finite stopping,
strict visibility, the apex case, bounded series, and the null remainder
explicit. It corrects the last sentence's possible implication that dimension
two requires regularity: a nonregular triangle with nonzero centroid attains
the strengthened bound. The weaker bound without the centroid term has the
additional equality condition g_K=0. Historical wording is clarified as ≥r.

## Computational check

`python3 verification/verify.py` and `python3 -O verification/verify.py` return
identical results: **298 checks in 18 cases, all passed**, using exact rational
arithmetic. The result is preserved in `output/verification.json`.

The implementation expands affine coordinate polynomials and integrates them
over the standard simplex. Polygon edge integrals separately check shell
volume and moments, exact orientation checks verify containment and disjoint
interiors, and equality/strictness cases cover dimensions 1–6. The code also
checks the retained-pair lower bound. These are algebraic and finite geometric
sanity checks; they cannot replace the proof of the infinite-body statement.

## Priority and limits

The bounded audit covers the original report and journal paper, four forward
citations found across citation indexes, author bibliographies, and searches
for equivalent formulations. No earlier resolution was found. Neither this
search nor the catalogue's Open label excludes unindexed or unpublished prior
work. The inequality, simplex formula, and polytope equality classification
are explicitly credited to FPS. No new-triangulation priority claim is made.

See `geometric-audit.md`, `independent-proof.md`, `final-manuscript-audit.md`,
`source-match.md`, and `priority-independent.md` for detailed evidence.

## Additional preprint review cycle

Two fresh adversarial subagents completed sequential reviews on 23 September
2026 without reading earlier review conclusions. Round 1 began with the
countable partition; round 2 began with a retained finite witness and its
limit. Both found zero actionable mathematical or preprint-presentation issues.
The manuscript, PDF, verifier, and version are unchanged. Two optional
explanatory expansions were judged unnecessary for this concise preprint;
the details and source-access limitation are recorded in the
[readiness disposition](preprint-readiness.md), with links to both full reports.
