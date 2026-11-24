# Independent reconstruction of the one-cut global-minimum certificate

Public edition dated 2026-10-12. This retains the complete substantive mathematical report, with transparent editorial changes to private references and review-status wording. Independently authored executable checkers, raw interval certificates, full numerical records, detailed diagnostic outputs, and source copies are not included. Hashes identify omitted evidence but do not provide executable public reproducibility. The work is AI-assisted and unrefereed, with no external human peer review or formal proof-assistant certification.

## Scope and status

This document reconstructs Certificate 6.1 of Shouqiao Wang, *A Proposed Complete Solution to Erdős Problem 1038*, Sections 6–6.1. It concerns only the zero-platform one-cut family. It does **not** establish the lower bound over all finite polynomials, the unrestricted infimum, or nonattainment. Those require the separate Certificate 7.1 and its analytic interfaces.

The independently authored standard-library checker has passed a complete exact-integer run and a float-free certificate replay. The original reconstruction requested independent fresh review before upgrading acceptance; that review and full independent recomputation have since been completed in the accompanying end-to-end audit. This note remains scoped to the one-cut family. No source-author verifier, Lean project, installer, or third-party mathematical software was executed. The construction is credited to Wang and Tao; no novelty is claimed.

Public sources:

- [Wang's proposal](https://multiscalar.ai/results/erdos-1038/paper.pdf), frozen PDF SHA-256 `3a7e857b12e59f24af17f36a30030b0ad6368c2d59955ef58e643400917565ad`, 488289 bytes, previously inspected 2026-10-11.
- [Public result page](https://multiscalar.ai/results/erdos-1038/), which labeled the manuscript Proposed at the inspected snapshot.
- [Companion source](https://multiscalar.ai/results/erdos-1038/numerical_verifier.py), SHA-256 `e84b94b40a27d2f3e254d4d14393a49c79ac4db57e4b55010441d4e04eff9616`, 110762 bytes. Static reference only; no code from it is imported or executed.
- [Tao's updated note](https://terrytao.wordpress.com/wp-content/uploads/2025/12/erdos-1038-2.pdf), which introduced the underlying family.

## Theorem reconstructed

Put

\[
H=\frac{2q}{(1+q)^2},\qquad s=\frac{1-q}{1+q},\qquad
A=\frac{\log H}{\log q},\qquad d=\log 2-2\log(1+q).
\]

There is a unique admissibility endpoint \(q_s\in(0,3-2\sqrt2)\) with \(A(q_s)=s(q_s)\). For \(0<q<q_s\), let \(u_+\in(1,q^{-1})\) and \(u_->q^{-1}\) denote the unique nontrivial roots of

\[
A\log\frac{u-q}{|1-qu|}-\log u=0.
\]

At \(q_s\), continue \(u_+=1\). Define

\[
\Lambda(q)=H\bigl(u_-+u_-^{-1}-u_+-u_+^{-1}\bigr).
\]

The certificate and the arguments below establish exactly one stationary point \(q_*\) on \((0,q_s]\), negative derivative before it, positive derivative after it, and hence a unique strict global minimum **within this family**. In particular,

\[
0.123630684649383<q_s<0.123630684649384,
\]
\[
0.025715536866527<q_*<0.025715536866528,
\]
\[
1.834430475762661<\Lambda(q_*)<1.834430475762662.
\]

The endpoint derivative is understood as its continuous one-sided extension.

## Exact arithmetic trust boundary

The checker represents an interval as two signed integers \([a,b]\), meaning the closed rational interval \([a/2^{240},b/2^{240}]\). Its output certificate records those integers verbatim. There are no parsed floating-point endpoints in the replay.

Addition and subtraction use exact integer operations. Multiplication takes the minimum and maximum of all four endpoint products, divides by \(2^{240}\), and rounds the lower endpoint toward minus infinity and the upper endpoint toward plus infinity. Reciprocal is allowed only when zero is excluded; it returns the outward-rounded interval with endpoints \(2^{480}/b\) and \(2^{480}/a\). Squaring explicitly includes zero when the input crosses zero. Rational and decimal inputs are converted by exact numerator/denominator division. Python integers have arbitrary precision.

The resulting operations satisfy the inclusion property by elementary interval arithmetic. Every check uses explicit exceptions, not optimization-removable assertions. Decimal strings in the summary are merely outward-rounded displays; all acceptance comparisons are on integers.

### Logarithm

For an exact positive dyadic endpoint \(x\), choose the exact integer \(k\) for which \(y=x2^{-k}\in[1,2)\). Any dyadic conversion of \(y\) is outward. Put \(t=(y-1)/(y+1)\), so \(0\le t\le1/3\). With \(N=96\),

\[
\log y=2\sum_{j=0}^{N-1}\frac{t^{2j+1}}{2j+1}+R,
\quad 0\le R\le\frac{2t^{2N+1}}{(2N+1)(1-t^2)}.
\]

The checker evaluates the finite sum and the upper bound through outward operations. The same calculation at \(y=2\) encloses \(\log 2\). It then forms \(\log x=\log y+k\log2\) by interval arithmetic, including negative \(k\). Monotonicity of log extends the two endpoint evaluations to every point of an interval. The summation truncation error and every arithmetic rounding error are therefore included.

### Exponential

For nonnegative \(x\), scale \(v=x/2^k\) so that \(0\le v\le1/8\). Evaluate \(\sum_{j=0}^{60}v^j/j!\). The omitted tail starts at \(v^{61}/61!\); every later term ratio is at most \(v/62\), so

\[
0\le R\le\frac{v^{61}}{61!\,(1-v/62)}.
\]

Add that outward error and square \(k\) times. Negative arguments are handled by reciprocal, and arbitrary input intervals by monotonic endpoint evaluation. No library logarithm or exponential is used in acceptance arithmetic.

## Admissibility and branch uniqueness

Let

\[
f(q)=(1+q)d(q)+2q\log q.
\]

Algebra gives \(A\le s\iff f\ge0\). Moreover,

\[
f'(q)=\log\frac{2q^2}{(1+q)^2}<0\qquad(0<q<1).
\]

The certificate supplies strict opposite signs at the exact endpoints of its \(q_s\) enclosure. It also checks that this enclosure lies below \(0.124\), and that \(0.124^2-6(0.124)+1>0\); since \(0.124<1\), this implies \(0.124<3-2\sqrt2\). The limit \(f(0+)=\log2>0\), strict monotonicity, and the certified signs give existence and uniqueness on the full required domain. For every admissible positive \(q\), \(0<A<1\).

For the plus equation, direct differentiation gives

\[
F_u=\frac{qu^2-Bu+q}{u(u-q)(1-qu)},\qquad B=1+q^2-A(1-q^2).
\]

When \(q<q_s\), \(A<s\), hence \(B>2q\). The two positive numerator roots are reciprocal, with exactly one in \((1,q^{-1})\). Consequently \(F\) first decreases and then increases on this interval. Since \(F(1)=0\) and \(F(u)\to+\infty\) at \(q^{-1}-\), its nontrivial root is unique. At \(q_s\), \(B=2q\), and the derivative numerator is \(q(u-1)^2\); the nontrivial root merges continuously into \(u=1\).

For \(u>q^{-1}\),

\[
F_u=-\frac{A(1-q^2)}{(u-q)(qu-1)}-\frac1u<0,
\]

and the boundary limits have opposite infinite signs. Thus the minus branch is unique. These analytic uniqueness facts identify every root bracket certified below with the required branch; numerical proximity is never used to select a root.

## Bulk equations and differentiation

Write \(r=(-\log q)^{-1}\), \(q=e^{-1/r}\), and \(z_\pm=qu_\pm\). The transformed equations are

\[
G_\pm(r,z)=A\log\frac{z-q^2}{|1-z|}-\log z-d=0,
\qquad A=1-rd.
\]

The width is

\[
\Lambda=\frac2{(1+q)^2}(z_--z_+)
+\frac{2q^2}{(1+q)^2}(z_-^{-1}-z_+^{-1}).
\]

The first and second derivatives of \(q,d,A\) used in the checker are obtained by ordinary differentiation:

\[
q_r=q/r^2,\quad q_{rr}=q(1-2r)/r^4,
\]
\[
d_r=-2q_r/(1+q),\quad d_{rr}=-2\{q_{rr}/(1+q)-q_r^2/(1+q)^2\},
\]
\[
A_r=-d-rd_r,\qquad A_{rr}=-2d_r-rd_{rr}.
\]

For \(W=\log(z-q^2)-\log|1-z|\), the checker explicitly evaluates

\[
W_z=(z-q^2)^{-1}+(1-z)^{-1},\quad
W_{zz}=-(z-q^2)^{-2}+(1-z)^{-2},
\]
\[
W_r=-2qq_r/(z-q^2),\quad
W_{rz}=2qq_r/(z-q^2)^2,
\]
\[
W_{rr}=-2(q_r^2+qq_{rr})/(z-q^2)-(2qq_r)^2/(z-q^2)^2.
\]

Product differentiation gives all partials of \(G=AW-\log z-d\). For each branch,

\[
z_r=-G_r/G_z,\qquad
z_{rr}=-(G_{rr}+2G_{rz}z_r+G_{zz}z_r^2)/G_z.
\]

A second-order single-variable jet then differentiates the displayed width expression, including all cross terms.

### Uniform root validation and interval Newton

For each parameter slab, the certificate records an initial rational box for each root. At its two exact endpoints, interval evaluations prove opposite signs uniformly over the **entire** parameter slab. It also proves \(G_z>0\) for the plus box and \(G_z<0\) for the minus box, throughout those boxes. The plus box is above \(q\) and below 1, and the minus box is above 1. Existence, uniqueness, and the analytic branch classification thus establish initial containment.

Each subsequent Newton step uses an exact dyadic point \(m\) in the current box and intersects the current box with

\[
m-G(r,m)/G_z(r,Z).
\]

For every fixed parameter and its already-contained true root \(z\), the mean-value theorem gives \(z=m-G(r,m)/G_z(r,\xi)\) for some \(\xi\) between \(m\) and \(z\). Therefore every intersection preserves containment. This is parametric interval contraction after a separate existence proof, not reliance on an approximate Newton orbit.

The generator uses ordinary binary floats solely to propose initial boxes. The saved certificate stores the exact rational meanings of those boxes. The replay never invokes any proposal routine and repeats all sign tests, contractions, and derivative enclosures from the saved exact boxes.

## The complete singular tail

For \(0\le r\le1/50\), use \(q(0)=0\). The function \(q=e^{-1/r}\), extended this way, is smooth and flat at zero. Both \(q\) and \(q_r=e^{-1/r}/r^2\) increase on this interval, since \(q_{rr}>0\) for \(0<r<1/2\). The checker therefore uses

\[
0\le q\le e^{-50},\qquad 0\le q_r\le2500e^{-50},
\]

with \(e^{-50}\) enclosed by its own exact exponential calculation.

Uniform endpoint signs and derivative signs on the fixed boxes

\[
z_+\in[499/1000,501/1000],\qquad
z_-\in[149/100,15001/10000]
\]

establish containment for the whole tail. At \(r=0\), the equation reduces to \(-\log(2|1-z|)=0\), with roots \(1/2\) and \(3/2\); \(G_z\ne0\) gives the regular implicit continuation there. The first-derivative formula then proves the strict enclosure

\[
-0.788<\Lambda_r<-0.737
\]

on the **closed** tail, including its limiting endpoint. No sampled positive cutoff replaces \(r=0\).

## Soft endpoint, series, and remainders

For the plus branch let \(x=\log u_+\), \(y=x^2\). Define

\[
C(y)=\sum_{m\ge0}\frac{y^m}{(2m)!},\quad
S(y)=\sum_{m\ge0}\frac{y^m}{(2m+1)!},\quad
T(w)=\sum_{m\ge0}\frac{w^m}{2m+1}.
\]

Put \(b=qS/(1-qC)\), \(w=yb^2\). The analytically deflated equation and width are

\[
D(q,y)=A-1+2AbT(w)=0,
\]
\[
\Lambda=\frac{2z_-}{(1+q)^2}+\frac{2q^2}{(1+q)^2z_-}-2HC(y).
\]

The checker requires \(1-qC>0\), \(y\ge0\), and \(0\le w<0.03\). Together these imply \(q e^{\sqrt y}<1\), so the hyperbolic/atanh identity defining the deflation is on its correct real branch. At zero, \(D(q,0)=A(1+q)/(1-q)-1\), and thus \(D(q,0)\le0\) for every admissible \(q\).

All three positive series are summed for \(m=0,\ldots,32\), so the omitted tail starts at \(K=33\). For \(C\) or \(S\), write \(\sigma=0\) or 1 and let \(Y\) be the outward upper argument bound. Define

\[
R=\frac{Y}{(2K+\sigma+2)(2K+\sigma+1)}.
\]

Value and first-derivative tail bounds are

\[
\frac{Y^K}{(2K+\sigma)!(1-R)},\qquad
\frac{K Y^{K-1}}{(2K+\sigma)![1-(K+1)R/K]}.
\]

These follow because the successive term ratios are decreasing and bounded by the displayed ratios at \(K\). For \(T\), with upper argument \(W\), the bounds are

\[
\frac{W^K}{(2K+1)(1-W)},\qquad
\frac{K W^{K-1}}{(2K+1)[1-(K+1)W/K]}.
\]

All relevant denominators are verified positive. The omitted derivative is a nonnegative scalar in its certified interval; multiplying that interval by each input derivative, with its actual sign, correctly bounds the chain-rule contribution. First-order three-variable jets propagate these bounds through \(D,G_-,\Lambda\).

Each regular soft slab has uniform opposite \(D\) signs at its two \(y\) endpoints and \(D_y>0\), and the minus root has its own uniform strict brackets. At the last slab the lower \(y\) endpoint is exactly zero. The lower sign there follows analytically from \(q\le q_s\), even though the numerical slab extends to the upper isolation endpoint, slightly beyond \(q_s\). A positive upper sign and \(D_y>0\) enclose the root for every admissible parameter, including \(q_s\). This is why the endpoint interval needs no unjustified negative lower sign at inadmissible points.

Finally,

\[
y_q=-D_q/D_y,\qquad (z_-)_q=-(G_-)_q/(G_-)_z
\]

are substituted into the total derivative of \(\Lambda\). The certificate proves this derivative positive on every soft slab, including the endpoint chart. The positive \(D_y\) makes the deflated branch regular at \(y=0\), so the width has the required continuous one-sided derivative.

## Exact, gap-free coverage

Unlike the source implementation's irrational chart boundaries, this reconstruction uses shared rational cutoffs, plus one certified overlap.

| Part | Domain | Finite slabs | Accepted sign |
|---|---|---:|---|
| Tail | \(0\le r\le1/50\) | 1 | \(\Lambda_r<0\) |
| Left bulk | \(1/50\le r\le27/100\) | 38 | \(\Lambda_r<0\) |
| Convex tube | \(27/100\le r\le28/100\) | 2 | \(\Lambda_{rr}>0\) |
| Right bulk | \(28/100\le r\le87/200\) | 75 | \(\Lambda_r>0\) |
| Regular soft | \(1/10\le q\le6181/50000\) | 51 | \(\Lambda_q>0\) |
| Endpoint soft | \(6181/50000\le q\le q_s\) | 1 | \(\Lambda_q>0\) |

Recursive subdivision uses exact Fraction midpoints, and conversion to dyadic endpoints is outward. Replay checks the first and last required endpoints and the overlap of every pair of consecutive slabs. It does not trust a slab count or a claimed domain label.

The checker additionally proves

\[
1/10<\exp(-200/87)<q_s.
\]

Thus the right bulk reaches strictly inside the soft domain, with overlap approximately \([0.1,0.1003741500\ldots]\). It cannot leave a chart-conversion gap. Since \(dq/dr=q/r^2>0\) for \(r>0\), first-derivative signs in the two charts have the same orientation.

For orientation only, the exact accepted bounds imply \(\Lambda_{rr}>3.81\) on the tube. All first-derivative signs have large margins outside the small stationary enclosure: the left-bulk upper bound is below \(-0.0041\), right-bulk lower bound exceeds \(0.00788\), regular-soft lower bound exceeds \(0.04318\), and endpoint-soft lower bound exceeds \(2.458\). These shortened margin displays are not acceptance inputs.

## Stationary-point isolation and global conclusion

Let the exact rational proposal

\[
q_c=0.02571553686652745032257637166391965344,
\qquad r_c=-1/\log q_c.
\]

The checker encloses \(r_c\) by its exact logarithm algorithm. It selects a dyadic point at or below the lower bound for \(r_c-10^{-30}\), and another at or above the upper bound for \(r_c+10^{-30}\). It proves a strictly negative derivative at the former and a strictly positive derivative at the latter. Both points are checked to lie strictly inside the convex tube.

Continuity gives a stationary point between them; strict convexity gives exactly one throughout the tube. The left and right covers, together with the tail and the overlapping soft charts, exclude all other stationary points and prove strict decrease followed by strict increase on the entire admissible domain. Therefore this point is the unique global minimizer of the one-cut family. The limiting value \(\Lambda(0+)=2\) is consistent with, but not needed in place of, the strict derivative argument.

A uniform branch enclosure on the entire narrow stationary parameter interval yields the following outward decimal displays:

- \(q_*\): `[0.02571553686652745032257637166357505416085527329520287597773595470, 0.02571553686652745032257637166426425271914472670479712402226614016]`
- \(L=\Lambda(q_*)\): `[1.834430475762661711090753635120553436511864256655884976379752017, 1.834430475762661711090753635129018849529897507462271417764406996]`

The replay mechanically checks the shorter theorem decimal inequalities. It also checks \(q_s\)'s displayed decimal enclosure. These comparisons are not inferred from printed scientific output.

## Interfaces and reproducibility

The omitted raw certificate consists of exact integer data with denominator \(2^{240}\). Its independently authored replay checks those records without floating proposals. The normal generator can regenerate independently proposed boxes but is unnecessary to trust the replay. The executable checker and full raw records are not provided in this public edition; the mathematical formulas, remainder estimates, stated rational bounds, and aggregate evidence identities are retained.

The reconstructed family minimum can supply the inequality \(\Lambda(q)\ge L\) for the terminal one-cut references used by Certificate 7.1. The previous accepted fixed-candidate result already supplies the separate one-sided comparison \(L<\mathrm{LSTAR\_HI}\) once family minimality is established. This document makes no claim that the global polynomial lower-bound gate has thereby passed.
