# Independent derivation of the whole claim

This derivation was built first in INITIAL_RECONSTRUCTION.md before foreign bodies or deposited programs. The following closes its external interfaces and makes the quantifier and boundary checks explicit. It uses the unchanged deposited definitions, not a repaired or narrowed replacement theorem.

Let composition be ordinary function composition. Let A_I be all increasing homeomorphisms of [0,1] having an affine right germ at every point a<1, including 0. Let A_R be all increasing real homeomorphisms having an affine right germ at every finite point and an eventually affine formula at minus infinity. Slopes in these two ambients are arbitrary positive real numbers. Let G be the subgroup with right slopes in 2^Z, identical near both 0 and 1. For L compactly contained in (0,1), G(L) has support closure compactly contained in L.

The exact assertion is existence of one alpha in Aut(G), preserving both Dlab biorders, such that for each A in {A_I,A_R}, every injective homomorphism e:G→A and every u in A, there exists f in G with e(alpha(f)) unequal to u^-1 e(f) u. There is no ambient order, order-preserving-embedding or rank-one-ambient assumption. Corollary 8 additionally includes all four interval and all four extended-real Dlab families for each positive-real slope subgroup H. Proposition 7 proves a countermodel when the minus-infinity hypothesis is omitted.

## 1. Well-ordered supports and individual initial identity germs

Suppose a nonempty family of support components of q has finite left endpoints with finite infimum a, but no minimum. Choose distinct endpoints a_n decreasing to a. Continuity gives q(a)=a. In a right-affine germ q(a+t)=a+s t, the fixed points a_n force s=1. The resulting identity neighborhood cannot contain a support endpoint: its interior points have open identity neighborhoods. This contradiction gives a first component. On [0,1], a<1; the hypothesis explicitly supplies the right germ even if a=0.

For q in A_R, an initial identity ray gives a lower bound for support endpoints. A nonidentity eventual affine formula q(x)=r x+t moves all sufficiently negative x (a nonidentity affine map has at most one finite fixed point). Thus it gives a single initial component with left endpoint minus infinity, and all remaining endpoints are bounded below. Any family containing the initial component has a first member; any other family reduces to the finite-infimum case. This proves well-ordering for arbitrary ambient q, including the future implementer u.

Dlab's exact compact-support group is simple. It contains a nonidentity finite two-slope bump and is torsion free: a moved point has strictly monotone iterates under a nonidentity increasing homeomorphism. An abelian simple nontrivial group would have prime finite order. Consequently G is nonabelian and perfect. Affine rescaling and identity extension identify G(L) with G; no restriction of breakpoint locations is introduced.

At 0, slopes give a homomorphism into the abelian positive multiplicative reals. At minus infinity, eventual affine formulas give a homomorphism into Aff_+(R). Its slope quotient and translation kernel are abelian, so it is metabelian. The image of a perfect group in either solvable group is trivial. Hence every element of a perfect ambient subgroup fixes some initial interval or ray. These neighborhoods may vary with the element: the proof never requires a common one. In particular its nontrivial elements have support components with finite left endpoints.

## 2. Why commuting local groups have disjoint action supports

Let a perfect subgroup P centralize q, where q has finite support-left endpoints. Each p in P permutes the support components of q increasingly. An order automorphism of a well-ordered set is the identity. To check this, use the least moved element: all its predecessors are fixed, so neither a smaller image nor a larger image with an available smaller preimage is possible. Thus P preserves each component J=(a,b) setwise and fixes finite a.

Right slopes at a are an abelian quotient of P and therefore equal 1. Each p is identical near a. Since q has no interior fixed point in J, either q(x)>x throughout J or the reverse. Iterating q in the direction toward a converges to a; any larger finite limit would be a fixed point. For any x in J, a sufficiently advanced iterate is fixed by p. Commutation transports that fixed-point identity back to x. Therefore P fixes supp(q) pointwise.

