# Final independent variational-family audit of PR #22

**Verdict: PASS as a known published negative answer to the literal AIM target.**
No required mathematical or source-scope repair was found. This is acceptance
of a source-status correction and verification of a known counterexample, with
no new discovery and no resolution of a conjecture repaired by adding formal
self-adjointness. Assigned audit completion: 100%.

Reviewed head: `5dff69d1f25ac585a87bd8c71bc9d9c136e8c13c`.
Reviewed candidate `SOURCE_STATUS.md`:
`b6d39596acb84613b15c43c5a9f6d2382bbd4826348638398d793fab4cbc7463`.
The two records are 20002011 and 20002052. All 15 original snapshot files were
individually hashed and compared byte for byte with their Git blobs at that
head. All remained unchanged after the checks.

## Independence and evidence order

The complete candidate and exact source records were read first. I fetched and
read the complete 30-page AIM source, including the relevant density conventions,
the original conjecture and its reprint, and the separate divergence questions.
The independent universal derivation was saved in
`CRITERION_AND_RECONSTRUCTION.md` and sealed at
2026-10-01T19:03:51.632362+00:00 before opening or executing old code, old detailed
reviews, or root/sibling mathematical findings. The seal's input list and honest
independence qualification are recorded in `FIRST_PASS_SEAL.json`. Allowed
candidate/manifest inputs contained high-level pass assertions; these were not
used as evidence. No sibling mathematical report was used at any later stage.

Only after that seal did I read the old diagnostics, examine the later primary
sources, reproduce the original scripts, and write new adversarial controls.
The initial reconstruction and its three sealed supporting artifacts were not
rewritten to incorporate later outcomes.

## The literal target and necessary condition

