# Independent analytic reconstruction

Target: Zenodo 23306332, *Nonunique nearest stable complex quadratics*, dated
11 October 2026, six-page unrefereed preprint. This reconstruction was written
from the current published PDF/TeX and primary references, without using an
earlier mathematical verdict. Finite computations below are controls, not
proofs of infinite quantifiers.

## 1. Exact conventions and success criteria

The monic coefficient vector is `(Re a, Im a, Re b, Im b)` in real dimension
four for `z^2+a z+b`. Stability means maximum root real part at most zero;
imaginary-axis and multiple roots are included. Distances use a fixed real
symmetric positive-definite matrix G. It may mix any real coefficient
coordinates. The claim is `for every fixed G, for every neighborhood of 0,
there exists an unstable input in it with at least two distinct attained
global minimizers over the whole complex stable set`. It does not say every
nearby unstable input has a tie.

Full degree uses `(Re ell, Im ell, Re a, Im a, Re b, Im b)`, `ell != 0`, and
base `(1,0,0)`. Multiples with different leading coefficients are different
coefficient vectors in that space. Epigraph metrics may additionally mix
height and coefficients. Proposition 3 is only claimed in the real Euclidean
monic coefficient metric, relative to each specified finite limiting
subgradient, with constants allowed to depend on it.

## 2. Quadratic radical, closure, and boundary cases

If D=a^2-4b and w is either square root of D, the two real root parts are
`-Re a/2 +/- Re w/2`. Since `|Re w|=sqrt((|D|+Re D)/2)`,

    alpha(a,b) = -Re a/2 + Phi(D)/2,
    Phi(D) = sqrt((|D|+Re D)/2).

Both square roots give the same formula, including D=0. The formula is
continuous on all C^2. Hence S={alpha<=0} is closed and nonempty. Every
distance to it is attained in finite dimension: a minimizing sequence is
bounded by comparison with the stable base, and closure passes its convergent
subsequence to a minimizer. This establishes existence over all complex
competitors; no real-only optimization surrogate is used.

With a=x+iy, b=u+iv and z=w-iy/2, the transformed polynomial is
`w^2+xw+U+iV`, with `U=u+y^2/4`, `V=v-xy/2`. Stability is equivalent to

    x>=0, U>=0, V^2<=x^2 U.

To check necessity without an invalid squaring step, first require x>=0 and
`|x^2-4U-4iV|<=x^2+4U`. This implies U>=0. Once U>=0, the right side is
nonnegative, and squaring gives exactly `16 V^2<=16 x^2 U`.
Conversely the displayed three inequalities give the original nonnegative
radical bound. At x=0 this forces V=0 while U can be any nonnegative number;
at U=0 it again forces V=0. Thus distinct imaginary roots, a double imaginary
root, and the zero double root are included. In the real coefficient slice
the criterion reduces to the convex orthant a>=0,b>=0, with unique projection
for every fixed positive-definite real inner product.

## 3. The path and all real derivatives

For t>0 the polynomial factors as

    z^2+t^2 z+t^2+i t^3 = (z+i t)(z+t^2-i t).

Its roots are lambda=-it and mu=-t^2+it. The active root is simple and its
real-part gap is t^2>0. Consequently in a sufficiently small neighborhood of
this fixed coefficient vector alpha is the smooth real part of the lambda
branch. The neighborhood may shrink with t; a uniform gap is not needed.

Implicit differentiation gives

    d lambda = -(lambda da+db)/(2 lambda+a),
    2 lambda+a = t^2-2it.

For real directions `(da,db)=(1,0),(i,0),(0,1),(0,i)`, the real parts are

    -2/(t^2+4), -t/(t^2+4), -1/(t^2+4), 2/[t(t^2+4)].

Thus `grad alpha=gamma n_t`, where

    gamma=2/[t(t^2+4)],
    n_t=(-t,-t^2/2,-t/2,1).

