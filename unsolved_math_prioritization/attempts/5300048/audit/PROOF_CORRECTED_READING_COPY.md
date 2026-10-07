# Periodic points on an attracting-basin boundary

Problem 5300048 / AMR-052-0048, rank 954. Research date: 7 October 2026.

**Disposition: unresolved after five substantive mathematical approaches.**
This note contains auxiliary results and precise failures of attempted arguments. It
does not claim a solution, a dynamical counterexample, historical novelty, or an
independent audit. All five approaches below were performed for this question;
source retrieval, duplicate checking and packaging are not counted as approaches.

## 0. Exact scope and source distinction

The primary problem is F. Przytycki, *On Invariant Measures for Iterations of
Holomorphic Maps*, in *Problems in Holomorphic Dynamics*, IMS 1992/7, printed
pp.29–30: https://www.math.stonybrook.edu/preprints/ims92-7.pdf .

Its attracting-basin setting is a simply connected domain U in the Riemann sphere,
a proper holomorphic self-map f:U→U of degree d≥2, and f^n→a∈U. The extension
is holomorphic on a neighborhood of the spherical closure of U. The question
asks whether every periodic q∈∂U is accessible by a continuous curve whose
remaining points lie in U. The source explicitly includes the polynomial basin
at infinity. It does not restrict to bounded polynomial basins. The catalogue's
notation f:U→f(U) must be read together with this self-map setting.
The cases U equal to the sphere or to the sphere minus one point have
empty or singleton boundary and are immediate. In the remaining case U
is hyperbolic and the Riemann maps used below exist.

The word “repelling” is absent from the printed question, as it is from the
catalogue. This matters. The repelling theorem in Przytycki (1994), Theorem D,
requires both shrinking coding-tree edges and local preservation of the basin
by the inverse return branch. Its Theorem A has the analogous basin-side
condition. Neither is a theorem about every neutral periodic point. See
https://www.impan.pl/~feliksp/access.pdf , especially pp.260, 265–270.

Roesch–Yin (2008), Theorem 1, proves that the boundary of a bounded polynomial
Fatou component not eventually a Siegel disk is a Jordan curve. Thus the whole
boundary of a bounded polynomial attracting basin is accessible by Carathéodory's
theorem. This is an imported prior theorem, not a result of the present work:
https://doi.org/10.1016/j.crma.2008.06.004 . It does not settle the stated general
rational/local-holomorphic setting or the neutral-point question at infinity.

## 1. Approach one: produce a neutral counterexample from a hedgehog

### 1.1 First classify the possible multiplier

Let q have period m and put h=f^m, so h(q)=q. Assume f extends as above.

**Lemma 1.** A boundary periodic point cannot be attracting or a linearizable
irrationally indifferent point. Nor can a positive iterate of its germ be the
identity.

**Proof.** If |h'(q)|<1, choose a small disk around q, disjoint from a, in which
all h-orbits converge to q. This disk intersects U because q∈∂U. An orbit of
a point in that intersection would converge both to a and q, a contradiction.
If h is conjugate near q to an irrational rotation, choose a small invariant
linearization disk disjoint from a. Orbits starting there stay in its compact
closure. A point of U in that disk cannot have h^n(z)→a, again a contradiction.
If h^k is the identity near q, there is a small open set meeting U on which
h^k(z)=z. Taking any point there different from a gives the same contradiction.
All the finitely many intermediate iterates can be defined on a sufficiently
small neighborhood of the periodic orbit by continuity. ∎

This leaves repelling, parabolic, and nonlinearizable irrationally indifferent
periodic points. For a repelling point the Lyapunov exponent equals
log|h'(q)|/m>0. For the last two types it is zero. Consequently one cannot
reduce the literal problem to the positive-exponent question 5300049.

### 1.2 The precise proposed negative construction

Biswas, *Positive area and inaccessible fixed points for hedgehogs*,
arXiv:1010.4496v4, Theorem 1.2, constructs a nonlinearizable germ with an
invariant full compactum K whose fixed point p is inaccessible from the
complement. The theorem is about a local germ:
https://arxiv.org/abs/1010.4496 . We use exactly version 4's inaccessibility conclusion and do not import
any stronger assertion about all prime-end impressions.

