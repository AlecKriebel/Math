# Boundary-parallel surfaces and integral skein torsion

## Disposition and scope

The universal conjecture 10400081 / AMR-103-0081 is **not resolved here**. Five distinct approaches are completed below. They give rigorous special cases, reduction criteria, and exact counterexamples to tempting algebraic shortcuts; none supplies a manifold counterexample or a proof for every manifold in the hypothesis. No novelty claim is made for the elementary algebra or for the classical surface-product theorem.

Set R = Z[A,A^-1], K = Q(A), and P = Q[A,A^-1]. For an oriented three-manifold M, S_R(M) denotes the Kauffman bracket skein module of unoriented framed links, including the empty link, with crossing relation L_cross = A L_0 + A^-1 L_infinity and deletion of a disjoint zero-framed trivial circle multiplying by delta = -A^2-A^-2. The drawing convention is the one in Ohtsuki, Section 4.1, printed page 446 [O]. Torsion means a nonzero element killed by a nonzero element of R, including an integer. It does not mean torsion in H_1(M), or only torsion killed by A+1, or torsion over K (which would be vacuous).

The source does not explicitly impose compactness in its one-sentence conjecture. Compactness will therefore be stated wherever used. The intended surface condition is read in light of the preceding explicit discussion of essential spheres and the later literature: every embedded closed two-sided essential surface is boundary-parallel. For this packet, the positive-genus closed surfaces under consideration are incompressible embedded surfaces, with boundary-parallel ones allowed; incompressible means there is no compressing disk. The essential-sphere condition means that the sphere does not bound a ball. Boundary-parallel means it cobounds a product with a boundary component. In an oriented manifold two-sided surfaces are orientable. The old sentence does not separately spell out the one-sided convention. If it was intended to quantify over one-sided surfaces too, that gives a stronger hypothesis; no unrestricted resolution is asserted under either reading. Counting every small ball sphere as a forbidden incompressible surface would make the closed-manifold formulation meaningless. Conversely, deleting essential spheres from the hypothesis would incorrectly admit S^1 x S^2.

Coefficient change is the usual presentation-compatible isomorphism S_R(M) tensor_R B = S_B(M), for a commutative R-algebra B [P, Proposition 2.2(4)]. All uses of this fact concern the same framed-link presentation.

## Approach 1. Direct normal forms on surface products

### Proposition 1 (classical product case, proof reconstructed)

For a compact oriented surface F, S_R(F x I) is a free R-module on the isotopy classes of multicurves in F with no disk-bounding component, including the empty multicurve. Hence it is torsion-free. This is the classical theorem recorded in [P, Theorem 2.3(b)]; the argument is included to specify what must survive in a generalization.

A generic projection of a framed link to F is a link diagram with crossing information and a framing correction relative to blackboard framing. Resolve every crossing and remove each disk-bounding state circle. Sum the resulting essential multicurves with coefficient A for one smoothing, A^-1 for the other, and delta for each removed circle. A framing correction contributes a unit (-A^3)^k. This gives an element of the free R-module C(F) on essential multicurves.

This assignment is invariant under diagram isotopy and the framed Reidemeister moves. For clarity, the two crucial local algebra identities can be checked in the Temperley-Lieb tangle algebra. With e_i^2 = delta e_i, e_i e_(i+1) e_i = e_i, and disjoint e_i commuting, put g_i = A 1 + A^-1 e_i and h_i = A^-1 1 + A e_i. Then

- g_i h_i = 1 + (A^2 + A^-2 + delta)e_i = 1;
- g_i g_(i+1) g_i - g_(i+1) g_i g_(i+1) has coefficient A + A^-1 delta + A^-3 on e_i-e_(i+1), and this coefficient is zero;
- the two curls evaluate to -A^3 and -A^-3, in the corresponding drawing conventions, precisely accounting for the framing change.

The planar tangle multiplication here is stacking, with each closed component replaced by delta. Consequently the state sum descends to an R-linear map S_R(F x I) -> C(F). The map C(F) -> S_R(F x I) putting a multicurve at height 1/2 is inverse: resolving all crossings shows one composite is the identity on any link, and a crossingless essential multicurve is unchanged by the other. This proves freeness without inverting a nonunit.

**Outcome.** Products, hence all handlebodies, are covered. In a handle decomposition of a general compact M, adding 2-handles imposes additional handle-slide relations [P, Proposition 2.2(5)-(6)]. The state sum alone does not prove that quotient free or torsion-free. The missing statement is that those extra relations are saturated over R. Having no essential closed surface has not supplied that statement.

**Exact control.** The checker constructs noncrossing tangle matchings, multiplies them by graph gluing, and verifies the local identities over integer Laurent polynomials. This tests signs, coefficient conventions, and local algebra; it does not enumerate ambient links or establish completeness of an arbitrary manifold's slide relations.