Full-degree differentiation adds `-lambda^2 d ell/(2lambda+a)` and produces
leading components `t^2/(t^2+4)` and `-2t/(t^2+4)`. Hence the six-component
covector is exactly

    N_t=(t^3/2,-t^2,-t,-t^2/2,-t/2,1).

These computations include both real and imaginary leading-coefficient
directions; normalizing the polynomial and silently keeping a constant
pullback metric is unnecessary.

## 4. Actual proximal normals and the universal-metric obstruction

At fixed t, Taylor's theorem and alpha(c)<=0 give a local estimate
`n_t.(c-c_t)<=K_t ||c-c_t||_G^2` for stable c. For
`q_t=c_t+tau G^{-1}n_t`, subtracting the squared distance to c_t gives

    ||c-q_t||_G^2-||c_t-q_t||_G^2
      >= (1-2 tau K_t)||c-c_t||_G^2.

Choose tau>0 with `2tau K_t<1` (if K_t<=0 no such upper restriction is
needed). If the Taylor estimate holds in a metric ball of radius r about
c_t, also choose the geometric step
`tau ||G^{-1}n_t||_G<r/2`. For stable points outside the ball the triangle
inequality gives a strictly greater distance than the step. Thus c_t is an
actual global unique nearest point to q_t, and `G^{-1}n_t` is proximal.
Neither K_t nor tau has to be uniform as t tends to zero.

Now `c_t=t^2 e+t^3 f`, `e=(1,0,1,0)`, `f=(0,0,0,1)`, and `n_t->f`.
The representing vectors converge to `G^{-1}f`, so this is a limiting normal
at zero under the primary PRT definition using proximal normals. However,

    f.c_t=t^3,
    ||c_t||_G^2=t^4(E+2t C+t^2 F),
    E=e^T G e>0, C=e^T G f, F=f^T G f>0.

For any fixed tau>0, the squared distance difference against zero along
the target `tau G^{-1}f` is

    t^4(E+2t C+t^2 F)-2tau t^3.

For 0<t<=1, set K=E+2|C|+F. This difference is negative whenever
`0<t<min(1,2tau/K)`. The competitors c_t tend to zero. Therefore the
limiting normal is not even locally proximal. Every metric here is fixed
before choosing t; no uniformity over all matrices or degenerating metrics
is claimed or needed. The same argument in full degree uses zero leading
displacements and the corresponding six-dimensional E,C,F.

## 5. The imported projection theorem and the global quantifier

PRT2000 Definition 1.1 requires a closed set, a point in the set, and a
specified limiting normal. It gives local unique projection to a localized
set along that normal when prox-regularity holds. In particular the normal
would have local quadratic support, contradicted by Section 4. Proposition
1.2 also supplies the equivalent local quadratic-support formulation.

PRT2000 Theorem 1.3(a),(k), printed p5234, says that prox-regularity and
single-valued metric projection on a neighborhood are equivalent for a
closed set when relative local weak closedness holds. The latter is automatic
in finite dimension, as explicitly stated there. The metric projection is
the global P_C, not projection onto a selected smooth boundary chart.
Applying the theorem after a linear isometry from G to Euclidean space is
valid. Since S is closed and all projections are nonempty, its failure of
prox-regularity implies that every neighborhood contains a target whose
global projection has at least two elements. A stable target has only itself
at distance zero, so these targets are unstable. This is a theorem-based
existence proof, not an explicit construction of a target/minimizer triple.

For full exact degree, global closure fails. Choose a closed G-ball B of
radius R about the base, wholly inside ell!=0. Abscissa is continuous there
by `(ell,a,b)->(a/ell,b/ell)`, so C=S_full intersect B is nonempty compact.
The path is in the interior of B for small t; local proximal normals are
unchanged, and the same nearby competitors prove that the limiting normal
is not locally proximal to C. Apply the closed-set theorem to C.

