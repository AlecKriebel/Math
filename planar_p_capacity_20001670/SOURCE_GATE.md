# Source and prior-attempt gate

Checked 3 October 2026. Problem 20001670, AIM-GEOMETRY-0008, rank 457.

## Exact mathematical target

For `1 < p < 2`, put `q = 2-p` and

\[
 C_p(K)=\inf\{\int_{\mathbb R^2}|\nabla u|^p:
 u\in C_c^1(\mathbb R^2),\ u\geq1\text{ on a neighborhood of }K\}.
\]

The question is whether every compact convex planar set of generalized perimeter
`L` satisfies `C_p(K) >= C_p(I_L)`, where `I_L` is a segment of length `L/2`.
Here `P(K)=int_0^pi w_K(theta) dtheta`, agreeing with boundary length on bodies
with interior and giving twice the length on segments. Translations and rotations
are irrelevant. Capacity scales with degree `q`, and its Brunn--Minkowski
concavity exponent is `1/q`, not `1/p`. The displayed homogeneous capacity at
`p=2` is defined but zero on all compact planar sets; logarithmic capacity is a
different, nondegenerate functional.

The imported catalogue title, "Attainment and a quantitative segment bound for
planar p-capacity," describes an earlier machine-generated partial result. It is
not the original problem. Attainment and a lower comparison factor less than one
do not settle the segment-minimizer conjecture.

## Retrieval and literature

- Exact catalogue URL: <https://www.unsolvedmath.com/problems/20001670>.
  Current web retrieval failed; the cloud browser displayed "This request was
  blocked", HTTP 403. No successful live rendering of the problem is claimed.
- Original AIM item: <http://aimpl.org/symmetrybreaking/2/>, item 2.5. Direct
  retrieval timed out. A hash-verified catalogue copy preserves its statement.
- Independently read official [2024 workshop report](https://aimath.org/pastworkshops/symmetrybreakingrep.pdf),
  page 3, section "p-capacity in the plane." It states the fixed-perimeter
  question, the reduction to triangles, and the remaining needle degeneration.
- Colesanti--Salani, *The Brunn--Minkowski inequality for p-capacity of convex
  bodies*, Math. Ann. 327 (2003), 459--479,
  <https://doi.org/10.1007/s00208-003-0460-7>. This is the underlying concavity
  theorem for `1<p<n`, with homothety as the equality case for bodies.
- Bucur--Fragala--Lamboley, *Optimal convex shapes for concave functionals*,
  ESAIM COCV 18 (2012), 693--711,
  <https://doi.org/10.1051/cocv/2011167>;
  author text <https://arxiv.org/html/1102.1887>. Remark 2.4 states the
  possibly-degenerate-triangle reduction and explicitly leaves the segment
  conclusion open. This primary text was read.
- van den Berg--Gavitone, *On functionals involving the p-capacity and the
  q-torsional rigidity*, Calc. Var. PDE 64 (2025), article 245,
  <https://doi.org/10.1007/s00526-025-03081-8>;
  author text <https://arxiv.org/html/2412.06563v2>. Its parallel-set upper
  bound (Theorem 1) is relevant below; its capacity/torsion optimization
  statements do not resolve the present segment conjecture.

Targeted current searches for planar capacity, perimeter, triangles, segments,
needles and the workshop participants found no later resolution. This is a
bounded literature search, not a completeness or novelty certificate.

## Genuine prior-attempt gate

The live default-branch queue row was queued, `0/5`. Repository searches for the
exact ID and code returned no matching PR or issue; the exact-ID commit search
returned none. All 477 current branch names were checked with no matching
problem branch. The catalogue's supplied attempt is explicitly partial and
machine-generated; it is background evidence, not a prior campaign completion
and not peer-reviewed literature. Research proceeds with a fresh five-turn
budget. Retrieval, review and packaging are not counted as proof attempts.

No claim of a resolved problem, verified novelty, or exact segment-capacity
formula is made.

## Additional primary input found during proof work

Lundstrom--Singh, *Estimates of p-harmonic functions in planar sectors*, Ark.
Mat. 61 (2023), 141--175, <https://doi.org/10.4310/ARKIV.2023.v61.n1.a8>,
author text <https://arxiv.org/html/2111.02721>, was read for Attempt 4.
Lemma 3.1 and equation (1.6) supply the slit-plane homogeneous solution of
degree (p-1)/p; Lemma 2.5 supplies the ordinary flat-boundary comparison.
This input is used to prove a local comparison only.
