# Exact sources, normalization, and literature scope

Checked 2026-09-30. The theorem in CANDIDATE.md is a candidate under separate
review. No historical novelty claim is made.

1. **Ohtsuki (editor), Problems on invariants of knots and 3-manifolds**,
   Geometry & Topology Monographs 4 (2002), Section 2.4, pp.403–405.
   [Full primary PDF](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).
   Conjecture 2.11 on p405 is the exact target, for every knot and every
   diagram with n crossings. The normalization on p403 is additive,
   mirror-odd v3 with right-trefoil value 1. Both pages were visually checked.
   The exact target is distinct from the broader joint-range question,
   Problem2.10 / related record10400032.

2. **Polyak and Viro, Gauss Diagram Formulas for Vassiliev Invariants**,
   International Mathematics Research Notices 1994, no.11, 445–453.
   [Primary scan](https://www.math.stonybrook.edu/~oleg/math/papers/1994-Polyak-Viro.pdf),
   [DOI](https://doi.org/10.1155/S1073792894000486).
   Theorem2, equation(5), p448 is the imported unbased formula. The original
   diagram was inspected at high resolution. The candidate makes its cyclic
   endpoint orders, arrow directions, signs, and normalized subdiagram counts
   explicit. Section2 defines the crossing signs and arrows from overpass
   to underpass.

3. **Willerton, On the First Two Vassiliev Invariants**,
   Experimental Mathematics11 (2002), 289–296.
   [Primary preprint](https://arxiv.org/abs/math/0104061v1).
   Section1 fixes v3 and gives its Jones-derivative formula. The
   two-strand torus evaluations establish the known odd-crossing sharpness.
   The paper's general coarse bound does not supply the requested sharp
   constant. Its finite knot tables are supporting historical observations.

4. **Chmutov, Duzhin, and Mostovoy, Introduction to Vassiliev Knot Invariants**.
   [Author-hosted full manuscript](https://www.math.cinvestav.mx/~mostovoy/cdbook/cdbook-as-submitted.pdf).
   Section13.1.1 defines the pairing by summing subdiagrams. Sections13.4.2
   and14.3 give formula and bound context. The book uses j3, the coefficient
   of h^3 in J(exp h), so j3=-6v3 in the present convention.
   That scale must not be suppressed when importing a numerical bound.

5. **Zhang, Gauss diagram formulae for Vassiliev invariants from Kauffman
   polynomial**, arXiv2306.01591v1 (2023).
   [Full primary preprint](https://arxiv.org/abs/2306.01591v1).
   Section3 defines the subdiagram pairing. Remark4.1 on pp19–20 explicitly
   expands unbased patterns into based ones, displaying the order-three
   cyclic multiplicity of the triangle. This is a convention check, not a
   new formula claimed by this package. Zhang's arrows use the opposite
   over/under convention; the candidate follows the original PV convention.

6. **Sukuse Abe, On finite type invariants of knots and 3-manifolds**,
   2015 doctoral thesis, Theorem3.10.
   [University repository PDF](https://sucra.repo.nii.ac.jp/record/10402/files/GD0000751.pdf).
   This states the bound for torus knots only. The associated paper is
   *On Vassiliev Invariants of Degrees2 and3 for Torus Knots*,
   Tokyo Journal of Mathematics38 (2015), 331–337,
   [DOI](https://doi.org/10.3836/tjm/1452806043).
   Its restricted scope is also confirmed by
   [the author's publication list](https://www.omu.ac.jp/orp/ocami-en/people/researchers/pdf/researcher/2020/Abe/list.pdf).
   This known special case is not used in the universal proof.

## A discrepancy in the original older-bound display

Equation(11) on Ohtsuki p403 prints
floor(n(n-1)(n-2)/15). Taken literally for all n, that is incompatible with
the normalization and examples in the same source: it gives 0 at n=3
where the right trefoil has v3=1, and 4 at n=5 where T(2,5) has v3=5.
No corrected version or unstated range is assumed here. The display is
not used anywhere in the candidate argument. The exact Conjecture2.11
inequality on p405 is consistent with both examples.

## Search and attribution limits

The pinned full record and earlier report were read before the attempt.
The earlier report supplied no verified complete proof and was marked as
unsourced triage. Repository branch, path-history, queue/state, and all-state
PR checks found no previous attempt of this target.

Searches included the exact conjecture, Willerton crossing-number bounds,
degree-three Gauss diagram formulas, and tournament/cyclic-triangle terminology.
The primary literature located above does not establish priority for the
present combination. Failure to locate an earlier full proof is not a
certificate of novelty or of the universal conjecture's current open status.

The Polyak–Viro identity, the tournament outdegree count, and the torus-knot
evaluations are established ingredients. The candidate's proposed contribution
is their explicit domination argument for the full target. No outside contact
or source-PDF redistribution is part of this package.
