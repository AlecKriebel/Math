# Independent dynamics route for Kourovka 21.149

Timestamp: 2026-10-17, 13:21 America/Los_Angeles (working checkpoint).
Authoring agent: `p21149_dynamics`.
Status: **partial extension mechanism, not a complete resolution of 21.149**.
Best guess toward the full residual problem: 25%; toward the finite-left/well-ordered-support embedding theorem below: 85% pending adversarial review and definition audit.

## Exact scope and central gap

Let G = D_<2>([0,1]), the compact-support group of locally right <2>-linear increasing homeomorphisms. Let A be an increasing homeomorphism group on a real interval with the following properties:

1. For every a in A, the family of components of supp(a) is well ordered from left to right.
2. At every finite fixed point c, each a has an affine right germ, a(c+t)=c+s(a,c)t for sufficiently small positive t, with s(a,c)>0.
3. Each support component of every element in an embedded local group e(G(L)) has a finite left endpoint. This holds automatically for bounded real intervals and for groups of maps whose supports are bounded below. More generally one can replace this by an appropriate solvable-germ argument at -infinity, but that replacement is not asserted without checking the actual definition.

The mechanism below gives a rank-independent, order-independent topological diagonal rigidity theorem for embeddings e:G -> A, and consequently excludes ambient conjugators implementing the known alternating-slope automorphism. It removes the rank-one order-classification dependence of the September 2026 preprint for the six families satisfying these properties.

**It does not resolve the problem if a permitted ambient Dlab family has action components extending without a first component toward -infinity, or if 'Dlab group' includes other families not satisfying (1).** The exact meaning and orderability of the reflected real family must be audited. A twisted diagonal embedding described below is a serious obstruction, rather than a route to be waved away.

## Lemma 1: perfect centralizers have disjoint support

**Claim.** If f is an element of A and B <= C_A(f) is perfect, and every support component of f has finite left endpoint, then B fixes supp(f) pointwise.

**Proof.** Every b in B sends supp(f) to itself and permutes its components in increasing order. An increasing bijection of a well-ordered set is the identity (transfinite induction), so B preserves every component J=(c,d) individually. It fixes the finite endpoint c.

The right-slope map sigma_c:B -> R_(>0) is a group homomorphism: germs of the elements at their common fixed point c compose by multiplying slopes. Since B is perfect and R_(>0) is abelian, all these slopes are 1. Thus each b is the identity on an interval (c,c+epsilon_b).

The restriction f|J has no fixed point, so it is everywhere greater than the identity or everywhere less than the identity. For each x in J, a sequence f^(n_k)(x), with n_k tending toward the suitable end of Z, converges to c. Choose n with f^n(x) in the identity interval for b. Since b and f commute, f^n(bx)=b(f^n x)=f^n x; injectivity gives bx=x. This holds for every x in J and every component J. QED.

**Corollary.** If P,Q <= A commute, Q is perfect, and the components of supp(p) have finite left endpoint for every p in P, then supp(P) and supp(Q) are disjoint. In particular this applies to e(G(L)), e(G(M)) for disjoint source intervals L,M.

This proof is self-contained and uses neither an order on A nor the rank of its slope group. It agrees with the centralizer mechanism in Dlab 1968, Lemma 3.6 / Theorem 4.6, but no unverified scope of those results is needed here.

## Lemma 2: least components and nesting

The group G and each local group G(L)={g:supp(g) compactly contained in L} are nonabelian simple; this is Dlab's standard simplicity theorem after an affine coordinate change. Every restriction of e(G), or of e(G(L)), to a nontrivial action component is faithful: its kernel is a proper normal subgroup of a simple group.

Fix 1 != b in G. Every nontrivial e(G)-action component contains a support component of e(b), by faithfulness of restriction. The well ordering of supp(e(b)) therefore implies that the nontrivial e(G)-action components have a least member J0.