Here is the exact way such a construction would refute our problem if a
suitable global realization were supplied.

**Lemma 2 (transfer of inaccessibility).** Let K⊂L be compact subsets of the
sphere, p∈K, and suppose p is inaccessible from the sphere minus K. If
p∈∂(sphere minus L), it is inaccessible from every domain contained in
the sphere minus L.

**Proof.** A proposed access curve in such a domain, excluding its endpoint,
would also lie in the sphere minus K, contradicting the hypothesis. ∎

In particular, a polynomial P with connected filled Julia set K(P), a periodic
p∈J(P), and a contained compactum K⊂K(P) making p inaccessible would give
a counterexample: U=sphere minus K(P) is simply connected, infinity is an
attracting point in U, P|U has degree deg P, and P is holomorphic as a map
of the sphere. The missing item is an actual polynomial and contained K
with the stated inaccessibility property for its periodic point.

There is a real obstruction to the immediate shortcut U=sphere minus K.

**Lemma 3 (direct hedgehog-complement obstruction).** Suppose K is a nonempty
compactum of empty interior. Suppose a map g is holomorphic and one-to-one
on a neighborhood of K and g(K)=K. There cannot be a holomorphic map F
on a neighborhood of the closure of U=sphere minus K which agrees with g
near K and restricts to a proper self-map U→U of degree at least two.

**Proof.** Since K has empty interior, closure(U) is the whole sphere. Thus F
would be a nonconstant rational map on the sphere. Because F(U)⊂U, every
preimage of a point y∈K lies in K. The equality g(K)=K gives one such preimage,
and one-to-one holomorphy near K makes it unique and of local degree one.
The global degree of F, computed by counting preimages with multiplicity,
would therefore be one. Its restriction cannot have degree at least two. ∎

This is stronger than saying the germ's domain is too small: even an extension
of this particularly direct construction would have the wrong degree. It
does not preclude embedding a hedgehog in a larger filled Julia set.

The alternative “red dwarf Julia set” route is conditional as well. Blokh–
Oversteegen, arXiv:0809.1071, Lemma 5.3, proves inaccessibility of the fixed
Cremer point for a red-dwarf Julia set; it does not establish the existence
of such a polynomial. The separate solar-existence result of Blokh–Buff–
Chéritat–Oversteegen does not supply a red-dwarf example. Their distinction
must not be collapsed. Sources: https://arxiv.org/abs/0809.1071 and
https://arxiv.org/abs/0812.1239 .

**Gap after approach one.** No polynomial/rational realization of an
inaccessible neutral periodic point satisfying the full basin hypotheses was
verified. No counterexample follows from the local-germ theorem alone.

## 2. Approach two: control the other inverse-basin components

The repelling inverse function contracts in the ambient surface, but may
send points into a different component of the attracting basin. We tried to
exclude this using the finite degree of a rational map.

**Lemma 4 (finite-component criterion).** Let R be a rational map of degree
D≥2 and U an invariant immediate attracting basin. Let q∈∂U be repelling
of period m, and put h=R^m. If q belongs to the boundary of no component
of h^{-1}(U) other than U, then q satisfies local backward invariance:
there is a neighborhood V and a contracting local inverse H of h fixing q
such that H(V∩U)⊂U.

**Proof.** The open set h^{-1}(U) has finitely many components: every component
maps properly and surjectively to U, and their positive degrees sum to D^m.
To see properness of a restriction, the inverse of a compact subset of U
is compact in the sphere and cannot have a limit point on a component
boundary, since such a point would still belong to the open set h^{-1}(U).
The image is both open and closed in the connected set U, hence is U.
Finiteness also follows by choosing a regular value in U and counting its
D^m preimages.

