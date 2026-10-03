# Independent Poisson/component baseline

This document was derived before reading the frozen submitted proof, programs,
historical review, root analysis, or sibling reviews. The only frozen content
read before this document was SOURCE_MANIFEST.json and SOURCE_NORMALIZATION.md.
The primary PDFs were fetched independently and matched their routed byte counts
and SHA256s. Complete private gzip captures and public hash receipts are retained.

## Claim and quantifiers

For every integer n >= 3 and every finite real-valued, nonconstant harmonic
u: R^n -> R, there is a continuous gamma: [1,infinity) -> R^n such that for
every real H and every R > 0 there is T with t >= T implying both
u(gamma(t)) > H and |gamma(t)| > R. The curve can be chosen polygonal on every
bounded parameter interval, with only finitely many pieces meeting any fixed
compact subset of R^n. Injectivity, a fixed ray, prescribed growth, finite length,
and monotone u-values are not part of the claim.

The independent mechanism below proves the more general continuous-subharmonic
statement, assuming sup u = infinity. It does not establish a discontinuous
subharmonic statement, where superlevel sets need not be open.

## Quantitative Poisson comparison

Let d sigma be probability surface measure on S^(n-1), and let f >= 0 be
continuous and subharmonic on all R^n. On B(0,R), comparison with the harmonic
Poisson extension of its boundary values gives

    f(x) <= integral P_R(x,theta) f(R theta) d sigma(theta),
    P_R(x,theta) = (1-|x|^2/R^2) / |theta-x/R|^n.

This comparison follows from the maximum principle applied to f minus the
Poisson extension; it needs no boundary regularity beyond the sphere and
continuity of f. If |x|/R <= q < 1, the exact extremal bounds, attained when
theta is opposite or parallel to x, are

    L_n(q) = (1-q)/(1+q)^(n-1) <= P_R(x,theta)
             <= K_n(q) = (1+q)/(1-q)^(n-1).

For nonnegative harmonic f both inequalities apply to f(x) versus its spherical
mean. For general subharmonic f only the upper comparison f(x) <= K_n(q) mean f
is asserted. As R grows with x fixed, q tends to zero and both constants tend
to one. The constants depend on n and the ratio |x|/R, not on a bound for f.

If 0 <= f <= M < infinity and M > 0, choose a point x with
f(x) > (1-eta) M. Then

    mean f(R theta)/M > (1-eta)/K_n(|x|/R).

Consequently the spherical mean tends to M: its liminf is at least (1-eta)M
for every eta > 0, and its limsup is at most M. The point x may depend on eta;
the R limit is taken after x is fixed. There is no uniformity assertion over
all possible f or x. This order of quantifiers is essential.

An explicit sufficient large-radius bound useful for an adversarial control is
R >= 8n max(1,|x|). It gives q <= 1/(8n), and Bernoulli's inequality gives
K_n(q) <= (9/8)/(7/8) = 9/7 < 3/2. This coarse bound is deliberately stronger
than needed and is valid for every n >= 2.

## At most one exceptional domain: a mean-value argument

Call an open domain D exceptional if it supports a continuous, nonzero,
bounded, nonnegative entire subharmonic f which is zero on R^n minus D.
This is an existence definition, not an appeal to the asymptotic-path theorem.
If D1 and D2 are disjoint and both exceptional, take witnesses fi with
Mi = sup fi > 0. Pointwise f1/M1 + f2/M2 <= 1 because supports are disjoint.
But the spherical means of both normalized witnesses tend to one by the
preceding lemma. Their sum would have mean tending to two, a contradiction.
Equivalently, take fi(xi) > 3Mi/4 and
R >= 8n max(1,|x1|,|x2|). Each spherical mean exceeds (3/4)/(9/7) = 7/12,
so their sum exceeds 7/6 although pointwise it is at most one.

Hence two disjoint domains cannot both be exceptional. A nonexceptional
domain retains that property under arbitrary open subdomains: any witness
supported in the smaller domain would be a witness in the larger one. This
simple inheritance avoids a thinness-at-infinity criterion.

## Superlevel-component exhaustion

For continuous subharmonic u, every component D of {u>c} is open. Its finite
boundary satisfies u=c. Indeed a boundary point with u<c cannot be approached
from D, while a point with u>c has a connected ball in {u>c} meeting D, so
belongs to the same component and cannot be a boundary point.

The function

    v_D(x) = u(x)-c for x in D, and 0 otherwise

is continuous, nonnegative and locally subharmonic, hence entire subharmonic.
Inside D this is immediate; away from its closure it is locally zero; at the
boundary its value is zero and every sufficiently small spherical mean is
nonnegative. Continuity at boundary points uses u=c. A bounded component is
impossible: the maximum principle for u-c on its compact closure contradicts
u>c inside and u=c on the boundary. This last statement needs no smoothness
of the component boundary; an interior maximum would be a strict positive
maximum on a connected open set, forcing constancy there, contrary to its
boundary value.