For every relatively compact open L subset (0,1), choose 1 != f in G(L). Faithfulness of e(G) on J0 makes e(G(L)) nontrivial there. Every nontrivial e(G(L))-action component in J0 contains a support component of e(f), hence these components have a least one K(L).

For L subset M, K(L) subset K(M). To see this carefully, e(G(M)) acts faithfully on K(M), so e(G(L)) has at least one component inside K(M). No component of e(G(L)) preceding K(M) is possible: it would be contained in an e(G(M))-component preceding K(M). Therefore the least e(G(L))-component is one of those lying in K(M). (One must choose the least such component, rather than claiming that an arbitrary component inside K(M) is already the least.)

For disjoint L,M, Lemma 1 gives disjoint supports of e(G(L)), e(G(M)), so in particular K(L), K(M) are disjoint. Conjugation gives e(g)K(L)=K(g(L)) for every g in G. The union of all K(L) is a nonempty invariant open interval in J0, hence is J0: otherwise an interior endpoint would be fixed by all e(G).

## Lemma 3: orientation is globally consistent

G is transitive on finite increasing tuples of distinct points. First, in an arbitrary open subinterval V of (0,1), local bumps with slopes 2 and 1/2 move any x in V to any y in V, by dividing the path into sufficiently short steps. For one short right step x<y, take a=2x-y and d=2y-x in V and use the two-slope bump supported on [a,d], with breakpoint x; it sends x to y. General left steps use inverses. For finite tuples, match points from left to right, using a bump supported to the right of the last already matched point.

Consequently G maps any ordered pair of intervals with distinct endpoints and a positive gap onto any other such pair, by mapping their four endpoints. Since e(g) is increasing and K is equivariant, the ordering of K(L),K(M) for L<M is independent of the pair: either always K(L)<K(M), or always K(M)<K(L). Pairs whose source intervals meet at an endpoint are handled by first shrinking both intervals and using nesting.

## Lemma 4: reconstruction gives increasing or decreasing conjugacy

In the increasing case, define for x in (0,1)

    a_x = sup{ right_endpoint K(L) : L compactly contained in (0,x) },
    b_x = inf{ left_endpoint K(R) : R compactly contained in (x,1) }.

Both cuts lie inside J0, and a_x <= b_x. Let F_x=[a_x,b_x]. If x<z, placing M strictly between x and z gives F_x<F_z. Equivariance of K gives e(g)F_x=F_(g(x)). If one F_x were nondegenerate, transitivity of G would make all F_z nondegenerate, yielding uncountably many disjoint open intervals in a separable interval. Thus F_x={phi(x)}. The equivariant increasing map phi can have no jump, for otherwise transitivity gives uncountably many disjoint jump intervals. Its image is a nonempty invariant open subinterval of J0; a proper image has an interior endpoint fixed by e(G), impossible. Therefore phi:(0,1)->J0 is an increasing homeomorphism and

    e(g) phi = phi g  for all g in G.

In the decreasing case interchange source-left and source-right in the two cuts. The same argument gives a decreasing homeomorphism with the same equivariance. This reconstruction uses no group order.

## Lemma 5: decreasing orientation is impossible

Construct f in G as a union of two-slope bumps on disjoint intervals I_n=(a_n,b_n), n>=1, with I_1<I_2<..., and with a_n,b_n increasing to an interior point b<1. Put f=identity elsewhere. Choose all intervals inside a fixed compact subset of (0,1). Each bump starts with slope 2 and ends with slope 1/2. At each point below b, only finitely many bumps occur to its left nearby; at b, f has identity right germ. Thus f is locally right <2>-linear everywhere, with compact support, so f in G.

A decreasing phi transports these support components to phi(I_n), an infinite strictly descending family. Each phi(I_n) is a genuine global support component of e(f), since its two finite endpoints are fixed and lie in J0. This contradicts well ordering of support components in A. Hence every reconstruction phi above is increasing.

Combining Lemmas 1-5 gives the advertised order-independent rigidity theorem under the three explicit target hypotheses.