Write the other components as V_1,...,V_s. Because h(q)=q∉U, q is in none
of their interiors. The assumed boundary exclusion therefore implies
q∉closure(V_j) for every j. Finiteness gives a neighborhood W of q disjoint
from all those closures. A repelling fixed point of h has a local inverse
H fixing q. In a coordinate centered at q, H'(q)=1/h'(q) has modulus less
than one. Shrink to a round disk V with closure(V)⊂W, H(V)⊂V, and a
uniform derivative bound |H'|≤ρ<1. For z∈V∩U, h(H(z))=z∈U, so H(z)
belongs to h^{-1}(U). It lies in V⊂W, hence in none of V_1,...,V_s. It must
lie in U. ∎

**Corollary 5 (credited accessibility consequence).** Under Lemma 4's
hypotheses, q is accessible from U. Consequently an inaccessible repelling
periodic point in this rational setting would have to lie on the boundary
of another component of (R^m)^{-1}(U).

**Proof.** We verify every hypothesis of the good-point theorem
(Theorem A) of Przytycki (1994), printed p.260, for the rational map h=R^m.
The set U is still an invariant immediate attracting basin for h, and q is
its repelling fixed boundary point. Choose a sufficiently small metric ball
V=B(q,r) whose closure lies in the domain of the local inverse H, with
H(V)⊂B(q,ρr) for some ρ<1. We can arrange that H is ρ-Lipschitz there:
its derivative norm is less than one at q and stays so on a sufficiently
small geodesically convex ball. Lemma 4 also gives H(V∩U)⊂U.

For k≥1, the component of h^{-k}(V) containing q is exactly H^k(V).
Indeed H^k is univalent on a neighborhood of closure(V), h^k∘H^k is the
identity there, and h^k maps the boundary of H^k(V) to ∂V. A path in
h^{-k}(V) therefore cannot leave H^k(V). Open connected subsets of the
sphere are path connected, proving the component assertion.

In the notation of that theorem the pullback B_{n,l} is H^{n−l}(V).
Take Δ=1, δ=(1−ρ)r/2, and κ=1/2. For every n≥1 and 0≤l≤n−1,

    B_{n,l} ⊂ B(q,ρ^{n−l}r) ⊂ B(q,r−δ).

Thus every positive n is a good time for (0.1), and (0.0) holds with
κ=1/2. Also diam(B_{n,0})≤2ρ^n r→0, verifying (0.2).
Finally, if x∈h^{-n}(U)∩H^n(V), set w=h^n(x)∈U∩V. Then x=H^n(w),
and repeated use of H(V∩U)⊂U shows x∈U. This verifies exactly (0.3).
Theorem A now gives the access curve. This imports the accessibility
theorem rather than claiming a new proof of it. The final assertion is
the contrapositive of Lemma 4 and this application. ∎

If R|U has degree d, the other components of R^{-1}(U) have total degree
D−d. In particular d=D forces complete invariance and removes this
obstruction for repelling periodic points. For the m-th return the
corresponding deficit is D^m−d^m. These observations do not show that a
particular repelling point avoids the finitely many other boundaries.

**Why finiteness does not finish the argument.** Finitely many closed
boundaries may meet, and each can accumulate on the same periodic point.
The absence of critical points close to q only gives an inverse branch; it
does not determine the basin component of its image. Neither the boundary
exclusion nor local backward invariance has been derived for all q.

**Gap after approach two.** Control of the designated basin side at shared
preimage boundaries remains absent. There is no conclusion about neutral
points from this argument.

## 3. Approach three: build an access from a controlled hyperbolic chain

We next tried to join a backward orbit by intrinsic geodesics, so that the
connecting curves are automatically in U. This yields a quantitative
criterion, with the missing estimate exposed.

Choose a coordinate making U a proper simply connected plane domain and
q finite. This is possible by sending a different point of the complement
to infinity. Let k_U be the Poincaré distance normalized so that
k_D(0,r)=log((1+r)/(1−r)). Write δ_U(z)=dist(z,∂U).

**Lemma 6 (hyperbolic-ball estimate).** For z,w∈U with k_U(z,w)≤R,

    |w−z| ≤ (exp(2R)−1) δ_U(z).

**Proof.** Take a conformal map ψ:D→U with ψ(0)=z. If ψ(ξ)=w then
|ξ|≤t=tanh(R/2). The growth estimate for a normalized univalent function
gives |ψ(ξ)−z|≤|ψ'(0)|t/(1−t)^2. The Koebe quarter theorem gives
|ψ'(0)|≤4δ_U(z). Finally 4t/(1−t)^2=exp(2R)−1. ∎

