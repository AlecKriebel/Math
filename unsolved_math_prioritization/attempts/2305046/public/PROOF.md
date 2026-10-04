# MacLane's arc-tract problem: partial results and construction obstructions

## 1. Exact target and outcome

Let D = {z in C: |z| < 1} and T = boundary D. A nonconstant holomorphic
function belongs to the MacLane class A when the boundary points at which it
has a point asymptotic value are dense in T. A point asymptotic value can be
finite or infinity: it is a limit along a continuous path in D ending at one
specified point of T.

Problem 2305046 / AMR-022-5046, Hayman--Lingham Problem 5.46, asks whether
there exists f in A such that f'(z) is nonzero for every z in D, and compact
arcs Gamma_n in D approach a nondegenerate compact boundary arc K while
min_{Gamma_n}|f| tends to infinity. We use Hausdorff convergence for the arcs,
as in the standard Koebe-arc formulation. For functions in A the equivalence
with the inverse-tract formulation is a published theorem, not an extra
assumption that may be applied to arbitrary functions.

**Outcome: unsolved.** No function satisfying all three requirements is
constructed, and no general impossibility proof is given. Five distinct
approaches have been completed and their precise gaps are recorded. The
proofs below establish partial results and exclusion tests. No novelty is
claimed for them.

A boundary path merely satisfying |z(t)| -> 1 need not end at a single boundary
point. This distinction is essential. An inverse tract with end T is also not
automatically a *global tract* in the stronger sense used in the 2017 paper.
Nothing below identifies these notions.

## 2. Explicit imported results

These are dependencies, not results independently proved here. Their stated
hypotheses and locations were checked against the sources in SOURCE_GATE.md.

- **D1, derivative criterion.** For a nonlinear holomorphic f with f' nowhere
  zero, f in A with no arc tracts is equivalent to f' in A. Source: Barth--Rippon
  (2002), as stated in Barth--Rippon--Sixsmith (2017), Theorem B, p. 860.
- **D2, growth criterion.** If I(h) = integral_0^1 log^+ log^+ M(r,h) dr is
  finite, a nonconstant holomorphic h belongs to A. Source: Hornblower (1971),
  restated in the 2017 paper, equation (4.1), p. 866, and Charpentier et al.
  (2025), Theorem 3.2.
- **D3, singular-value obstruction.** For f in A with bounded critical values,
  bounded finite asymptotic values exclude arc tracts. Source: 2017, Theorem 1(a).
- **D4, two-point obstruction.** If an A-function has an arc tract and infinity
  is monotonically accessible at two interior points of its end, its critical
  values are unbounded in a boundary neighbourhood between them. Source:
  2017, Theorem 6, pp. 863--866.
- **D5, boundary consequence.** At interior points of an A-function's arc-tract
  end there are no finite point asymptotic values. Source: Barth--Rippon
  (2004 volume/2005 issue), Theorem A(a)(ii), p. 406.

“Monotonically accessible” concerns the *image curve*: sufficiently large
circles each meet it in exactly one point. It is stronger than tending to
infinity. “Finite asymptotic values” in D3 includes limits along general
boundary paths, not only paths ending at a point.

The nonlinearity proviso in D1 removes a harmless convention issue: A is defined
for nonconstant functions, whereas the derivative of an affine map is constant.
Affine maps are bounded on D and plainly cannot answer the problem. They are
handled directly whenever a derivative criterion is used.

We also use standard elementary complex analysis: existence of a holomorphic
logarithm of a zero-free function on a simply connected domain, Cauchy's
estimate, the identity theorem, and Liouville's theorem. The proper-covering
fact needed in Proposition 6 is justified there.

## 3. Logarithmic derivatives and an exact reformulation

### Proposition 1 (primitive parametrization)

Every holomorphic f on D with f' nowhere zero has the form

    f(z) = c + integral_0^z exp(g(w)) dw,

where g is holomorphic on D. Conversely, every function of this form has
nowhere-zero derivative. Among nonlinear functions the target is therefore
exactly the problem of finding g for which its exponential primitive F belongs
to A but exp(g) does not belong to A.