For a resulting target q with `||q-base||_G<R/3`, every point outside B
and every point on its boundary has distance at least
`R-||q-base||_G>2R/3`. The stable base is at distance less than R/3. Thus
none of these points can minimize. Every C-minimizer is interior to B and
is also a global S_full-minimizer; conversely any S_full-minimizer must be
one of these C-minimizers. Existence comes from compact C. Taking targets
in an arbitrarily small intersection with this R/3 ball proves the full
neighborhood quantifier and global attainment. The target has ell!=0 and
cannot be stable, by the same distance-zero observation.

## 6. Whole epigraphs and mixed height metrics

At `(c_t,0)` the epigraph constraint `alpha(c)-r<=0` is smooth. Its outward
normal covector `(gamma n_t,-1)` can be positively scaled to

    v_t=(n_t,-1/gamma) -> (f,0),
    1/gamma=t(t^2+4)/2.

The fixed-t smooth Taylor and remote-point exclusion argument works in every
fixed positive-definite real coefficient/height metric H. Thus H^{-1}v_t are
proximal normal vectors. Pairing the limiting covector with `(c_t,0)` gives
t^3, while its squared H-distance from the base has a positive quartic
leading term. The same calculation as Section 4 excludes local proximality
of H^{-1}(f,0). Monic epi(alpha) is closed by continuity; the full epigraph
is locally closed inside ell!=0. Replacing n_t by N_t proves its claim.
The limit is horizontal as a covector. H^{-1} can tilt its vector
representative when H mixes height and coefficients; horizontality of the
vector is not used.

## 7. Function prox-regularity at every finite subgradient

Write L=(-infinity,0] in C. For D outside L, Phi is smooth and direct
differentiation yields

    grad Phi=(Phi/(2|D|), Im D/(4|D| Phi)),
    ||grad Phi||^2=1/(4|D|).

The algebra uses `2Phi^2=|D|+Re D`; no limiting expression is substituted
at a zero denominator. At D=-s<0, rationalization yields

    Phi(-s+h)=|Im h|/[sqrt(2(|-s+h|+s-Re h))]
             = |Im h|/(2sqrt(s))+O(|h|^2).

The regular and proximal subdifferentials are consequently the pure imaginary
interval `iq`, `|q|<=1/(2sqrt(s))`. The limiting subdifferential is the same:
nearby on-ray intervals converge to it, while the two off-ray gradients
approach its endpoints. This checks the endpoints as well as the interior.

For |D|<=delta,

    Phi(D)>=dist(D,L)/(2sqrt(delta)).

If Re D>=0, dist=|D| and `Phi>=sqrt(|D|/2)`, which is stronger than the
claimed bound. If Re D<0, the rationalized denominator is
`sqrt(2(|D|-Re D))<=2sqrt(delta)` and dist=|Im D|. At D=0 the statement
is interpreted directly as 0>=0.

For any finite q with Re q>=0, convex normal support to L gives
`q.D<=|q|dist(D,L)`. Choosing delta sufficiently small shows that q has
local linear lower support to Phi at zero, hence is both regular and
proximal. Conversely testing increments along the negative real ray forces
Re q>=0 for a regular subgradient. To audit limiting subgradients at zero:
off-ray gradients diverge in norm, and bounded on-ray subgradients have zero
real part. Points exactly at zero already supply the full half-plane.
Therefore all three subdifferentials at zero are
`N_L(0)={q:Re q>=0}`.

The map T(a,b)=(a,a^2-4b) is a global real C-infinity diffeomorphism with
explicit inverse `(a,D)->(a,(a^2-D)/4)`. Regular lower supports transform
by its Jacobian in both directions; proximal lower supports transform in
both directions using bounded local second derivatives and a local
bi-Lipschitz bound; limiting supports transform by continuity of the
Jacobian/inverse and of the function. Adding the smooth linear `-Re a/2`
and multiplying by 1/2 therefore gives exactly

    v_a=(-1/2,0)+conjugate(a) q, v_b=-2q,
    q in partial Phi(D).

