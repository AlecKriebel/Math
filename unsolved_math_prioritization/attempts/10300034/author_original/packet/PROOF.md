# Transverse surgery: five scoped approaches to Calegari Question 9.1

Problem 10300034 / AMR-102-0034; queue rank 1005.

**Author disposition: unsolved after five substantive approach families.**
These are elementary partial results and method obstructions. None is a
counterexample to the original existential question. No novelty, complete
literature-status, independent-review, or formal-proof claim is made.

## 1. The target and the scope of this note

Calegari's 2002 problem list, Question 9.1 on printed page 21, asks whether
one 3-manifold M can serve as the surgery output for every tautly foliated
input (N,F), with a surgery link everywhere transverse to the specified F.
Definition 1.1 uses a closed transverse circle that meets every leaf as
the tautness condition. The neighboring remark suggests normal triangulations
and a Heegaard decomposition; its common-link-exterior variant is a separate
question. [C02]

The displayed question does not repeat closedness, orientability, smoothness,
or coorientation. Its Lickorish comparison indicates the usual closed
3-manifold surgery setting. We investigate the closed, connected, oriented
setting and make every additional smoothness/coorientation assumption below
explicit. We do not exploit omitted category conventions to claim a negative
answer. All test manifolds below are closed and oriented, and their foliations
are smooth and cooriented. Thus they are legitimate subclasses of the intended
question, but a positive theorem restricted to them would not be the full
answer.

The output M need not carry the input foliation, a contact structure, or a
specified fibration. The link may have any finite number of components and
the question does not prescribe surgery coefficients. Confusing any of these
optional restrictions with the actual target invalidates a proposed solution.

Our notation: X=N\int(nu L) is the compact link exterior. A meridian mu_i
bounds a disk in the original tubular neighborhood. A longitude lambda_i is
any primitive curve on its boundary that maps to the oriented core generator
in that neighborhood. A Dehn-filling slope is an unoriented primitive class
p_i mu_i+q_i lambda_i. Original meridional filling has q_i=0 and |p_i|=1.
The framings are choices, not canonical longitudes or preferred null-homologous
framings. All fundamental-group quotients use normal closures and basepoint
paths; their conclusions are unchanged by conjugating component classes.

## 2. Approach I: ordinary surgery, then transverse isotopy

**Attempt.** Start with an ordinary surgery description and isotope its dual
link in N to be transverse to F, preserving the surgery output.

### Proposition 1: a period obstruction to this isotopy step

Let alpha be a smooth nonsingular closed 1-form on a closed manifold N, and
let F=ker(alpha). An oriented closed curve gamma that is positively transverse
to F satisfies

    <[alpha],[gamma]> = integral_gamma alpha > 0.

In particular, a knot whose alpha-period is zero has no representative in its
isotopy class transverse to F, in either orientation.

