# Research log: threshold extension v3

Started: 2026-08-08 (America/Los_Angeles)

No literature search and no external communication were used.

## Scope

Starting from the proved dilute pair--leaf threshold

\[
R_{\rm hyb}=1.5028569127905696\ldots,
\]

search for a genuinely new fitness-independent construction using bounded
weakly coupled gadgets with nonuniform portal loads, correlated satellite
types, or a second-order cancellation.  Every numerical lead must include
the far-field singleton terms and must be reconstructed exactly before it is
treated as a theorem.

## 2026-08-08: invariant reduction of the bounded-gadget tangent

For a fixed connected weighted gadget, the previously derived successful
gate odds can be compressed to three local invariants.  Writing

\[
 A_B={\bar h_B^+\over p},\qquad A_D={\bar h_D^+\over p},
 \qquad K=Z_BZ_D,
 \qquad p=1-r^{-1},
\]

and using the free internal/core scale to set `z=Z_B`, the leaf-eliminated
separator per gadget vertex is

\[
 S(z)={A_DK\over K+z}+(r-1){A_Bz\over1+z}-r.             \tag{1}
\]

Thus portal loads affect the first-order feasibility only through `K`,
while the isolated gadget supplies `A_B,A_D`.  This reduction keeps the
ordinary singleton subtraction `-r`; omitting it is exactly the kind of
far-field error that produced earlier false leads.

For `K>1`, if

\[
 a=\sqrt{(r-1)A_B},\qquad b=\sqrt{A_DK},\qquad a<b<aK,
\]

the unique interior maximum is

\[
 \max_{z>0}S(z)=a^2+{(b-a)^2\over K-1}-r,               \tag{2}
\]

at `z=(aK-b)/(b-a)`.  Otherwise the supremum is at an
endpoint.  These formulas will be verified symbolically and used as the
hostile search objective.

## 2026-08-08: fully absorbing gadget screen

- Corrected the discovery objective to maximize the affine separator itself,
  not only balance against ordinary leaves.  This is necessary because a
  Bd-special gadget with negative dB coordinate could still improve the
  convex cone when mixed with a dB-special pair.
- Screened every connected unweighted gadget through six vertices with
  arbitrary portal loads, selected weighted supports through order six, and
  star gadgets through order 300.  No separator above the isolated `K_2`
  tangency was found.  This is **NUMERICALLY OBSERVED** only.

## 2026-08-08: portal-linked pair doublets

- Introduced a genuinely new trace regime: two strong `K_2` modules linked
  to each other on the same weak scale as their core portals.  This is not a
  fully absorbing four-vertex gadget.
- Derived the four Bd/dB macro rates directly.  Both rules have inter-pair
  infection/recovery ratio exactly `r^2`, but the conflict intensity differs
  by a factor of `sigma`.
- Solved the three-state trace and reduced the full separator to a quadratic
  in the correlation parameter `u`.
- **PROVED:** at `r=R_hyb`, the cleared numerator is
  `-r(Q0+u Q1+u^2 Q2)`, where `Q0` is the old sextic tangency square and
  `Q1,Q2` are strictly positive for every `sigma>0`.  Their positivity has
  an exact Sturm/discriminant certificate.
- Equality requires `u=0` and `sigma=sigma_*`.  Therefore fixed nonzero
  symmetric portal correlation cannot extend the hybrid threshold at first
  order.  Arbitrary mixtures of these doublets, uncoupled pairs, and ordinary
  leaves inherit the obstruction.
- Asymmetric two- and three-pair optimizations returned to the same boundary,
  but this remains numerical.  The exact remaining escape is an asymmetric
  portal network, a growing-rank correlated gadget, or positive second order
  along the zero tangent.