For disjoint source intervals L and M, G(L) and G(M) commute and are perfect. Apply this argument to each q in e(G(L)), whose support-left endpoints are finite, and P=e(G(M)). Taking the union over q proves S(e(G(L))) and S(e(G(M))) disjoint. This is a geometric statement and uses neither a sign rule nor an order on e(G).

## 3. Least components and the one global orientation alternative

For any nontrivial action component J of e(G), restriction to J has a proper normal kernel in G. Simplicity makes that kernel trivial. Fix f≠1. Every such J therefore contains a support component of e(f); those support components cannot cross common fixed endpoints. The least support component of e(f), supplied by part 1, lies in the least action component J_0. If an earlier action component existed, faithfulness would put an earlier support component of e(f) in it. This proves existence of J_0 without assuming that an arbitrary union of well-ordered supports is well ordered.

The same argument applies to each simple G(L), restricted inside J_0, giving its least nontrivial action component K(L). It exists because every fixed nonidentity element of G(L) acts nontrivially on J_0. Its boundary cannot cross the common fixed boundary of J_0, so it is also a global action component. Part 2 makes K(L),K(M) disjoint when L,M are disjoint. For each g in G,

K(gL)=e(g)K(L),

since g conjugates G(L) onto G(gL), e(g) preserves J_0, and increasing maps preserve least components.

For arbitrary equal-length increasing tuples of interior points, choose common outer endpoints c,d inside (0,1), fix c,d, and map successive source and target segments. If source length is ell and target length r ell, choose s=2^k with s≤r≤2s. The two lengths

ell(2s-r)/s and ell(r-s)/s

are nonnegative, sum to ell and, with slopes s and 2s, give image length r ell. This includes r=s or 2s by omitting the zero piece. Joining finitely many segments and extending identity outside [c,d] gives an element of G. Apply this four-point transitivity to endpoints of any two positively separated interval pairs. Equivariance and increasing e(g) show that all pairs L<M have the same relative K-order. Exactly one global alternative holds: all K(L)<K(M), or all K(M)<K(L). This admits orientation-reversing abstract embeddings; it does not promote an order-preserving reconstruction to an unrestricted one.

## 4. One automorphism defeats both alternatives

For m≥0 set b_m=2^(-2m-2), a_m=b_m/2, C_m=(a_m,b_m), D_m=(1-b_m,1-a_m). These pairs are separated, C_(m+1)<C_m and D_m<D_(m+1). On the closure of any one of these intervals (a,b), define h with slope 2 until a+(b-a)/3 and slope 1/2 thereafter; fix all remaining points. The two formulas agree because each gives a+2(b-a)/3 at the join. They fix a,b and have h(x)>x inside. Blocks accumulate only at 0 and 1, with displacements bounded by block lengths, so h is a continuous increasing endpoint-fixing homeomorphism. It is finitely PL on every interior compact set, though it is not right affine at 0.

Every f in G has support in an interior compact set, and h and h^-1 are locally finite PL there. Thus alpha(f)=h^-1 f h and its inverse preserve G. They transport compact support to its h-preimage and preserve the allowed slope group. At a transported first support point a'=h^-1(a), if the right slopes of h and f are c and k, the conjugate right slope is c^-1 k c=k. Hence both first-slope positive cones, and therefore both Dlab orders, are preserved.

Each C_m and D_m is h-invariant, so alpha normalizes G(C_m) and G(D_m). It is nontrivial on each. Indeed choose a small compactly contained interval V moved by h with V disjoint from h^-1(V), and a nontrivial finite two-slope bump supported there. Its conjugate has disjoint support. This checks the local nontriviality needed in the obstruction, not merely global non-innerness.

Suppose an implementer u exists. The asserted identity for all f makes u normalize e(G), so it preserves its common fixed set and the least action component J_0. For every tail interval L, alpha(G(L))=G(L), hence u fixes K(L) setwise. It cannot be the identity on K(L): otherwise the implementation identity and faithfulness of G(L) on K(L) would force alpha to be the identity on G(L). Choose a moved point there and let U(L) be its full support component under u. Because u preserves K(L), all finite endpoints of K(L) are fixed, so U(L) is contained in K(L); infinite endpoints also cannot be crossed.