These are the classical growth and quarter theorems for univalent maps;
their use, rather than any numerical test, is the analytic input to this
estimate.

**Proposition 7 (landing criterion).** Suppose z_n∈U, z_n→q∈∂U, and
R_n=k_U(z_n,z_{n+1}). If

    exp(2R_n) |z_n−q| → 0,

then q is accessible from U.

**Proof.** Join z_n to z_{n+1} by its hyperbolic geodesic segment Γ_n. A
point of Γ_n has hyperbolic distance at most R_n from z_n. Lemma 6 and
δ_U(z_n)≤|z_n−q| show that every point of Γ_n has distance at most
exp(2R_n)|z_n−q| from q. Concatenate the segments on consecutive intervals
[1−2^{-n},1−2^{-(n+1)}], beginning with n=0. The concatenation stays in U.
The displayed bound tends to zero uniformly on the final segments, so
assigning endpoint q at time 1 gives the required continuous curve. ∎

**Corollary 8.** If |z_n−q|≤Cρ^n for some 0<ρ<1, it suffices that
limsup R_n/n < −(log ρ)/2. In particular sublinear hyperbolic step growth
suffices.

**Proof.** Choose c strictly between the limsup and −(log ρ)/2. For all
large n, exp(2R_n)|z_n−q|≤C exp(n(2c+log ρ))→0. ∎

For a local repelling inverse branch H, the ambient estimate
|H^n(z)−q|≤Cρ^n is automatic as long as the iterates stay in its small
domain. Two separate issues remain: all those points must belong to U,
and their intrinsic distances must satisfy the stated growth bound.

Schwarz–Pick gives the wrong direction for the second issue. If h(z_n)=
z_{n−1} along a backward orbit in U, then

    k_U(z_{n−1},z_n) ≤ k_U(z_n,z_{n+1}).

Thus the backward hyperbolic increments are nondecreasing. This is no
upper bound. It would be invalid to invoke Schwarz–Pick to assert a
uniform bound for a local inverse branch which is not a self-map of U.

For a simple control take U=D, h(z)=z^d, and z_n=exp(−c/d^n), c>0. These
points lie on a single radius and converge to the repelling point 1.
For positive real r<s, k_D(r,s)=log((1+s)(1−r)/((1−s)(1+r))). Substitution
and 1−exp(−t)∼t give R_n→log d. Proposition 7 therefore applies. This
checks the mechanism on a genuine basin, but not the missing upper bound
for a general basin.

**Gap after approach three.** No basin-side backward orbit with the required
intrinsic-distance growth was constructed for an arbitrary periodic point.
The proposition is a conditional landing theorem, not a general solution.

## 4. Approach four: force a periodic prime-end address

Let φ:D→U be a Riemann map with φ(0)=a. Then
B=φ^{-1}fφ is a finite Blaschke product with B(0)=0 and degree d≥2.
For q∈∂U define the cluster-address set

    S(q) = {ζ∈∂D: there are z_j∈U with z_j→q and φ^{-1}(z_j)→ζ}.

This is an impression-address set; it is not the set of radial rays landing
at q. Confusing the two would assume what is being proved.

**Lemma 9.** S(q) is nonempty and compact. If f^m(q)=q, then
B^m(S(q))⊂S(q).

**Proof.** Choose points z_j∈U tending to q and pass to a subsequence of
w_j=φ^{-1}(z_j) convergent in the closed disk. The limit cannot be in D,
since φ is continuous there and its value lies in U. Thus S(q) is nonempty.
It is closed: if ζ_k∈S(q) and ζ_k→ζ, choose for each k a witness z_k with
distance(z_k,q)<1/k and |φ^{-1}(z_k)−ζ_k|<1/k. These witnesses give ζ∈S(q).
Compactness follows. For ζ∈S(q), use its witnesses and the identity
φ^{-1}(f^m(z_j))=B^m(φ^{-1}(z_j)). Continuity of the extension at q and
continuity of B^m on the closed disk imply B^m(ζ)∈S(q). ∎

