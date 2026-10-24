# Independent adversarial audit of the integral Artin-kernel bound

Review date: 2026-10-24 UTC. Reviewer: a fresh subagent that did not author the
three target notes. Inputs are frozen by SHA-256 in `FROZEN_INPUTS.json`.

**Outcome: PASS for the stated partial class exclusion. No substantive
mathematical objection remains from this review.** This is neither a complete
resolution of Kourovka 21.126 nor an originality certification. An independent
audit is evidence of scrutiny, not a substitute for the proofs recorded below.

The audited assertion is: for a finite defining graph and a nonzero integral
character, if its rank-one Artin kernel is finitely presented and there are d
zero-weight vertices, its intrinsic homotopical Dehn function has the upper bound

    delta(n) <=_coarse n^((9*3^d-1)/2).

I attempted to break the finite-presentation implication, geometric disk
construction, residue decomposition, distortion transfer, and repeated filling
estimate. I did not read an earlier review as a premise of the conclusion.

## 1. External finite-presentation criterion

I inspected [Meier--Meinert--VanWyk's original primary
PDF](https://ems.press/content/serial-article-files/42788?nt=1), printed p.24,
and its local text, lines 110--136. Corollary A(i), with n=2, concerns F2,
which is finite presentation. It therefore supplies the required homotopical
criterion; using the FP2 clause instead would not suffice.

Expanding the recursive domination definition gives exactly the conditions used
in the target note: the living flag complex is simply connected; each dead
vertex has a nonempty connected living link; every dead-dead edge has a common
living neighbor. The nonemptiness is necessary and is explicitly present.
No condition on a dead triangle is missing at n=2: the additional recursion at
this dimension checks vertices of the full link, hence dead-dead edges only.

The primary statement in Casals-Ruiz--Kazachkov--Roy, arXiv:2409.06315,
Theorem 3.2, agrees. Its finite-presentation constructions are not used to infer
a quantitative Dehn bound. The old source already establishes the implication
needed here.

## 2. Weighted pushing: disks, weights, and uniform constants

I checked the local primary PDF of Abrams--Brady--Dani--Duchin--Young and the
independently accessible [arXiv primary PDF](https://arxiv.org/pdf/1004.4253).
Theorem 4.2, Lemma 4.5, Remark 4.6, and Theorem 5.1 support the unit-weight
construction. The weighted assertion is an adaptation proved in the target
note, rather than a false claim that their displayed theorem already states it.

The adaptation survives these tests:

* Inverting any selected standard generators preserves the RAAG. Dividing by
  the gcd changes neither the kernel nor the zero set. Thereafter positive
  integer weights give integral vertex heights and edge lengths at least one.
* Changing a cube to the corresponding orthogonal rectangular product retains
  its right angles and its flag links, so the universal cover remains CAT(0).
  Fixed weights and finite dimension only change metric constants.
* On every all-positive or all-negative ray the height changes at unit speed
  for weighted l1 length. A folded link simplex stays in the complete standard
  flat of each incident cube. Both endpoint maps of an edge hit the same point
  of that complete line at height zero; they are not incompatible local choices.
* The truncated rectangles, further cut along the zero slice where needed, have
  finitely many shapes. Integral starting heights can affect a zero-intersecting
  rectangle only in a bounded range. Their coning targets are convex slices of
  complete flats. Consequently the higher-cell extensions have uniform constants
  times the largest incident height.
* Extending the link fold over a cone's 2-skeleton requires paths and triangular
  disk fillings in L, precisely connectedness and simple connectivity. It does
  not require L contractible. Finite L supplies finitely many fixed PL fillings;
  composing with rays scales their constants linearly with the vertex height.
* A polyhedral 1-cell of a nonzero-height level slice lies in an original
  2-face. One can therefore fill a loop after moving it to that 1-skeleton by a
  genuine disk in the ambient 2-skeleton. Relative deformation/cellular
  approximation of a CAT(0) quadratic disk can be made with quadratic area and
  linear height range, because the ambient rectangular complex has finitely
  many local cell types. Composition with the extended map keeps the disk's
  domain a disk. This is not the invalid inference from a homological chain
  bound to a homotopical filling bound. The cited Remark 4.6 explicitly permits
  this use of admissible ball fillings and controlled deformation.

The resulting area estimate is O(n^2) times the square of O(n), hence O(n^4).
The level set is connected and simply connected by the same extensions. Its
kernel action is free, proper, and cocompact by the bounded-height cube-orbit
argument. Its finite polyhedral cell types give the usual cellular/Lipschitz
comparison and finite presentation.

With connected L only, the 1-skeleton extension still gives quadratic distortion
of the all-nonzero kernel. No simple-connectivity assumption is silently used
for that length estimate. The connected, locally finite level complex has the
proper cocompact length geometry needed for its word-metric comparison.

## 3. Cubic length rewriting with dead vertices

The Schreier factors in Lemma 1 telescope in the ambient group. Their prefix
heights are at most a constant times the original word length. For a live
letter, its factor is a live height-zero word of ambient length O(n), with
quadratic live-kernel length. For a dead letter, Euclidean division of a possibly
negative prefix height gives q=i+ell*d_z with 0<=i<d_z. The proposed h has
height zero and live ambient length O(n); the conjugacy identity follows because
the chosen height-d_z live-link word commutes with that dead generator.

This gives at most n terms of quadratic intrinsic length, or O(n^3). It proves
finite generation at the same time. No absence of dead-dead relations is
needed: the word identities hold before imposing any such additional
commutations and hence in the actual RAAG. Fixed Bezout coefficients, large
weights, and large link gcds affect constants only.

## 4. The identity HNN decomposition really is injective

Adding one dead vertex to the previous induced RAAG is an identity HNN
extension over the full link parabolic, regardless of prior dead-dead edges.
The prior induced graph still contains all live vertices, so the normalized
character on its base is onto. The displayed finitely many stable letters have
residue indices in the correct range for the link image d_z Z.

Surjectivity follows from the explicit h-conjugacy above. For injectivity, expand
a reduced word in the claimed kernel HNN presentation into the ambient HNN
presentation. Any ambient Britton pinch has opposite signs of the same new dead
letter and intervening base word t^(-i) g t^j. Membership in its link parabolic
forces j-i divisible by d_z. Its two residue indices lie in [0,d_z), so i=j.
The remaining membership condition is exactly g in t^i K t^(-i), a forbidden
pinch of the claimed reduced word. This works with both stable signs, negative
heights, and nonunit link gcds. A word with no stable letters is handled by the
base embedding. I found no omitted conjugation or hidden automorphism of an
associated subgroup.

For distortion transfer, parabolic inclusion is isometric: inclusion and the
generator-killing retraction give the two word-length inequalities. A word of
G_j-length n has ambient length O(n). Fixed conjugation by t^i adds a constant;
the link kernel's ambient cubic bound is therefore also a cubic bound in G_j.
Its intrinsic metric may use any fixed finite generating set. Normalizing the
restricted link character by a different gcd does not change that subgroup.

## 5. Filling pinches without iterated expansion

This is the critical step, and it survives scrutiny. In a null boundary word of
length n, successively delete a Britton pair while retaining its intervening
literal base word u. All current base words are concatenations of the original
base letters, so their total length never exceeds n. The longer subgroup word
v is used only to certify the area of that replacement, not inserted into the
next boundary word.

The relation t*u*t^(-1)=u has a disk consisting of two base disks for u*v^(-1)
and the length-|v| commutation corridor. With |v|<=f(Cn), this costs at most
2*delta_G(n+C*f(Cn))+C*f(Cn), after harmless fixed-generator constants. At most
n/2 replacements occur. The final base null word still has length at most n.
Gluing these disks into the word reduction preserves a disk diagram and proves
the estimate in the note. This argument does not require the associated subgroup
to be finitely presented; finite generation is sufficient for the finite
centralizer presentation and the commutation corridor.

For cubic f and a polynomial base exponent a>=4, the resulting exponent is
3a+1. Starting with a=4 gives (9*3^d-1)/2. Multiple residue stable letters at
one step are treated simultaneously; there is no extra iteration per residue.

## 6. Dead-dead edges, boundary cases, and attempted counterexamples

An arbitrary order of dead vertices is allowed. At a new vertex z, its living
link stays the original connected S_z. Every earlier dead neighbor y has a
common live neighbor with z by condition (C); that live vertex is in the
associated link and dominates y there. Thus the cubic lemma applies at every
step without assuming simply connected link complexes or independence of the
dead set. This is the new mechanism that closes the gap in the narrower note.

The following potential falsifications did not work:

* With only one living vertex, the group is a direct product with its star's
  dead RAAG when that vertex dominates. The height kernel can have much smaller
  Dehn function, which is consistent with a nonsharp polynomial upper bound.
* Connected live links with nontrivial fundamental group need only generate
  the associated kernel; their lack of finite presentation is not an obstruction
  to the identity HNN's finite presentation.
* Mixed signs, character image rZ, and distinct global/link gcds preserve the
  argument after the explicitly permitted normalizations.
* Large d yields arbitrarily large fixed exponents across a family, not a
  superpolynomial Dehn function for any one finite graph.

`independent_checks.py` passed using exact arithmetic and legal RAAG
cancellations, without importing an author's checker. It checks 32,767
graph/living-set pairs through five vertices, 30,654 dead-vertex orders,
82,455 link-induction steps, 1,428 signed residue conjugacy identities,
4,900 Britton-residue arithmetic cases, and 1,515 weighted edge compatibility
identities. The script explicitly limits its claims: it neither decides arbitrary
flag-complex simple connectivity nor proves an unbounded assertion from samples.
`INDEPENDENT_RESULTS.json` records the outputs.

## 7. Supplemental 2026 source caution

At the root's request I inspected [Roy,
arXiv:2607.08900v1](https://arxiv.org/html/2607.08900v1), dated July 9, 2026.
Its subject is finite generation and presentations, and I located no Dehn bound.
Fact 3.2 chooses generator images in general position. The introduction's
arbitrary-epimorphism reading must not replace the living-complex criterion.

Here is an independent obstruction to that broad reading. For the path a-b-c,
A(Gamma)=F(a,c) x Z_b. Send a to 1 and b,c to 0. The kernel is

    ker(F(a,c) -> Z) x Z_b = F({a^q*c*a^(-q): q in Z}) x Z_b.

The countable free basis follows by the covering graph with one a-line and one
c-loop at each integer vertex, using that line as a maximal tree. Its
abelianization has infinite rank, so the kernel is not finitely generated.
The full path is connected and its flag complex is simply connected. Thus the
unqualified arbitrary-map version is false. This warning concerns extrapolation
of that supplemental source, not the current polynomial proof: the latter uses
MMV's exact character-dependent criterion. I have not audited the whole 2026
paper or asserted that every intended, qualified version of its results fails.

## Conclusion and scope

The target theorem survives this adversarial review as a nonsharp polynomial
upper bound for finitely presented **rank-one integral Artin kernels**. The
mechanism is analytically justified, including homotopical disks and dead-dead
edges. It supplies a partial class exclusion for a research route. It gives no
bound for arbitrary finitely presented subgroups of those kernels, higher-corank
kernels, or all RAAG subgroups. No solution of either full existence branch of
21.126, priority claim, publication gate, or independent human review is implied.
