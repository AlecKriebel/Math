# Distinct differences of three-term progressions: verified prior partial resolution

Problem 2487 / EP-1097. Review date: 2026-10-06 (UTC).

## Result

The proposed uniform O(n^(3/2)) bound is false by prior work. The open-ended question of the optimal asymptotic order is not solved here. This is a source audit and an authored exposition of known mathematics, with no novelty claim and no improved exponent.

The original question is problem 89:27 on page 14 of the 1989 Western Number Theory problem list [1]. The scan concerns n distinct integers and three-term progressions with distinct common differences. There is no prescribed ambient interval. The suggested exponent is 3/2. Our conventions exclude difference zero and count signed differences; counting only positive differences divides their number by two, so neither the exponent nor the negative answer changes.

## Verified mathematical content

Let D(A) be the nonzero integers d for which x, x+d, x+2d all lie in A for some x. Let F(n) be the maximum of |D(A)| over integer sets of size at most n. Let M(N) maximize the number of restricted differences |U -_G V| when U,V are finite integer sets, G is a subset of U x V, and |U|, |V|, |U +_G V| are at most N.

The exact comparison

    F(n) <= M(n),       M(N) <= F(3N) + 1

shows equality of the infima of their uniform upper-bound exponents. PROOF.md gives both maps over integers, handles zero and sign, and includes a self-contained weak refutation obtained by tensoring Ruzsa's classical three-point seed. That illustration is prior mathematics, not a new bound.

Katz and Tao's Theorem 1.1 [2] gives M(N) <= N^(11/6), hence F(n) <= n^(11/6). Lemm's Theorem 2.1 [3], together with its entropy-to-finite-set construction, gives a lower exponent strictly above 1.77898. Lemm's seed has integer coordinates; high-dimensional integer examples can be embedded in Z using sufficiently separated digits. These are theorem-dependent literature conclusions, not a numerical optimization rerun.

Georgiev, Gomez-Serrano, Tao, and Wagner [4], Section 6.15 / PDF page 41, report only an eighth-decimal improvement to this three-slope lower bound. Tao [5], Section 1.1, separately records the same displayed interval. Neither the four-slope lower bound 1.668 nor the many-slope upper bound 1.67513 applies to this three-term problem. We deliberately do not invent additional digits of the lower endpoint.

Thus the verified literature bounds for the exponent gamma are

    1.77898 < gamma <= 11/6.

This statement concerns the exponent threshold; it does not assert that F(n) equals n^gamma, that an endpoint big-O estimate follows from an infimum, or that the full order including logarithmic factors is known.

## What remains open

An improvement of the uniform upper exponent needs a fixed epsilon > 0 and a theorem bounding |U -_G V| by O(N^(11/6-epsilon)) under only the three cardinality conditions above. An improved construction must raise the restricted-difference exponent. Determining the exact exponent, and then the sharper order if applicable, remains unresolved by the sources verified in this review.

No incidence argument establishing exponent 3/2 can be correct without additional restrictions: it is contradicted by the prior constructions. We stop at the prior-resolution finding rather than spend research attempts on that false target.

## Retrieval and search limits

The exact-ID inherited record and report were read in full before mathematical work. The separate report is empty; the inherited background is literature triage, not a prior substantive research attempt. Supplied statement and full-pair hashes match.

Direct retrieval of unsolvedmath.com/problems/2487 and the live Erdős tracker returned 403. Search-indexed first-party history, LaTeX, and discussion pages corroborated the statement and Chan's reduction, but are not represented as a successful fresh live-page inspection. The original 1989 scan was downloaded and its page 14 visually inspected. Primary PDFs [2], [3], and [4] were downloaded, hashed, text-inspected, and their relevant pages visually inspected. Source files are not included in this package.

Bounded repository searches on AlecKriebel/Math returned no matches for 2487 or EP-1097 in code and issues, for 2487 or 1097 in commits, and for 2487 in branches. This is not a proof that no prior work exists in all repository history or unpublished branches.

A bounded current-literature pass also inspected the abstracts of [6]-[8]. Their stated results concern, respectively, fractal/Fourier hypotheses, forbidden differences in finite vector spaces, and the normalized complete sumset/difference-set problem. None supplies a settlement of the unrestricted three-slope question in its abstract. These manuscripts were not fully audited. Absence of a located later result is not evidence of novelty or a complete literature census.

## Classification and scope

- Main problem: open; no solution claimed.
- 3/2 subquestion: disproved by prior work.
- Local outcome: verified prior partial resolution.
- New substantive research approaches: 0 of 5.
- Numerical searches or experimental proofs: none.
- Executable verifier: none; the mathematical argument is in PROOF.md.
- Publication and queue changes: not performed by this review.

See REFERENCES.md and VERIFICATION_METADATA.json for citation and verification details.