## Consequence for the alternating-slope automorphism

Let h be the known increasing, locally finite PL map on (0,1) whose slopes are powers of 2, with infinitely descending bump components accumulating at 0, and identity near 1. Conjugation by h defines an order automorphism alpha of G, because each g in G has support compactly contained in (0,1), and h is locally finite PL away from 0.

If u in A normalizes e(G) and induces alpha, u preserves the least e(G)-action component J0. Lemmas 1-5 produce an increasing phi with e(g)|J0=phi g phi^-1. The map phi^-1 u phi induces alpha on G. The centralizer of G in Homeo_+((0,1)) is trivial: if c(x)!=x, a small local bump near x with support disjoint from its image under c contradicts centralization. Thus phi^-1 u phi equals h (or its inverse depending on the chosen convention for alpha). Consequently u has an infinite descending family of genuine bump components phi(C_n), contradicting target well ordering.

This would cover arbitrary-rank slope groups in the six well-ordered-support families, after checking their definitions exactly. It is not a full answer until all admissible Dlab targets are covered.

## Obstruction for a bounded-above real target without a first component

Suppose a target contains all locally right H-linear increasing homeomorphisms of R with support bounded above, without any global well-order requirement on their support components. Then consider blocks I_n=[-2^(n+1),-2^n], n in Z. For any automorphism alpha of G, put an affinely rescaled copy of alpha^n(g) in I_n and identity elsewhere. This yields a diagonal embedding e:G->Homeo_+(R), and scaling t(x)=2x for x<0, t(x)=x for x>=0 shifts the blocks. The resulting conjugation implements alpha or alpha^-1, according to the indexing convention. Every element is locally right affine at each finite point: block endpoints have identity neighborhoods, and at 0 the map is identity on the right. Slopes remain in the group generated by 2 and the source slopes. The support is bounded above by 0.

**This construction needs an exact definition audit.** Such a whole bounded-above group cannot be bi-orderable when it contains t and all alternating block maps. Indeed repeat a fixed bump f in even blocks and f^-1 in odd blocks. Then t conjugates this alternating element to its inverse, which is impossible in a bi-ordered group. Thus the reflected real family, if it is defined this way, may be outside the meaning of an ordered Dlab group even though it is a subgroup of the ambient homeomorphism group. No conclusion about Kourovka's intended quantifiers is made from this preliminary observation.

## Primary source consulted

V. Dlab, On a family of simple ordered groups, J. Austral. Math. Soc. 8 (1968), 591-608, DOI 10.1017/S1446788700006261. Authoritative Cambridge PDF:
https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2FC98980CF8D6CE6001298088EC1E5FA/S1446788700006261a.pdf/div-class-title-on-a-family-of-simple-ordered-groups-div.pdf

The local-right-affine definition is on pp. 591-592; simplicity/order results and centralizers are in Sections 3-4. The proof above does not use the rank-one classification from Gong-Yang-Zeng.

## 13:22 checkpoint: shorter two-tail argument, independently checked

The root agent proposed replacing h by a map with **two** tails of bump components. This removes the need for Lemmas 4-5 entirely. Best guess toward the abstract target-class obstruction theorem: 95%, pending fresh adversarial review. Full Kourovka resolution still depends on auditing the target definitions and priority.

Take a locally finite PL increasing homeomorphism h of (0,1), slopes in <2>, with disjoint bump components C_m decreasing toward 0 and D_m increasing toward 1. Put identity between the tails. One can take the standard left alternating-slope construction on (0,1/4] and its reflection on [3/4,1), keeping h identity on [1/4,3/4]. On each compact subinterval of (0,1), h and h^-1 have only finitely many breakpoints. Thus alpha(g)=h g h^-1 normalizes G and preserves either Dlab order: at the leftmost support endpoint of each g, conjugation preserves the right slope because h has an affine right germ at the corresponding point. First support components retain their order.