In particular, `partial alpha(0,0)` consists of
`(-1/2,0,b_R,b_I)` with b_R<=0. This description follows independently
from the diffeomorphism, rather than from an unconditional chain-rule
equality citation.

Fix finite v0 in this subdifferential. Restrict v to a bounded neighborhood
of v0. Since v_b=-2q, choose a common M>=1 with |q|<=M. Choose a coefficient
ball whose discriminants satisfy `|D|<delta=1/(16M^2)`. If a base x in it
with v near v0 had D_x outside L, its only q would satisfy
`|q|=1/(2sqrt(|D_x|))>2M`, a contradiction. Hence D_x lies on L,
Phi(D_x)=0 and q is in the convex normal cone N_L(D_x).

For every comparison point y in the ball, let z be its nearest point to
L. Then

    q.(D_y-D_x) = q.(D_y-z)+q.(z-D_x)
                <= M dist(D_y,L) <= Phi(D_y).

The exact discriminant increment is
`D_y-D_x=J_D(x)Delta+(Delta a)^2`. Consequently

    alpha(y)-alpha(x)-v.Delta
      >= (1/2)q.(Delta a)^2
      >= -(M/2)|Delta a|^2 >= -(M/2)||Delta||^2.

Replacing curvature M by M+1 gives strict inequality for y!=x, exactly as
PR2010 Definition 1.1 demands. The estimate holds for all such base x and
comparison y and all subgradients near v0. Thus it is uniform in that
localized set. It even holds without the extra function-value restriction,
so the function-attentive requirement is satisfied. Continuity follows
from the radical formula. No constant uniform over every finite v0 is
asserted.

PR2010 Theorem 3.1 is a sufficient prox-regularity composition theorem with
a horizon constraint qualification and prox-regularity assumptions on the
outer function. It is not itself an unconditional exact subdifferential
identity. The manuscript's nearby citation is imprecise for that identity,
but its explicit two-sided diffeomorphism argument above supplies the
needed equality without that misuse. The original theorem's hypotheses
also fit T with an invertible Jacobian once the scalar function estimate
is supplied, but no circular invocation is necessary.

PR2010 p205 gives the function/epigraph correspondence at `(v0,-1)`.
The normal in Section 6 has limiting last component zero instead. Along
the stable path `||grad alpha||=gamma ||n_t||` diverges, so it does not
remain in a fixed finite-subgradient neighborhood. There is no conflict
between the epigraph set failure and Proposition 3.

## 8. Falsifiable controls and exact remaining gap

`evidence/independent_exact.py` was written independently without importing
submitted code. Its 4305 exact rational assertions include 625 complex-root
chart cases, all six real implicit derivatives at 64 nondyadic rational t,
mixed positive-definite metric controls in dimensions 4,5,6,7, exact radical
inequalities by sign-aware squaring, and 609 full coefficient lower-support
checks. Mutants dropping x>=0 or U>=0 are rejected. On D=0, a purely
imaginary coefficient change gives the exact adverse deficit `-M h^2/2`;
using half the curvature or omitting the quadratic discriminant term fails.
These controls would expose relevant sign, branch, and curvature mistakes.

The two current submitted mathematical scripts were fully statically read,
copied byte for byte to `quarantine/`, and executed with isolated Python
from that owned folder. Both exited zero. The exact helper performs 2005
assertions; the Decimal helper reports 45 scalar boundary cases and 1200
coefficient support cases. Decimal checks are not interval certificates.
Their finite successes do not prove the universal-metric or global-nearest
quantifiers; Sections 2-7 and PRT's theorem provide that argument.

The strongest verified mathematical result is all four stated claims C1-C4
under their precise conventions. No central mathematical gap was found.
This lane did not prove firstness, present-day openness, an all-degree or
real-only classification, an explicit tied target/minimizer triple, or
uniformity over varying/degenerate metrics. Original Cross, Moses-Liu and
Bottema bodies remain unread/inaccessible in the supplied cache; their
specific historical attributions are not independently certified here.
This is a bounded bibliographic gap and does not support a novelty claim.
