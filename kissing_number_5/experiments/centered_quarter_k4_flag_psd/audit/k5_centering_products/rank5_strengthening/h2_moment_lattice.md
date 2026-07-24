# Exact H2 quarter-grid moment lattice

> **Centered specialization only.**  This note assumes the exact geometric
> centering identity \(\sum_a a\,m_a=-82\).  For a general 41-point
> quarter-grid profile use `general_quarter_grid_moment_lattice.md`.  In
> particular, the `r12` endpoint has \(A=-81\), so the centered selectors
> below must not be applied to it.

## Definitions

For \(a\in\{-4,-3,-2,-1,0,1,2\}\), set

\[
 b_a=5a^2-16,\qquad
 H_2(a/4)=\frac{b_a}{64}.
\]

Thus the seven integer numerators are

\[
 (b_{-4},\ldots,b_2)=(64,29,4,-11,-16,-11,4).
\]

For an actual 41-point quarter-grid code, let \(m_a\) be the unordered
pair counts and put

\[
 S=\sum_a m_ab_a^2.
\]

For every ordered triple of distinct vertices \((i,j,k)\), let
\(a_{ij}=4\langle x_i,x_j\rangle\), and put

\[
 R=\sum_{i,j,k\ {\rm distinct}}
 b_{a_{ij}}b_{a_{ik}}b_{a_{jk}}.
\]

Let \(K\) be the entrywise H2 transform of the Gram matrix and define

\[
 T_2=\operatorname{tr}(K^2),\quad
 T_3=\operatorname{tr}(K^3),\quad
 V=T_2-\frac{41^2}{14},\quad
 D=T_3-\frac{3\cdot41}{14}T_2+\frac{2\cdot41^3}{14^2}.
\]

## Exact affine forms

Separating equal-index and distinct-index terms gives

\[
 T_2=41+\frac{S}{2048},
 \qquad
 T_3=41+\frac{3S}{2048}+\frac{R}{262144}.
\]

Consequently the integer-scaled moments

\[
 X_2=14336V,\qquad Y_2=12845056D
\]

satisfy

\[
 X_2=7S-1133568,
\]

\[
 Y_2=49R-36288S+4933287936
    =49R-5184X_2-943128576.
\]

The rank-14 centered spectral inequality

\[
 144V^3-182D^2\ge0
\]

is exactly

\[
 576X_2^3-13Y_2^2\ge0.
\]

## Lattice congruences

In fact the seven values satisfy the stronger pointwise congruence

\[
 b_a^2\equiv 16+15a\pmod {30}.
\]

For a centered 41-point quarter-grid code,
\(\sum_a m_a=\binom{41}{2}=820\) and
\(\sum_a a\,m_a=-82\).  Therefore

\[
 S\equiv16(820)+15(-82)\equiv10\pmod {30},
\]

and the affine identity for \(X_2\) gives the stronger selector

\[
 X_2\equiv82\pmod {210}.
\]

In particular this implies the previously used
\(X_2\equiv12\pmod {35}\).

There is a sharper joint selector with the H1 moment.  Write

\[
 Q=\sum_a a^2m_a,\qquad X_1=5Q-11808.
\]

The pointwise congruence

\[
 b_a^2\equiv15a^2-150a+256\pmod {300}
\]

holds for every integer \(a\).  (After expanding, the difference is
\(25a(a-1)(a-2)(a+3)\), and the four-factor product is divisible by
12.)  Hence

\[
 S\equiv15Q-150(-82)+256(820)
   \equiv15Q+220\pmod {300}.
\]

Substituting the exact affine formulas for \(X_1,X_2\) gives

\[
 \boxed{X_2\equiv21X_1+40\pmod {2100}}.
\]

Since \(X_1\equiv2\pmod {10}\), reduction modulo 210 recovers
\(X_2\equiv82\pmod {210}\).

Every unordered vertex triple occurs six times in \(R\), so \(R\equiv0\pmod6\).
Also each summand of \(R\) is \(4^3\equiv4\pmod5\), while the number of
ordered distinct triples is \(41\cdot40\cdot39\), a multiple of five.
Thus \(R\equiv0\pmod {30}\).  Substitution in the affine identity yields

\[
 Y_2\equiv66\pmod {210},
 \qquad
 Y_2\equiv10X_2+2\pmod {49}.
\]

These selectors require empirical integer pair and triple multiplicities.
They do not constrain a continuous pair/triple pseudodistribution unless
those global empirical integrality conditions are added explicitly.