One might try to deduce a periodic address from the nonempty compact
forward-invariant set S(q). This is false for expanding circle dynamics
alone, as the following complete construction shows.

**Proposition 10 (an aperiodic compact invariant set for doubling).** The
map T(x)=2x mod 1 has a nonempty compact invariant set K containing no
periodic point.

**Proof.** Fix any irrational α∈(0,1), for example α=√2−1. For t∈R define
a one-sided binary sequence

    s_n(t)=floor(t+(n+1)α)−floor(t+nα), n≥0.

Each digit is 0 or 1. Let X be the closure of all these sequences in the
compact product space {0,1}^{N}. It is nonempty and compact. If σ is the
left shift, then σs(t)=s(t+α); every original sequence is also the shift of
s(t−α). Continuity, compactness and passage to limits give σ(X)=X.

For every original sequence and N≥1, telescoping gives

    Σ_{n=0}^{N−1}s_n(t)=floor(t+Nα)−floor(t).

Its difference from Nα has absolute value less than 1. Finite blocks
stabilize under convergence in the product topology, so every s∈X satisfies
the same bound. In particular every s∈X has frequency of ones equal to
the irrational number α. No sequence in X is eventually periodic.

Define π(s)=Σ_{n≥0}s_n/2^{n+1} in R/Z. This is continuous and
πσ=Tπ. Thus K=π(X) is nonempty, compact and T-invariant. Binary expansion
ambiguity occurs only for eventually constant sequences, which X excludes.
If π(s) were periodic under T, its binary expansion would be eventually
periodic: indeed (2^m−1)π(s) is an integer for some m≥1, and the repeating
binary expansion of such a rational number is periodic (with the sole
endpoint ambiguity again eventually constant). This contradicts the
irrational digit frequency. ∎

The construction uses the actual doubling map, a particularly simple
finite Blaschke boundary map. It is not asserted to be the address set
S(q) of a holomorphic basin. It shows precisely that compactness,
forward invariance and circle expansion do not alone force a periodic
address. Additional planar or analytic information is indispensable.

There is a second missing step even if a periodic address is found:
q∈an impression does not mean that the radial limit is q. The source's
known landing of periodic internal rays supplies a periodic landing point,
but identification with the specified q would follow from a singleton
impression, from proof that q belongs to the principal set of that landing
ray, or from a further separation argument. None of these bridges has been
established here.

**Gap after approach four.** Neither an appropriate periodic address in
S(q) nor identification of its landing point with q has been proved.

## 5. Approach five: transport z² to an inaccessible comb domain

We tried to construct a counterexample by prescribing a simply connected
domain with an inaccessible point and conjugating a proper disk map into
it. The holomorphic extension requirement defeats this explicit model.

Identify C with R² and put

    U=((0,1)×(0,1)) minus ⋃_{n≥2}({1/n}×(0,1/2]),
    q=(0,1/4).

**Lemma 11.** U is a simply connected domain and q is inaccessible from U.

**Proof.** The removed set is relatively closed in the rectangle: its only
new accumulation points have x=0, outside the rectangle. Thus U is open.
Every point can be joined by a vertical segment to a point above height
1/2, and points above that height can be connected horizontally. Thus U
is connected. Its complement in the sphere is connected, since the
rectangle's outside is connected and every removed slit attaches to the
bottom side. The plane-domain criterion therefore makes U simply
connected.

If a curve in U tended to q, a final tail would have y∈(1/8,3/8). At one
time on that tail let its x coordinate be b>0. Choose n with 1/n<b. At
a later time its x coordinate is less than 1/n. The intermediate value
theorem forces the curve to cross the removed slit x=1/n at a height
less than 1/2, a contradiction. ∎

For any conformal φ:D→U, the map f=φ∘(z↦z²)∘φ^{-1} is a proper
degree-two holomorphic self-map of U whose iterates converge to φ(0).
This checks the properness, degree, simple connectivity and attracting
dynamics without merely drawing a topological picture. But this f has
no holomorphic extension to a neighborhood of closure(U).