**Proof.** Since D is simply connected and f' has no zeros, choose a
holomorphic logarithm g of f'. Integrating f' proves the formula, with c=f(0).
Conversely differentiation gives F'=exp(g), which never vanishes. If F is
nonlinear and belongs to A, D1 says it has no arc tracts if and only if exp(g)
belongs to A. Taking the negation proves the reformulation. If g is constant,
F is affine and is already excluded. QED.

This equivalence does not solve the problem. Merely producing exp(g) outside A
leaves membership of its primitive in A unproved.

### Proposition 2 (what polynomial approximation does certify)

For each locally univalent f on D, there is a sequence of entire locally
univalent functions F_n converging to f uniformly on compact subsets of D.
Every F_n is bounded on the closed unit disk, belongs to A, and has no
high-modulus arc sequence. These finite-stage properties do not furnish a
boundary certificate for the limit.

**Proof.** Let p_n be the Taylor polynomials of the g in Proposition 1 and put
F_n(z)=f(0)+integral_0^z exp(p_n(w))dw. These are entire, with
F_n'=exp(p_n), so their derivatives do not vanish. If |z|<=r<1, integration
along the segment from 0 to z gives

    |F_n(z)-f(z)| <= r sup_{|w|<=r}|exp(p_n(w))-exp(g(w))| -> 0.

Entire F_n extend continuously to the closed disk, so they have finite radial
limits at all boundary points and are bounded there. This proves the assertions
about each F_n. The displayed bound is on a fixed compact disk only; it makes
no assertion for r tending to 1 with n. QED.

For example, even the simpler sequence z^n tends to zero on compact subsets
while its supremum on D is one. Thus a compact-convergence estimate cannot
silently be used as an estimate on boundary-approaching arcs. This example is
only an illustration of the topology, not a locally univalent candidate.

## 4. A complete quantitative growth exclusion

Define log^+ x=max(log x,0), with log^+0=0. Set

    L(x) = log(1+log^+ x),
    J(h) = integral_0^1 L(M(r,h)) dr.

For a>=0, 0<=log(1+a)-log^+a<=log 2 (with log^+0=0).
Consequently J(h) is finite if and only if I(h) from D2 is finite.

### Proposition 3 (Cauchy transfer)

