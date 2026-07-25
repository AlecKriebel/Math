# Companion-at-infinity exclusion for the rank-two-restriction line-\((2,2)\) pencil

**Status:** exact theorem with independent hostile audits of the outer,
nonresonant finite, and final resonance charts.  This is not peer reviewed.

**First recorded:** 2026-07-25T06:46:00Z.

## 1. Statement

Let
\[
F=LX+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have total degree four and constant nonzero Jacobian.  Put
\[
p=x^2,\qquad q=yz
\]
and suppose the cubic normal component is the
companion-at-infinity form
\[
R:=(H_3)_3=xq.                                         \tag{1}
\]

There is no loss in omitting a constant term: subtracting \(F(0)\) in the
target leaves the Jacobian and every positive-degree homogeneous part
unchanged.

### Theorem

No Keller map has either of the following leading forms:

1. one outer critical point at infinity,
   \[
   H_4=((p-aq)^2,q^2,0),\qquad a\in\mathbb C;           \tag{2}
   \]
2. both outer critical points finite and distinct,
   \[
   H_4=((p-tq)^2,(p-q)^2,0),\qquad t\in\mathbb C,
   \quad t\ne1.                                        \tag{3}
   \]

Thus every companion-at-infinity orbit in the
rank-two-restriction pencil \(\langle x^2,yz\rangle\) is excluded.

Together with the previously audited finite-companion chart theorems and
the earlier zero-normal-cubic exit, this closes the complete
unique-double-line line-\((2,2)\) subrow having quadratic pencil
\(\langle x^2,yz\rangle\).  The distinct rank-one-restriction pencil
\(\langle x^2,y^2+xz\rangle\) is closed by its separately audited
marked and unmarked orbit packages.  Together, these results close the
entire genuine line-image \((2,2)\) taxonomy row.

## 2. Orbit ledger

The unique double line forces every source linear stabilizer of the pencil
to send \(x\) to a scalar multiple of \(x\).  Comparing the \(xy,xz\)
terms in the other member shows that, up to interchanging \(y,z\), the
stabilizer is diagonal.  Its induced base action on
\[
u=p/q
\]
is exactly \(u\mapsto\lambda u\).  The interchange of \(y,z\) acts
trivially on the base.

Relative to the marked companion (1), an unordered pair of distinct
outer critical points has exactly two forms.

- If one point is at infinity, it is \(\{a,\infty\}\), giving (2).
  Scaling has the two orbits \(a=0\) and \(a\ne0\), although the proof
  below works for all \(a\) without division.
- If both points are finite, normalize the unordered pair to
  \(\{t,1\}\), \(t\ne1\), giving (3).  For \(t\ne0\), swapping the two
  points gives \(t\sim t^{-1}\).  The finite resonances
  \[
  t=-2,\qquad t=-\frac12                              \tag{4}
  \]
  are therefore one orbit.  The endpoint \(t=0\) stays in the finite
  chart, while \(t=\infty\) is (2) with \(a\ne0\) after swapping target
  coordinates.

The value \(t=1\) makes the two quartic coordinates proportional and is
not a degree-two outer cover.  Hence (2)--(4) exhaust the valid moduli.

## 3. Raw \(E_7\) away from the resonance

Write
\[
U=(H_3)_1,\qquad V=(H_3)_2,\qquad W=(H_2)_3.
\]
The raw degree-seven identity is a \(36\times26\) linear coefficient
matrix in two general cubics \(U,V\) and one general quadratic \(W\).

For (3), an exact \(18\times18\) minor is
\[
-347892350976
(t-1)^{10}(t+2)^4(2t+1)^4.                            \tag{5}
\]
For (2), an exact \(18\times18\) minor is the constant
\[
-5566277615616.                                        \tag{6}
\]

In both charts there are eight explicit kernel directions: six
first-integral directions
\[
(x^3,0,0),\ (xq,0,0),\ (0,x^3,0),\ (0,xq,0),\
(0,0,p),\ (0,0,q)
\]
and the \(y,z\) affine-translation jets.  Their coefficient matrix has
constant minor \(4\).  Equations (5)--(6) therefore give the complete
kernel for
\[
(t-1)(t+2)(2t+1)\ne0                                  \tag{7}
\]
and for every \(a\).

The \(x\)-translation jet is already a combination of the six invariant
directions.  Using it together with the \(y,z\) translations and target
shears adding the third component to the first two gives the complete
normal form
\[
H_3=(0,Cx^3,xq),\qquad W=w_0p+w_1q.                    \tag{8}
\]
No normalization divides by \(t\) or \(a\); all lower pieces are merely
relabelled.

## 4. Nonresonant and outer lower exit

Write the first two quadratic components in the basis
\[
p,\ xy,\ xz,\ y^2,\ q,\ z^2
\]
and let \(L=(\ell_{ij})\).  After (8), the complete \(E_6\) system is
linear in exactly the ten variables
\[
\widehat\alpha_1,\ldots,\widehat\alpha_4,\quad
\widehat\beta_1,\ldots,\widehat\beta_4,\quad
\ell_{32},\ell_{33},                                   \tag{9}
\]
where the hats denote the \(xy,xz,y^2,z^2\) coefficients.
It is independent of all other lower coefficients.  Exact forcing minors
are
\[
\begin{aligned}
-1048576(t-1)^6(t+2)^2(2t+1)^2
   &&\text{for (3)},\\
-4194304
   &&\text{for (2)}.                                   \tag{10}
\end{aligned}
\]
Setting the ten variables to zero annihilates the full \(E_6\)
polynomial, so these are converse solves.

The remaining \(E_5\) matrices on
\[
\ell_{12},\ell_{13},\ell_{22},\ell_{23}
\]
have exact minors
\[
64(t-1)^2,\qquad64,                                    \tag{11}
\]
respectively.  Thus all six entries in columns two and three of \(L\)
vanish under (7) and for every \(a\).  This contradicts
\(\det L\ne0\).

The endpoint \(t=0\) is included: the exact ranks of \(E_7,E_6,E_5\)
there are \(18,10,4\).

## 5. Complete resonance kernel

It remains to treat the single unordered orbit (4).  Use \(t=-2\):
\[
H_4=((p+2q)^2,(p-q)^2,0).                             \tag{12}
\]
The raw \(E_7\) matrix has rank \(14\) and nullity \(12\).  Five legal
gauge directions (two target shears and three source translations) and
the following seven normal directions span its kernel, with constant
independence minor \(82944\):
\[
\begin{aligned}
W={}&w_0p+w_1xy+w_2xz+w_3y^2+w_4q+w_5z^2,\\
U={}&0,\\
V={}&Cx^3-6w_1x^2y-6w_2x^2z-6w_3xy^2-6w_5xz^2,\\
R={}&xq.
\end{aligned}                                          \tag{13}
\]
Thus (13) is a complete affine/target normal form, not an ansatz.

## 6. Resonance \(E_6/E_5\) exit

Put
\[
K=C+4w_0-2w_4.                                         \tag{14}
\]
The complete affine \(E_6\) system has generic lower-variable rank \(8\).
Denominator-cleared polynomial left-kernel syzygies give, up to nonzero
numerical factors,
\[
w_3^2,\qquad w_5^2,\qquad Kw_3-w_1^2,\qquad Kw_5-w_2^2. \tag{15}
\]
Over \(\mathbb C\), (15) successively gives
\[
w_3=w_5=w_1=w_2=0.                                    \tag{16}
\]

After (16), an exact \(8\times8\) minor is
\[
5308416,
\]
and the complete \(E_6\) solution is
\[
\begin{gathered}
\alpha_1=\alpha_2=\alpha_3=\alpha_5=0,\\
\beta_1=-6\ell_{32},\qquad
\beta_2=-6\ell_{33},\qquad
\beta_3=\beta_5=0.                                    \tag{17}
\end{gathered}
\]
Substitution of (17) annihilates every \(E_6\) coefficient.

At degree five, the four-variable pivot minor is \(576\).  Its exact solve
is
\[
\begin{aligned}
\ell_{12}&=-2K\ell_{32},&
\ell_{13}&=-2K\ell_{33},\\
\ell_{22}&=-5K\ell_{32},&
\ell_{23}&=-5K\ell_{33},
\end{aligned}                                          \tag{18}
\]
with complete residual
\[
36K\bigl(\ell_{32}y^3z^2-\ell_{33}y^2z^3\bigr).        \tag{19}
\]

If \(K\ne0\), (19) kills \(\ell_{32},\ell_{33}\), so columns two and
three of \(L\) vanish.  If \(K=0\), (18) kills their first two entries,
and the columns are
\[
(0,0,\ell_{32})^T,\qquad(0,0,\ell_{33})^T,
\]
again dependent.  Thus \(\det L=0\) in every specialization, completing
the proof.

## 7. Exact coverage

The raw ranks are
\[
\operatorname{rank}E_7=
\begin{cases}
18,&(7),\\
14,&t=-2,-1/2,\\
8,&t=1.
\end{cases}
\]
The last value belongs only to the invalid coincident outer map.  Sections
3--6 therefore treat every valid finite-pair orbit, while (6) treats every
outer-critical-at-infinity orbit.  No projective endpoint or resonance is
obtained by an unsafe specialization.

## 8. Verification and disclosure

`verify_companion_infinity_sympy.py` reconstructs both raw matrices,
kernel directions, all special ranks, affine gauges, complete lower
coefficient matrices, forcing minors and converses, and the full resonance
compatibility tree.

`verify_companion_infinity_pari.gp` independently reconstructs the outer
and nonresonant finite charts.  Its strict wrapper requires an exact output
transcript, and `test_companion_infinity_guards.sh` injects optimized
Python, diagnostic, extra-output, wrong-sentinel, and nonzero-exit
failures.

`audit_hostile/verify_resonance_pari.gp` independently reconstructs the
projective orbit ledger and the full \(t=-2\) resonance in PARI/GP,
including a nonzero \(14\times14\) raw minor, the complete twelve-dimensional
kernel and five legal gauges, universal polynomial \(E_6\) syzygies, the
constant-rank converse, and both \(E_5\) branches.  Its strict wrapper and
six mutation tests fail closed.

AI systems materially assisted discovery, calculation, verification, and
exposition.  Exact checks are evidence about the encoded algebra, not peer
review.  This note is unreviewed, and its source-specific priority audit is
not a guarantee of worldwide priority.