## Approach 2. Topological stabilization and compact support

### Proposition 2 (spherical boundary filling)

Attaching a 3-ball to a spherical boundary component induces an isomorphism on S_R. This is [P, Proposition 2.2(2)(i)]. A compact link can be isotoped off the center of the added ball; then radial pushing places it in the old manifold plus a collar. An isotopy of links has a two-dimensional trace in space-time, and may be put in general position disjoint from the one-dimensional trace of that center in four-dimensional space-time. Thus the isotopy also pushes off the ball. Skein relations are supported in balls and, after moving their supporting local configurations, are treated the same way. Equivalently, the zero-dimensional cocore of a 3-handle introduces neither new link generators nor new relations.

If a compact M satisfies the surface hypothesis, capping its spherical boundary components yields a manifold N satisfying the corresponding hypothesis with those components removed. Indeed, any closed surface in N can first avoid the finitely many ball centers, and then be moved into M. Incompressibility in N implies incompressibility in M. A sphere essential in N remains essential in M; if parallel to a capped spherical boundary, however, it bounds a ball in N, a contradiction. A positive-genus incompressible surface must have been parallel to a non-spherical boundary component of M. In particular, if all boundary components of M are spheres, N is closed, irreducible and non-Haken, and S_R(M) = S_R(N).

Only this forward preservation of the hypothesis is asserted. Arbitrary puncturing need not preserve the literal sphere condition, even though it preserves the skein module. No connected-sum tensor-product formula over R is used.

### Proposition 3 (directed compact-support extension)

Suppose M is an increasing union of oriented submanifolds M_i such that every compact subset of M lies in the interior of some M_i. Then S_R(M) is the filtered colimit of S_R(M_i). If every S_R(M_i) is torsion-free, so is S_R(M). The bonding maps need not be injective.

Every link is compact and hence comes from some stage. Every relation in the skein quotient is a finite R-linear combination of local relations and isotopy identifications; all links, balls, and isotopy traces used in such a finite expression have compact union. Thus every equality is witnessed in a later stage. This proves the colimit assertion directly from the presentation.

Now let x in the colimit be represented by x_i, and suppose 0 != f in R kills x. The equality f x = 0 is witnessed by f x_j = 0 at some later stage j. Torsion-freeness there gives x_j = 0, hence x = 0. This proves the assertion without any injectivity premise on the transitions.

**Outcome.** Any manifold admitting such an exhaustion by handlebodies (or by other already torsion-free pieces) has torsion-free skein module. This covers nested-solid-torus exhaustions without identifying their limit with a solid torus or claiming its skein module free. Compact non-Haken manifolds need not admit a suitable exhaustion; a finite compact-support argument cannot replace a missing global normal form.

**Sphere control.** S_R(S^1 x S^2) has known summands R/(1-A^(2i+4)), i >= 1 [P, Theorem 2.3(d)]. Its nonseparating sphere is essential and not boundary-parallel. It is not a counterexample to the intended conjecture. Removing some balls cannot eliminate its skein torsion, by Proposition 2, but does not turn that nonseparating sphere into a boundary-parallel one.

## Approach 3. Character schemes, specialization, and invisible torsion

This route tries to compare generic rank with the classical A=-1 fiber. It succeeds in excluding one primary torsion type in important cases; it does not prove integral torsion-freeness.

### Proposition 4 (correct specialization count)

Let N be a finitely generated P-module of generic rank r. By the structure theorem over the PID P, write N = P^r direct-sum (direct-sum_j P/(f_j)), where each f_j is a nonconstant nonunit Laurent polynomial. For lambda in C*,

  dim_C(N tensor_(A=lambda) C) = r + number of j for which f_j(lambda)=0.

Indeed, tensoring a cyclic summand gives C/(f_j(lambda)), which is C if the scalar vanishes and zero otherwise. In particular the lambda fiber has dimension r if and only if the complexified module has no (A-lambda)-primary torsion. This counts cyclic blocks, not their exponents: P/((A+1)^e) has Q-dimension e but its A=-1 fiber has dimension 1. No statement identifying torsion length with fiber excess is used.

The conclusion also follows for the lambda-primary part of a tame direct sum when the relevant fiber is finite; there are then finitely many contributing blocks. The finite-generation formulation above is enough for the concrete families below.

In [DKS-small, Theorems 1.1 and 3.1], a tame rational Laurent skein module and a reduced character scheme give equality of generic rank and the dimension of the A=-1 fiber. Proposition 4 then explains why (A+1)-primary torsion over P vanishes. For an oriented manifold the spin-structure sign isomorphism relates parameters A and -A, so the analogous (A-1)-conclusion can also be obtained. This last symmetry is a cited topological input, not needed for any of the algebraic countercontrols.

