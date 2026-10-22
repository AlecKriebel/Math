# Research report: AIM-ALGEBRAIC_GEOMETRY-0276 / 20000276

Date: 2026-10-05. Queue rank at selection: 757.

## Exact target and source limitations

The imported canonical record identifies AIM's 2011 workshop *Relating test
ideals and multiplier ideals*, section “Characteristic p>0 invariants,”
Problem 11.2. The target is whether `lim_m m fpt(I_m)` exists for a graded
sequence of ideals in a ring R. The supplied title refers to the prior
partial results, rather than narrowing the original question to Noetherian
filtrations or monomial ideals. This is not a colength, volume, multiplicity,
finite-generation, or realizability question.

The record gives no explicit regularity, locality, F-finiteness, nonzero-ideal,
or descendingness condition. Its stated comparison is with log canonical
thresholds. This packet does not manufacture missing primary hypotheses.
The standard regular-local reading used by the prior report is stated as a
separate exact theorem in `PROOFS.md`. The unrestricted F-pure-ring reading
has a separately proved counterexample.

Fresh retrieval of the requested [catalog page](https://www.unsolvedmath.com/problems/20000276)
returned HTTP 403. The [AIM primary problem page](http://aimpl.org/testandmultiplierideals/1/)
and its HTTPS counterpart were unavailable (502/timeouts). No access control
was bypassed. The current [AIM problem-list index](https://aimath.org/problemlists/)
links this workshop, and the [official workshop page](https://aimath.org/pastworkshops/testideals.html)
confirms August 8–12, 2011 and the organizers Karl Schwede and Kevin Tucker.
Neither page verifies Problem 11.2's missing ring assumptions. Therefore the
exact imported wording and location have corroborated provenance, but the
full original problem page has **not** been independently re-read here.

## Mathematical advance over the imported prior report

The complete imported report was inspected before the proof attempt. It
already had the following correct partial mechanisms in the regular-local
setting: inclusion monotonicity, power scaling, divisibility monotonicity of
`m fpt(I_m)`, the supremum/limsup identity, a crossing-index formula,
a Noetherian-descending Veronese squeeze, and monomial Newton-polyhedron
subadditivity. Those are prior work and are not counted as discoveries here.

Its descending-filtration gap is removed immediately: for fixed r and
`k=ceil(m/r)`, one has `I_r^k⊆I_(kr)⊆I_m`. The resulting lower bound tends
to `r fpt(I_r)`, and taking the supremum proves convergence without any
Noetherian hypothesis.

For a general family, the missing step is control of the fixed remainder
factor in `I_r^k I_s⊆I_(kr+s)`. The Frobenius separation lemma supplies that
control and proves `k fpt(I^k J)→fpt(I)`. A finite residue-class argument
then proves the full regular-local theorem. It does not require a reciprocal
product inequality, convexity of mixed test-ideal regions, or a
threshold-preserving Groebner degeneration.

The singular example shows why specifying the ring is substantive. It has
all positive family terms nonzero, contains nonzerodivisors, has a finitely
generated Rees algebra, and has a bounded oscillation. It is not the
zero-ideal degeneracy already present in the prior report.

## Primary literature checked and credited

1. **Blickle–Mustaţă–Smith**, *Discreteness and rationality of F-thresholds*,
   Michigan Math. J. 57 (2008), 43–61;
   [arXiv:math/0607660v2](https://arxiv.org/abs/math/0607660v2).
   The complete PDF was retrieved. Section 2's regular F-finite setup,
   Frobenius flatness/freeness and ideal-root machinery were inspected,
   as were the ordinary and mixed-test-ideal discussions. PDF page 3 was
   visually inspected. These are standard foundational inputs. The present
   proof uses only finite free Frobenius and elementary threshold properties;
   it is not presented as introducing those ingredients.

2. **Mitra Koley and Arvind Kumar**, *F-thresholds of filtrations of ideals*;
   [arXiv:2312.07761v1](https://arxiv.org/abs/2312.07761v1), and
   [Journal of Algebra 693 (2026), 1–35](https://doi.org/10.1016/j.jalgebra.2026.01.012).
   The full **2023 v1** PDF was retrieved and its definitions, standard
   Veronese statement and Theorem 3.15 inspected, with PDF page 11 visually
   checked. The 2026 publisher abstract and bibliographic status were checked;
   the published 35-page full text was not retrieved. Their invariant is a
   crossing-index limit in Frobenius degree. That is a different definition
   from the AIM termwise limit; `PROOFS.md` proves their equality in the
   regular-local setting. The imported bibliography's initials for these
   authors were inaccurate; the names above follow the primary sources.

3. **Alessandro De Stefani and Luis Núñez-Betancourt**, *F-thresholds of
   graded rings*, Nagoya Math. J. 229 (2018), 141–168;
   [DOI 10.1017/nmj.2016.65](https://doi.org/10.1017/nmj.2016.65).
   The publisher PDF was retrieved and Section 3's local/graded F-finite
   F-pure threshold and splitting-ideal conventions were inspected. These
   conventions distinguish the F-pure threshold of a singular ring from
   ordinary Frobenius containment against its maximal ideal. The singular
   counterexample is proved using explicit R-linear maps and annihilators,
   without assuming these two invariants are equal.

4. **Wágner Badilla-Céspedes**, *On F-thresholds of differential power
   filtrations*, [arXiv:2607.09028v1](https://arxiv.org/abs/2607.09028v1),
   submitted July 10, 2026. This later primary source concerns differential
   power filtrations of monomial ideals. Its source-inspection depth is
   recorded in `SOURCE_METADATA.json`. Its existence statement should not
   be substituted for the different arbitrary-family termwise theorem.

Searches included the exact problem title, the AIM workshop identifier,
“asymptotic F-pure threshold,” “F-pure threshold graded sequence of ideals,”
and product-limit formulations. No directly matching published theorem or
attributed prior counterexample was verified in that bounded search.
**This is not evidence of novelty.** No comprehensive MathSciNet/zbMATH
review or expert historical check was performed. The elementary proof may
well be known to specialists or implicit in the general mixed-test-ideal
formalism.

## Actual repository and related-record checks

The repository's root and queue-specific instructions, queue README,
selected row, and related-target index were read. At inspection the row was
queued, 0/5. The complete imported prior report was read from the corpus.
Read-only GitHub code queries for `20000276` and `fpt`, an exact-ID PR query,
and an exact-ID commit query returned no matches. The actual main-branch
attempt directory tree contained no folder matching this ID or filtration
title. A broader PR search returned unrelated filtration uses, which were
not treated as previous attempts at this target. These checks do not prove
that no unindexed branch or differently named artifact exists.
The related-target index did not contain this ID. A corpus search for other
F-pure-threshold targets mentioning graded sequences or filtrations produced
no additional match.

## Disposition and stopping condition

Three substantive approaches were used: the descending squeeze, the
fixed-factor Frobenius argument, and the singular-boundary construction.
The regular-local result and the boundary counterexample are complete
candidate artifacts. Stop proof search early and submit this frozen packet
for fresh independent review. Do not consume two more attempts merely to
fill the five-turn ceiling.

A global `verified_solved` label for the original AIM problem is premature
until the independent audit has checked the mathematics **and** the original
ring/ideal conventions have been established or the statement has been
explicitly scoped. This packet supports the precise claims in `PROOFS.md`;
it does not silently settle arbitrary global, singular strongly F-regular,
or non-F-finite variants. The latter variants are neither asserted false
nor left as claimed counterexamples by the regular-local theorem.