In the preserved orientation case, U(C_(m+1))<U(C_m) for every m. In the reversed orientation case, U(D_(m+1))<U(D_m). These are infinitely descending sequences of distinct full support components of u, contradicting part 1. The same h and alpha handle every e,A,u; alpha is chosen before those universal quantifiers. No topological conjugacy classification of all embeddings is assumed.

## 5. The exact omitted-end countermodel

Let B be increasing real homeomorphisms with locally right 2^Z-affine germs at every finite point and support bounded above, without a minus-infinity condition. For arbitrary beta in Aut(G), let I_n=(-2^-n,-2^(-n-1)), n in Z, and let phi_n map [0,1] increasingly and affinely onto its closure. Define E(f) on I_n by phi_n beta^n(f) phi_n^-1; fix all endpoints and [0,infinity).

Every beta^n(f) is identical near both source endpoints, so each finite cell endpoint has an identity right neighborhood. At 0 the right ray is identical; the cell diameters tend to 0 as n→+infinity, giving left continuity there. As n→-infinity, cells escape to minus infinity, preserving properness. Interior affine conjugation cancels the rescaling factors in slopes. Thus E(f) is in B. Cellwise multiplication gives a homomorphism, and the n=0 cell proves injectivity. With v(x)=x/2 on x<0 and v(x)=x on x≥0, v phi_n=phi_(n+1), and direct substitution gives

v^-1 E(f) v |_I_n = phi_n beta^(n+1)(f) phi_n^-1 = E(beta(f)) |_I_n.

All remaining points are fixed. This proves the full arbitrary-beta proposition, not just a sampled automorphism. In particular the main result does not extend to B. For nontrivial f, E(f) has a nontrivial support block in every cell toward minus infinity; it has no eventual affine left germ. Therefore the countermodel does not contradict the stated theorem or the full Zenkov–Medvedev family.

## 6. Remaining boundaries and reproducibility

All four interval Dlab families are subsets of A_I, with arbitrary H. The actual extended-real definition/decomposition supplies an eventual affine left germ for the full group; all three named support-restricted subgroups, including the reflected bounded-above family, lie in it and hence in A_R. Extending this defining-geometric inclusion to arbitrary H uses no rank-one order classification. H={1} creates no exception: an impossible embedding simply makes the ambient assertion vacuous.

A one-tail construction alone would not handle the reversed orientation: reflection x↦1-x carries an infinite descending left tail to an increasing tail accumulating at the excluded right endpoint, making its conjugator compatible with A_I. The second tail is essential for this proof. Conversely, no right-germ hypothesis at the right endpoint of [0,1] is needed. Infinite left accumulating support within an interior point, or at 0, is forbidden exactly where the right-germ hypothesis is used. The perfect-centralizer argument needs finite left support endpoints; part 1 establishes them for the image elements before that lemma is applied.

The native program was inspected: it checks 1,562 rational segment cases, three tuple examples, 200 bump intervals, 441 scalar conjugated germs and 36 affine cases. Its normal output exactly equals the deposited JSON; optimized execution deliberately fails so assertions cannot disappear. Independent PL-function checks do not import it: 320 whole tuple maps with inverses, 48 local nontriviality/first-germ cases, a whole-function automorphism product, 69 orientation interval comparisons and 132 exact knots in positive/negative exponent cell-shift identities. They pass normally and under optimization using explicit require checks. These bounded identities corroborate formulas and composition conventions. The universal theorem rests on the written support/perfectness/simple-action derivation above, not finite tests.

No substantive gap or counterexample to the full deposited theorem, corollary or proposition was found in this source/scope family. The exact remaining limitations are independent human review and formal verification not being claimed, and historical worldwide priority not being established by a focused literature comparison. These are not replacements for the stated claim or repairs to it.
