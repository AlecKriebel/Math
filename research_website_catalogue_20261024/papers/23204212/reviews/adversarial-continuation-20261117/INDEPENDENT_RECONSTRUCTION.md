# Independent reconstruction before packaged scientific opinions

Recorded 2026-11-17 UTC during actual-primary reading. This document is written
before opening the packaged `agent_notes` scientific audit bodies. Original
manuscript claims, the packaged finite-check program/manifest and BUILD scope
assertions have been exposed; the last are not accepted as scientific proof.

## Actual nonamenability mechanism

The fetched actual pinned OpenAI paper is 13 pages / 354266 bytes, SHA256
a474b04a7e94e172d4260fc42c3643f1f9a4924d7383e12448f4ba8d636175e5.
I read all its extracted text, with a separate complete reread of lines270-410
to cover the variance formulas lost in one initially truncated tool response.
Its separate representation/percolation consequences are not used here and
their imported companion claims are outside this review.

Let f map a real Hilbert closed unit ball B to itself, be L-Lipschitz for L>0,
and have ||f(x)-x||>=delta>0. Choose integer D>=2 with D>4L^2/delta^2.
Choose D internal basic dyadic parents with positive gaps. Their affine copies
inside every parent produce D^2 children. For every ordered separated pair
among this fixed finite family, choose an element of genuine standard F
carrying it affinely to the first two parents. S is this fixed finite set.

Every basic partition T receives the recursively defined ball color
p(T)=f(D^{-1} sum_j p(T_Ij)) when all restrictions exist; otherwise zero.
An internal parent has partition cells outside it, hence a proper restriction
has strictly fewer cells. Therefore this is induction on an actual natural
number, without a fixed-point hypothesis and without assuming finite-dimensional
range, finite color palette, linear f, compact Hilbert ball or any invariant
Hilbert-valued mean.

For each nonempty finite A subset F, first set eta=max_{h in S}|hA triangle A|/|A|.
Only now choose a uniform dyadic level n making every g in A union SA admissible
for every parent and child. This is possible: each actual finite PL map has
finitely many dyadic breakpoints and affine offsets, so sufficiently fine source
cells have basic image cells; their maximum length tends to zero. Thresholds
are taken over a finite union. There is no uniform n over all F, and none is
required. n may depend on A without changing S, D, f, L or delta.

Use zero extension outside admissibility to define all interval colors on all
of F, and scalar correlations phi_IJ in [-1,1]. Exact affine covariance at the
two admissible points g,hg equates the relevant colors. Cancellation on hA
intersection A then gives
|E_A phi_IJ-alpha|<=eta for every separated pair, where alpha=E_A phi_I1I2.
This finite cancellation is valid for EVERY bounded scalar function, so using
the particular function determined by n(A) is legitimate. No exchange of a
limit with an invariant mean and no uniformity over infinitely many functions
is invoked.

Set x_i=X_Ii, y_ij=X_Ii.Ij, m=D^{-1}sum_k x_k and z_i=D^{-1}sum_j y_ij.
Recursion and normalized restriction associativity give x_i=f(z_i) pointwise
on A. For each fixed i the sums have exactly the following counts:

- E||m||^2 <= (1-1/D)(alpha+eta)+1/D, from D(D-1) separated ordered
  off-diagonal parent pairs and D diagonal terms <=1.
- E||z_i||^2 has the same upper bound from siblings.
- E<z_i,m> >= (1-1/D)(alpha-eta)-1/D. Precisely the D terms with parent
  index k=i may be nested and are only bounded below by -1; the remaining
  D(D-1) ordered terms are separated. Children in different parents retain
  their parents' positive gap; shared endpoints never enter a separated pair.

Consequently
E||z_i-m||^2 <= 4/D+4(1-1/D)eta,
with the coefficients of alpha cancelling exactly. No assumption alpha>=0 is
needed. The ordered-pair convention includes both symmetric off-diagonal terms
and introduces no missing factor two.

By convexity of squared norm and Lipschitz continuity, pointwise on A,
delta^2 <= ||m-f(m)||^2
 = ||D^{-1}sum_i (f(z_i)-f(m))||^2
 <= (L^2/D)sum_i ||z_i-m||^2.
