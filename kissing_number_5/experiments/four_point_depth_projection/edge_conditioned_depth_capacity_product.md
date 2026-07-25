# A genuinely four-point depth/capacity product inequality

## Statement

Let \(C\subset S^4\) be a hypothetical 41-point kissing code and put
\(\delta=1/300\).  Fix any collection \(E\) of unordered code-point base
pairs \(e=\{y,z\}\) with
\[
q_e=\langle y,z\rangle>-1.
\]
For every \(e\), define the negative depth count
\[
H_e=\#\left\{x\in C\setminus e:
 \langle x,y\rangle+\langle x,z\rangle
 <-\delta\sqrt{2+2q_e}\right\}.                      \tag{1}
\]
The robust-depth theorem applied to
\((y+z)/\sqrt{2+2q_e}\) gives
\[
H_e\ge7.                                             \tag{2}
\]

Fix \(b>0\), and let
\[
\Gamma_e=\#\left\{w\in C\setminus e:
 \langle w,y\rangle\ge b,\
 \langle w,z\rangle\ge b\right\}.                    \tag{3}
\]
Suppose a proved local projection theorem supplies the pointwise integer
capacity
\[
\Gamma_e\le M_e.                                     \tag{4}
\]
The value \(M_e\) may depend on \(q_e\); no averaging or finite support is
assumed.

Then
\[
\boxed{\;
\sum_{e\in E}H_e\Gamma_e
\le
\sum_{e\in E}\bigl(M_eH_e+7\Gamma_e-7M_e\bigr).
\;}                                                  \tag{5}
\]

## Proof and four-point character

For each base pair separately, (2) and (4) give
\[
(H_e-7)(M_e-\Gamma_e)\ge0.
\]
Expanding and summing is exactly (5).

There is no hidden diagonal in its left side.  A point counted by \(H_e\)
has the sum of its two base correlations strictly negative, while a point
counted by \(\Gamma_e\) has that sum at least \(2b>0\).  Hence the two
sets are disjoint and
\[
H_e\Gamma_e
=\#\{(x,w):x\ne w,\ x\text{ satisfies (1)},\
                    w\text{ satisfies (3)}\}.
\]
Every term therefore uses four distinct code points \(y,z,x,w\).
The right side uses only pair and triple counts.  Thus (5) is a linear
four-point extension of the two pointwise local theorems, with every
strict and non-strict boundary retained in the correct direction.

## Why pair/triple marginals cannot recover it

Pair/triple data determine only aggregate sums such as
\(\sum_eH_e\) and \(\sum_e\Gamma_e\).  They do not determine their
edgewise product \(\sum_eH_e\Gamma_e\).  Two edge populations can have
the same marginals while correlating large depth counts with large common
neighborhoods differently.  This is the precise common-source statistic
lost by the centered quarter-grid Bachoc--Vallentin witness.

The inequality alone is not a five-dimensional separator: the exact
rank-six \(E_6\) countermodel in this folder is a genuine configuration
and therefore satisfies it.  Its role is to identify the smallest new
four-point variable required by a depth/common-pair synthesis.  Any
successful use must combine (5) with a dimension-five or rank-five
constraint that rejects the \(E_6\) source.

## Subsequent K5 audit

The first stored symmetric local Gram-PSD `K5` extension of the centered
quarter-grid witness violates (5) in the exact base strata
\((q,b,M)=(-1/2,1/2,1)\) and \((-1/4,1/2,3)\).
However, this is not a universal local-`K5` obstruction.  An amended
marginal LP has an exact 64-atom extension satisfying (5) and every
general-direction version, including the overlap correction
\[
247hg-234i\le13Mh+13rg-rME.
\]
See `k5_product_audit/`.  Thus the next missing condition is not raw local
five-point Gram consistency; it must couple overlapping subsets globally,
impose a genuine Lasserre/moment PSD condition, or recover rank five.