**Proof.** On a positive parametrization alpha(gamma') is a continuous strictly
positive function; its integral is positive. A transverse connected circle
has a continuous nowhere-zero alpha(gamma'), hence constant sign, and can be
oriented positively. Closedness of alpha makes the integral depend only on
homology. Isotopy preserves that class up to the chosen orientation. Zero
cannot become positive or negative. This also excludes null-homologous knots.

For a concrete taut example take N=Sigma_g x S1 with g>=1 and alpha=dt,
where t has period one. The fibre foliation is taut: {z}xS1 meets every fibre.
A knot contained in a fibre has zero period, as does a small knot in a ball.
Consequently there is no universal theorem that arbitrary knots in tautly
foliated manifolds may be isotoped transverse. QED.

This refutes the indicated isotopy lemma, not the existence of a different
surgery link. Kirby moves can change isotopy and homology classes and are not
ruled out. The missing theorem would be a controlled sequence of surgery-
preserving moves producing an F-transverse link for every specified foliation.

The classical Lickorish theorem concerns closed connected orientable
3-manifolds without a foliation constraint [L62]. Surgery duality reverses
an ordinary link description, but provides no transverse-isotopy assertion.

## 3. Approach II: group and homology obstructions

**Attempt.** Find an invariant of every permitted filling that excludes a
fixed output manifold. Unlike Approach I, the link itself is now allowed to
vary.

### Proposition 2: a common quotient of every filling

For a link L with r components in any closed connected 3-manifold N, and any
Dehn filling M=X(s_1,...,s_r), there is a surjection

    pi1(M) -> pi1(N)/normal([L_1],...,[L_r]).

Consequently there is a surjection of integral abelian groups

    H1(M;Z) -> H1(N;Z)/<[L_1],...,[L_r]>,

and, writing d for the dimension of the rational span of the component
classes,

    b1(M) >= b1(N)-d >= b1(N)-r.

**Proof.** Van Kampen identifies pi1(N) with pi1(X)/normal(mu_1,...,mu_r).
Killing also the images of the longitudes gives the displayed quotient of
pi1(N), since each longitude maps to its core, up to conjugacy. Every filling
slope mu_i^{p_i}lambda_i^{q_i} maps to the identity in that quotient. Thus the
surjective map from pi1(X) factors through pi1(M), which van Kampen describes
by killing these slopes. Abelianization preserves surjections. Tensoring the
abelian quotient with Q subtracts precisely d dimensions. QED.

This statement needs no foliation, no null-homology assumption, and no
integrality restriction on the rational surgery slopes beyond primitivity.

### Corollary 2A: no bounded-component strengthening

For a fixed closed M, any universal description of the stated type must use
unboundedly many link components. More precisely, on
N_g=Sigma_g x S1 with its taut fibre foliation, it requires

    r >= 2g+1-b1(M).

**Proof.** The first Betti number of N_g is 2g+1. Apply Proposition 2. Since g
is unbounded, so is the lower bound. QED.

The original question allows unbounded r, so this is not its refutation.

### Proposition 3: the quotient obstruction can vanish for transverse links

For each g>=1, N_g contains a link with 2g+1 disjoint positively transverse
degree-one components that normally generate pi1(N_g). Their homology classes
are an integral basis of H1(N_g;Z).

**Proof.** Write the surface group in its standard generators a_i,b_i and
write t for the central S1 generator. Consider the free homotopy classes

    t, a_1 t, b_1 t, ..., a_g t, b_g t.

Each class has a smooth section representative s -> (gamma(s),s), with
gamma a loop on Sigma_g. Such a curve is embedded regardless of self-crossings
of gamma, because its S1 projection is the identity, and is positive transverse
to ker(dt). Choose all 2g+1 loops generically as functions of the common
parameter. For each pair the coincidence condition gamma_i(s)=gamma_j(s)
has codimension two in the target product and a one-dimensional parameter
domain; a transverse perturbation therefore avoids it. A finite simultaneous
perturbation makes the section images pairwise disjoint, stays in their free
homotopy classes, and retains positive transversality. Equivalently this is
the elementary general-position separation of finitely many curves in a
3-manifold, within the open set of transverse curves.

Killing t and every a_i t,b_i t kills a_i,b_i and hence the entire group.
Conjugacy choices from basepoint paths do not affect the normal closure.
In homology subtract the t column from each other column: the resulting
matrix has the standard basis columns, up to ordering. Its determinant is
therefore +/-1. QED.

Thus even normal generation and the strongest displayed homology quotient
need not obstruct a transverse surgery link. There is no claim that any
choice of slopes on this constructed link yields S3 or another fixed M.
Sufficiency of the quotient condition is the exact failed step of this route.

## 4. Approach III: drilling braids from a surface bundle

**Attempt.** Use the explicit structure of fibre foliations to control the
filled manifold, perhaps retaining a fibration invariant that a fixed M
cannot support.

### Proposition 4: exactly when the original fibre class extends

Let f:N->S1 be a smooth fibration of a closed connected 3-manifold with
connected surface fibres. Let L be a nonempty link positively transverse
to its fibre foliation. Put phi=f^*[dt] in H^1(N;Z), and let phi_X be its
restriction. If d_i is the positive degree of f on L_i, then phi_X extends
to H^1(M;Z) for M=X(p_i mu_i+q_i lambda_i)_i if and only if

    q_i d_i = 0 for every i.

Equivalently, only the original meridional filling on every component allows
this particular class to extend.

**Proof.** The restriction f|L_i is a local orientation-preserving
diffeomorphism of circles, hence a covering of positive integer degree d_i.
The meridian is zero in H1(N), while the longitude maps to the component
class. Therefore phi_X(mu_i)=0 and phi_X(lambda_i)=d_i. Integral first
cohomology is Hom(pi1,Z). A homomorphism on pi1(X) factors through the Dehn-
filling quotient exactly when it vanishes on each killed slope, namely when
p_i*0+q_i*d_i=0. As d_i>0, this forces q_i=0. A primitive slope with q_i=0
is the original meridian, up to sign. Conversely those fillings recover N
and its original class. QED.

One can choose disjoint small tubular neighborhoods of L that meet each
fibre in disks. The exterior is then a surface bundle with punctured fibre;
the total number of punctures is sum_i d_i. For example, transport small
disks around the moving finite set L intersect f^{-1}(t); their monodromy
permutes them. This gives the familiar braid description but does not alter
the peripheral class calculation.

The conclusion concerns extension of the original restricted class, not
existence of some other fibration or foliation on M. Since Calegari's target
requires neither, the invariant cannot settle it. The obstruction is precise:
the nontrivial surgeries one hopes to use are exactly those allowed to
destroy this class.

## 5. Approach IV: contact approximation and transfer of links

**Attempt.** Approximate F by a contact plane field, exploit the flexibility
of contact-transverse knots, and transfer a resulting link back to F.

Bowden proves contact approximation for coorientable C0 surface foliations
on closed oriented 3-manifolds, excluding the sphere-foliated S2 x S1 and
plane-foliated exceptional case on T3 in the displayed Theorem 1.2. Here C0
means smooth leaves with continuous tangent planes. [B16] No approximation
theorem claims that every transverse knot for the approximating structure
is transverse to the original foliation.

### Proposition 5: a fixed-knot countercontrol to transfer

On T3=(R/Z)^3 with coordinates x,y,t, put F=ker(dt) and, for epsilon>0,

    beta_epsilon = dt + epsilon cos(2*pi*t) dx
                        + epsilon sin(2*pi*t) dy.

Then beta_epsilon is a contact form, ker(beta_epsilon) converges uniformly
to F as epsilon->0, and the fixed knot K(s)=(s,0,0) is beta_epsilon-positive
for every epsilon. Nevertheless K is not transverse to F, and no knot
isotopic to K can be transverse to F.

**Proof.** Direct differentiation gives

    beta_epsilon wedge d beta_epsilon
       = -2*pi*epsilon^2 dx wedge dy wedge dt,

which is nowhere zero. The sign specifies negative contact relative to the
displayed volume orientation; changing the sign of the sine term yields
the positive-contact version with the same knot property. The coefficients
converge uniformly to those of dt. Along K, beta_epsilon(K')=epsilon>0,
whereas dt(K')=0. The dt-period of K is zero, so Proposition 1 excludes all
isotopic representatives. The foliation F is taut by vertical circles. QED.

There is a valid conditional transfer criterion. For a Riemannian metric,
forms alpha,beta, and a unit positively parametrized tangent v to a compact
link, if beta(v)>=c>0 and ||alpha-beta||_infinity<c, then
alpha(v)>=c-||alpha-beta||_infinity>0. This is just the dual-norm inequality.
In the example the contact margin is epsilon and the perturbation norm is
epsilon, so the strict inequality fails at every stage.

Thus the missing ingredient is uniform angle/margin control for a suitable
surgery link, with respect to the given foliation. Tightness, fillability,
and C0 approximation alone do not provide it. This is independent of whether
a particular contact-surgery theorem has its own sign or framing constraints;
no such theorem is needed for, or claimed by, the countercontrol.

## 6. Approach V: recurrent triangulations and directed cycles

**Attempt.** Implement the source's triangulation suggestion by building
transverse links from recurrent directed edges, then seeking surgery
coefficients that cancel the associated topology.

### Proposition 6: exact finite circulation criterion

For a finite directed graph, the following are equivalent:
(a) every edge is contained in a directed cycle;
(b) there is a positive integer weight on every edge with total incoming
weight equal to total outgoing weight at every vertex.

**Proof.** For (a), select a directed cycle containing each edge and add all
their edge-count vectors. Every coordinate is positive and every cycle is
balanced. For the converse suppose e:u->v has no directed return path from
v to u. Let R be the vertices reachable from v. There is no edge leaving R,
but e enters R. Summing the balance equations over R gives total incoming
weight equal to total outgoing weight, impossible with e positive and no
outgoing edges. Thus a return path exists for each edge. QED.

### Proposition 7: realizing the combinatorial circulation

Suppose such a graph is actually embedded in a smoothly cooriented foliated
3-manifold, with each edge positively transverse away from its endpoints,
and with incident edges locally positively transverse at each vertex in a
foliation chart. Then a positive integral circulation can be realized by a
finite disjoint positive transverse link arbitrarily close to the graph,
following its directed edges with precisely the specified multiplicities.

**Proof.** Replace each edge by the prescribed number of directed copies.
At every vertex incoming and outgoing copies have equal count; pair them.
Following pairings decomposes the finite edge set into closed directed walks.
In a sufficiently small foliation chart at a vertex, the incoming cut ends
are below the vertex's leaf and the outgoing cut ends are above it. Connect
each paired set by a smooth path whose transverse coordinate strictly
increases. This is possible by monotone interpolation in that coordinate;
the leaf coordinates may be interpolated freely. Take parallel edge paths
outside the vertex charts and smooth the joins within the open positive
transverse cone. Finally apply a sufficiently small generic perturbation
of the finite collection of immersed circles in dimension three. Coincidence
conditions have codimension three and a two-dimensional pair-of-parameters
domain, so both self-intersections and mutual intersections disappear.
Positivity is preserved because it is open and the compact smoothed curves
have a strictly positive transverse margin. The perturbation may be made
inside the chosen edge tubes and vertex balls, retaining edge multiplicities.
QED.

This proposition is conditional on an actually transverse embedded graph;
an abstract directed graph is not a foliation or a 3-manifold construction.
It also preserves edge multiplicities, not a previously specified knot type.

Calegari's earlier paper assumes smooth, oriented, cooriented foliations.
Its Lemma 4.2 obtains a recurrent local orientation from a taut foliation;
local orientations also impose link-connectivity and tetrahedron-ordering
conditions. Its stronger positive orientation additionally has one
cohomology class positive on all directed cycles; Theorem 2.2 then gives a
surface bundle. [C00] These hypotheses are different. In particular one
cannot silently replace recurrence with a common positive cohomology class.

Propositions 6 and 7 provide many transverse components under the stated
geometric hypotheses. They give neither surgery coefficients nor a
handle-cancellation argument. A combinatorial circulation records no
framing, attaching-map, or fixed-output condition. That is the exact
remaining step of this construction route.

## 7. What remains

The five attempted mechanisms are: surgery-preserving isotopy; algebraic
obstruction across all fillings; preservation of a bundle class; contact-
approximation transfer; and a directed-graph construction of the link.
They are separate mathematical approaches, not source searches, audit
passes, tool calls, or five versions of the same computation.

No fixed M has been constructed with the required property. No family of
tautly foliated inputs has been proved to avoid every possible fixed M.
The remaining existence problem includes simultaneous control of the
transverse link, its surgery slopes, and its global filling topology. The
obstructions above exclude several tempting shortcuts and a bounded-
component strengthening, while leaving the original quantifiers intact.

All results are elementary or credited consequences; their historical
novelty was not established. Bounded literature searches found no verified
resolution, which is not certification of worldwide current openness.

## References

- [C02] Danny Calegari, *Problems in foliations and laminations of 3-manifolds*,
  arXiv:math/0209081v1 (2002), Definition 1.1 and Question 9.1.
  https://arxiv.org/abs/math/0209081v1
- [C00] Danny Calegari, *Foliations Transverse to Triangulations of
  3-Manifolds*, Comm. Anal. Geom. 8 (2000), 133–158;
  arXiv:math/9803109v1, convention at printed page 2, Lemma 2.1,
  Theorem 2.2, local-orientation definition and Lemma 4.2.
  https://arxiv.org/abs/math/9803109v1
- [B16] Jonathan Bowden, *Approximating C0-foliations by contact structures*,
  Geom. Funct. Anal. 26 (2016), 1255–1296;
  arXiv:1509.07709v2, Theorem 1.2 and regularity convention.
  https://arxiv.org/abs/1509.07709v2
- [L62] W. B. R. Lickorish, *A Representation of Orientable Combinatorial
  3-Manifolds*, Ann. of Math. 76 (1962), 531–540.
  https://www.jstor.org/stable/1970373
  Primary opening-page text was available in the indexed facsimile;
  local full-PDF retrieval failed. No full-paper inspection is claimed.