[AIM 2003](https://aimath.org/WWN/confstruct/confstruct.pdf), printed pp. 16–18,
uses density-valued invariants and requires the primitive identity at every
background metric and every conformal direction. Conjecture 1 on p. 17 and
Problem 30 on p. 28 have the same hypothesis and conclusion. The source does
not impose variational symmetry as a hypothesis. The adjacent statements
allowing arbitrary divergences are separately numbered and are different targets.
The typeset pages 17 and 28 were independently rendered and inspected.

For any conformal gradient density H, the two-variable functional
`F(exp(2s phi+2t psi)g)` has symmetric mixed partials. Consequently

`integral phi D_g H(psi) = integral psi D_g H(phi)`.

The directions phi and psi are fixed affine coordinates on the conformal class.
There is no derivative of either direction in this computation. The critical
Q-density has density linearization equal to the self-adjoint critical GJMS
operator; AIM pp. 12–14 states these properties and the transformation law.
A pointwise conformal invariant density has zero linearization. Hence the
asserted decomposition imposes formal self-adjointness on the linearization of S.
The condition is necessary without any inverse-variational theorem, locality
converse, or claim that every divergence has a primitive.

## Recalculation of the density and its adjoint

In dimension six, with the submitted positive-trace Laplacian convention, put
`B=|P|^2` and `T psi=P^{ij} Hess_ij psi`. Independently differentiating the
Schouten tensor, two inverse metrics in B, the Laplacian, and the volume form
gives the complete density operator

`A psi = -4 div(B grad psi) - 2 Delta(T psi)`.

In particular the `6 psi dV` variation was included before cancellations. The
operator `-4 div(B grad)` is symmetric, and integrating T by parts twice gives

`T^* h = nabla_j nabla_i(P^{ij}h)
       = T h + 2 <dJ,dh> + (Delta J)h`.

This uses the contracted Bianchi identity and does not commute tensor covariant
derivatives improperly. The skew operator is therefore exactly

`A-A^* = -2(Delta T-T^* Delta)`.

Adjoints in these formulas use the fixed background volume. The conformal
derivative already contains the measure variation, so varying that measure again
when forming A's adjoint would double count it.

For the exact conformal coordinate calculation, if
`g=exp(2f)delta` and `C=sum_ij P_ij^2` in Euclidean components, then

`S = [Delta_0 C-4 <df,dC>-4 C Delta_0 f] dx`.

The three active coordinates in the original author's program are legitimate:
its Schouten matrix is still six dimensional, and the metric and functions near
the witness are independent of the remaining coordinates. The full coordinate
operator is adjointed with respect to dx; the intrinsic scalar operator has
the corresponding volume factors. At the witness `f(p)=0`, those two reported
values agree. The new controls also test the complete operator at nonzero lower
jets, where such factors cannot simply be discarded.

## Cubic geometry and the closed integral witness

For a cutoff of `f=x1 x2 x3` at the center p of a coordinate ball in the flat
six-torus, `f=df=Hess f=0`. Thus the metric's first jet and Christoffel symbols
vanish at p, while `P=0` and `nabla_k P_ij=-f_ijk`. Because psi is the same
local cubic, its first two jets also vanish. Differentiating its covariant
Hessian gives ordinary third derivatives at p: the connection terms multiply
vanishing lower scalar jets. Raising P's indices introduces no first metric-jet
term there.

The cubic is harmonic and
`J=-exp(-2f)(Delta_0 f+2|df|^2)` vanishes through degree three. Hence `dJ=0`.
Expanding the product in `Delta(T psi)` leaves only the mixed first-derivative
term, namely `-2 sum_ijk f_ijk^2=-12`. The six ordered permutations of 123
have value one. The three terms of `T^*(Delta psi)` vanish because they contain
P, dJ, or `Delta psi`, respectively. Consequently

`(A-A^*)psi(p)=24`, with `A psi(p)=24` and `A^* psi(p)=0`.

No periodic polynomial is used globally. Smooth cutoffs supply the same local
jets on a closed oriented torus, and `exp(2f)` is a globally smooth positive
metric factor. Continuity makes the defect positive on a neighborhood. A
nonnegative, nonzero smooth phi supported there gives a strictly positive
integral asymmetry after legitimate closed-manifold integration by parts.

The density is a natural parity-even polynomial curvature contraction of scalar
weight -6: two curvature factors and two derivatives have exactly critical
weight. Its integral is zero for every metric on every closed six-manifold.
Thus it meets even the intended polynomial critical-weight hypothesis. The
construction is conformally flat and does not depend on nonpolynomial naturality,
an open manifold, a boundary term, or a merely pointwise non-realizable curvature
jet. A single such realization defeats the literal universal assertion.

The Ricci identity is `|Ric|^2=16|P|^2+14J^2`. Directly varying `integral J^3dV`
gives `-3 integral psi Delta(J^2)dV`, so `-(1/3)J^3dV` is a local primitive for
the latter density. Its adjoint defect is zero. The Ricci-norm variant therefore
has defect `16*24=384`. Laplacian sign changes reverse these witnesses' signs,
without restoring symmetry.

## Published source verification and exact boundary

[Branson 2005](https://www.dml.cz/bitstream/handle/10338.dmlcz/701742/WSGP_24-2004-1_3.pdf),
printed p. 34, Proposition 13 and Conjecture 14, explicitly restricts the repaired
statement to formal self-adjointness. Printed p. 40, equations (53)–(54), exhibits
a nonzero skew linearization and identifies the divergence
`nabla^c(P_ab|c P^{ab})` as a proportional representative. Metric compatibility
makes this half the submitted positive-trace Laplacian density. The text also
states that the distinction persists for conformally flat metrics. I checked
the actual rendered pages 34 and 40 and the surrounding definitions and
six-dimensional calculations. The bibliographic title page says 2005, despite
the conference-volume filename containing 2004.

[Case–Lin–Yuan, arXiv:1711.05579v1](https://arxiv.org/pdf/1711.05579v1),
Section 2, gives the conformally variational framework. Section 8.4, Lemma 8.2
and (8.15), printed pp. 31–32, independently corroborates the J-cubed gradient
calculation and critical Delta(J^2) variational term. The actual fetched PDF is
v1 dated 15 November 2017; no claim about an uninspected journal edition is made.

[Alexakis 2011](https://sigma-journal.com/2011/019/sigma11-019.pdf), Theorem 1.1,
printed pp. 1–2, permits arbitrary natural divergences in the polynomial critical
class. The present example already is such a divergence. Nothing here challenges
that theorem or establishes the present status of a repaired general conjecture.

Full foreign PDFs, extracted text, and rendered pages remain excluded in tmp.
The first-party source ledgers contain exact byte counts and SHA-256 hashes.

## Reproduction and distinct falsification controls

Both original programs were copied and executed without modifying the original
snapshot. With `/usr/bin/python3` 3.9.6 and existing SymPy 1.14.0, the original
25-check and 21-check result receipts reproduced byte for byte. Their hashes
are recorded in `REPRODUCTION_RESULTS.json`. The written proof is separately
needed for naturality, mixed-variation necessity, and closed-manifold localization.

`fresh_variational_controls.py` passed **3,391 exact assertions**, without
sampling or tolerances. Its materially distinct challenges are:

* The complete 56-dimensional homogeneous cubic-jet space, including trace
  terms, not just additional harmonic examples. For arbitrary cubic tensors A
  and B, the covariant product rule derives defect
  `4(<A,B>-<tr A,tr B>)`. Exact basis checks and trace projection show the
  resulting quadratic form has inertia 50 positive and 6 negative directions.
  Full coordinate derivatives and adjoints separately verify positive, zero,
  and negative nonharmonic examples. In particular `x1^3` tested against itself
  gives zero defect, while tested against `x1 x2^2` gives -48; omitting the
  Bianchi trace terms would fail these controls.
* Exact equality of the full coordinate density variation and the intrinsic
  operator formula at a background with nonzero first and second jets. This
  challenges measure and connection simplifications valid only at the cubic
  point.
* An independent full-coordinate Euler derivative of `-(1/3)J^3dV`, followed
  by direct coefficient-adjoint verification that the resulting Delta(J^2)
  density operator is self-adjoint at that same nonflat-jet background.

The finite controls challenge the derivation. The universal reconstruction and
closed integral witness establish the counterexample; finite checks are not
presented as a general proof by sampling.

## Administrative advisory and disposition

The frozen `provenance.json` has `shared_queue_modified=false`, whereas the
current frozen PR diff explicitly includes QUEUE.md. Preserve that historical
artifact, but current PR scope and
acceptance metadata should correctly acknowledge that both queue rows change.
This is a documentation advisory, not a mathematical repair or a change to the
verified candidate. Do not transfer this verdict to a different mathematical
candidate hash without a fresh binding check.

The defensible result is `already_solved` in the user's convention: the literal
claim already has a published negative answer. The duplicate shares its sole
substantive attempt, so the budget remains 1/5 for the common target. This
assigned validation consumed no new proof-search attempt. A repaired formally
self-adjoint target requires a separate precise source audit; it was not solved
here. No new research paper, preprint, DOI, or tracker entry is warranted for
this source-status acceptance.