There are two independent obstructions to upgrading this result.

1. Let N_1 = R^r direct-sum R/(A-2). It has nonzero R-torsion and has no integer torsion, since R/(A-2) is Z[1/2]. Yet its fiber over every complex root of unity has dimension exactly r: no root of unity is 2. Its generic rank is r. Its rational completion at A=-1 (or at A=1) also loses the torsion summand because A-2 has nonzero constant term in that formal local coordinate. Even all root-of-unity tests do not settle the conjecture without a separate theorem restricting torsion support.
2. Let N_2 = R^r direct-sum R/(2,A-1). Its final summand is F_2, so it is nonzero integral torsion. Tensoring with Q, K, or any complex specialization kills that summand because 2 becomes a unit. Thus every complex fiber, not only the root-of-unity fibers, can have exactly the generic dimension while integral torsion remains.

Both are abstract modules, not asserted to be skein modules of manifolds. They rigorously refute proposed algebraic inferences, not the topological conjecture.

**Current-source limit.** Nonreduced character schemes of small Seifert manifolds were studied in the September 24, 2026 version of [D-nonreduced]. Such nilpotents do not themselves imply skein torsion: a finite free deformation can have a nonreduced special fiber, for example P[x]/(x^2-(A+1)), free on 1,x over P. Conversely a nonzero nilradical leaves room for, but does not force, a dimension jump. [BD-effective] proves finiteness after coefficient and boundary-curve localization. Those localizations likewise cannot certify injectivity of the integral module into its localization.

## Approach 4. A sharp integral generating-set certificate

### Proposition 5 (rank-matched generators)

Let D be an integral domain with fraction field E and let N be a D-module. If N is generated by r elements and dim_E(N tensor_D E) = r < infinity, then those generators form a D-basis.

Let pi:D^r -> N be the surjection. After tensoring with E it is a surjection between r-dimensional vector spaces and is therefore an isomorphism. If v lies in ker pi then v maps to zero in E^r. The map D^r -> E^r is injective, so v=0. Thus pi is an isomorphism. This argument uses no PID, finite-presentation, or freeness conjecture. The skein application is also present in [DKS-Seifert, Proposition 2.1].

For any closed M for which an exact generic rank r is known, an integral spanning set of exactly r skeins would therefore prove the desired conclusion, indeed the stronger statement of freeness. A set which is a basis only after tensoring with K is not an integral spanning set.

For example let M_q be 1/q Dehn filling on the figure-eight knot, q a nonzero integer. [DKS-small, Theorems 1.3 and 1.5] supply rational-Laurent finite generation, reducedness for p=1, and the generic-rank formula. Substitution p=1 gives

  r_q = (|4q+1|+|4q-1|)/2 = 4|q|.

Consequently, an R-spanning set of 4|q| links would certify R-freeness for M_q. This statement is a conditional reduction only. Neither the rational-Laurent finite-generation theorem nor the published K-basis proves that those links span over R. The exact control checks the arithmetic specialization of the rank formula; it does not construct the required integral spanning set.

The same issue remains for the Seifert computations: [DKS-Seifert] proves integral finite generation for the specified non-Haken class and gives K-bases in its reduced weakly-coprime cases. Its Proposition 2.1 carefully distinguishes integral finite generation, integral freeness, and integral torsion-freeness. No arrow from finite generation alone to torsion-freeness may be supplied.

**Why mere rank agreement is insufficient.** N_1 and N_2 in Approach 3 both have generic rank r while requiring additional generators. Nor does a basis in one fiber imply integral generation: the r standard free generators in R^r direct-sum R/(A-2) are a basis in every root-of-unity fiber and in K, but they miss the entire nonzero torsion summand.

## Approach 5. Integral saturation and finite relation certificates

### Proposition 6 (saturation exactly equals torsion)

Let F be a free R-module, possibly of infinite rank, J a submodule, and N=F/J. Define

  J_sat = {v in F: f v is in J for some nonzero f in R}.

Then the torsion submodule of N is J_sat/J. Under the natural embedding F -> K tensor_R F,

  J_sat = F intersect (K tensor_R J).

The first equality is the definition of torsion applied to a representative. For the second, f v in J implies v belongs to the K-span of J. Conversely a K-linear expression for v uses finitely many elements of J; multiplying all denominators gives a nonzero f with f v in J. This proves the claim without assuming finite generation.

Thus the conjecture can be restated as saturation of the full handle-slide relation submodule in a handlebody's multicurve module for every M in its scope. Establishing only the K-span of those relations loses precisely the obstruction being sought.

### Proposition 7 (arithmetic and polynomial torsion are separate)