Averaging this inequality over A yields
eta >= (delta^2/L^2-4/D)/(4(1-1/D)) > 0.
The finite S and positive right side are independent of A, contradicting the
forward finite-set Folner consequence of an invariant mean. The declaration
`Main.thompson_F_not_amenable` uses actual bounded real functions and the
composition multiplication convention; its visible top-level assumptions do
not include amenability failure, a synthetic coloring certificate or an
uninstantiated tube-separation certificate.

## Independent analytic checks on the explicit map

The written appendix supplies the displacement map rather than relying only
on a cited theorem statement. In H=L^2([0,1];R^2), v(t)(w)=(cos(theta(t)w),
sin(theta(t)w)), gamma(t)=a(t)v(t). The measure has total mass one; hence
||v(t)||=1 and <v(s),v(t)>=sinc(theta(t)-theta(s)), while
||gamma'(t)||^2=a'(t)^2+a(t)^2 theta'(t)^2/3. The integral of w^2 is 1/3,
not one; this factor is present in actual Lean `AnalyticOscillator` and `Curve`.
For t<=2 the first square is 1/64. For t>=2, a>=1/4 and theta'=1, so
the squared speed is >=1/48>1/64. At t<=1 equality gives inf speed=1/8.
Profile first derivatives match at every junction 1,2,3. Uniform pointwise
quadratic trigonometric remainders for 0<=w<=1 give actual L2 differentiability,
not a bare pointwise-to-L2 exchange. Lean uses a.e. equality of representatives.

Uniform separation for |s-t|>=d>0 is stronger than pointwise injectivity and is
proved separately. Negative-tail pairs have exact distance |s-t|/8; a single
negative-divergent parameter gives diverging norm. Positive-tail pairs have
squared distance 2(5/16)^2(1-sinc(t-s)); on [d,infinity) the sinc supremum is
strictly below one by compactness plus decay. A fixed finite parameter against
the positive tail has limiting squared distance a(s)^2+(5/16)^2>0. Finite
limits contradict injectivity. The Lean version instead covers explicit finite
regions and a compact parameter set. An infinite-dimensional compactness
assumption is unnecessary: uniform separation confines the nearest-parameter
minimization to a compact REAL interval.

The tube projection uses positive radius with curvature/separation slack.
Orthogonality of its minimizing residual follows by differentiating squared
distance at a genuine attained minimum. The tangent projection estimate and
Lipschitz tangent bound give |t(x)-t(y)|<=16||x-y|| for nearby tube points;
setting x=y supplies uniqueness, rather than assuming it.

R=I+A+A^2/(1+<u,v>) with A(h)=v<u,h>-u<v,h> rotates u to v. Since
<u,v>=a'/||gamma'||>=0, the denominator never approaches zero. In the span
of u,v, A^2=-(1-kappa^2)I and R=kappa I+A, an orthogonal operator; in its
orthogonal complement R=I. The formula also covers u=v, where A=0. Thus a
normal residual remains perpendicular to v after rotation, including the
degenerate span limit. Normalization by ||G|| is justified only after proving
the uniform lower bound ||G||>=rho/4.

I checked every cutoff boundary: r=rho/4, rho/2, rho and t=1. In the inner
quarter, the v-coefficient is min(a,-1/8), hence cannot vanish. In the next
quarter, the rotated perpendicular residual has norm >=rho/4. In the outer
tube, beta=0: for t>1 the radial norm is >=1/8 and the blended residual norm
is <=r<rho<1/32; for t<=1 R=I and the residual is perpendicular to v. Outside
the tube, ||x||>=rho because gamma(0)=0. These are exhaustive cases.

The additive correction is uniformly bounded and its two cutoffs tend to zero
at the actual tube boundary at a rate proportional to rho-r. Distance to the
curve is 1-Lipschitz, so this glues the inside/outside Lipschitz bound; distant
pairs are controlled by the bounded additive change. The outer annulus identity
G(x)=x for ||x||>=1/2 uses |a(t)|>=||x||-r>1/2-rho>5/16, forcing the
negative straight ray, where both corrections vanish. Negative normalization
f=-G/||G|| has unit norm and displacement >=1/2: reverse triangle inequality
handles ||x||<1/2; the outer identity gives distance 1+||x|| otherwise.

These checks reconstruct the written analytic argument. They are not a fresh
Lean kernel validation, nor do they certify unseen Mathlib proofs by file names.
Further actual source reading and classical interface checks continue in the
coverage ledger. Scientific conclusions remain private until the root gate.