**Proposition 12 (analytic rigidity of this comb).** Every proper
holomorphic self-map F:U→U which extends holomorphically across closure(U)
has degree one. In particular the degree-two conjugate just constructed
cannot extend as required.

**Proof.** First, an extension of any proper self-map sends ∂U into ∂U.
For x∈∂U, choose x_j∈U tending to x. Continuity gives F(x)∈closure(U).
If F(x) lay in U, a closed disk L⊂U around it would contain F(x_j) for
all large j. Properness would make F^{-1}(L) compact in U, impossible
for a sequence tending to a boundary point. Thus F(x)∈∂U.

The boundary of U is contained in the countable union of the vertical
lines x=0, x=1, x=1/n (n≥2), and the two horizontal lines y=0 and y=1.
For each n, consider the segment L_n={1/n+iy: 1/8≤y≤3/8}, which lies
inside a slit. Its F-image lies in that countable union of lines. The
preimages, under the continuous parametrized image, of each closed line
are closed sets covering the complete interval [1/8,3/8]. By the Baire
category theorem one has nonempty relative interior. Therefore either
Re F(1/n+iy) is constant on a nontrivial y interval, or Im F(1/n+iy) is.
Each is a real-analytic function of y on an open interval containing
[1/8,3/8]. The real-analytic identity principle extends the constancy
throughout the interval. Thus each entire segment is mapped into one
vertical or one horizontal line. F is nonconstant, so it cannot be
constant on a segment.

There are infinitely many n of at least one of those two types. Suppose
first that infinitely many are vertical. Differentiating with respect to
y gives Im F'(1/n+iy)=0 for all y∈(1/8,3/8) and those n. Since F extends
across the compact segment {iy:1/8≤y≤3/8}, there is ε>0 on which F is
holomorphic for |x|<ε and 1/8<y<3/8 (shrinking the y interval slightly
would also suffice). For each fixed y, the real-analytic function
x↦Im F'(x+iy) has infinitely many zeros 1/n accumulating at the interior
point 0. It is identically zero near 0, and by its identity principle on
the interval, throughout |x|<ε. Thus F' is real-valued on a nonempty
open rectangle. The open mapping theorem makes F' a real constant there.
Holomorphic continuation on the connected neighborhood component
containing U gives F(z)=az+b on U.

If infinitely many segments map into horizontal lines, differentiation
instead gives Re F'(1/n+iy)=0 and the same argument makes F' a purely
imaginary constant. Again F is affine. The constant a is nonzero, since
a proper self-map of U is nonconstant and surjective. An affine map is
one-to-one, so its proper self-map degree is one. ∎

If “holomorphic” is interpreted as a sphere-valued map, no pole occurs
on closure(U), because its continuous image is in the bounded set
closure(U). Shrinking the extension neighborhood therefore reduces to
the ordinary complex-valued argument just given.

This proof uses the same familiar comb shape as a topological diagnostic
in nearby accessibility work, but the result here is different: it proves
an analytic obstruction to *every* degree≥2 extended self-map of the
comb. It is not a repeat of the observation that its limit-side point is
inaccessible. The obstruction explains why an arbitrary Riemann-map
transport of z² does not manufacture a counterexample to this problem.

**Gap after approach five.** The explicit construction fails the extension
hypothesis. No alternative inaccessible domain with an admissible
extended proper map and periodic inaccessible point was constructed.

## 6. What remains

For repelling points, the unresolved issue is to obtain a curve in the
specified basin at periodic points shared with other inverse-basin
components, without assuming local backward invariance, a controlled
hyperbolic chain, or the required prime-end identification. The literal
statement also retains neutral periodic points, so a repelling-only proof
would still not settle it.

The verified local hedgehog counterexamples do not supply the needed
global/basin realization. The source comments about polynomial infinity
basins must not be promoted into a theorem covering arbitrary Cremer
points merely because the question's wording says “periodic.” The exact
published repelling hypotheses have been preserved throughout.

The finite checks accompanying this note test arithmetic identities and
finite controls for the mechanisms above. They do not certify the imported
analytic theorems or any universal accessibility claim. No queue change,
commit, push, pull request, release, or external publication was made.