For any R-module N, the following are equivalent:

(a) N is R-torsion-free.
(b) N has no nonzero integer-torsion element and N tensor_Z Q is torsion-free over P.

The forward implication follows by localization: a polynomial relation on an element of N tensor Q clears integer denominators to a relation in N. For the reverse implication, if f x=0 with f nonzero in R, then the image of x in N tensor Q vanishes because its P-module is torsion-free. Vanishing under this localization means some nonzero integer kills x. The first assumption then gives x=0.

Equivalently, because R is a UFD, multiplication by every irreducible element of R must be injective. If f=q_1 ... q_s kills a nonzero x, choose the first zero in the successive products; it is a nonzero element killed by a single q_i. Testing all irreducibles as multiplication maps is NOT the same as testing localizations at their height-one prime ideals.

The latter weaker test fails for T=R/(2,A-1). Every height-one prime is generated by an irreducible, and none contains both 2 and A-1: a common irreducible divisor would have to divide 2 and the primitive polynomial A-1. Hence at least one of those two annihilators is inverted at every height-one prime, and T localizes to zero there, despite T being nonzero. This is a codimension-two arithmetic obstruction. Its residue test is simply evaluation A=1 in F_2.

### Proposition 8 (maximal-rank minors annihilate torsion)

Let B be an n by m matrix over an integral domain D, let its rank over E=Frac(D) be q>0, and let N=coker B. Every nonzero q by q minor Delta of B annihilates every torsion element of N. In particular, if the ideal generated by all q by q minors is the unit ideal, then N is torsion-free.

Choose the q columns and q rows defining Delta. Those columns form an E-basis of the E-column space of B. If v in D^n represents a torsion element, v is in that E-column space, since its image in E tensor N is zero. Write v = C a using the selected n by q submatrix C. Restrict to the chosen rows, obtaining v_0 = C_0 a. The adjugate identity gives Delta a = adj(C_0) v_0 in D^q. Therefore Delta v = C adj(C_0) v_0 is in im B, proving the annihilation. If a D-linear combination of the minors is 1, the same combination annihilates every torsion element, so all such elements are zero. If q=0, B=0 and the cokernel is free directly.

This gives a reproducible sufficient certificate once a COMPLETE finite presentation is known. It is not a necessary certificate: D=R and B=(A-1,2)^T has a torsion-free cokernel isomorphic to the nonprincipal ideal (2,A-1), while its maximal-minor ideal is not the unit ideal. To see the isomorphism, use the map R^2 -> (2,A-1), (x,y) -> 2x-(A-1)y. Its kernel is generated by (A-1,2): from 2x=(A-1)y and coprimeness, y=2t and x=(A-1)t. The ideal is torsion-free as a submodule of R. It is nonprincipal, since a principal generator would divide both 2 and A-1 and thus be a unit, whereas evaluation in F_2 at A=1 shows the ideal proper.

A stronger sufficient route is a terminating, confluent monic rewriting system for the FULL relation module: if each reduction replaces one basis element with a combination of smaller elements with leading coefficient 1, every class has a unique R-linear normal form in irreducible basis elements. The normal-form map is then inverse to their inclusion, proving freeness. Over K a relation (A-2)e=0 may be normalized to e=0; over R that division is forbidden and the quotient contains nonzero torsion. This is exactly the failure mode any geometric rewriting proof must exclude.

**Outcome.** No complete finite slide presentation, unit-minor certificate, or monic normal form has been obtained for every small manifold. The absence of a closed essential surface has not been shown to imply integral saturation. This is the precise remaining bridge.

## Why the modern torsion examples do not refute the target

- Closed hyperbolic manifolds with positive first Betti number, including the higher-genus constructions of [BD-torsion], have closed essential surfaces; ruling out spheres and tori is weaker than ruling out every genus.
- The August 2026 examples of [K-shared] explicitly have a closed nonseparating incompressible surface. They lie outside the hypothesis, even though their surface structure is tightly controlled.
- The four-strand Montesinos examples of [Chen] answer the atoroidal variant, not this stronger all-surfaces condition. No inference that all closed incompressible surfaces are boundary-parallel was verified for those examples here.
- Essential-sphere examples and connected sums violate the intended sphere condition. Localization does not repair this hypothesis failure.

## Final mathematical gap

A full proof must extract from the topological hypothesis one of: a complete saturated integral slide presentation, a sufficiently sharp integral normal form, an injective map to an R-torsion-free module, or another argument excluding BOTH arithmetic torsion and all polynomial torsion. The tested character and generic-finiteness results do not provide that. A full counterexample must specify an oriented M satisfying the ALL-closed-essential-surfaces hypothesis and a nonzero integral skein torsion class. Neither has been produced.