If D is nonexceptional, then u is unbounded above in D: otherwise v_D is a
bounded nonzero witness contradicting nonexceptionality.

There are two exhaustive cases for sup u=infinity.

1. Every integer superlevel {u>j}, j>=1, is connected. Choose x_j with
u(x_j)>j+1. Join x_j to x_(j+1) by a finite polygon in {u>j}; open connected
sets in Euclidean space are polygonally connected. The resulting jth block
has u>j everywhere.
2. An integer superlevel {u>j0} has at least two components. At least one
component A0 is nonexceptional by the disjoint-domain lemma. In A0, u is
unbounded. Select x1 in A0 with u(x1)>j0+1, and let A1 be its component of
{u>j0+1}. Then A1 is contained in A0 and is nonexceptional by inheritance.
Inductively choose x_(k+1) in Ak with u(x_(k+1))>j0+k+1 and let A_(k+1)
be its higher-superlevel component. Each is nested, nonempty and has
unbounded u. Join x_k to x_(k+1) by a finite polygon within Ak, for k>=1.
The kth block has u>j0+k everywhere. Missing initial blocks are irrelevant.

Parametrize each finite polygon continuously on [k,k+1], with endpoints
matching. After finitely many blocks, every point of the curve, including
all segment interiors, lies above any prescribed H. Continuity of u bounds
it above on every compact spatial set K, so sufficiently high blocks avoid
K. Thus |gamma(t)| tends to infinity and only finitely many polygonal pieces
meet K. An unbounded sequence of vertices alone would not establish these
conclusions. Self-intersections in the finitely many earlier blocks are harmless.

## One-sided harmonic Liouville reduction

If entire harmonic u has finite upper bound M, let h=M-u >=0. At any center a,
differentiate the ball Poisson formula at its center to obtain

    partial_i h(a) = (n/R) integral theta_i h(a+R theta) d sigma(theta).

Nonnegativity and the mean-value identity give |partial_i h(a)| <= n h(a)/R
for every R>0. Sending R to infinity makes every derivative zero. Hence h,
and u, are constant. Therefore the nonconstant harmonic hypothesis supplies
sup u=infinity and the preceding construction. A positive entire harmonic
function is constant by the same argument. Constants do not satisfy the
asymptotic +infinity conclusion and are properly excluded.

The Poisson and component mechanism also works in dimension two. In dimension
one, entire harmonic functions are affine u(x)=ax+b; if a is nonzero the
appropriate half-line gives the conclusion. These extensions do not change
the source's n>=3 problem. Entire-domain assumptions are essential: bounded
positive harmonic functions exist on proper domains, for example h=1 on any
ball, and the large-radius limit cannot be taken there.

## Bounded subharmonic boundary control

For n>=3 define b(x)=-1 on |x|<=1 and b(x)=-|x|^(2-n) on |x|>1. This is
continuous, finite at the origin and nonconstant, with supremum zero.
Its distributional Laplacian is the nonnegative surface measure
(n-2) dS on the unit sphere: outside and inside the Laplacian is zero and the
outward normal derivative jumps from zero to n-2. Thus b is subharmonic.
It has no path along which b tends to +infinity. This disproves replacing
harmonic nonconstancy by mere subharmonic nonconstancy. Positive scaling or
adding a constant changes its supremum but does not make it unbounded above.
Using -|x|^(2-n) at the origin without truncation would change the finite and
continuous hypotheses and is not the example being used.

## Source receipt and attribution boundary

Read receipt: independent fetches completed on 2026-10-03 at 18:37:35Z and
18:37:38Z. Hayman-Lingham printed p60/PDF61 was read as extracted text and
visually checked in a local rendering. All five Carleson pages (printed
35-39) were read as complete extracted text and all five rendered pages were
visually checked. Full fetch/render hashes are in receipts/primary_*.json.

Hayman-Lingham Problem3.2 asks the harmonic claim above; Update3.2 credits the
asymptotic existence result to Fuglede and explicitly records polygonal
availability for the continuous/harmonic case, followed by Carleson's general
subharmonic result. Carleson's printed p35 states the unbounded-subharmonic
polygonal theorem and pp35-36 address the continuous case. The general
discontinuous approximation on pp36-39 was read but is not independently
recertified here. These credits preclude calling this a new solution.

The printed p35 thinness lemma has an apparent direction issue if interpreted
literally: a half-space has the bounded maximum-principle property while its
inverted complement is not thin at zero. The present mechanism proves the
needed disjoint-domain and inheritance facts directly, so this textual issue
does not become an unsupported dependency. No novelty certification follows
from a source editorial update.

## Baseline status

Strongest independently derived result: the full required harmonic path theorem,
and its continuous subharmonic unbounded-above version, with explicit Poisson
constants and complete component/all-tail reasoning. Remaining audit work is
comparison with all frozen target files, reproducibility and provenance checks.
The general discontinuous proof, smooth/injective path refinements, and any
novelty claim remain outside this verification. New authored discovery turns:0;
new theorems:0. Existing credited resolution:100%; audit workflow:40%.