Suppose u in A induces alpha via e. Lemmas 1-3 give J0, nested/equivariant K(L), disjointness for disjoint L, and a uniform orientation of K on ordered source intervals. Because h preserves each C_m and D_m setwise, alpha normalizes every G(C_m),G(D_m). The map u preserves J0 (least e(G)-action component), and normalizes e(G(C_m)). It therefore preserves the least e(G(C_m))-component K(C_m) in J0. The same holds for D_m.

Crucially, u acts nontrivially on each such K(L). If u were the identity on K(L), then for all g in G(L),

    e(alpha(g))|K(L) = (u e(g) u^-1)|K(L) = e(g)|K(L).

Both g and alpha(g) lie in G(L), and the restriction of e(G(L)) to K(L) is faithful. Therefore alpha(g)=g for all g in G(L). This is false: h is nonidentity on L, so choose x in L moved by h and a sufficiently small subinterval V compactly contained in L for which V and h(V) are disjoint. A nontrivial bump g supported in V has alpha(g) supported in h(V), so alpha(g)!=g.

Since u preserves K(L), it fixes its finite endpoints, and at any moved point in K(L), the support component of u containing that point is contained in K(L). Thus each K(C_m),K(D_m) contains a genuine support component of u. If the uniform orientation is increasing, the K(C_m) form an infinite descending sequence. If it is decreasing, the K(D_m) form an infinite descending sequence. Either yields infinitely descending genuine support components of u, contradicting the well-ordering assumption.

**Audit of endpoint caveat.** The K(L) are pairwise disjoint for pairwise disjoint source L. An infinite strictly descending sequence cannot contain a member with left endpoint -infinity, because no subsequent nonempty interval can lie to its left. For each chosen support component inside such a K(L), the interval containment follows directly from fixed finite boundary points. If a K(L) has an infinite right endpoint, this does not allow a support component to exit through that endpoint in the real line; containment still holds. Therefore no endpoint exception breaks the descending-sequence contradiction.

This two-tail proof is strictly shorter than full action reconstruction and avoids any dependence on uniqueness of a topological conjugacy, ambient order classification, or natural orientation. Its remaining input requirements are exactly target well-ordered support components, affine right germs at finite fixed points, and finite-left-endpoint support for the embedded local source groups.

## Real-line reduction if the actual definition includes affine left tails

The following elementary criterion makes the endpoint hypothesis and global well ordering directly checkable from definitions, without an order-classification theorem.

**Affine-left-tail criterion.** Suppose every a in A <= Homeo_+(R) is locally right affine at each finite point and is affine on some initial interval (-infinity,c_a). Then (i) every component family supp(a) is well ordered from left to right, and (ii) every element of a perfect subgroup P<=A is the identity on some initial interval.

For (ii), the germ-at-minus-infinity map A -> Aff_+(R) is a homomorphism: an affine initial germ x->sx+t is represented by the unique pair (s,t); eventual compositions are well defined because increasing homeomorphisms send minus infinity to minus infinity. Aff_+(R) is metabelian. The image of a perfect group is perfect, and the only perfect subgroup of a solvable group is trivial. Hence the initial affine germ of every p in P is identity. In particular all its support components have finite left endpoints.

For (i), take a nonempty family F of support components and let c be the infimum of the union of these components. If c=-infinity, the initial affine tail is either nonidentity and has one support interval extending to minus infinity, which must be the least member of F, or is identity and there is no support sufficiently far left, contradicting c=-infinity. If c is finite, continuity makes c a fixed point. The affine right germ at c is either identity, contradicting that the chosen union has infimum c, or nonidentity, in which case the first interval (c,c+epsilon) lies in a single support component which must be the least member of F. This proves well ordering.

Thus an actual Dlab real family with an affine germ at minus infinity satisfies the short two-tail theorem for arbitrary H automatically, including targets whose support is not assumed bounded below. The deliberately larger bounded-above construction above fails precisely this affine-left-tail condition.