For every holomorphic f on D,

    J(f') <= 2 J(f) + 1 + log 2.

In particular, any solution of Problem 5.46 must have both J(f)=infinity and
J(f')=infinity.

**Proof.** Put s=(1+r)/2 and delta=(1-r)/2. Cauchy's estimate on the circle of
radius delta around each point |z|=r gives

    M(r,f') <= [2/(1-r)] M(s,f).

Let a=log^+ M(s,f) and b=log(2/(1-r)), both nonnegative. Then

    L(M(r,f')) <= log(1+a+b)
                  <= log(1+a)+log(1+b).

The second inequality is just 1+a+b <= (1+a)(1+b). Integrating, the first term
is 2 integral_{1/2}^1 L(M(s,f)) ds, at most 2J(f). The second term is at most
integral_0^1 b dr = log 2 + 1, since log(1+b)<=b. All estimates remain valid
for zero or constant functions under the stated conventions.

Now suppose f answers the target. It is not affine. By D1, f' is not in A.
The contrapositive of D2 gives J(f')=infinity. The displayed inequality then
forces J(f)=infinity. QED.

### Corollary 3.1 (a broad class of explicit attempts fails)

If f is locally univalent and for some C>0 and 0<=alpha<1 it satisfies,
for all sufficiently large r,

    M(r,f) <= exp(exp(C/(1-r)^alpha)),

then f cannot answer the target. Indeed L(M(r,f)) is bounded above by a
constant plus C/(1-r)^alpha, which is integrable. Proposition 3, D2 and D1
exclude arc tracts (with the affine case handled directly).

Failure of this upper bound when alpha>=1 is **not** evidence of existence.
D2 is sufficient, not necessary. The borderline integral alone gives no
construction and no converse theorem.

## 5. Inverse coverings and a fully analyzed near-miss

### Proposition 4 (necessary singular-value behaviour)

Any solution must have an unbounded set of finite asymptotic values.

**Proof.** Its critical-value set is empty, because f' never vanishes. If its
finite asymptotic values were bounded, D3 would exclude its arc tract. QED.

The inverse-function approach therefore cannot impose a bounded singular-value
set. Moreover, absence of critical points does not say that inverse branches
continue across finite asymptotic values. An argument claiming “f' nonzero,
therefore a covering over the entire image” has omitted this obstruction.

### Proposition 5 (exponential Cayley map)

Let C(z)=(1+z)/(1-z) and E(z)=exp(C(z)). Then:

1. E' never vanishes on D;
2. E belongs to A;
3. its finite asymptotic-value set is exactly the unit circle;
4. its high-modulus inverse regions shrink to the boundary point 1, and it has
   no arc tract of the target kind.

**Proof.** C maps D biholomorphically to the right half-plane, and
E'(z)=2 exp(C(z))/(1-z)^2 is nonzero. E extends holomorphically across every
boundary point other than 1. It therefore has finite radial limits on a dense
set and belongs to A.

Its modulus is greater than one throughout D. Suppose E(z(t))->a is finite
along a boundary path, so |a|>=1 and a is nonzero. Choose a disk about a that
avoids zero, with a holomorphic logarithm ell. For sufficiently late t,

    C(z(t)) - ell(E(z(t))) is in 2 pi i Z.

It is continuous on a connected tail, hence constant. Thus C(z(t)) tends to a
finite value w0. Since z(t)=(C(z(t))-1)/(C(z(t))+1) tends to the boundary,
Re w0=0. Therefore |a|=1. Conversely, for every real y the boundary value at
zeta=(iy-1)/(iy+1), reached radially, is exp(iy). This yields every value of
modulus one and proves item 3, even for general boundary paths.

For R>1, put l=log R. The set |E(z)|>R is the disk

    |z - l/(l+1)| < 1/(l+1).

This follows by expanding Re C(z)=(1-|z|^2)/|1-z|^2 > l. These disks shrink to
1 as R tends to infinity. If compact arcs Gamma_n had minimum modulus tending
to infinity, then for every R they would eventually lie in this disk. Their
Hausdorff limit could only be {1}, never a nondegenerate arc. QED.

This example has infinite valence: if |a|>1, all points obtained from
C(z)=Log a+2 pi i k, k in Z, are distinct preimages in D. Consequently replacing
local univalence with finite valence would discard relevant complexity.

## 6. Geometric attempts: what paths and closed barriers permit

### Proposition 6 (closed high barriers are impossible)

Let f be holomorphic on D with nowhere-zero derivative. There cannot be Jordan
domains Omega_n with closures compactly contained in D, all containing one
fixed point z0, such that

    min_{boundary Omega_n}|f| -> infinity.

The domains need not be nested.

**Proof.** Fix R>|f(z0)| and choose n so that |f|>R on boundary Omega_n. Let V_R
be the component of f^{-1}({|w|<R}) containing z0. It cannot cross boundary
Omega_n: an open connected planar set is path connected, and such a path
would meet a point where |f|>R. Thus V_R is contained in Omega_n. Its closure
is compact in D. At each point of its boundary, |f|=R: a boundary point with
|f|<R has a neighbourhood in the same preimage component, a contradiction.

Hence f:V_R -> {|w|<R} is proper. To check this explicitly, the inverse image
in V_R of a compact subset of {|w|<R} cannot accumulate at boundary V_R and is
therefore compact. The image is both open and closed in the disk (closedness
follows from properness by extracting a convergent inverse-image subsequence),
so it is the whole disk.

A proper holomorphic map without critical points is a covering: each fiber is
a compact discrete set, hence finite; take local inverse neighbourhoods at its
points, and properness prevents additional preimages from entering when the
target neighbourhood is sufficiently small. A connected covering of a simply
connected disk has one sheet. For completeness, lift paths from a chosen base
point; homotopic paths have the same lift endpoint by the local inverse
property, so simple connectedness supplies one global inverse. Thus f is
biholomorphic on V_R.

The preceding construction works for every R>|f(z0)|. The V_R are nested and
exhaust D: for any z in D, a compact path from z0 to z has bounded f-image and
lies in V_R once R is sufficiently large. It follows that f is injective on D
and has image C. Its inverse would be a bounded entire map C->D, contradicting
Liouville. QED.

An open arc near a proper boundary arc is not the boundary of a relatively
compact Jordan domain surrounding a fixed point. Closing its two ends adds
pieces where no lower modulus estimate is known. That missing estimate is
exactly why this proposition does not solve Problem 5.46.

### Proposition 7 (bounded variation of the derivative along a path)

Let gamma:[0,1)->D be locally C^1 and tend to zeta in T. If
h(t)=f'(gamma(t)) has finite total variation on [0,1), then f(gamma(t)) tends
to a finite limit. No finite-length assumption on gamma is needed.

**Proof.** h has a finite limit h1. On every compact parameter interval,
ordinary integration by parts gives

    f(gamma(t))-f(gamma(0))
      = gamma(t)h(t)-gamma(0)h(0) - integral_0^t gamma(s) dh(s).

The Stieltjes integral converges as t tends to 1 because |gamma|<=1 and the
total variation of h is finite. The product gamma(t)h(t) tends to zeta h1.
All terms on the right therefore have finite limits. Also, for every t,

    |f(gamma(t))-f(gamma(0))|
        <= |h(t)|+|h(0)|+Var_{[0,t]} h.

QED.

By D5, a putative solution cannot have such a derivative-BV path to an interior
point of an arc-tract end. By D4 its tract interior contains at most one point
where infinity is monotonically accessible. These are necessary obstructions,
not a proof that all asymptotic paths have bounded variation or can be
straightened. Local univalence of f gives no corresponding control over f''
or the variation of f' along a path.

## 7. Universal radial approximation produces the wrong boundary class

An Abel universal function is a holomorphic f on D such that, for every proper
compact K subset T and every continuous phi:K->C, there exist r_n increasing
to 1 with sup_{zeta in K}|f(r_n zeta)-phi(zeta)|->0. Such functions are known
to exist; we do not reconstruct that existence theorem. The following
incompatibility is proved directly from the definition, and agrees with
Charpentier--Manolaki--Maronikolakis (2025), p. 873.

### Proposition 8 (universal approximation cannot give an A-example)

Every Abel universal f has high-modulus arcs approaching any fixed proper
nondegenerate boundary arc, but has no point asymptotic value at any boundary
point. In particular f is not in A.

**Proof.** Fix a compact proper boundary arc K. For each positive integer n,
universality for the constant n+2 lets us choose r_n>max(r_{n-1},1-1/n) with
sup_K |f(r_n zeta)-(n+2)|<1 (start with n>=2). The arcs r_n K approach K,
and their minimum modulus exceeds n+1.

Now take any continuous gamma:[0,1)->D tending to a specified zeta in T. Choose
a proper compact arc K whose relative interior contains zeta. For any a in C,
universality supplies radii s_n->1 on whose scaled arcs s_n K the values of f
converge uniformly to a. Eventually gamma lies in the angular sector over the
interior of K. By the intermediate value theorem applied to |gamma(t)|, it
meets the circle of radius s_n within that tail, for all sufficiently large n.
Choose meeting times t_n. They tend to 1, because each initial compact path
segment has modulus bounded away from 1. Thus f(gamma(t_n))->a.

Applying this to two distinct finite a excludes a finite limit, and applying it
to a=0 excludes an infinite limit. Since gamma and zeta were arbitrary, there
are no point asymptotic values. QED.

The first half produces exactly the easy boundary-arc behaviour one might want
from Runge or Baire-category approximation. The second half destroys the
MacLane condition. An infinity-asymptotic *general* boundary path with more
than one boundary accumulation point is not contradicted by this proposition.
No claim that these universal functions have nonvanishing derivative is made.

## 8. Precise residual target and verification boundary

What remains is to construct a nonlinear g whose primitive F=int exp(g) is
in A but whose derivative exp(g) is outside A, or to prove that impossible.
A construction must also survive the unbounded finite-asymptotic-value
requirement and the path restrictions above. An alternative contradiction must
use only open-arc geometry, without inserting closed barriers, bounded
singular values, growth integrability, or monotone accessibility as extra
hypotheses.

Propositions 1--8 have complete proofs of their stated partial conclusions.
D1--D5 and existence of Abel universal functions remain explicitly external
inputs. The computation checks selected algebra, growth-threshold controls,
and reproducibility metadata; it does not prove these inputs, decide MacLane
membership, construct an infinite boundary object, or establish the full
problem. The original target remains unsolved after five approaches.
